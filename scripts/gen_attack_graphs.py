"""Generate one attack graph per topology family and solve it with A* under every heuristic.

Usage: python scripts/gen_attack_graphs.py [n_hosts] [seed]

Prints the task sizes, the optimal cost from the independent oracle, and per
heuristic: plan cost, nodes expanded and generated, and wall-clock time.
Unreachable goals are listed in their own FAILURES section, never dropped
(CLAUDE.md rule 10).
"""

import sys
from pathlib import Path

from ahg.attack_graph import UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.heuristics import HEURISTICS
from ahg.oracle import optimal_cost
from ahg.search import astar
from ahg.topology import GENERATORS

STATE_CAP = 200_000  # stop counting reachable states beyond this

n_hosts = int(sys.argv[1]) if len(sys.argv) > 1 else 8
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
pool = load_table(Path(__file__).resolve().parent.parent / "data" / "derived" / "cves.csv")


def count_reachable(task) -> str:
    seen, stack = {task.init}, [task.init]
    while stack:
        for _, s2 in task.successors(stack.pop()):
            if s2 not in seen:
                if len(seen) >= STATE_CAP:
                    return f">{STATE_CAP}"
                seen.add(s2)
                stack.append(s2)
    return str(len(seen))


failures = []
for family in GENERATORS:
    try:
        inst = make_instance(family, seed, n_hosts, pool)
    except UnreachableGoal as e:
        failures.append((family, seed, n_hosts, str(e)))
        continue
    t = inst.task
    logins = [a for a in t.actions if a.name.startswith("login")]
    conj = sum(len(a.pre) == 2 and 0 not in a.pre for a in logins)
    hstar = optimal_cost(t)
    print(f"=== {family}  seed={seed}  n_hosts={n_hosts}  goal={t.facts[inst.target]}")
    print(f"    facts={len(t.facts)}  actions={len(t.actions)} (exploit {len(t.actions) - len(logins)}, "
          f"login {len(logins)}, two internal preconditions {conj})  reachable states={count_reachable(t)}")
    print(f"    h* (oracle) = {hstar}  = {hstar / 38:.2f} effort units")
    print(f"    {'heuristic':9s} {'h(init)':>7s} {'cost':>6s} {'expanded':>8s} {'generated':>9s} {'ms':>8s}")
    for name, h in HEURISTICS.items():
        r = astar(t, h)
        print(f"    {name:9s} {h(t, t.init):7} {r.cost:6} {r.expanded:8} {r.generated:9} {1000 * r.seconds:8.2f}")
    plan = astar(t, HEURISTICS["lmcut"]).plan
    print("    optimal plan (A*/lmcut):")
    for i in plan:
        print(f"      {t.actions[i].cost:4}  {t.actions[i].name}")
    print()

print(f"FAILURES (unreachable goals): {len(failures)}")
for f in failures:
    print("   ", f)
