"""Is an n = 30 size-shift split feasible under D15+D16? (D17 input; a feasibility check, not a result.)

Usage: python scripts/check_size_shift.py [--n 30] [--seeds 5] [--no-write]

Instances: D16 depth knob (exposed_level0), D in {2, 3}, every (rho, m) of the
D15 grid, the four family variants, seeds 0..S-1. Per instance, in one process:
  - status: ok / unreachable / generation_failure (all logged, rule 10);
  - generation time; A*+LM-cut, A*+h_max and UCS from the initial state
    (200k-expansion budget each); the independent oracle (src/ahg/oracle.py)
    from the initial state, only where UCS finished (as D15 §5 does at n = 20);
  - labelling cost: exact_cost (A*+LM-cut cross-checked by A*+h_max) on the
    first LABEL_STATES states of the [S]-stream walk sample, as a label batch
    would do (D14).
A* h* must equal UCS and the oracle wherever those finished, or the run aborts.
"""

import argparse
import importlib.util
import random
import statistics
import sys
import time
from pathlib import Path

from ahg.attack_graph import KnobInfeasible, UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.heuristics import hmax, lmcut
from ahg.measure import exact_cost, sample_states
from ahg.oracle import optimal_cost
from ahg.runlog import write_run
from ahg.search import astar, uniform_cost

ROOT = Path(__file__).resolve().parent.parent
BUDGET, STATE_BUDGET = 200_000, 20_000
LABEL_STATES = 20
SAMPLE_CAP, WALKS_PER_SAMPLE = 300, 10
LEVELS = [2, 3]

_spec = importlib.util.spec_from_file_location("dc", ROOT / "scripts" / "measure_depth_coupling.py")
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)


def measure(fam, variant, params, n, D, rho, m, seed, pool):
    rec = {"variant": variant, "n": n, "D": D, "rho": rho, "m": m, "seed": seed}
    t0 = time.perf_counter()
    try:
        inst = make_instance(fam, seed, n, pool, cred_levels=D, coupling=rho, share_pool=m,
                             exposed_level0=True, **params)
    except UnreachableGoal:
        return {**rec, "status": "unreachable", "gen_s": time.perf_counter() - t0}
    except KnobInfeasible:
        return {**rec, "status": "generation_failure", "gen_s": time.perf_counter() - t0}
    task = inst.task
    rec.update(status="ok", gen_s=time.perf_counter() - t0, facts=len(task.facts), actions=len(task.actions))
    runs = {"lmcut": astar(task, lmcut, max_expansions=BUDGET), "hmax": astar(task, hmax, max_expansions=BUDGET),
            "h0": uniform_cost(task, max_expansions=BUDGET)}
    rec["init"] = {h: {"expanded": r.expanded, "seconds": r.seconds, "budget_hit": r.budget_hit,
                       "cost": r.cost if r.solved else None} for h, r in runs.items()}
    hs = rec["init"]["lmcut"]["cost"]
    rec["plan_len"] = len(runs["lmcut"].plan) if runs["lmcut"].solved else None
    if runs["hmax"].solved and hs is not None and runs["hmax"].cost != hs:
        sys.exit(f"{rec}: A*+h_max != A*+LM-cut")
    if runs["h0"].solved and hs is not None and runs["h0"].cost != hs:
        sys.exit(f"{rec}: UCS != A*+LM-cut")
    rec["oracle_s"] = None
    if runs["h0"].solved:
        t = time.perf_counter()
        o = optimal_cost(task)
        rec["oracle_s"] = time.perf_counter() - t
        if hs is not None and o != hs:
            sys.exit(f"{rec}: oracle {o} != h* {hs}")
    rng = random.Random(f"landscape:{fam}:{n}:{seed}")  # the [S] stream
    states, _ = sample_states(task, rng, SAMPLE_CAP, WALKS_PER_SAMPLE)
    t, unknown = time.perf_counter(), 0
    for s in states[:LABEL_STATES]:
        unknown += exact_cost(task, s, STATE_BUDGET)[0] is None
    k = min(LABEL_STATES, len(states))
    rec["label"] = {"states": k, "hstar_unknown": unknown, "seconds_per_state": (time.perf_counter() - t) / max(1, k)}
    rec["total_s"] = time.perf_counter() - t0
    return rec


