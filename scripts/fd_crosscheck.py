"""Fast Downward cross-check and C++ baseline timing on D15+D16 instances (D17 input).

Usage: python scripts/fd_crosscheck.py [--no-write]   (needs scripts/setup_fast_downward.sh first)

Instances: 20 of the 391 instances in the feasibility run [B] (D15+D16, D = 3,
n = 20), evenly spaced after sorting by (variant, rho, m, seed), rebuilt with
make_instance and exported to grounded PDDL (src/ahg/pddl.py).

1. Values. On the initial state and the first SAMPLED_STATES states of the
   [S]-stream random-walk sample, Fast Downward's h_max and LM-cut values and
   its A*+LM-cut plan cost are compared with ours (src/ahg/heuristics.py, and
   h* from A*+LM-cut). h_max is unique, so it must match exactly. LM-cut
   depends on tie-breaking in the cut computation, so a mismatch there is
   reported, not fatal, as long as both values are <= h*. A plan cost that
   differs from h* aborts the run.
2. Timing (FD's own clock, "Search time"). From the initial state, FD runs
   A*+lmcut, A*+hmax and A*+blind. Per-state heuristic cost =
   T_h / N_h - T_blind / N_blind, where N is FD's evaluation count; the blind
   run gives the C++ search's own per-evaluation overhead.
3. Break-even against FD, per instance and paired with [B]'s measurements on
   the same instance (p = a learned heuristic's per-expansion cost in [B],
   o = [B]'s Python search overhead per expansion):
     E*_fd_hm = T_fd_hmax / (o + p) and E*_fd_lm = T_fd_lmcut / (o + p): the
     largest expansion count at which a learned heuristic inside this repo's
     Python A* would still beat FD's A*+h_max / A*+LM-cut on time. The same
     with o = 0 is the optimistic bound for a learned heuristic inside a C++
     search loop.
"""

import argparse
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from ahg.attack_graph import make_instance
from ahg.cve import load_table
from ahg.heuristics import hmax, lmcut
from ahg.measure import exact_cost, sample_states
from ahg.pddl import domain_pddl, problem_pddl
from ahg.runlog import load_raw, write_run

ROOT = Path(__file__).resolve().parent.parent
FD_DIR = ROOT / "third_party" / "downward"
FD = FD_DIR / "fast-downward.py"
BENCH = Path("results/feasibility/inference_microbench/2026-10-29T062211Z-1627e16")
N_INSTANCES = 20
SAMPLED_STATES = 9  # plus the initial state: 10 states per instance
SAMPLE_CAP, WALKS_PER_SAMPLE = 300, 10  # the [S] sampler settings, as in the sweep
STATE_BUDGET = 20_000
D, N = 3, 20
METHODS = ["mlp/cpu1/batched", "gnn64x3/cpu1/batched", "gnn128x6/cpu1/batched"]
PARAMS = {"flat": {}, "hub_and_spoke": {}, "tiered3": {}, "tiered5": {"n_tiers": 5}}


def fd(sas, search):
    out = subprocess.run([sys.executable, str(FD), str(sas), "--search", search],
                         capture_output=True, text=True, check=False).stdout
    grab = lambda pat, f=float: (lambda m: f(m.group(1)) if m else None)(re.search(pat, out))
    return {"h0": grab(r"Initial heuristic value for \w+: (\d+)", int), "cost": grab(r"Plan cost: (\d+)", int),
            "evaluations": grab(r"Evaluations: (\d+)", int), "expanded": grab(r"Expanded (\d+) state", int),
            "search_s": grab(r"Search time: ([\d.]+)s")}


def translate(task, state, d):
    (d / "domain.pddl").write_text(domain_pddl(task))
    (d / "problem.pddl").write_text(problem_pddl(task, state))
    sas = d / "task.sas"
    subprocess.run([sys.executable, str(FD), "--sas-file", str(sas), "--translate",
                    str(d / "domain.pddl"), str(d / "problem.pddl")], capture_output=True, check=True)
    return sas


def pick(bench_insts):
    srt = sorted(bench_insts, key=lambda i: (i["variant"], i["rho"], -1 if i["m"] is None else i["m"], i["seed"]))
    return [srt[round(k * (len(srt) - 1) / (N_INSTANCES - 1))] for k in range(N_INSTANCES)]


