"""Attack-graph generator: a CVE-assigned network becomes a delete-free Task (D12).

Facts. Fact i is about host i, so a state's bitmask is the set of hosts the
attacker controls:

    attackerLocated(internet)   fact 0, the only initial fact
    execCode(h)                 the attacker can run code on internal host h

Actions (all preconditions conjunctive):

    exploit  one per reach edge (src -> service s on host h):
             pre {fact(src)}, add {execCode(h)}, cost cost_units(E) of s's CVE (D9)
    login    one per pair (trust edge t -> h, reach edge a -> login service on h):
             pre {execCode(t), fact(a)}, add {execCode(h)}, cost LOGIN_COST
             i.e. credentials taken from t AND network access to h's login service

Goal: execCode(target). These are MulVAL's execCode/attackerLocated facts with
MulVAL's cost-free intermediate facts (netAccess, canAccessHost,
principalCompromised) folded into the actions that consume them; D12 gives
the correspondence and why.

PR-gated variant (pr_gated=True; the default schema above is unchanged).
Each exploit also needs the capability its CVE's CVSS Privileges Required
(D13) asks for, as one extra conjunctive precondition. Two capability facts
follow the host facts, at indices n and n + 1:

    capability(user)    a low-privilege account. Taken from any internal host
                        the attacker controls: pre {execCode(h)}, cost LOGIN_COST
    capability(admin)   admin credentials. Taken only from a trust source t, the
                        hosts holding shared admin credentials (network.py):
                        pre {execCode(t)}, add both capabilities, cost LOGIN_COST

    PR:N exploit  pre {fact(src)}                     (unchanged)
    PR:L exploit  pre {fact(src), capability(user)}
    PR:H exploit  pre {fact(src), capability(admin)}

So the first foothold must come from a PR:N exploit. If no such exploit leads
anywhere, the goal is unreachable and build_task raises UnreachableGoal.

D15 sweep knobs (all off by default; off, the output is byte-identical to the
schema above, with or without pr_gated: tests/data/golden_tasks.json).
Their facts come after every other fact, so no existing index moves.

Depth, cred_levels = D. Tiered administrative credentials, as in
Active-Directory-style tiering: a level-k host accepts access only with
level-k credentials, which are cached on level k-1 machines where level-k
admins log in. assign_levels gives every internal host a level in {0..D}
(rng stream "depth:family:seed"): the target is at level D, one other host is
forced to each level 0..D-1 so the chain can exist, the rest are uniform.

    cred(k), k = 1..D       facts after the capabilities (if any)
    harvest cred(k)@h       h at level k-1: pre {execCode(h)}, add {cred(k)}, cost LOGIN_COST
    entry into level-k h    every exploit and login adding execCode(h), k >= 1,
                            also needs cred(k)

So entering a level-k host needs a credential taken from a different
(level k-1) host AND network access from a controlled src: a chain of D
conjunctive steps across hosts on the way to the target.

Coupling, coupling = rho and share_pool = m. Lateral movement that also
needs material from a third host: a database password read from an app
server's config, NTLM relay (a coercion host plus a host that reaches the
target), a payload staged on a file share. couple_exploits (rng stream
"coupling:family:seed") draws a pool of m secret-holder hosts (None: all
internal hosts), then selects each exploit with an internal src with
probability rho and adds execCode(k), k drawn from the pool minus {src, h}.
Exploits from the internet are never coupled, so the first foothold is as
before. A selected exploit with no eligible k is left unchanged and counted.
Small m means a few shared prerequisites; m = all hosts mostly distinct ones.
"""

import random
from dataclasses import dataclass

from .assign import assign_cves
from .cost import SCALE, cost_units
from .cve import CveRecord
from .heuristics import INF, hmax
from .network import INTERNET, Network, hop_distances
from .task import Action, Task
from .topology import generate

LOGIN_FAMILIES = ("rdp", "smb", "ssh")  # services that accept a login with stolen credentials
LOGIN_COST = SCALE  # c = 1 effort unit, the cost-model floor (D12)