def med(xs):
    return statistics.median(xs) if xs else None


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None


def render(raw):
    R, cfg = raw["instances"], raw["config"]
    L = [f"# {cfg['name']}", "", f"D15+D16 (exposed_level0), n = {cfg['n']}, D ∈ {LEVELS}, all (ρ, m), 4 variants, "
         f"seeds 0–{cfg['seeds'] - 1}: {len(R)} instances, one process. Feasibility check only.", "",
         "| group | reachable | gen. fail | init budget hit (LM-cut / h_max / UCS) | median plan len | median expansions "
         "LM-cut / h_max / UCS | median s: LM-cut / h_max / UCS / oracle | label s/state median (p90) | median total s (max) |",
         "|---|---|---|---|---|---|---|---|---|"]
    groups = [(f"D={D} {v}", [r for r in R if r["D"] == D and r["variant"] == v]) for D in LEVELS
              for v in dict.fromkeys(r["variant"] for r in R)] + [(f"D={D} all", [r for r in R if r["D"] == D])
                                                                  for D in LEVELS] + [("all", R)]
    for name, g in groups:
        ok = [r for r in g if r["status"] == "ok"]
        if not ok:
            L.append(f"| {name} | 0/{len(g)} | {sum(r['status'] == 'generation_failure' for r in g)} | — | — | — | — | — | — |")
            continue
        hit = " / ".join(str(sum(r["init"][h]["budget_hit"] for r in ok)) for h in ("lmcut", "hmax", "h0"))
        ex = " / ".join(f"{med([r['init'][h]['expanded'] for r in ok]):g}" for h in ("lmcut", "hmax", "h0"))
        sec = " / ".join(f"{med([r['init'][h]['seconds'] for r in ok]):.3f}" for h in ("lmcut", "hmax", "h0"))
        orc = [r["oracle_s"] for r in ok if r["oracle_s"] is not None]
        lab = [r["label"]["seconds_per_state"] for r in ok]
        tot = [r["total_s"] for r in ok]
        L.append(f"| {name} | {len(ok)}/{len(g)} | {sum(r['status'] == 'generation_failure' for r in g)} | {hit} | "
                 f"{med([r['plan_len'] for r in ok if r['plan_len']]):g} | {ex} | {sec} / "
                 f"{f'{med(orc):.3f}' if orc else '—'} ({len(orc)} run) | {med(lab):.3f} ({pct(lab, 0.9):.3f}) | "
                 f"{med(tot):.2f} ({max(tot):.1f}) |")
    unk = sum(r["label"]["hstar_unknown"] for r in R if r["status"] == "ok")
    L += ["", f"Labelled states with h\\* unknown (state budget {STATE_BUDGET:,} hit): {unk}. "
          f"Elapsed {cfg['elapsed_seconds']} s."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    pool = load_table(ROOT / "data" / "derived" / "cves.csv")
    t0, out = time.perf_counter(), []
    jobs = [(f, v, p, D, rho, m, s) for f, v, p in dc.VARIANTS for D in LEVELS for rho, m in dc.COUPLINGS
            for s in range(args.seeds)]
    for j, (f, v, p, D, rho, m, s) in enumerate(jobs, 1):
        out.append(measure(f, v, p, args.n, D, rho, m, s, pool))
        r = out[-1]
        print(f"[{j}/{len(jobs)} {time.perf_counter() - t0:6.0f}s] {v} D={D} rho={rho} m={m} seed={s} "
              f"{r['status']} {r.get('total_s', 0):.2f}s", flush=True)
    config = {"name": f"size_shift_n{args.n}", "n": args.n, "levels": LEVELS, "couplings": dc.COUPLINGS,
              "variants": dc.VARIANTS, "seeds": args.seeds, "exposed_level0": True, "budget": BUDGET,
              "state_budget": STATE_BUDGET, "label_states": LABEL_STATES,
              "elapsed_seconds": round(time.perf_counter() - t0, 1)}
    raw = {"config": config, "instances": out}
    if args.no_write:
        print(render(raw))
        return
    print("wrote", write_run(config["name"], raw, render(raw), list(range(args.seeds)), config,
                             root=ROOT / "results" / "feasibility"))


if __name__ == "__main__":
    main()
