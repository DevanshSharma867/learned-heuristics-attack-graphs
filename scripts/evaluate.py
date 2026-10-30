"""Run the D21 §4 harness: every baseline and every given model in A* on one split's label batches.

Usage:
  python scripts/evaluate.py --batches DIR [DIR ...] --models RUN [RUN ...] [--max-hmax RUN ...] [--name NAME]
                             [--purpose evaluation --permitted-by D-ENTRY]

  RUN: a results/training/ run folder (its model.pt is loaded).
  --max-hmax RUN: also search with max(h_max, h_θ) for that model, named <model>+max (D22 variant b).
  A test-split batch is opened only with --purpose; open_batch logs the read in
  results/test_access_log.jsonl before anything is loaded, and refuses a second
  evaluation of a split without --permitted-by.

The learned heuristics run with one torch thread: the baselines are single-threaded
Python, so every heuristic gets one core and the end-to-end times compare like with like.
Output: results/evaluation/<name>/<stamp>-<commit>/ (raw records, summary, report).
"""

import argparse
import hashlib
from pathlib import Path

import torch

from ahg.dataset import open_batch
from ahg.evaluate import BASELINES, STATE_GROUPS, evaluate, summarise
from ahg.learning.heuristic import Learned
from ahg.learning.train import load
from ahg.runlog import load_raw, write_run

ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "results" / "evaluation"
BUDGET = 200_000


def model_name(run: Path) -> str:
    return load_raw(run)["name"].replace("search/", "")


def fmt(ci) -> str:
    return "—" if ci is None else f"{ci[0]:.3f} [{ci[1]:.3f}, {ci[2]:.3f}]"


def order(v) -> str:
    o = v.get("sibling_order")
    return "—" if not o or o["accuracy"] is None else f"{o['accuracy']:.3f} ({o['tie_rate']:.3f}, {o['pairs']})"


def render(raw) -> str:
    s, split = raw["summary"], raw["split"]
    L = [f"# evaluation on {split} (D21 §4)", "", f"{raw['instances']} labelled instances; budget {BUDGET:,} "
         f"expansions; torch threads {raw['torch_threads']}. Ratios are model / baseline, geometric mean "
         "[bootstrap 95% CI over instances]; < 1 means the model expands fewer nodes or is faster.", "",
         "## Expansions", "", "| model | " + " | ".join(BASELINES) + " |", "|---|" + "---|" * len(BASELINES)]
    L += [f"| {m} | " + " | ".join(fmt(v["vs"][b]["expansions"]) for b in BASELINES) + " |" for m, v in s.items()]
    L += ["", "## End-to-end time", "", "| model | " + " | ".join(BASELINES) + " |", "|---|" + "---|" * len(BASELINES)]
    L += [f"| {m} | " + " | ".join(fmt(v["vs"][b]["time"]) for b in BASELINES) + " |" for m, v in s.items()]
    L += ["", "## Plan cost and coverage", "",
          "| model | solved | budget hits | optimal | plan cost / h* | fewer / more expansions than LM-cut | "
          "sibling order acc. (tie rate, pairs) |", "|---|---|---|---|---|---|---|"]
    L += [f"| {m} | {v['solved']}/{v['instances']} | {v['budget_hits']} | {v['optimal']} | {fmt(v['plan_cost'])} | "
          f"{v['vs']['lmcut']['fewer']} / {v['vs']['lmcut']['more']} | {order(v)} |" for m, v in s.items()]
    L += ["", "## Overestimation (effort units)", "", "| model | states | rate h_θ > h* | mean violation | "
          "max violation | mean abs error |", "|---|---|---|---|---|---|"]
    for m, v in s.items():
        for g in STATE_GROUPS:
            o = v["overestimation"][g]
            L.append(f"| {m} ({g}) | {o['states']} | {o['rate']:.3f} | {o['mean_violation']:.3f} | "
                     f"{o['max_violation']:.3f} | {o['mean_abs_error']:.3f} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batches", type=Path, nargs="+", required=True)
    ap.add_argument("--models", type=Path, nargs="+", required=True)
    ap.add_argument("--max-hmax", type=Path, nargs="*", default=[])
    ap.add_argument("--name")
    ap.add_argument("--purpose")
    ap.add_argument("--permitted-by")
    args = ap.parse_args()
    torch.set_num_threads(1)
    batches = [open_batch(b, purpose=args.purpose, permitted_by=args.permitted_by) for b in args.batches]
    splits = {b.manifest["split"] for b in batches}
    if len(splits) != 1:
        raise SystemExit(f"one split per evaluation, got {sorted(splits)}")
    split = splits.pop()
    learned, models = [], []
    for run, combine in [(r, None) for r in args.models] + [(r, "max_hmax") for r in args.max_hmax]:
        model, cfg = load(run / "model.pt")
        name = model_name(run) + ("+max" if combine else "")
        learned.append(Learned(model, cfg, name, combine))
        models.append({"name": name, "run": str(run), "combine": combine,
                       "model_sha256": hashlib.sha256((run / "model.pt").read_bytes()).hexdigest()})
    if len({m["name"] for m in models}) != len(models):
        raise SystemExit(f"model names must be unique: {[m['name'] for m in models]}")
    records = evaluate(batches, learned, BUDGET)
    raw = {"split": split, "batches": [b.manifest["batch_id"] for b in batches], "models": models,
           "instances": len(records), "torch_threads": torch.get_num_threads(), "budget": BUDGET,
           "records": records, "summary": summarise(records, [m["name"] for m in models], BUDGET)}
    out = write_run(args.name or split, raw, render(raw), [], {"batches": raw["batches"], "models": models},
                    root=EVALUATION)
    print(out)
    print(render(raw))


if __name__ == "__main__":
    main()