def run_instance(b, pool):
    fam = "tiered" if b["variant"].startswith("tiered") else b["variant"]
    task = make_instance(fam, b["seed"], N, pool, cred_levels=D, coupling=b["rho"], share_pool=b["m"],
                         exposed_level0=True, **PARAMS[b["variant"]]).task
    rng = __import__("random").Random(f"landscape:{fam}:{N}:{b['seed']}")  # the [S] stream (D15 §3)
    states, _ = sample_states(task, rng, SAMPLE_CAP, WALKS_PER_SAMPLE)
    rec = {"cell": b["cell"], "seed": b["seed"], "states": []}
    with tempfile.TemporaryDirectory() as tmp:
        for k, s in enumerate([task.init, *states[:SAMPLED_STATES]]):
            hs, _, _ = exact_cost(task, s, STATE_BUDGET)
            sas = translate(task, s, Path(tmp))
            f_lm, f_hm = fd(sas, "astar(lmcut())"), fd(sas, "astar(hmax())")
            row = {"init": k == 0, "hstar": hs, "ours": {"hmax": hmax(task, s), "lmcut": lmcut(task, s)},
                   "fd": {"hmax": f_hm["h0"], "lmcut": f_lm["h0"], "cost": f_lm["cost"]}}
            if hs is not None and f_lm["cost"] != hs:
                sys.exit(f"{b['cell']} seed={b['seed']} state {k}: FD plan cost {f_lm['cost']} != h* {hs}")
            if max(row["fd"]["lmcut"], row["ours"]["lmcut"]) > (hs if hs is not None else float("inf")):
                sys.exit(f"{b['cell']} seed={b['seed']} state {k}: an LM-cut value exceeds h*")
            rec["states"].append(row)
            if k == 0:
                rec["timing"] = {"lmcut": f_lm, "hmax": f_hm, "blind": fd(sas, "astar(blind())")}
    t = rec["timing"]
    over = t["blind"]["search_s"] / t["blind"]["evaluations"]
    rec["fd_per_state_s"] = {h: max(0.0, t[h]["search_s"] / t[h]["evaluations"] - over) for h in ("lmcut", "hmax")}
    rec["fd_overhead_per_eval_s"] = over
    return rec


def break_even(rec, b):
    """[B]'s per-expansion cost p of each learned method, against FD's search times on the same instance."""
    o = b["break_even"]["rerun"]["o_s"]
    out = {}
    for m in METHODS:
        p = b["break_even"]["rerun"][m]["p_s"]
        out[m] = {"p_s": p, **{f"E_star_fd_{h}{'_o0' if o_ == 0 else ''}": rec["timing"][h]["search_s"] / (o_ + p)
                               for h in ("hmax", "lmcut") for o_ in (o, 0)}}
    return out


def med(xs):
    return statistics.median(xs) if xs else None


def ms(x, nd=4):
    return "—" if x is None else f"{1000 * x:.{nd}f}"


