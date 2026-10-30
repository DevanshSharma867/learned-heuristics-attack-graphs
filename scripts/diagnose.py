"""D22 §3 diagnostics on validation: headroom, sibling ordering, and the effect of f-ties.

Usage:
  python scripts/diagnose.py --batches DIR [DIR ...] --models RUN [RUN ...] [--tie-models RUN ...] [--name NAME]

  headroom    per instance, expansions of A* with h* itself against A* with h_max and LM-cut (D3 ties).
              h*(s) is the label where one exists, else A*+LM-cut from s (the labels' own solver).
  ordering    sibling-ordering accuracy (evaluate.sibling_order) of h_max, LM-cut, h_add, h_sp and each
              model, next to each model's MSE on all val labels (effort units).
  ties        each --tie-models model in A* as is, with h rounded to whole D9 units (a control), and
              rounded to whole effort units (38 D9 units, which creates f-ties); expansion ratios vs h_max.
Refuses test splits: D22 is validation only.
Output: results/evaluation/<name>/<stamp>-<commit>/.
"""

import argparse
import math
import statistics
from pathlib import Path

import torch

from ahg.cost import SCALE
from ahg.dataset import open_batch
from ahg.evaluate import _geo_ci, evaluate, sibling_groups, sibling_order, summarise
from ahg.heuristics import hadd, hmax, hsp, lmcut
from ahg.learning.heuristic import Learned
from ahg.learning.train import load
from ahg.runlog import load_raw, write_run
from ahg.search import astar

ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "results" / "evaluation"
BUDGET = 200_000
ORDER_BASELINES = {"hmax": hmax, "lmcut": lmcut, "hadd": hadd, "hsp": hsp}


class Rounded:
    """A learned heuristic with its value rounded to a multiple of `unit` D9 units (ties diagnostic only)."""

    def __init__(self, base: Learned, unit: int):
        self.base, self.unit, self.name = base, unit, f"{base.name}@round{unit}"

    def bind(self, inst):
        h, u = self.base.bind(inst), self.unit
        return lambda task, s: u * round(h(task, s) / u)

    def predict_states(self, inst, states):
        h = self.bind(inst)
        return [h(inst.task, s) / SCALE for s in states]


def by_instance(batch):
    out: dict[int, list] = {}
    for ex in batch.examples:
        out.setdefault(ex.instance, []).append(ex)
    return out


def headroom(batches) -> list[dict]:
    rows = []
    for batch in batches:
        exs_of = by_instance(batch)
        for i, rec in enumerate(batch.manifest["instances"]):
            if rec["stats"] is None:
                continue
            task = batch.instances[i].task
            memo = {ex.state: ex.hstar for ex in exs_of[i]}

            def hstar(t, s):
                if s not in memo:
                    memo[s] = astar(t, lmcut, start=s).cost  # INF when the goal is unreachable from s
                return memo[s]

            labelled = len(memo)
            r_star, r_hm, r_lm = astar(task, hstar), astar(task, hmax), astar(task, lmcut)
            if r_star.cost != rec["stats"]["hstar_init"]:
                raise AssertionError(f"seed {rec['spec']['seed']}: A* with h* cost {r_star.cost} != label")
            rows.append({"seed": rec["spec"]["seed"], "hstar": r_star.expanded, "hmax": r_hm.expanded,
                         "lmcut": r_lm.expanded, "plan_len": rec["stats"]["plan_len"],
                         "oracle_calls": len(memo) - labelled})
    return rows


def summarise_headroom(rows) -> dict:
    return {"instances": len(rows),
            "median": {k: statistics.median(r[k] for r in rows) for k in ("hstar", "hmax", "lmcut", "plan_len")},
            "hmax_optimal_effort": sum(r["hmax"] <= r["hstar"] for r in rows),
            "lmcut_optimal_effort": sum(r["lmcut"] <= r["hstar"] for r in rows),
            "hstar_over_hmax": _geo_ci([math.log(r["hstar"] / r["hmax"]) for r in rows], "headroom:hmax"),
            "hstar_over_lmcut": _geo_ci([math.log(r["hstar"] / r["lmcut"]) for r in rows], "headroom:lmcut"),
            "oracle_calls": sum(r["oracle_calls"] for r in rows)}


