"""Training runs (D21 §3), the validation hyperparameter search (D21 §5), epoch timing and the cost projection.

Usage:
  python scripts/train.py run [--set KEY=VALUE ...] [--name NAME]
      One run from configs/training/d21.json with overrides, e.g. --set kind=gnn --set loss=asym.
  python scripts/train.py search [--budget-hours 3] [--set device=mps]
      The D21 §5 grid (seed 0, MSE), cheapest models first. A config starts only while the
      wall-clock budget lasts; the rest are recorded as not run. Every config is recorded,
      failures included, and the per-kind selection is by validation MSE.
  python scripts/train.py sequence --name NAME --budget-hours H --run "KEY=VALUE ..." [--run ...]
      Several runs in order under one shared hard budget (D22 §5); every run recorded.
  python scripts/train.py plan CONFIG
      The D23 multi-seed plan (configs/training/d23.json): the reproduction seeds first (stop unless
      identical to D22), then every model × seed. No deadline. Resumable: a run with a model.pt is
      skipped, so rerunning the same command continues. Writes <name>/frozen.json when complete.
  python scripts/train.py timing [--epochs 2]
      Seconds per training epoch for the GNN and MLP, on CPU and on MPS (no checkpoint).
  python scripts/train.py project --timing RUN --primary RUN [RUN ...] --ablation RUN [RUN ...]
      Projects the D17 seed plan's training cost from the wall time of the given pilot runs
      (selected configs; the config the ablation grid is priced at) and the timing run.

Runs go to results/training/<name>/<stamp>-<commit>/ through runlog (append-only).
"""

import argparse
import hashlib
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

# D21 §5, fixed before training. Order (D21 amendment 1): cheapest first, and for the GNN both
# learning rates at each size before the next size, so the budget cuts the largest models, not one lr.
GRID = {
    "wl": [{"lam": lam} for lam in (0.1, 1.0, 10.0)],
    "mlp": [{"lr": lr, "hidden": h} for h, lr in itertools.product((64, 128), (1e-3, 3e-3))],
    "gnn": [{"lr": lr, "hidden": h, "layers": l}
            for (h, l), lr in itertools.product(((64, 3), (128, 3), (64, 6), (128, 6)), (1e-3, 3e-3))],
}
# The D17 §4 seed plan, used only for the projection: primary models × {MSE, asym} × 5 seeds;
# about 30 ablation runs in all (D17 §5), priced at the GNN 64×3.
PLAN = {"gnn": 2 * 5, "mlp": 2 * 5, "wl": 2, "gnn_ablation": 30}  # WL is deterministic: one run per loss


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
    size = f"-{cfg['hidden']}x{cfg['layers']}-lr{cfg['lr']:g}" if cfg["kind"] == "gnn" else (
        f"-{cfg['hidden']}-lr{cfg['lr']:g}" if cfg["kind"] == "mlp" else f"-lam{cfg['lam']}")
    kind = cfg["kind"] + ("res" if cfg.get("target", "hstar") == "residual" else "")  # D22 a, d
    return f"{kind}{size}-{cfg['loss']}-s{cfg['seed']}"


def load_batches(cfg):
    return ([open_batch(ROOT / p) for p in cfg["train_batches"]], [open_batch(ROOT / p) for p in cfg["val_batches"]])


def cmd_run(args):
    cfg = make_config(**parse_set(args.set))
    out, raw = train_run(cfg, args.name or run_name(cfg))
    print(f"{out}  best val loss {raw['best_val_loss']:.4f}  {raw['wall_seconds']:.0f} s")


