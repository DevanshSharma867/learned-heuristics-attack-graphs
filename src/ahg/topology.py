"""Seeded synthetic topology generators: flat, tiered, hub-and-spoke.

Each generator is a pure function of (seed, n_hosts, parameters) and returns
a Network (network.py). All randomness comes from one random.Random seeded
on (family, seed), consumed in a fixed order, and nothing iterates over a
set while drawing.
So the same arguments give byte-identical JSON in any process.

All three families share these rules:

- Each internal host runs k services with distinct families,
  k ~ U[services[0], services[1]].
- A link from host a to host b allows each of b's services independently
  with the family's link probability.
- After the random edges, repair edges are added until every host can be
  reached from the internet. Each repair edge comes from a reached host
  that the family's rules allow. Without this, part of every network would
  be dead weight that no attack can touch.

The families differ only in which host pairs may link:

- flat: one LAN, any internal host may reach any other.
- tiered: a DMZ and deeper tiers. Hosts reach their own tier and the next
  one down, never skipping a tier. Only the DMZ is exposed to the internet.
- hub_and_spoke: spokes talk only to their own hub, hubs talk to each other.
  Only spokes are exposed to the internet.
"""

import random
from collections import deque

from .network import INTERNET, SCHEMA_VERSION, SERVICE_FAMILIES, Host, Network, Reach, Service, Trust


class _Builder:
    """Accumulates hosts and edges; finish() returns the canonical Network."""

    def __init__(self, rng: random.Random, services: tuple[int, int]):
        lo, hi = services
        if not 1 <= lo <= hi <= len(SERVICE_FAMILIES):
            raise ValueError(f"services range must satisfy 1 <= lo <= hi <= {len(SERVICE_FAMILIES)}")
        self.rng = rng
        self.k_range = services
        self.hosts = [Host(INTERNET, "internet", "internet")]
        self.services: list[Service] = []
        self.services_of: list[list[int]] = [[]]
        self.reach: set[Reach] = set()
        self.trust: set[Trust] = set()

    def add_host(self, zone: str) -> int:
        h = len(self.hosts)
        self.hosts.append(Host(h, f"{zone}-{h}", zone))
        k = self.rng.randint(*self.k_range)
        ids = []
        for fam in sorted(self.rng.sample(SERVICE_FAMILIES, k)):
            ids.append(len(self.services))
            self.services.append(Service(len(self.services), h, fam))
        self.services_of.append(ids)
        return h

    def link(self, src: int, dst: int, p: float) -> None:
        for s in self.services_of[dst]:
            if self.rng.random() < p:
                self.reach.add(Reach(src, s))

    def maybe_trust(self, src: int, dst: int, p: float) -> None:
        if self.rng.random() < p:
            self.trust.add(Trust(src, dst))

    def reached(self) -> set[int]:
        out = {INTERNET: []}
        for r in self.reach:
            out.setdefault(r.src, []).append(self.services[r.service].host)
        seen = {INTERNET}
        queue = deque([INTERNET])
        while queue:
            for b in out.get(queue.popleft(), ()):
                if b not in seen:
                    seen.add(b)
                    queue.append(b)
        return seen

    def ensure_exposed(self, hosts: list[int]) -> None:
        """If the internet reaches nothing, expose one service of a random host in hosts."""
        if not any(r.src == INTERNET for r in self.reach):
            h = self.rng.choice(hosts)
            self.reach.add(Reach(INTERNET, self.rng.choice(self.services_of[h])))

    def connect_unreached(self, allowed_src) -> None:
        """Add edges until every host is reachable from the internet.

        Each round takes the lowest-id unreached host that has a reached
        allowed source (allowed_src(h)) and adds one edge from such a source
        to one of its services. It then recomputes reachability, because that
        host may unlock others. The family rules always leave a path, so
        getting stuck is a bug.
        """
        while True:
            seen = self.reached()
            unreached = [h for h in range(1, len(self.hosts)) if h not in seen]
            if not unreached:
                return
            for h in unreached:
                candidates = [a for a in allowed_src(h) if a in seen]
                if candidates:
                    self.reach.add(Reach(self.rng.choice(candidates), self.rng.choice(self.services_of[h])))
                    break
            else:
                raise RuntimeError(f"hosts {unreached} have no reached allowed source; generator bug")

    def finish(self, family: str, seed: int, params: dict) -> Network:
        return Network(
            hosts=tuple(self.hosts),
            services=tuple(self.services),
            reach=tuple(sorted(self.reach)),
            trust=tuple(sorted(self.trust)),
            meta={"family": family, "seed": seed, "params": params, "schema_version": SCHEMA_VERSION},
        )


def _rng(family: str, seed: int) -> random.Random:
    # Seed on the family as well as the seed. Otherwise the same seed draws
    # the same service assignment in every family, which would correlate
    # train and test graphs in the held-out-family split. String seeds are
    # hashed with SHA-512, not hash(), so PYTHONHASHSEED does not affect them.
    return random.Random(f"{family}:{seed}")


def _check_probs(**probs: float) -> None:
    for name, p in probs.items():
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"{name} must be in [0, 1], got {p}")