def render(raw):
    R, cfg = raw["instances"], raw["config"]
    rows = [s for r in R for s in r["states"]]
    hm_eq = sum(s["fd"]["hmax"] == s["ours"]["hmax"] for s in rows)
    lm_eq = sum(s["fd"]["lmcut"] == s["ours"]["lmcut"] for s in rows)
    cost_eq = sum(s["fd"]["cost"] == s["hstar"] for s in rows if s["hstar"] is not None)
    L = [f"# {cfg['name']}", "", f"Fast Downward {cfg['fd_tag']} ({cfg['fd_commit'][:7]}); {len(R)} instances from "
         f"`{cfg['bench_run']}` (D15+D16, D = {D}, n = {N}); {len(rows)} states (initial + {SAMPLED_STATES} sampled "
         "per instance).", "", "## Values", "",
         f"- h_max: FD = ours on **{hm_eq}/{len(rows)}** states.",
         f"- LM-cut: FD = ours on **{lm_eq}/{len(rows)}** states; every value of both is ≤ h\\* (checked; the run aborts "
         "otherwise). Mismatch gaps (FD − ours, D9 units): "
         + (", ".join(str(s["fd"]["lmcut"] - s["ours"]["lmcut"]) for s in rows if s["fd"]["lmcut"] != s["ours"]["lmcut"])
            or "none") + ".",
         f"- FD A\\*+LM-cut plan cost = our h\\* on **{cost_eq}/{sum(s['hstar'] is not None for s in rows)}** states "
         "where h\\* is known (any mismatch aborts).", "",
         "## Per-state cost from the initial-state search (ms)", "",
         "FD: search time / evaluations, minus the blind search's per-evaluation overhead. Python and learned: the "
         "feasibility run's per-state medians on the same instances.", "",
         "| method | median per state | min | max |", "|---|---|---|---|"]
    for h in ("hmax", "lmcut"):
        xs = [r["fd_per_state_s"][h] for r in R]
        L.append(f"| FD {h} (C++) | {ms(med(xs))} | {ms(min(xs))} | {ms(max(xs))} |")
    L.append(f"| FD search overhead per evaluation | {ms(med([r['fd_overhead_per_eval_s'] for r in R]))} | | |")
    for k in ("hmax", "lmcut", *METHODS):
        xs = [r["bench_per_state_s"][k] for r in R]
        L.append(f"| {k} (this repo) | {ms(med(xs))} | {ms(min(xs))} | {ms(max(xs))} |")
    L += ["", "Median FD search time from the initial state (ms): " + ", ".join(
        f"A\\*+{h} {ms(med([r['timing'][h]['search_s'] for r in R]))} ({med([r['timing'][h]['expanded'] for r in R]):g} "
        f"expansions)" for h in ("hmax", "lmcut", "blind")) + ".", "",
        "## Break-even against FD", "",
        "E\\* = the largest expansion count at which the learned heuristic (per-expansion cost p from the feasibility run) "
        "still beats FD's A\\* on time. `py loop` adds this repo's Python search overhead per expansion; `C++ loop` "
        "assumes zero loop overhead (optimistic). Median over instances; `≥ plan` = fraction of instances where "
        "E\\* ≥ the optimal plan length (a perfect heuristic of that cost would win).", "",
        "| method | p (ms) | E\\* vs FD h_max, py loop | C++ loop | E\\* vs FD LM-cut, py loop | C++ loop | ≥ plan vs FD LM-cut, C++ loop |",
        "|---|---|---|---|---|---|---|"]
    for m in METHODS:
        g = lambda k: med([r["break_even"][m][k] for r in R])
        win = sum(r["break_even"][m]["E_star_fd_lmcut_o0"] >= r["plan_len"] for r in R) / len(R)
        L.append(f"| {m} | {ms(g('p_s'), 3)} | {g('E_star_fd_hmax'):.2f} | {g('E_star_fd_hmax_o0'):.2f} | "
                 f"{g('E_star_fd_lmcut'):.2f} | {g('E_star_fd_lmcut_o0'):.2f} | {win:.0%} |")
    L.append(f"\nMedian optimal plan length on these instances: {med([r['plan_len'] for r in R]):g}; median FD "
             f"A\\*+LM-cut expansions {med([r['timing']['lmcut']['expanded'] for r in R]):g}.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    if not FD.exists():
        sys.exit("Fast Downward not found: run scripts/setup_fast_downward.sh")
    git = lambda *a: subprocess.run(["git", "-C", str(FD_DIR), *a], capture_output=True, text=True).stdout.strip()
    bench = load_raw(ROOT / BENCH)["instances"]
    pool = load_table(ROOT / "data" / "derived" / "cves.csv")
    t0, out = time.perf_counter(), []
    for j, b in enumerate(pick(bench), 1):
        rec = run_instance(b, pool)
        rec["plan_len"] = b["plan_len"]
        rec["bench_per_state_s"] = {k: b["per_state_s"][k] for k in ("hmax", "lmcut", *METHODS)}
        rec["break_even"] = break_even(rec, b)
        out.append(rec)
        print(f"[{j}/{N_INSTANCES} {time.perf_counter() - t0:5.0f}s] {b['cell']} seed={b['seed']}", flush=True)
    config = {"name": "fd_crosscheck", "bench_run": str(BENCH), "fd_tag": git("describe", "--tags"),
              "fd_commit": git("rev-parse", "HEAD"), "n_instances": N_INSTANCES, "sampled_states": SAMPLED_STATES,
              "state_budget": STATE_BUDGET, "D": D, "n": N, "exposed_level0": True,
              "elapsed_seconds": round(time.perf_counter() - t0, 1)}
    raw = {"config": config, "instances": out}
    if args.no_write:
        print(render(raw))
        return
    print("wrote", write_run("fd_crosscheck", raw, render(raw), sorted({r["seed"] for r in out}), config,
                             root=ROOT / "results" / "feasibility"))


if __name__ == "__main__":
    main()
