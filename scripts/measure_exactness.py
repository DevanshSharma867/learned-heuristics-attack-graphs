"""How exact h_max and LM-cut are, on three state populations reported separately (AUDIT_2, D24 §7).

Usage: python scripts/measure_exactness.py BATCH [BATCH ...] [--enum-cap N] [--workers K] [--name NAME]

BATCH: a non-test label batch (train or val; a test batch is refused, so no test label is read).
Populations, per heuristic h in {h_max, LM-cut}:
  1. initial states: one per labelled instance, h(init) against the label h*(init);
  2. all reachable non-goal states, by exact enumeration (measure.enumerate_exact), for the instances with
     at most --enum-cap reachable states; state-weighted and instance-weighted (mean of per-instance rates);
  3. label states: the batch's labelled states, overall and by label source (optimal path, walk, A*-expanded
     by LM-cut / h_max, successor). A state with several sources counts in each.
"Exact" means h(s) = h*(s). Gaps are h* - h in effort units (D9 units / 38); both heuristics are admissible,
so a gap is never negative (checked). Output: results/landscape/exactness/<name>/<stamp>-<commit>/.
"""

import argparse
import statistics
from functools import cache
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from ahg.cost import SCALE
from ahg.dataset import open_batch
from ahg.heuristics import hmax, lmcut
from ahg.labels import SOURCES
from ahg.measure import enumerate_exact
from ahg.runlog import LANDSCAPE, write_run
from ahg.splits import SPLITS

HEURISTICS = {"hmax": hmax, "lmcut": lmcut}


def gaps(task, pairs):
    """pairs: (state, h*) in D9 units -> {heuristic: [h* - h in effort units]}."""
    out = {name: [] for name in HEURISTICS}
    for s, hs in pairs:
        for name, h in HEURISTICS.items():
            g = hs - h(task, s)
            assert g >= 0, f"{name} overestimates: h* {hs}, h {hs - g}"
            out[name].append(g / SCALE)
    return out


@cache
def _batch(batch_dir):  # once per worker process
    return open_batch(batch_dir)


def one_instance(args):
    batch_dir, i, cap = args
    b = _batch(batch_dir)
    inst, rec = b.instances[i], b.manifest["instances"][i]
    task = inst.task
    exs = [ex for ex in b.examples if ex.instance == i]
    res = {"seed": rec["spec"]["seed"], "cell": {k: rec["spec"][k] for k in ("variant", "n", "D", "rho", "m")},
           "init": gaps(task, [(task.init, rec["stats"]["hstar_init"])]),
           "labels": {src: gaps(task, [(ex.state, ex.hstar) for ex in exs if src in ex.sources]) for src in SOURCES}}
    res["labels"]["all"] = gaps(task, [(ex.state, ex.hstar) for ex in exs])
    hstar = enumerate_exact(task, cap)
    res["reachable"] = None if hstar is None else gaps(task, [(s, h) for s, h in hstar.items() if h > 0])
    return res


def summary(gs: list[float]) -> dict:
    return {"n": len(gs), "exact": sum(g == 0 for g in gs) / len(gs) if gs else None,
            "mean_gap": statistics.fmean(gs) if gs else None, "max_gap": max(gs, default=None)}


def summarise(recs: list[dict]) -> dict:
    out = {}
    for h in HEURISTICS:
        enum = [r for r in recs if r["reachable"] is not None]
        rates = [summary(r["reachable"][h])["exact"] for r in enum if r["reachable"][h]]
        out[h] = {"init": summary([g for r in recs for g in r["init"][h]]),
                  "reachable": {**summary([g for r in enum for g in r["reachable"][h]]),
                                "instances": len(enum), "instance_weighted_exact": statistics.fmean(rates) if rates else None},
                  "labels": {src: summary([g for r in recs for g in r["labels"][src][h]]) for src in [*SOURCES, "all"]}}
    return out


def fmt(s) -> str:
    if not s["n"]:
        return "— (0)"
    return f"{s['exact']:.3f} ({s['mean_gap']:.2f}; {s['max_gap']:.2f}; {s['n']:,})"


def render(raw) -> str:
    L = [f"# Exactness of h_max and LM-cut by state population ({', '.join(raw['batches'])})", "",
         f"{raw['instances']} labelled instances. Each cell: fraction with h = h\\* (mean gap; max gap, effort units; "
         f"states). All reachable states: the {raw['summary']['hmax']['reachable']['instances']} instances with at most "
         f"{raw['enum_cap']:,} reachable states (state-weighted; instance-weighted in its own column).", "",
         "| heuristic | initial states | all reachable (state-wt.) | all reachable (inst.-wt.) | label states (all) | "
         + " | ".join(f"label: {s}" for s in SOURCES) + " |", "|---|---|---|---|---|" + "---|" * len(SOURCES)]
    for h, v in raw["summary"].items():
        iw = v["reachable"]["instance_weighted_exact"]
        L.append(f"| {h} | {fmt(v['init'])} | {fmt(v['reachable'])} | {'—' if iw is None else f'{iw:.3f}'} | "
                 f"{fmt(v['labels']['all'])} | " + " | ".join(fmt(v["labels"][s]) for s in SOURCES) + " |")
    L += ["", "By cell (initial states; fraction exact, h_max / LM-cut):", "", "| variant | n | D | instances | h_max | LM-cut |",
          "|---|---|---|---|---|---|"]
    cells = {}
    for r in raw["records"]:
        cells.setdefault((r["cell"]["variant"], r["cell"]["n"], r["cell"]["D"]), []).append(r)
    for (v, n, D), rs in sorted(cells.items()):
        ex = {h: sum(r["init"][h][0] == 0 for r in rs) for h in HEURISTICS}
        L.append(f"| {v} | {n} | {D} | {len(rs)} | {ex['hmax']}/{len(rs)} | {ex['lmcut']}/{len(rs)} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batches", type=Path, nargs="+")
    ap.add_argument("--enum-cap", type=int, default=20_000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--name", default="exactness")
    args = ap.parse_args()
    jobs = []
    for d in args.batches:
        b = open_batch(d)
        if SPLITS[b.manifest["split"]].is_test:
            raise SystemExit("test batches are not read here")
        jobs += [(d, i, args.enum_cap) for i, r in enumerate(b.manifest["instances"]) if r["stats"] is not None]
    with ProcessPoolExecutor(args.workers) as ex:
        recs = list(ex.map(one_instance, jobs))
    raw = {"batches": [d.name for d in args.batches], "instances": len(recs), "enum_cap": args.enum_cap,
           "records": recs, "summary": summarise(recs)}
    out = write_run(args.name, raw, render(raw), sorted({r["seed"] for r in recs}),
                    {"batches": raw["batches"], "enum_cap": args.enum_cap}, root=LANDSCAPE / "exactness")
    print(out)
    print(render(raw))


if __name__ == "__main__":
    main()