def flat(
    seed: int,
    n_hosts: int,
    services: tuple[int, int] = (1, 3),
    p_exposed: float = 0.2,
    p_reach: float = 0.3,
    p_trust: float = 0.05,
) -> Network:
    """One unsegmented LAN: any host may reach any other host's services."""
    if n_hosts < 1:
        raise ValueError("n_hosts must be >= 1")
    _check_probs(p_exposed=p_exposed, p_reach=p_reach, p_trust=p_trust)
    b = _Builder(_rng("flat", seed), services)
    hosts = [b.add_host("lan") for _ in range(n_hosts)]
    for h in hosts:
        b.link(INTERNET, h, p_exposed)
    for src in hosts:
        for dst in hosts:
            if src != dst:
                b.link(src, dst, p_reach)
                b.maybe_trust(src, dst, p_trust)
    b.ensure_exposed(hosts)
    b.connect_unreached(lambda h: [a for a in hosts if a != h])
    params = {"n_hosts": n_hosts, "services": list(services), "p_exposed": p_exposed, "p_reach": p_reach, "p_trust": p_trust}
    return b.finish("flat", seed, params)


def tiered(
    seed: int,
    n_hosts: int,
    services: tuple[int, int] = (1, 3),
    n_tiers: int = 3,
    p_exposed: float = 0.5,
    p_intra: float = 0.3,
    p_down: float = 0.2,
    p_trust: float = 0.05,
) -> Network:
    """DMZ, then tier1..tier{n_tiers-1}. Edges stay inside a tier or go one tier deeper."""
    if n_tiers < 1 or n_hosts < n_tiers:
        raise ValueError("need n_tiers >= 1 and n_hosts >= n_tiers")
    _check_probs(p_exposed=p_exposed, p_intra=p_intra, p_down=p_down, p_trust=p_trust)
    b = _Builder(_rng("tiered", seed), services)
    base, extra = divmod(n_hosts, n_tiers)
    tiers = []
    for t in range(n_tiers):
        zone = "dmz" if t == 0 else f"tier{t}"
        tiers.append([b.add_host(zone) for _ in range(base + (t < extra))])
    tier_of = {h: t for t, hs in enumerate(tiers) for h in hs}
    for h in tiers[0]:
        b.link(INTERNET, h, p_exposed)
    for t, hs in enumerate(tiers):
        deeper = tiers[t + 1] if t + 1 < n_tiers else []
        for src in hs:
            for dst in hs:
                if src != dst:
                    b.link(src, dst, p_intra)
                    b.maybe_trust(src, dst, p_trust)
            for dst in deeper:
                b.link(src, dst, p_down)
                b.maybe_trust(src, dst, p_trust)
    # Repair edges come only from the tier directly above, so the
    # no-tier-skipping property, and hence depth >= n_tiers, holds.
    b.connect_unreached(lambda h: [INTERNET] if tier_of[h] == 0 else tiers[tier_of[h] - 1])
    params = {
        "n_hosts": n_hosts, "services": list(services), "n_tiers": n_tiers, "p_exposed": p_exposed,
        "p_intra": p_intra, "p_down": p_down, "p_trust": p_trust,
    }  # fmt: skip
    return b.finish("tiered", seed, params)


def hub_and_spoke(
    seed: int,
    n_hosts: int,
    services: tuple[int, int] = (1, 3),
    n_hubs: int = 1,
    p_exposed: float = 0.2,
    p_link: float = 0.5,
    p_trust: float = 0.3,
) -> Network:
    """Hubs first, then spokes, each assigned to one hub round-robin.

    Edges: spoke <-> own hub, hub <-> hub. Trust: hub -> own spokes (central
    administration). Spokes face the internet, hubs do not.
    """
    if n_hubs < 1 or n_hosts <= n_hubs:
        raise ValueError("need n_hubs >= 1 and n_hosts > n_hubs")
    _check_probs(p_exposed=p_exposed, p_link=p_link, p_trust=p_trust)
    b = _Builder(_rng("hub_and_spoke", seed), services)
    hubs = [b.add_host("hub") for _ in range(n_hubs)]
    spokes = [b.add_host("spoke") for _ in range(n_hosts - n_hubs)]
    hub_of = {s: hubs[i % n_hubs] for i, s in enumerate(spokes)}
    for s in spokes:
        b.link(INTERNET, s, p_exposed)
        b.link(s, hub_of[s], p_link)
        b.link(hub_of[s], s, p_link)
        b.maybe_trust(hub_of[s], s, p_trust)
    for a in hubs:
        for c in hubs:
            if a != c:
                b.link(a, c, p_link)
    b.ensure_exposed(spokes)

    def allowed(h: int) -> list[int]:
        if h in hub_of:
            return [hub_of[h]]
        return [c for c in hubs if c != h] + [s for s in spokes if hub_of[s] == h]

    b.connect_unreached(allowed)
    params = {"n_hosts": n_hosts, "services": list(services), "n_hubs": n_hubs, "p_exposed": p_exposed, "p_link": p_link, "p_trust": p_trust}
    return b.finish("hub_and_spoke", seed, params)


GENERATORS = {"flat": flat, "tiered": tiered, "hub_and_spoke": hub_and_spoke}


def generate(family: str, seed: int, n_hosts: int, **params) -> Network:
    return GENERATORS[family](seed, n_hosts, **params)
