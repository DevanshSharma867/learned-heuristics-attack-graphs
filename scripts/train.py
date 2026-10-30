"""Training runs (D21 §3), the validation hyperparameter search (D21 §5), epoch timing and the cost projection.

Usage:
  python scripts/train.py run [--set KEY=VALUE ...] [--name NAME]
      One run from configs/training/d21.json with overrides, e.g. --set kind=gnn --set loss=asym.
  python scripts/train.py search [--budget-hours 3] [--set device=mps]
      The D21 §5 grid (seed 0, MSE), cheapest models first. A config starts only while the
      wall-clock budget lasts; the rest are recorded as not run. Every config is recorded,
      failures included, and the per-kind selection is by validation MSE.
  python scripts/train.py timing [--epochs 2]
      Seconds per training epoch for the GNN and MLP, on CPU and on MPS (no checkpoint).
  python scripts/train.py project --timing RUN --runs RUN [RUN ...]
      Projects the D17 seed plan's training cost from a timing run and the epochs the given
      pilot runs actually took before early stopping.

Runs go to results/training/<name>/<stamp>-<commit>/ through runlog (append-only).
"""

import argparse
import itertools
import json
import time
import traceback
from pathlib import Path

import torch

from ahg.dataset import open_batch
from ahg.learning.runs import ROOT, TRAINING, make_config, train_run
from ahg.learning.train import train_model
from ahg.runlog import load_raw, write_run

# D21 §5, fixed before training. Order: cheapest first, so a budget overrun loses the expensive configs.
GRID = {
    "wl": [{"lam": lam} for lam in (0.1, 1.0, 10.0)],
    "mlp": [{"lr": lr, "hidden": h} for lr, h in itertools.product((1e-3, 3e-3), (64, 128))],
    "gnn": [{"lr": lr, "hidden": h, "layers": l} for lr, h, l in itertools.product((1e-3, 3e-3), (64, 128), (3, 6))],
}
# The D17 §4 seed plan, used only for the projection: primary models × {MSE, asym} × 5 seeds;
# about 30 ablation runs (D17 §5) of the GNN at 3 seeds.
PLAN = {"gnn": 2 * 5, "mlp": 2 * 5, "gnn_ablation": 30}


def parse_set(pairs: list[str]) -> dict:
    out = {}
    for p in pairs:
        k, v = p.split("=", 1)
        try:
            out[k] = json.loads(v)  # numbers, lists, booleans
        except json.JSONDecodeError:
            out[k] = v  # a bare string such as gnn or mps
    return out


def run_name(cfg: dict) -> str:
    size = f"-{cfg['hidden']}x{cfg['layers']}" if cfg["kind"] == "gnn" else (
        f"-{cfg['hidden']}" if cfg["kind"] == "mlp" else f"-lam{cfg['lam']}")
    return f"{cfg['kind']}{size}-{cfg['loss']}-s{cfg['seed']}"


def load_batches(cfg):
    return ([open_batch(ROOT / p) for p in cfg["train_batches"]], [open_batch(ROOT / p) for p in cfg["val_batches"]])


def cmd_run(args):
    cfg = make_config(**parse_set(args.set))
    out, raw = train_run(cfg, args.name or run_name(cfg))
    print(f"{out}  best val loss {raw['best_val_loss']:.4f}  {raw['wall_seconds']:.0f} s")


def cmd_search(args):
    base = parse_set(args.set)
    batches = load_batches(make_config(**base))
    t0, budget = time.perf_counter(), args.budget_hours * 3600
    rows = []
    for kind, configs in GRID.items():
        for over in configs:
            cfg = make_config(**{**base, "kind": kind, "loss": "mse", "seed": 0, **over})
            row = {"kind": kind, "overrides": over, "config": cfg}
            if time.perf_counter() - t0 >= budget:
                rows.append({**row, "status": "not run (budget)"})
                continue
            try:
                out, raw = train_run(cfg, f"search/{run_name(cfg)}", batches)
                row.update(status="ok", best_val_loss=raw["best_val_loss"], seconds=raw["wall_seconds"],
                           epochs=sum("epoch" in e for e in raw["history"]), run=str(out.relative_to(ROOT)))
            except Exception as e:  # recorded, never dropped (D21 §5)
                row.update(status="failed", error=f"{type(e).__name__}: {e}", traceback=traceback.format_exc())
            rows.append(row)
            print(kind, over, row["status"], row.get("best_val_loss"), flush=True)
    selected = {}
    for kind in GRID:
        ok = [r for r in rows if r["kind"] == kind and r["status"] == "ok"]
        if ok:
            best = min(ok, key=lambda r: r["best_val_loss"])
            selected[kind] = {"overrides": best["overrides"], "best_val_loss": best["best_val_loss"], "run": best["run"]}
    raw = {"grid": GRID, "budget_hours": args.budget_hours, "elapsed_seconds": time.perf_counter() - t0,
           "rows": rows, "selected": selected}
    out = write_run("hpsearch", raw, render_search(raw), [0], {"base": base, "grid": GRID}, root=TRAINING)
    print(out)