def ordering(batches, models: list[Learned]) -> dict:
    counts = {name: {"pairs": 0, "concordant": 0, "ties": 0} for name in [*ORDER_BASELINES, *(m.name for m in models)]}
    sq = {m.name: [0.0, 0] for m in models}
    for batch in batches:
        for i, exs in by_instance(batch).items():
            inst = batch.instances[i]
            groups = sibling_groups(inst.task, exs)
            states = {s for grp in groups for _, s, _ in grp}
            for name, h in ORDER_BASELINES.items():
                c = sibling_order(groups, {s: h(inst.task, s) for s in states})
                for k in c:
                    counts[name][k] += c[k]
            for m in models:
                preds = m.predict_states(inst, [ex.state for ex in exs])
                c = sibling_order(groups, {ex.state: p * SCALE for p, ex in zip(preds, exs)})
                for k in c:
                    counts[m.name][k] += c[k]
                sq[m.name][0] += sum((p - ex.hstar / SCALE) ** 2 for p, ex in zip(preds, exs))
                sq[m.name][1] += len(exs)
    out = {}
    for name, c in counts.items():
        out[name] = {**c, "accuracy": (c["concordant"] + 0.5 * c["ties"]) / c["pairs"], "tie_rate": c["ties"] / c["pairs"]}
        if name in sq:
            out[name]["val_mse"] = sq[name][0] / sq[name][1]
    return out


def render(raw) -> str:
    h = raw["headroom"]
    f = lambda ci: f"{ci[0]:.3f} [{ci[1]:.3f}, {ci[2]:.3f}]"
    L = ["# D22 §3 diagnostics (validation)", "", "## Headroom: A* with h* itself", "",
         f"{h['instances']} instances; {h['oracle_calls']} states needed an oracle h* (A*+LM-cut).", "",
         "| | h* | h_max | LM-cut | plan length |", "|---|---|---|---|---|",
         "| median expansions | " + " | ".join(f"{h['median'][k]:g}" for k in ("hstar", "hmax", "lmcut", "plan_len")) + " |",
         "", f"- h_max expands no more than h*: {h['hmax_optimal_effort']} of {h['instances']} instances; "
             f"LM-cut: {h['lmcut_optimal_effort']}.",
         f"- exp(h*) / exp(h_max), geometric mean [95% CI]: {f(h['hstar_over_hmax'])}. This is the ratio vs h_max "
         "that a heuristic as good as h* reaches under D3.",
         f"- exp(h*) / exp(LM-cut): {f(h['hstar_over_lmcut'])}.", "",
         "## Sibling ordering (c(a) + h(s') vs c(a) + h*(s'))", "",
         "| heuristic | pairs | accuracy | tie rate | val MSE (effort²) |", "|---|---|---|---|---|"]
    for name, o in raw["ordering"].items():
        mse = f"{o['val_mse']:.3f}" if "val_mse" in o else "—"
        L.append(f"| {name} | {o['pairs']} | {o['accuracy']:.3f} | {o['tie_rate']:.3f} | {mse} |")
    L += ["", "## Ties: rounding learned h", "", "| model | expansions vs h_max | vs LM-cut | plan cost / h* |",
          "|---|---|---|---|"]
    for name, s in raw["ties"].items():
        L.append(f"| {name} | {f(s['vs']['hmax']['expansions'])} | {f(s['vs']['lmcut']['expansions'])} | "
                 f"{f(s['plan_cost'])} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batches", type=Path, nargs="+", required=True)
    ap.add_argument("--models", type=Path, nargs="+", required=True)
    ap.add_argument("--tie-models", type=Path, nargs="*", default=[])
    ap.add_argument("--name", default="d22-diagnostics")
    args = ap.parse_args()
    torch.set_num_threads(1)
    batches = [open_batch(b) for b in args.batches]  # no purpose: a test split is refused
    if {b.manifest["split"] for b in batches} != {"val"}:
        raise SystemExit("D22 diagnostics run on validation only")

    def learned(run):
        model, cfg = load(run / "model.pt")
        return Learned(model, cfg, load_raw(run)["name"].replace("search/", ""))

    models = [learned(r) for r in args.models]
    raw = {"batches": [b.manifest["batch_id"] for b in batches], "models": [str(r) for r in args.models]}
    raw["headroom_rows"] = headroom(batches)
    raw["headroom"] = summarise_headroom(raw["headroom_rows"])
    print("headroom", raw["headroom"], flush=True)
    raw["ordering"] = ordering(batches, models)
    print("ordering done", flush=True)
    tie = []
    for r in args.tie_models:
        base = learned(r)
        tie += [base, Rounded(base, 1), Rounded(base, SCALE)]
    records = evaluate(batches, tie, BUDGET)
    raw["ties"] = {name: {k: v[k] for k in ("vs", "plan_cost", "optimal", "solved")}
                   for name, v in summarise(records, [m.name for m in tie], BUDGET).items()}
    raw["tie_records"] = records
    out = write_run(args.name, raw, render(raw), [], {"batches": raw["batches"], "models": raw["models"],
                                                      "tie_models": [str(r) for r in args.tie_models]}, root=EVALUATION)
    print(out)
    print(render(raw))


if __name__ == "__main__":
    main()
