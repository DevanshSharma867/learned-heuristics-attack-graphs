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


def fact_name(net: Network, h: int) -> str:
    return "attackerLocated(internet)" if h == INTERNET else f"execCode({net.hosts[h].name})"


def build_task(net: Network, cves: dict[int, CveRecord], target: int, pr_gated: bool = False) -> Task:
    """The fact–action graph of net as a Task with goal execCode(target).

    pr_gated selects the PR-gated variant (module docstring).
    Raises UnreachableGoal if the goal cannot be reached.
    """
    if not 0 < target < len(net.hosts):
        raise ValueError(f"target {target} is not an internal host")
    name = [h.name for h in net.hosts]
    user, admin = len(net.hosts), len(net.hosts) + 1  # capability facts, used only if pr_gated
    gate = {"N": (), "L": (user,), "H": (admin,)} if pr_gated else {"N": (), "L": (), "H": ()}
    actions = []
    for r in net.reach:
        s = net.services[r.service]
        cve = cves[s.id]
        actions.append(Action(f"exploit {cve.cve_id} {s.family}@{name[s.host]} from {name[r.src]}",
                              (r.src, *gate[cve.privileges_required]), (s.host,),
                              cost_units(cve.exploitability_score)))
    for t in net.trust:
        for r in net.reach:
            s = net.services[r.service]
            if s.host == t.dst and s.family in LOGIN_FAMILIES:
                # Two preconditions unless the credentials and the network access
                # come from the same host.
                actions.append(Action(f"login {s.family}@{name[t.dst]} from {name[r.src]} creds@{name[t.src]}",
                                      tuple(sorted({t.src, r.src})), (t.dst,), LOGIN_COST))
    facts = [fact_name(net, h.id) for h in net.hosts]
    if pr_gated:
        facts += ["capability(user)", "capability(admin)"]
        for h in net.hosts[1:]:
            actions.append(Action(f"harvest user@{h.name}", (h.id,), (user,), LOGIN_COST))
        # Admin credentials also grant the user capability: PR:H implies PR:L.
        for t in sorted({t.src for t in net.trust}):
            actions.append(Action(f"harvest admin@{name[t]}", (t,), (user, admin), LOGIN_COST))
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


def make_instance(family: str, seed: int, n_hosts: int, pool: list[CveRecord], pr_gated: bool = False,
                  **params) -> Instance:
    """Topology, CVE assignment, goal and Task, all from one seed (three separate rng streams)."""
    net = generate(family, seed, n_hosts, **params)
    cves = assign_cves(net, pool, seed)
    target = choose_target(net, seed)
    return Instance(net, cves, target, build_task(net, cves, target, pr_gated))