class KnobInfeasible(ValueError):
    """A D15 knob setting cannot be realised on this network, e.g. too few hosts for D levels.

    Logged as a generation failure, separately from UnreachableGoal (D15 §4).
    """


class UnreachableGoal(Exception):
    """The goal privilege cannot be reached from the initial state.

    Generators guarantee reachability, so this is a generation failure: the
    caller logs it separately and never drops it or counts it as solved
    (CLAUDE.md rule 10).
    """


@dataclass(frozen=True)
class Instance:
    network: Network
    cves: dict[int, CveRecord]  # service id -> assigned CVE
    target: int  # goal host
    task: Task
    levels: dict[int, int] | None = None  # D15 depth knob: host -> credential level
    coupled: dict[int, int] | None = None  # D15 coupling knob: reach index -> extra host
    coupled_unchanged: int = 0  # selected for coupling but no eligible secret holder


def fact_name(net: Network, h: int) -> str:
    return "attackerLocated(internet)" if h == INTERNET else f"execCode({net.hosts[h].name})"


def build_task(net: Network, cves: dict[int, CveRecord], target: int, pr_gated: bool = False,
               levels: dict[int, int] | None = None, coupled: dict[int, int] | None = None) -> Task:
    """The fact–action graph of net as a Task with goal execCode(target).

    pr_gated selects the PR-gated variant; levels (from assign_levels) and
    coupled (from couple_exploits) the D15 knobs (module docstring).
    Raises UnreachableGoal if the goal cannot be reached.
    """
    if not 0 < target < len(net.hosts):
        raise ValueError(f"target {target} is not an internal host")
    name = [h.name for h in net.hosts]
    user, admin = len(net.hosts), len(net.hosts) + 1  # capability facts, used only if pr_gated
    gate = {"N": (), "L": (user,), "H": (admin,)} if pr_gated else {"N": (), "L": (), "H": ()}
    depth = max(levels.values()) if levels else 0
    cred0 = len(net.hosts) + (2 if pr_gated else 0)  # fact index of cred(1); cred(k) is cred0 + k - 1
    coupled = coupled or {}

    def cred_gate(h):
        # D15 depth: entering a host at level k >= 1 needs cred(k).
        k = levels.get(h, 0) if levels else 0
        return (cred0 + k - 1,) if k else ()

    actions = []
    for i, r in enumerate(net.reach):
        s = net.services[r.service]
        cve = cves[s.id]
        extra = (coupled[i],) if i in coupled else ()  # D15 coupling: control of a third host
        label = f" needs@{name[coupled[i]]}" if i in coupled else ""
        actions.append(Action(f"exploit {cve.cve_id} {s.family}@{name[s.host]} from {name[r.src]}{label}",
                              (r.src, *gate[cve.privileges_required], *extra, *cred_gate(s.host)), (s.host,),
                              cost_units(cve.exploitability_score)))
    for t in net.trust:
        for r in net.reach:
            s = net.services[r.service]
            if s.host == t.dst and s.family in LOGIN_FAMILIES:
                # Two preconditions unless the credentials and the network access
                # come from the same host.
                actions.append(Action(f"login {s.family}@{name[t.dst]} from {name[r.src]} creds@{name[t.src]}",
                                      (*sorted({t.src, r.src}), *cred_gate(t.dst)), (t.dst,), LOGIN_COST))
    facts = [fact_name(net, h.id) for h in net.hosts]
    if pr_gated:
        facts += ["capability(user)", "capability(admin)"]
        for h in net.hosts[1:]:
            actions.append(Action(f"harvest user@{h.name}", (h.id,), (user,), LOGIN_COST))
        # Admin credentials also grant the user capability: PR:H implies PR:L.
        for t in sorted({t.src for t in net.trust}):
            actions.append(Action(f"harvest admin@{name[t]}", (t,), (user, admin), LOGIN_COST))
    for k in range(1, depth + 1):
        facts.append(f"cred({k})")
        for h in net.hosts[1:]:
            if levels[h.id] == k - 1:
                actions.append(Action(f"harvest cred({k})@{h.name}", (h.id,), (cred0 + k - 1,), LOGIN_COST))
    task = Task(facts, actions, 1 << INTERNET, (target,))
    # The task is delete-free, so hmax is finite exactly when the goal is reachable.
    if hmax(task, task.init) == INF:
        raise UnreachableGoal(f"execCode({name[target]}) unreachable in {net.meta}")
    return task