def run_budgeted(configs: list[tuple[dict, dict]], deadline: float, batches, prefix: str) -> list[dict]:
    """Train (overrides, config) pairs in order under one hard deadline; every config gets a row, failures included."""
    rows = []
    for over, cfg in configs:
        row = {"kind": cfg["kind"], "overrides": over, "config": cfg}
        if time.time() >= deadline:
            rows.append({**row, "status": "not run (budget)"})
            continue
        try:
            out, raw = train_run(cfg, f"{prefix}{run_name(cfg)}", batches, deadline=deadline)
            # A run the budget cut short is recorded but never selected: it did not finish the protocol.
            row.update(status="stopped (budget)" if raw["stopped"] else "ok",
                       best_val_loss=raw["best_val_loss"], seconds=raw["wall_seconds"],
                       epochs=sum("epoch" in e for e in raw["history"]), run=str(out.relative_to(ROOT)))
        except Exception as e:  # recorded, never dropped (D21 §5)
            row.update(status="failed", error=f"{type(e).__name__}: {e}", traceback=traceback.format_exc())
        rows.append(row)
        print(cfg["kind"], over, row["status"], row.get("best_val_loss"), flush=True)
    return rows


def cmd_search(args):
    base = parse_set(args.set)
    batches = load_batches(make_config(**base))
    t0 = time.time()
    deadline = t0 + args.budget_hours * 3600  # hard: a running config stops at its next epoch boundary
    configs = [(over, make_config(**{**base, "kind": kind, "loss": "mse", "seed": 0, **over}))
               for kind, overs in GRID.items() for over in overs]
    rows = run_budgeted(configs, deadline, batches, "search/")
    selected = {}
    for kind in GRID:
        ok = [r for r in rows if r["kind"] == kind and r["status"] == "ok"]
        if ok:
            best = min(ok, key=lambda r: r["best_val_loss"])
            selected[kind] = {"overrides": best["overrides"], "best_val_loss": best["best_val_loss"], "run": best["run"]}
    raw = {"grid": GRID, "budget_hours": args.budget_hours, "elapsed_seconds": time.time() - t0,
           "rows": rows, "selected": selected}
    out = write_run("hpsearch", raw, render_search(raw), [0], {"base": base, "grid": GRID}, root=TRAINING)
    print(out)


def cmd_sequence(args):
    """Several runs under one shared budget (D22 §5). --run "k=v k=v" per run, in order; no selection here
    (D22 selects on validation expansions, with scripts/evaluate.py)."""
    configs = [(over, make_config(**over)) for over in (parse_set(r.split()) for r in args.run)]
    batches = load_batches(configs[0][1])
    t0 = time.time()
    rows = run_budgeted(configs, t0 + args.budget_hours * 3600, batches, f"{args.name}/")
    raw = {"budget_hours": args.budget_hours, "elapsed_seconds": time.time() - t0, "rows": rows}
    L = [f"# {args.name}: {len(rows)} runs under one {args.budget_hours} h budget", "",
         f"Elapsed {raw['elapsed_seconds'] / 3600:.2f} h.", "",
         "| overrides | status | best val loss | epochs | seconds | run |", "|---|---|---|---|---|---|"]
    L += [f"| `{json.dumps(r['overrides'])}` | {r['status']} | "
          f"{r['best_val_loss']:.4f} | {r['epochs']} | {r['seconds']:.0f} | {r['run']} |" if "run" in r else
          f"| `{json.dumps(r['overrides'])}` | {r['status']} | — | — | — | {r.get('error', '')} |" for r in rows]
    print(write_run(args.name, raw, "\n".join(L) + "\n", [r["config"]["seed"] for r in rows],
                    {"runs": [r["overrides"] for r in rows]}, root=TRAINING))


def same_model(a: Path, b: Path) -> list[str]:
    """What differs between two runs: config, weights (bitwise), per-epoch losses (timings excluded). [] if nothing."""
    ca, cb = (torch.load(r / "model.pt", weights_only=False) for r in (a, b))
    sa, sb = ca["state_dict"], cb["state_dict"]
    strip = lambda r: [{k: v for k, v in e.items() if not k.endswith("seconds")} for e in load_raw(r)["history"]]
    return ([] if ca["config"] == cb["config"] else ["config"]) + \
        ([] if sa.keys() == sb.keys() and all(torch.equal(sa[k], sb[k]) for k in sa) else ["weights"]) + \
        ([] if strip(a) == strip(b) else ["history"])


