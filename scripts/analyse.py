"""D23 §2 statistics for one evaluation run: multi-seed estimates, nested bootstrap CIs, Holm-corrected Wilcoxon.

Usage:
  python scripts/analyse.py EVAL_RUN --manifest results/training/d23t1/frozen.json [--name NAME]

EVAL_RUN: a results/evaluation/<name>/<stamp>-<commit>/ folder written by scripts/evaluate.py --manifest.
Reads only its raw records (rule 11: aggregates are regenerated from raw outputs) and the manifest, which
maps each run to its D23 id (A, B, ablations) and seed. Writes results/analysis/<name>/<stamp>-<commit>/.

Per model id and comparator (A* with h0, h_max, h_sp, h_add, LM-cut; GBFS+h_add; wA*+h_add, w = 1.5, 2):
- per seed: the geometric-mean ratio over instances; reported as mean ± sd across seeds;
- pooled: geometric mean over instances and seeds, with the nested bootstrap 95% CI (instances, then seeds);
- primaries only (role "primary" in the manifest): the H1 Holm family, by expansions. Wilcoxon on
  d_i = (seed-mean log model expansions) - (log comparator expansions), Holm over every primary x comparator
  test, the rank-biserial r, and the D23 §2 verdict. Time and plan cost: CIs only, no p-values.
H2 per model: plan-cost ratio CI; "small cost" if its upper bound <= 1.05, "falsified" if its lower bound > 1.10.
On val every number here is a diagnostic: the primaries were selected on val (D22, D23 §1).
"""

import argparse
import json
import math
import statistics
from pathlib import Path

from ahg.evaluate import comparators
from ahg.runlog import load_raw, write_run
from ahg.stats import holm, nested_bootstrap, verdict, wilcoxon

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "results" / "analysis"


def groups(raw: dict, frozen: dict) -> dict[str, list[tuple[int, str]]]:
    """D23 id -> [(seed, model name in raw)], sorted by seed; max(h_max, .) runs become '<id>+max'."""
    out: dict[str, list[tuple[int, str]]] = {}
    for m in raw["models"]:
        hits = [r for r in frozen["runs"] if m["run"].endswith(r["run"])]
        if len(hits) != 1:
            raise SystemExit(f"{m['run']} matches {len(hits)} manifest runs")
        gid = hits[0]["id"] + ("+max" if m["combine"] else "")
        out.setdefault(gid, []).append((hits[0]["seed"], m["name"]))
    return {k: sorted(v) for k, v in out.items()}


def analyse(raw: dict, frozen: dict) -> dict:
    recs, budget = raw["records"], raw["budget"]
    comps = comparators(recs)
    exp = lambda r, h: max(1, r["runs"][h]["expanded"] if not r["runs"][h]["budget_hit"] else budget)
    metric = {
        "expansions": lambda r, m, c: math.log(exp(r, m) / exp(r, c)),
        "time": lambda r, m, c: math.log(r["runs"][m]["seconds"] / r["runs"][c]["seconds"]),
    }
    primaries = {r["id"] for r in frozen["runs"] if r["role"] == "primary"}
    out = {"split": raw["split"], "instances": len(recs), "comparators": comps, "models": {}, "searches": {}}
    tests = []
    for gid, members in groups(raw, frozen).items():
        seeds, names = [s for s, _ in members], [n for _, n in members]
        g = {"seeds": seeds, "primary": gid in primaries, "vs": {}}
        for c in comps:
            g["vs"][c] = {}
            for key, f in metric.items():
                logs = [[f(r, m, c) for m in names] for r in recs]
                per_seed = [math.exp(statistics.fmean(col)) for col in zip(*logs)]
                g["vs"][c][key] = {
                    "per_seed": per_seed, "mean": statistics.fmean(per_seed),
                    "sd": statistics.stdev(per_seed) if len(per_seed) > 1 else 0.0,
                    "pooled": nested_bootstrap(logs, f"{gid}:{c}:{key}")}
            if gid in primaries:
                d = [statistics.fmean(math.log(exp(r, m)) for m in names) - math.log(exp(r, c)) for r in recs]
                tests.append((gid, c, wilcoxon(d)))
        cost = [[math.log(r["runs"][m]["cost"] / r["hstar"]) if r["runs"][m]["cost"] is not None else float("nan")
                 for m in names] for r in recs]
        pc = nested_bootstrap(cost, f"{gid}:cost")
        optimal = [sum(r["runs"][m]["cost"] == r["hstar"] for r in recs) for m in names]
        solved = [sum(r["runs"][m]["cost"] is not None for r in recs) for m in names]
        over = {grp: [raw["summary"][m]["overestimation"][grp]["rate"] for m in names]
                for grp in raw["summary"][names[0]]["overestimation"]}
        g["h2"] = {"plan_cost": pc, "optimal_per_seed": optimal, "solved_per_seed": solved,
                   "verdict": "small cost" if pc[2] <= 1.05 else "falsified" if pc[1] > 1.10 else "neither",
                   "overestimation_rate_mean": {k: statistics.fmean(v) for k, v in over.items()}}
        out["models"][gid] = g
    adj = holm([t["p"] for _, _, t in tests])
    out["h1"] = [{"model": gid, "comparator": c, **t, "p_holm": p,
                  "ratio": out["models"][gid]["vs"][c]["expansions"]["pooled"],
                  "verdict": verdict(out["models"][gid]["vs"][c]["expansions"]["pooled"], p)}
                 for (gid, c, t), p in zip(tests, adj)]
    for c in [c for c in ("hadd", "gbfs_hadd", "wastar1.5_hadd", "wastar2_hadd") if c in comps]:
        cost = [[math.log(r["runs"][c]["cost"] / r["hstar"]) if r["runs"][c]["cost"] is not None else float("nan")]
                for r in recs]
        out["searches"][c] = {"plan_cost": nested_bootstrap(cost, f"{c}:cost"),
                              "optimal": sum(r["runs"][c]["cost"] == r["hstar"] for r in recs),
                              "solved": sum(r["runs"][c]["cost"] is not None for r in recs)}
    return out


