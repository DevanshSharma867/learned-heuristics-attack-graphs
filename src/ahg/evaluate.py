"""The evaluation harness (D21 §4): every heuristic in A* on every labelled instance of one split.

evaluate() takes already-opened batches. For a test split, opening them went
through the test-access log (dataset.open_batch with purpose="evaluation"),
so this module has no per-split branches: validation and test go through the
same code.

Per instance it runs A* from the initial state with each baseline and each
learned heuristic (same best_first_search, tie-breaking, duplicate
detection and budget), and checks that every admissible baseline returns the
label h*(init). Per learned model it also evaluates h_θ on the instance's
labelled states, for overestimation statistics by source, and the sibling-ordering
accuracy (D22 §3.2) on the labelled successors of labelled A*-expanded states.
summarise() turns the raw records into ratios with bootstrap CIs; it reads
nothing but the raw records, so aggregates can always be regenerated.
"""

import math
import random
from itertools import combinations

from .cost import SCALE
from .heuristics import ADMISSIBLE, INF, h0, hadd, hmax, hsp, lmcut
from .measure import HardFailure
from .search import astar
from .task import plan_cost

BASELINES = {"h0": h0, "hmax": hmax, "hsp": hsp, "hadd": hadd, "lmcut": lmcut}
STATE_GROUPS = {"walk": {"walk"}, "astar_expanded": {"expanded_lmcut", "expanded_hmax"}, "successor": {"successor"}}
BOOTSTRAP = 10_000


def sibling_groups(task, exs) -> list[list[tuple[int, int, int]]]:
    """For each labelled A*-expanded state: its labelled successors as (action cost, state, h*), D9 units.

    A* orders siblings by c(a) + h(s'), since they share g; a successor reached by several actions
    keeps the cheapest. Only labelled successors are used, so no new labels are computed.
    """
    lab = {ex.state: ex.hstar for ex in exs}
    groups = []
    for ex in exs:
        if not set(ex.sources) & STATE_GROUPS["astar_expanded"]:
            continue
        best: dict[int, int] = {}
        for ai, s2 in task.successors(ex.state):
            if s2 in lab:
                best[s2] = min(task.actions[ai].cost, best.get(s2, INF))
        if len(best) > 1:
            groups.append([(c, s2, lab[s2]) for s2, c in best.items()])
    return groups


def sibling_order(groups, h: dict) -> dict:
    """Pairs of siblings whose c + h* differ: concordant if c + h orders them the same way, tied if c + h is
    equal (counted 0.5 in the accuracy). h: state -> value in D9 units."""
    pairs = concordant = ties = 0
    for grp in groups:
        for (c1, s1, t1), (c2, s2, t2) in combinations(grp, 2):
            true = (c1 + t1) - (c2 + t2)
            if true == 0:
                continue
            est = (c1 + h[s1]) - (c2 + h[s2])
            pairs += 1
            if abs(est) < 1e-9:
                ties += 1
            elif (est > 0) == (true > 0):
                concordant += 1
    return {"pairs": pairs, "concordant": concordant, "ties": ties}


def _run(task, h, budget):
    r = astar(task, h, max_expansions=budget)
    if r.solved:
        assert plan_cost(task, r.plan) == r.cost  # the plan is executable and its cost is what search says
    return {"expanded": r.expanded, "generated": r.generated, "evaluations": r.evaluations,
            "cost": r.cost if r.solved else None, "seconds": r.seconds, "budget_hit": r.budget_hit}


