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
  python scripts/train.py plan CONFIG --phase gate|rest [--worker K --workers N]
  python scripts/train.py gate CONFIG
  python scripts/train.py finalize CONFIG
      The D23 multi-seed plan (configs/training/d23.json; amendment 1), at the plan's torch thread count.
      plan: worker K of N trains its share of the phase (gate = seed 0 of each primary and a second copy;
      rest = everything else); a run with a model.pt is skipped, so rerunning continues. No deadline.
      gate: the copies are bitwise identical and the val ratios lie inside the D22 CIs, or exit 1.
      finalize: summary of every run; writes <name>/frozen.json once, if the gate passed and all finished.
      scripts/d23_local.sh runs the phases in order.
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


def plan_runs(plan: dict) -> list[tuple[str, dict, str]]:
    """(model id, config, run name) in D23 order: the gate runs (seed 0 of each reproduce id, and a second
    copy of it under <name>-check/), then every other model × seed."""
    runs = [(m["id"], make_config(**m["overrides"], seed=s)) for m in plan["models"] for s in m["seeds"]]
    gate = [r for r in runs if r[0] in plan["reproduce"] and r[1]["seed"] == 0]
    named = lambda rs, prefix: [(i, c, f"{prefix}/{run_name(c)}") for i, c in rs]
    return (named(gate, plan["name"]) + named(gate, plan["name"] + "-check")
            + named([r for r in runs if r not in gate], plan["name"]))


def is_gate(plan: dict, run: tuple) -> bool:
    return run[0] in plan["reproduce"] and run[1]["seed"] == 0


def shard(plan: dict, runs: list, worker: int, workers: int) -> list:
    """Longest-first assignment to the least-loaded worker, by the plan's est_seconds per model (deterministic)."""
    est = {m["id"]: m["est_seconds"] for m in plan["models"]}
    load, mine = [0.0] * workers, []
    for r in sorted(runs, key=lambda r: -est[r[0]]):  # stable sort: ties keep plan order
        w = load.index(min(load))
        load[w] += est[r[0]]
        if w == worker:
            mine.append(r)
    return mine