def ci(v) -> str:
    return "—" if v is None else f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"


def ms(v) -> str:
    return f"{v['mean']:.3f} ± {v['sd']:.3f}"


def render(a: dict, source: str) -> str:
    comps, models = a["comparators"], a["models"]
    L = [f"# D23 statistics on {a['split']}", "", f"Source: `{source}`. {a['instances']} instances.",
         "Ratios are model / comparator. **mean ± sd**: the per-seed geometric mean over instances, then the mean "
         "and sd of those across seeds. **pooled**: the geometric mean over instances and seeds, with the nested "
         "bootstrap 95% CI (10,000 resamples: instances, then seeds within each). Diagnostic on val: the primaries "
         "were selected on val.", ""]
    for key in ("expansions", "time"):
        L += [f"## {key.capitalize()}: mean ± sd across seeds", "", "| model | seeds | " + " | ".join(comps) + " |",
              "|---|---|" + "---|" * len(comps)]
        L += [f"| {g} | {len(v['seeds'])} | " + " | ".join(ms(v["vs"][c][key]) for c in comps) + " |"
              for g, v in models.items()]
        L += ["", f"## {key.capitalize()}: pooled, nested bootstrap CI", "",
              "| model | " + " | ".join(comps) + " |", "|---|" + "---|" * len(comps)]
        L += [f"| {g} | " + " | ".join(ci(v["vs"][c][key]["pooled"]) for c in comps) + " |" for g, v in models.items()]
        L.append("")
    L += ["## H1 family (primaries, expansions): Wilcoxon signed-rank, Holm over all rows", "",
          "| model | comparator | ratio (pooled CI) | n nonzero | W+ | W- | p | p Holm | rank-biserial r | verdict |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {t['model']} | {t['comparator']} | {ci(t['ratio'])} | {t['n_nonzero']} | {t['w_plus']:.1f} | "
          f"{t['w_minus']:.1f} | {t['p']:.2e} | {t['p_holm']:.2e} | {t['rank_biserial']:+.3f} | {t['verdict']} |"
          for t in a["h1"]]
    L += ["", "r < 0: the model expands fewer nodes on most instances.", "",
          "## H2: plan cost / h*", "", "H2 (D17 §2): **small cost** if the CI upper bound is ≤ 1.05; **falsified** if "
          "the CI lower bound is > 1.10; **neither** otherwise (not met, not falsified).", "", "| model | plan cost (pooled CI) | optimal per seed | solved per seed | "
          "H2 | overestimation rate, mean over seeds (walk / A*-expanded / successor) |", "|---|---|---|---|---|---|"]
    for g, v in models.items():
        o = v["h2"]["overestimation_rate_mean"]
        L.append(f"| {g} | {ci(v['h2']['plan_cost'])} | {v['h2']['optimal_per_seed']} | {v['h2']['solved_per_seed']} | "
                 f"{v['h2']['verdict']} | {' / '.join(f'{o[k]:.3f}' for k in o)} |")
    L += ["", "## Inadmissible classical searches: plan cost / h* (instance bootstrap)", "",
          "| search | plan cost | optimal | solved |", "|---|---|---|---|"]
    L += [f"| {c} | {ci(v['plan_cost'])} | {v['optimal']}/{a['instances']} | {v['solved']}/{a['instances']} |"
          for c, v in a["searches"].items()]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", type=Path)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--name")
    args = ap.parse_args()
    raw, frozen = load_raw(args.run), json.loads(args.manifest.read_text())
    a = analyse(raw, frozen)
    source = str(args.run.resolve().relative_to(ROOT))
    a["source"], a["manifest"] = source, str(args.manifest)
    md = render(a, source)
    out = write_run(args.name or f"{raw['split']}-stats", a, md, [], {"source": source, "manifest": str(args.manifest)},
                    root=ANALYSIS)
    print(out)
    print(md)


if __name__ == "__main__":
    main()
