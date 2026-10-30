"""The evaluation harness (D21 §4): every heuristic in A* on every labelled instance of one split.

evaluate() takes already-opened batches. For a test split, opening them went
through the test-access log (dataset.open_batch with purpose="evaluation"),
so this module has no per-split branches: validation and test go through the
same code.

Per instance it runs A* from the initial state with each baseline and each
learned heuristic (same best_first_search, tie-breaking, duplicate
detection and budget), and checks that every admissible baseline returns the
label h*(init). Per learned model it also evaluates h_θ on the instance's
labelled states, for overestimation statistics by source.
summarise() turns the raw records into ratios with bootstrap CIs; it reads
nothing but the raw records, so aggregates can always be regenerated.
"""

import math
import random

from .cost import SCALE
from .heuristics import ADMISSIBLE, h0, hadd, hmax, hsp, lmcut
from .measure import HardFailure
from .search import astar
from .task import plan_cost

BASELINES = {"h0": h0, "hmax": hmax, "hsp": hsp, "hadd": hadd, "lmcut": lmcut}
STATE_GROUPS = {"walk": {"walk"}, "astar_expanded": {"expanded_lmcut", "expanded_hmax"}, "successor": {"successor"}}
BOOTSTRAP = 10_000


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
                   "hstar": hstar, "runs": {}, "over": {}}
            for name, h in BASELINES.items():
                rec["runs"][name] = _run(task, h, budget)
                got = rec["runs"][name]["cost"]
                if name in ADMISSIBLE and not rec["runs"][name]["budget_hit"] and got != hstar:
                    raise HardFailure(f"seed {rec['seed']}: A*+{name} cost {got} != label h* {hstar}")
            exs = by_inst[i]
            for model in learned:
                rec["runs"][model.name] = _run(task, model.bind(inst), budget)
                preds = model.predict_states(inst, [ex.state for ex in exs])
                rec["over"][model.name] = {
                    g: [p - ex.hstar / SCALE for p, ex in zip(preds, exs) if set(ex.sources) & srcs]
                    for g, srcs in STATE_GROUPS.items()}
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
        out[m] = s
    return out