def finished(name: str) -> tuple[Path | None, list[Path]]:
    """The latest finished folder of run `name` (it has a model.pt), and folders an interrupted run left without one."""
    dirs = sorted(p for p in (TRAINING / name).glob("*") if p.is_dir())
    done = [p for p in dirs if (p / "model.pt").exists()]
    return (done[-1] if done else None), [p for p in dirs if not (p / "model.pt").exists()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cmd_plan(args):
    """D23 amendment 1: one worker's share of one phase. Each run is written by train_run when it finishes,
    so a crash loses at most the runs in progress; rerunning the same command skips finished runs."""
    plan = json.loads(args.plan.read_text())
    torch.set_num_threads(plan["torch_threads"])  # 1 thread: bitwise reproducible under any machine load
    runs = [r for r in plan_runs(plan) if is_gate(plan, r) == (args.phase == "gate")]
    mine = shard(plan, runs, args.worker, args.workers)
    batches = load_batches(mine[0][1]) if mine else None
    failed = 0
    for mid, cfg, name in mine:
        out, _ = finished(name)
        status = "done earlier"
        if not out:
            try:
                out, _ = train_run(cfg, name, batches)
                status = "ok"
            except Exception:  # recorded in the worker log and by finalize (no model.pt); the worker goes on
                status, failed = "failed\n" + traceback.format_exc(), failed + 1
        print(name, status, flush=True)
    if failed:
        raise SystemExit(1)


def cmd_gate(args):
    """D23 amendment 1 gate: (a) each reproduce id's seed 0 and its -check copy are bitwise identical;
    (b) on val, its expansion ratio vs h_max and its plan-cost ratio (geometric means) lie inside the
    95% CIs of the D22 model it reproduces, read from the D22 val evaluation."""
    from ahg.evaluate import evaluate, summarise
    from ahg.learning.heuristic import Learned
    from ahg.learning.train import load
    plan = json.loads(args.plan.read_text())
    ref = load_raw(ROOT / plan["reproduce_val"])["summary"]
    rows, models = [], []
    for mid, cfg, name in [r for r in plan_runs(plan) if is_gate(plan, r)]:
        out, _ = finished(name)
        if out is None:
            raise SystemExit(f"gate run {name} has not finished")
        if not name.startswith(plan["name"] + "-check/"):
            check, _ = finished(f"{plan['name']}-check/{run_name(cfg)}")
            d22 = load_raw(ROOT / plan["reproduce"][mid])["name"]
            rows.append({"id": mid, "run": str(out.relative_to(ROOT)), "check": str(check.relative_to(ROOT)),
                         "identical": same_model(out, check), "d22": d22})
            model, mcfg = load(out / "model.pt")
            models.append(Learned(model, mcfg, mid))
    val = [open_batch(ROOT / p) for p in make_config()["val_batches"]]
    summ = summarise(evaluate(val, models, 200_000), [m.name for m in models], 200_000)
    for r in rows:
        new, old = summ[r["id"]], ref[r["d22"]]
        r["hmax"] = {"new": new["vs"]["hmax"]["expansions"][0], "d22_ci": old["vs"]["hmax"]["expansions"]}
        r["plan_cost"] = {"new": new["plan_cost"][0], "d22_ci": old["plan_cost"]}
        inside = lambda x, ci: ci[1] <= x <= ci[2]
        r["passed"] = (r["identical"] == [] and inside(r["hmax"]["new"], r["hmax"]["d22_ci"])
                       and inside(r["plan_cost"]["new"], r["plan_cost"]["d22_ci"]))
    passed = all(r["passed"] for r in rows)
    L = [f"# {plan['name']} gate (D23 amendment 1): {'PASSED' if passed else 'FAILED'}", "",
         "| id | bitwise identical to its copy | val exp. ratio vs h_max (D22 CI) | val plan cost (D22 CI) | passed |",
         "|---|---|---|---|---|"]
    f = lambda d: f"{d['new']:.4f} ([{d['d22_ci'][1]:.4f}, {d['d22_ci'][2]:.4f}])"
    L += [f"| {r['id']} | {'yes' if not r['identical'] else 'NO: ' + ', '.join(r['identical'])} | {f(r['hmax'])} | "
          f"{f(r['plan_cost'])} | {r['passed']} |" for r in rows]
    print(write_run(plan["name"] + "-gate", {"rows": rows, "passed": passed, "summary": summ}, "\n".join(L) + "\n",
                    [0], plan, root=TRAINING))
    print("\n".join(L))
    if not passed:
        raise SystemExit(1)


def cmd_finalize(args):
    """Summary of every plan run; writes <name>/frozen.json once, only if the gate passed and every run finished."""
    plan = json.loads(args.plan.read_text())
    gates = sorted(p for p in (TRAINING / f"{plan['name']}-gate").glob("*") if p.is_dir())
    gate_ok = bool(gates) and load_raw(gates[-1])["passed"]
    rows = []
    for mid, cfg, name in plan_runs(plan):
        out, orphans = finished(name)
        row = {"id": mid, "seed": cfg["seed"], "name": name, "orphans": [str(p.relative_to(ROOT)) for p in orphans]}
        if out:
            raw = load_raw(out)
            row.update(run=str(out.relative_to(ROOT)), best_val_loss=raw["best_val_loss"], seconds=raw["wall_seconds"],
                       epochs=sum("epoch" in e for e in raw["history"]), torch_threads=raw["torch_threads"])
        rows.append(row)
    complete = gate_ok and all("run" in r for r in rows)
    raw = {"plan": str(args.plan), "plan_sha256": sha256(args.plan), "gate": str(gates[-1].relative_to(ROOT)) if gates else None,
           "gate_passed": gate_ok, "rows": rows, "complete": complete}
    if complete:
        role = {m["id"]: m["role"] for m in plan["models"]}
        frozen = {"decision": plan["decision"], "plan": str(args.plan), "plan_sha256": raw["plan_sha256"],
                  "gate": raw["gate"], "max_hmax": plan["max_hmax"],
                  "runs": [{"id": r["id"], "role": role[r["id"]], "seed": r["seed"], "run": r["run"],
                            "model_sha256": sha256(ROOT / r["run"] / "model.pt")}
                           for r in rows if not r["name"].startswith(plan["name"] + "-check/")]}
        path = TRAINING / plan["name"] / "frozen.json"
        text = json.dumps(frozen, indent=1) + "\n"
        if path.exists() and path.read_text() != text:  # the manifest is written once (D23 §7)
            raise SystemExit(f"{path} exists with different contents; not overwritten")
        path.write_text(text)
        raw["frozen"] = str(path.relative_to(ROOT))
    L = [f"# {plan['name']}: {plan['decision']} multi-seed plan", "",
         f"Gate passed: {gate_ok}. Finished {sum('run' in r for r in rows)} of {len(rows)} runs. Complete: {complete}.", "",
         "| id | seed | run name | best val loss | epochs | seconds | threads | run |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| {r['id']} | {r['seed']} | {r['name']} | " + (
        f"{r['best_val_loss']:.4f} | {r['epochs']} | {r['seconds']:.0f} | {r['torch_threads']} | {r['run']} |" if "run" in r
        else "— | — | — | — | not finished |") for r in rows]
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
    p.add_argument("--phase", choices=("gate", "rest"), required=True)
    p.add_argument("--worker", type=int, default=0)
    p.add_argument("--workers", type=int, default=1)
    for c in ("gate", "finalize"):
        p = sub.add_parser(c)
        p.add_argument("plan", type=Path)
    p = sub.add_parser("timing")
    p.add_argument("--epochs", type=int, default=2)
    p = sub.add_parser("project")
    p.add_argument("--timing", type=Path, required=True)
    p.add_argument("--primary", type=Path, nargs="+", required=True)
    p.add_argument("--ablation", type=Path, nargs="+", required=True)
    args = ap.parse_args()
    {"run": cmd_run, "search": cmd_search, "sequence": cmd_sequence, "plan": cmd_plan, "gate": cmd_gate, "finalize": cmd_finalize, "timing": cmd_timing,
     "project": cmd_project}[args.cmd](args)


if __name__ == "__main__":
    main()
