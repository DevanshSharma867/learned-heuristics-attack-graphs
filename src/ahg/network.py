"""Network intermediate representation: what a topology generator produces.

This is the network, not the attack graph. It lists hosts, the services they
run (each labelled with a service family, used later to sample CVEs),
firewall reachability, and trust relationships. The attack-graph builder
turns it into a delete-free planning task (task.py).

Host 0 is always the internet: the attacker's starting point. It runs no
services.

- Reach(src, service): host src can open a connection to that service
  (a firewall allow rule).
- Trust(src, dst): control of src gives login on dst, e.g. shared admin
  credentials or SSH keys.

Every list is stored in a canonical sorted order, and to_json sorts keys,
so a network serialises to the same bytes whenever its content is the same.
"""

import json
from collections import deque
from dataclasses import asdict, dataclass

SCHEMA_VERSION = 1
INTERNET = 0
SERVICE_FAMILIES = ("dns", "ftp", "http", "mail", "rdp", "smb", "sql", "ssh")


@dataclass(frozen=True)
class Host:
    id: int
    name: str
    zone: str


@dataclass(frozen=True)
class Service:
    id: int
    host: int
    family: str


@dataclass(frozen=True, order=True)
class Reach:
    src: int
    service: int


@dataclass(frozen=True, order=True)
class Trust:
    src: int
    dst: int


@dataclass(frozen=True)
class Network:
    hosts: tuple[Host, ...]
    services: tuple[Service, ...]
    reach: tuple[Reach, ...]
    trust: tuple[Trust, ...]
    meta: dict  # family, seed, params, schema_version

    def __post_init__(self):
        validate(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=1) + "\n"

    @classmethod
    def from_json(cls, text: str) -> "Network":
        d = json.loads(text)
        return cls(
            hosts=tuple(Host(**h) for h in d["hosts"]),
            services=tuple(Service(**s) for s in d["services"]),
            reach=tuple(Reach(**r) for r in d["reach"]),
            trust=tuple(Trust(**t) for t in d["trust"]),
            meta=d["meta"],
        )


def validate(net: Network) -> None:
    """Raise ValueError if the network is malformed (also guards loaded JSON)."""
    n = len(net.hosts)
    if [h.id for h in net.hosts] != list(range(n)) or [s.id for s in net.services] != list(range(len(net.services))):
        raise ValueError("host and service ids must be 0..n-1 in order")
    if n == 0 or net.hosts[INTERNET].zone != "internet":
        raise ValueError("host 0 must be the internet")
    for s in net.services:
        if not 0 < s.host < n:
            raise ValueError(f"service {s.id} is on an invalid host {s.host}")
        if s.family not in SERVICE_FAMILIES:
            raise ValueError(f"service {s.id} has unknown family {s.family!r}")
    for r in net.reach:
        if not 0 <= r.src < n or not 0 <= r.service < len(net.services):
            raise ValueError(f"reach edge {r} out of range")
        if net.services[r.service].host == r.src:
            raise ValueError(f"reach edge {r} is a self-loop")
    for t in net.trust:
        if not 0 < t.src < n or not 0 < t.dst < n or t.src == t.dst:
            raise ValueError(f"trust edge {t} invalid")
    if list(net.reach) != sorted(set(net.reach)) or list(net.trust) != sorted(set(net.trust)):
        raise ValueError("reach and trust must be sorted and duplicate-free")
    for key in ("family", "seed", "params", "schema_version"):
        if key not in net.meta:
            raise ValueError(f"meta is missing {key!r}")


def host_links(net: Network) -> set[tuple[int, int]]:
    """Directed host-to-host connectivity implied by the reach edges."""
    return {(r.src, net.services[r.service].host) for r in net.reach}


def structure_stats(net: Network) -> dict:
    """Cheap label-free structural statistics (ignore zones and meta).

    - depth: largest BFS hop distance from the internet over host links.
    - deep_share: fraction of internal hosts at distance >= 3. A flat LAN
      puts almost every host one hop behind an exposed host (distance <= 2).
      Tiers and hubs force longer paths.
    - hub_share: fraction of internal host pairs with a link that touch the
      single highest-degree host (1.0 for a one-hub star).
    """
    links = host_links(net)
    out = {h.id: [] for h in net.hosts}
    for a, b in links:
        out[a].append(b)
    dist = {INTERNET: 0}
    queue = deque([INTERNET])
    while queue:
        a = queue.popleft()
        for b in sorted(out[a]):
            if b not in dist:
                dist[b] = dist[a] + 1
                queue.append(b)
    pairs = {tuple(sorted(p)) for p in links if INTERNET not in p}
    degree = {h.id: 0 for h in net.hosts[1:]}
    for a, b in pairs:
        degree[a] += 1
        degree[b] += 1
    top = max(degree.values(), default=0)
    return {
        "hosts": len(net.hosts) - 1,
        "services": len(net.services),
        "reach_edges": len(net.reach),
        "trust_edges": len(net.trust),
        "exposed_hosts": len({b for a, b in links if a == INTERNET}),
        "reachable_hosts": len(dist) - 1,
        "depth": max(dist.values()),
        "deep_share": sum(d >= 3 for d in dist.values()) / max(len(net.hosts) - 1, 1),
        "hub_share": top / len(pairs) if pairs else 0.0,
    }