def choose_target(net: Network, seed: int) -> int:
    """Goal host, drawn uniformly among the hosts the most hops from the internet.

    The deepest hosts stand in for the protected asset, and this rule avoids
    trivial one-exploit instances in every family. The rng stream
    "goal:family:seed" is separate from the topology and CVE streams.
    """
    dist = hop_distances(net)
    deepest = max(dist.values())
    rng = random.Random(f"goal:{net.meta['family']}:{seed}")
    return rng.choice(sorted(h for h, d in dist.items() if d == deepest))


def assign_levels(net: Network, target: int, cred_levels: int, seed: int) -> dict[int, int]:
    """D15 depth knob: internal host -> credential level in {0..cred_levels} (module docstring).

    The target is at the top level and one other host is forced to each lower
    level, so every level is occupied: without a level-0 host cred(1) could
    never be harvested. Raises KnobInfeasible if there are too few hosts.
    """
    others = [h.id for h in net.hosts[1:] if h.id != target]
    if len(others) < cred_levels:
        raise KnobInfeasible(f"{len(others) + 1} internal hosts cannot hold {cred_levels + 1} credential levels")
    rng = random.Random(f"depth:{net.meta['family']}:{seed}")
    level = {target: cred_levels}
    for k, h in enumerate(rng.sample(others, cred_levels)):
        level[h] = k
    for h in others:
        if h not in level:
            level[h] = rng.randint(0, cred_levels)
    return level


def couple_exploits(net: Network, coupling: float, share_pool: int | None, seed: int) -> tuple[dict[int, int], int]:
    """D15 coupling knob: (reach index -> extra precondition host, number left unchanged).

    share_pool = number of secret-holder hosts (None: every internal host).
    """
    internal = [h.id for h in net.hosts[1:]]
    m = len(internal) if share_pool is None else share_pool
    if not 1 <= m <= len(internal):
        raise KnobInfeasible(f"share_pool {m} outside 1..{len(internal)} internal hosts")
    rng = random.Random(f"coupling:{net.meta['family']}:{seed}")
    holders = sorted(rng.sample(internal, m))
    extra, unchanged = {}, 0
    for i, r in enumerate(net.reach):
        if r.src == INTERNET or rng.random() >= coupling:
            continue
        h = net.services[r.service].host
        eligible = [k for k in holders if k not in (r.src, h)]
        if eligible:
            extra[i] = rng.choice(eligible)
        else:
            unchanged += 1
    return extra, unchanged


def make_instance(family: str, seed: int, n_hosts: int, pool: list[CveRecord], pr_gated: bool = False,
                  cred_levels: int = 0, coupling: float = 0.0, share_pool: int | None = None,
                  **params) -> Instance:
    """Topology, CVE assignment, goal and Task, all from one seed (separate rng streams).

    cred_levels, coupling and share_pool are the D15 knobs; at their defaults
    no knob rng is drawn and the Task is the one built without them.
    """
    net = generate(family, seed, n_hosts, **params)
    cves = assign_cves(net, pool, seed)
    target = choose_target(net, seed)
    levels = assign_levels(net, target, cred_levels, seed) if cred_levels else None
    coupled, unchanged = couple_exploits(net, coupling, share_pool, seed) if coupling else (None, 0)
    task = build_task(net, cves, target, pr_gated, levels, coupled)
    return Instance(net, cves, target, task, levels, coupled, unchanged)