def evaluate(batches, learned: list, budget: int = 200_000) -> list[dict]:
    """One record per labelled instance. learned: list of learning.heuristic.Learned."""
    records = []
    for batch in batches:
        by_inst: dict[int, list] = {}
        for ex in batch.examples:
            by_inst.setdefault(ex.instance, []).append(ex)
        for i, inst_rec in enumerate(batch.manifest["instances"]):
            if inst_rec["stats"] is None:
                continue
            inst, hstar = batch.instances[i], inst_rec["stats"]["hstar_init"]
            task = inst.task
            rec = {"batch": batch.manifest["batch_id"], "seed": inst_rec["spec"]["seed"],
                   "cell": {k: inst_rec["spec"][k] for k in ("variant", "n", "D", "rho", "m")},
                   "hstar": hstar, "runs": {}, "over": {}, "order": {}}
            for name, h in BASELINES.items():
                rec["runs"][name] = _run(task, h, budget)
                got = rec["runs"][name]["cost"]
                if name in ADMISSIBLE and not rec["runs"][name]["budget_hit"] and got != hstar:
                    raise HardFailure(f"seed {rec['seed']}: A*+{name} cost {got} != label h* {hstar}")
            exs = by_inst[i]
            groups = sibling_groups(task, exs)
            for model in learned:
                rec["runs"][model.name] = _run(task, model.bind(inst), budget)
                preds = model.predict_states(inst, [ex.state for ex in exs])
                rec["over"][model.name] = {
                    g: [p - ex.hstar / SCALE for p, ex in zip(preds, exs) if set(ex.sources) & srcs]
                    for g, srcs in STATE_GROUPS.items()}
                h_of = {ex.state: p * SCALE for p, ex in zip(preds, exs)}
                rec["order"][model.name] = sibling_order(groups, h_of)
            records.append(rec)
    return records


def _geo_ci(logs: list[float], key: str):
    """Geometric mean of exp(logs) with a bootstrap 95% CI over instances."""
    n = len(logs)
    if not n:
        return None
    rng = random.Random(f"bootstrap:{key}")
    means = sorted(sum(rng.choices(logs, k=n)) / n for _ in range(BOOTSTRAP))
    return [math.exp(sum(logs) / n), math.exp(means[int(0.025 * BOOTSTRAP)]), math.exp(means[int(0.975 * BOOTSTRAP) - 1])]


def summarise(records: list[dict], models: list[str], budget: int) -> dict:
    """Per model: expansion and time ratios against every baseline, plan-cost ratio, overestimation by group."""
    out = {}
    for m in models:
        s = {"instances": len(records), "budget_hits": sum(r["runs"][m]["budget_hit"] for r in records),
             "vs": {}}
        exp = lambda r, h: max(1, r["runs"][h]["expanded"] if not r["runs"][h]["budget_hit"] else budget)
        for b in BASELINES:
            s["vs"][b] = {
                "expansions": _geo_ci([math.log(exp(r, m) / exp(r, b)) for r in records], f"{m}:{b}:exp"),
                "time": _geo_ci([math.log(r["runs"][m]["seconds"] / r["runs"][b]["seconds"]) for r in records],
                                f"{m}:{b}:time"),
                "fewer": sum(exp(r, m) < exp(r, b) for r in records),
                "more": sum(exp(r, m) > exp(r, b) for r in records)}
        solved = [r for r in records if r["runs"][m]["cost"] is not None]
        s["plan_cost"] = _geo_ci([math.log(r["runs"][m]["cost"] / r["hstar"]) for r in solved], f"{m}:cost")
        s["optimal"] = sum(r["runs"][m]["cost"] == r["hstar"] for r in solved)
        s["solved"] = len(solved)
        s["overestimation"] = {}
        for g in STATE_GROUPS:
            d = [x for r in records for x in r["over"][m][g]]
            viol = [x for x in d if x > 1e-9]
            s["overestimation"][g] = {"states": len(d), "rate": len(viol) / len(d) if d else None,
                                      "mean_violation": sum(viol) / len(viol) if viol else 0.0,
                                      "max_violation": max(viol, default=0.0),
                                      "mean_abs_error": sum(abs(x) for x in d) / len(d) if d else None}
        o = [r["order"][m] for r in records if m in r.get("order", {})]
        n = sum(x["pairs"] for x in o)
        s["sibling_order"] = {"pairs": n, "accuracy": (sum(x["concordant"] for x in o) + 0.5 * sum(x["ties"] for x in o)) / n
                              if n else None, "tie_rate": sum(x["ties"] for x in o) / n if n else None}
        out[m] = s
    return out