def plan_runs(plan: dict) -> list[tuple[str, dict]]:
    """(model id, config) in D23 §5 order: the seed-0 reproduction runs first, then each model's seeds in turn."""
    runs = [(m["id"], make_config(**m["overrides"], seed=s)) for m in plan["models"] for s in m["seeds"]]
    first = [r for r in runs if r[0] in plan["reproduce"] and r[1]["seed"] == 0]
    return first + [r for r in runs if r not in first]


def finished(name: str) -> tuple[Path | None, list[Path]]:
    """The latest finished folder of run `name` (it has a model.pt), and folders an interrupted run left without one."""
    dirs = sorted(p for p in (TRAINING / name).glob("*") if p.is_dir())
    done = [p for p in dirs if (p / "model.pt").exists()]
    return (done[-1] if done else None), [p for p in dirs if not (p / "model.pt").exists()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cmd_plan(args):
    """D23 §5–§6. Runs are trained one at a time in this process; each is written by train_run on completion,
    so a crash loses at most the run in progress, and rerunning the command resumes after the last finished run."""
    plan = json.loads(args.plan.read_text())
    runs = plan_runs(plan)
    batches = load_batches(runs[0][1])
    t0, rows, halt = time.time(), [], None
    for mid, cfg in runs:
        name = f"{plan['name']}/{run_name(cfg)}"
        out, orphans = finished(name)
        row = {"id": mid, "seed": cfg["seed"], "config": cfg, "orphans": [str(p.relative_to(ROOT)) for p in orphans]}
        if out:
            row["status"] = "done earlier"
        else:
            try:
                out, _ = train_run(cfg, name, batches)
                row["status"] = "ok"
            except Exception as e:  # recorded, never dropped; the plan goes on
                row.update(status="failed", error=f"{type(e).__name__}: {e}", traceback=traceback.format_exc())
        if out:
            raw = load_raw(out)
            row.update(run=str(out.relative_to(ROOT)), best_val_loss=raw["best_val_loss"], seconds=raw["wall_seconds"],
                       epochs=sum("epoch" in e for e in raw["history"]))
        if mid in plan["reproduce"] and cfg["seed"] == 0:  # D23 §6: extend the D22 models, not new ones
            ref = plan["reproduce"][mid]
            row["reproduce_diffs"] = same_model(out, ROOT / ref) if out else ["no run"]
            if row["reproduce_diffs"]:
                halt = f"{mid} seed 0 does not reproduce {ref}: differs in {row['reproduce_diffs']}"
        rows.append(row)
        print(mid, cfg["seed"], row["status"], row.get("best_val_loss"), row.get("reproduce_diffs", ""), flush=True)
        if halt:
            print("HALT:", halt, flush=True)
            break
    complete = not halt and len(rows) == len(runs) and all("run" in r for r in rows)
    raw = {"plan": str(args.plan), "plan_sha256": sha256(args.plan), "elapsed_seconds": time.time() - t0,
           "rows": rows, "halt": halt, "complete": complete}
    if complete:
        role = {m["id"]: m["role"] for m in plan["models"]}
        frozen = {"decision": plan["decision"], "plan": str(args.plan), "plan_sha256": raw["plan_sha256"],
                  "max_hmax": plan["max_hmax"],
                  "runs": [{"id": r["id"], "role": role[r["id"]], "seed": r["seed"], "run": r["run"],
                            "model_sha256": sha256(ROOT / r["run"] / "model.pt")} for r in rows]}
        path = TRAINING / plan["name"] / "frozen.json"
        text = json.dumps(frozen, indent=1) + "\n"
        if path.exists() and path.read_text() != text:  # the manifest is written once (D23 §7)
            raise SystemExit(f"{path} exists with different contents; not overwritten")
        path.write_text(text)
        raw["frozen"] = str(path.relative_to(ROOT))
    L = [f"# {plan['name']}: {plan['decision']} multi-seed plan", "",
         f"{len(rows)} of {len(runs)} runs reached; elapsed this invocation {raw['elapsed_seconds'] / 3600:.2f} h. "
         f"Complete: {complete}." + (f" **HALT: {halt}**" if halt else ""), "",
         "| id | seed | status | best val loss | epochs | seconds | reproduces D22 | run |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        rep = "—" if "reproduce_diffs" not in r else ("yes (bitwise)" if not r["reproduce_diffs"] else
                                                     f"NO: {', '.join(r['reproduce_diffs'])}")
        L.append(f"| {r['id']} | {r['seed']} | {r['status']} | " + (
            f"{r['best_val_loss']:.4f} | {r['epochs']} | {r['seconds']:.0f} | {rep} | {r['run']} |" if "run" in r else
            f"— | — | — | {rep} | {r.get('error', '')} |"))
    orphans = [o for r in rows for o in r["orphans"]]
    if orphans:
        L += ["", "Folders left by interrupted runs (no model.pt; kept, append-only): " + ", ".join(orphans)]
    print(write_run(plan["name"], raw, "\n".join(L) + "\n", sorted({r["seed"] for r in rows}), plan, root=TRAINING))
    if not complete:
        raise SystemExit(1)


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
    """Training cost of the D17 seed plan, priced at the mean wall time of the pilot runs of each config.

    --primary RUN... are pilot runs of the selected configs (gnn, mlp, wl), --ablation RUN... are runs of
    the config the ablation grid is priced at. The timing run gives the CPU-vs-MPS speedup per epoch.
    """
    def mean_hours(runs):
        return sum(load_raw(r)["wall_seconds"] for r in runs) / len(runs) / 3600

    by_kind: dict[str, list[Path]] = {}
    for r in args.primary:
        by_kind.setdefault(load_raw(r)["config"]["kind"], []).append(r)
    rows = [{"item": k, "runs": PLAN[k], "pilot_runs": [str(r) for r in rs], "hours_per_run": mean_hours(rs)}
            for k, rs in by_kind.items()]
    rows.append({"item": "gnn_ablation", "runs": PLAN["gnn_ablation"], "pilot_runs": [str(r) for r in args.ablation],
                 "hours_per_run": mean_hours(args.ablation)})
    for r in rows:
        r["hours"] = r["runs"] * r["hours_per_run"]
    total = sum(r["hours"] for r in rows)
    epoch = {}  # (kind, device) -> mean train + val seconds per epoch
    for t in load_raw(args.timing)["rows"]:
        epoch[t["kind"], t["device"]] = (sum(t["epoch_seconds"]) + sum(t["val_seconds"])) / len(t["epoch_seconds"])
    raw = {"timing_run": str(args.timing), "rows": rows, "total_hours": total,
           "epoch_seconds": {f"{k}/{d}": v for (k, d), v in epoch.items()}}
    L = ["# training-cost projection (D17 seed plan)", "", "Priced at the mean training wall time (label loading excluded; "
         "encoding included where it was not cached yet) of the pilot runs of each config, sequential on one M4 CPU process.", "",
         "| item | runs | h per run (pilot) | hours |", "|---|---|---|---|"]
    L += [f"| {r['item']} | {r['runs']} | {r['hours_per_run']:.2f} | {r['hours']:.1f} |" for r in rows]
    L += ["", f"Total: {total:.1f} h.", "", "Seconds per epoch, train + val (timing run):", ""]
    L += [f"- {k} on {d}: {v:.1f}" for (k, d), v in sorted(epoch.items())]
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
    p = sub.add_parser("sequence")
    p.add_argument("--name", required=True)
    p.add_argument("--budget-hours", type=float, required=True)
    p.add_argument("--run", action="append", required=True)
    p = sub.add_parser("plan")
    p.add_argument("plan", type=Path)
    p = sub.add_parser("timing")
    p.add_argument("--epochs", type=int, default=2)
    p = sub.add_parser("project")
    p.add_argument("--timing", type=Path, required=True)
    p.add_argument("--primary", type=Path, nargs="+", required=True)
    p.add_argument("--ablation", type=Path, nargs="+", required=True)
    args = ap.parse_args()
    {"run": cmd_run, "search": cmd_search, "sequence": cmd_sequence, "plan": cmd_plan, "timing": cmd_timing,
     "project": cmd_project}[args.cmd](args)


if __name__ == "__main__":
    main()
