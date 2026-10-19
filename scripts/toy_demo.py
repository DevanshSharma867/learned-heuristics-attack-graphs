"""Print every heuristic and every search algorithm on the toy network (used in docs/learn)."""

from ahg.examples import toy_network
from ahg.heuristics import HEURISTICS
from ahg.search import astar, gbfs, uniform_cost, weighted_astar

t = toy_network()
print("initial state:", t.describe(t.init))
print("\nheuristic values at the initial state (true optimal cost h* = 150):")
for name, h in HEURISTICS.items():
    print(f"  {name:6s} {h(t, t.init)}")

print("\nsearch results:")
runs = {"UCS": uniform_cost(t)}
for name in ("hsp", "hmax", "lmcut", "hadd", "hff"):
    runs[f"A*({name})"] = astar(t, HEURISTICS[name])
runs["WA*(hmax, w=2)"] = weighted_astar(t, HEURISTICS["hmax"], 2.0)
runs["GBFS(hadd)"] = gbfs(t, HEURISTICS["hadd"])
for name, r in runs.items():
    plan = [t.actions[i].name for i in r.plan]
    print(f"  {name:15s} cost={r.cost:<4} expanded={r.expanded:<3} generated={r.generated:<3} plan={plan}")