def render_search(raw) -> str:
    L = [f"# hyperparameter search (D21 §5)", "",
         f"Budget {raw['budget_hours']} h; elapsed {raw['elapsed_seconds'] / 3600:.2f} h. Seed 0, MSE, selection by val MSE.",
         "", "| kind | overrides | status | best val MSE | epochs | seconds |", "|---|---|---|---|---|---|"]
    for r in raw["rows"]:
        v = f"{r['best_val_loss']:.4f}" if "best_val_loss" in r else "—"
        L.append(f"| {r['kind']} | `{json.dumps(r['overrides'])}` | {r['status']} | {v} | {r.get('epochs', '—')} | "
                 f"{r.get('seconds', 0):.0f} |")
    L += ["", "Selected: " + ", ".join(f"{k} {json.dumps(v['overrides'])}" for k, v in raw["selected"].items())]
    return "\n".join(L) + "\n"


def cmd_timing(args):
    devices = ["cpu"] + (["mps"] if torch.backends.mps.is_available() else [])
    base = make_config()
    batches = load_batches(base)
    rows = []
    for kind, device in itertools.product(("gnn", "mlp"), devices):
        cfg = make_config(kind=kind, device=device, max_epochs=args.epochs, patience=args.epochs)
        _, history = train_model(cfg, *batches)
        ep = [e for e in history if "epoch" in e]
        rows.append({"kind": kind, "device": device, "epoch_seconds": [e["epoch_seconds"] for e in ep],
                     "val_seconds": [e["val_seconds"] for e in ep]})
        print(kind, device, [round(e["epoch_seconds"], 1) for e in ep], flush=True)
    raw = {"rows": rows, "torch_threads": torch.get_num_threads(), "train_states": sum(len(b.examples) for b in batches[0])}
    L = ["# epoch timing (D21 §5)", "", f"torch threads {raw['torch_threads']}; {raw['train_states']} train states.", "",
         "| model | device | train s/epoch (each epoch) | val s |", "|---|---|---|---|"]
    L += [f"| {r['kind']} 64 | {r['device']} | {', '.join(f'{x:.1f}' for x in r['epoch_seconds'])} | "
          f"{', '.join(f'{x:.1f}' for x in r['val_seconds'])} |" for r in rows]
    print(write_run("epoch_timing", raw, "\n".join(L) + "\n", [base["seed"]], {"epochs": args.epochs, **base},
                    root=TRAINING))


def cmd_project(args):
    """Training cost of the D17 seed plan: runs × mean epochs taken in the pilot × best measured s/epoch."""
    timing = load_raw(args.timing)
    per_epoch = {}  # fastest device per kind: (device, train + val seconds per epoch)
    for r in timing["rows"]:
        s = sum(r["epoch_seconds"]) / len(r["epoch_seconds"]) + sum(r["val_seconds"]) / len(r["val_seconds"])
        if r["kind"] not in per_epoch or s < per_epoch[r["kind"]][1]:
            per_epoch[r["kind"]] = (r["device"], s)
    epochs: dict[str, list[int]] = {}
    for run in args.runs:
        raw = load_raw(run)
        if raw["config"]["kind"] in per_epoch:
            epochs.setdefault(raw["config"]["kind"], []).append(sum("epoch" in e for e in raw["history"]))
    rows, total = [], 0.0
    for item, n_runs in PLAN.items():
        kind = item.split("_")[0]
        ep = sum(epochs[kind]) / len(epochs[kind])
        dev, s = per_epoch[kind]
        hours = n_runs * ep * s / 3600
        total += hours
        rows.append({"item": item, "runs": n_runs, "mean_epochs": ep, "device": dev, "s_per_epoch": s, "hours": hours})
    raw = {"timing_run": str(args.timing), "pilot_runs": [str(r) for r in args.runs], "rows": rows, "total_hours": total}
    L = ["# training-cost projection (D17 seed plan)", "", "Ablations are costed at the 64×3 GNN epoch time "
         "(128×6 runs cost more).", "", "| item | runs | mean epochs (pilot) | device | s/epoch | hours |",
         "|---|---|---|---|---|---|"]
    L += [f"| {r['item']} | {r['runs']} | {r['mean_epochs']:.1f} | {r['device']} | {r['s_per_epoch']:.1f} | "
          f"{r['hours']:.2f} |" for r in rows]
    L += ["", f"Total: {total:.1f} h sequential on one M4 process."]
    print("\n".join(L))
    print(write_run("projection", raw, "\n".join(L) + "\n", [], {"plan": PLAN}, root=TRAINING))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--set", action="append", default=[])
    p.add_argument("--name")
    p = sub.add_parser("search")
    p.add_argument("--budget-hours", type=float, default=3.0)
    p.add_argument("--set", action="append", default=[])
    p = sub.add_parser("timing")
    p.add_argument("--epochs", type=int, default=2)
    p = sub.add_parser("project")
    p.add_argument("--timing", type=Path, required=True)
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    args = ap.parse_args()
    {"run": cmd_run, "search": cmd_search, "timing": cmd_timing, "project": cmd_project}[args.cmd](args)


if __name__ == "__main__":
    main()
