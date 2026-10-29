"""D15 depth-coupling sweep: does any knob setting make h_max / LM-cut stop being near-exact?

Usage: python scripts/measure_depth_coupling.py pilot|full [--d16] [--workers N]
       python scripts/measure_depth_coupling.py confirm --cells "KEY;KEY" [--d16] [--workers N]
       python scripts/measure_depth_coupling.py replicate --d16 [--workers N]

  pilot  seed 0 of every grid cell, plus the anchor cells (D12 + pr_gated,
         knobs off, n in {8, 12}) on seeds 0-19. The anchors must reproduce
         landscape_small_n [S] exactly, or the run aborts before writing.
         Written to results/landscape/depth_coupling_sweep/pilot/.
  full   seeds 0-19 of every grid cell -> results/landscape/depth_coupling_sweep/full/.
  confirm  the D15 §6 fresh-seed confirmation: the named cells (keys as in
         report.md) on seeds 100-119 -> .../depth_coupling_sweep/confirm/.
  replicate  the D17 §1 fresh-seed replication of C1: every grid cell on
         seeds 100-119 -> .../depth_coupling_sweep/replicate/ (R1-R3 of D17
         are then read off by summarize_depth_coupling.py).
  --d16  the D16 variant of the depth knob (internet-exposed hosts at level 0);
         run names get a "_d16" suffix. Anchor cells have D = 0, so D16 does
         not touch them.

Grid (D15 §2): cred_levels D x (coupling rho, share_pool m) x family variant x n.
Per instance (D15 §3-§5):
  - status: ok / unreachable (UnreachableGoal) / generation_failure (KnobInfeasible),
    every one kept and listed (CLAUDE.md rule 10);
  - init: the [S] block (h*, plan length, expansions and budget hits of h0,
    h_max, LM-cut), plus R = expanded(LM-cut) / plan length. R is None and
    "censored" True when A*+LM-cut hit the budget (D15 §6: counts as +inf);
  - sampled states (the [S] walks and rng stream), A*-expanded states of the
    LM-cut and the h_max search, and every reachable state if enumerated:
    fraction with h < h*, mean and max gap, for h_max and LM-cut;
  - oracle checks: the independent src/ahg/oracle.py on the initial state and,
    on enumerated instances, 20 drawn states, each recorded with both values.
Any h* mismatch or admissible heuristic above h* aborts before anything is written.
"""

import glob
import json
import random
import statistics
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from ahg.attack_graph import KnobInfeasible, UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.measure import HardFailure, check_admissible, enumerate_exact, exact_cost, gap_stats, sample_states
from ahg.network import hop_distances
from ahg.oracle import optimal_cost
from ahg.runlog import load_raw, write_run
from ahg.search import INF, uniform_cost

ROOT = Path(__file__).resolve().parent.parent
BUDGET = 200_000  # max expansions per search from the initial state
STATE_BUDGET = 20_000  # max expansions per search when labelling one measured state
LABEL_BUDGET = 2_000_000  # max expansions per instance over all labelling searches
SAMPLE_CAP = 300  # sampled non-goal states per instance, as in [S]
WALKS_PER_SAMPLE = 10
EXPANDED_CAP = 300  # expanded states labelled by A* when the instance is not enumerated
ENUM_CAP = 50_000
ORACLE_STATES = 20  # drawn states checked by the oracle on enumerated instances
BOOTSTRAP = 10_000
R_THRESHOLD, R_CI_LOWER = 5, 3  # D15 §6, fixed before any run

LEVELS = [0, 1, 2, 3]
COUPLINGS = [(0.0, None), (0.25, 1), (0.25, None), (0.5, 1), (0.5, None), (1.0, 1), (1.0, None)]  # None = all hosts
VARIANTS = [("flat", "flat", {}), ("hub_and_spoke", "hub_and_spoke", {}),
            ("tiered", "tiered3", {}), ("tiered", "tiered5", {"n_tiers": 5})]
SIZES = [8, 12, 20]
SEEDS = range(20)
CONFIRM_SEEDS = range(100, 120)  # D15 §6 condition 2
ANCHOR_SIZES = [8, 12]


def grid_cells(d16=False):
    return [dict(family=f, variant=v, params=p, n=n, D=D, rho=rho, m=m, pr_gated=False, e0=d16)
            for n in SIZES for f, v, p in VARIANTS for D in LEVELS for rho, m in COUPLINGS]


def anchor_cells():
    return [dict(family=f, variant=v, params=p, n=n, D=0, rho=0.0, m=None, pr_gated=True, e0=False)
            for n in ANCHOR_SIZES for f, v, p in VARIANTS if v != "tiered5"]


def cell_key(c):
    m = "all" if c["m"] is None else c["m"]
    return f"{c['variant']} n={c['n']} D={c['D']} rho={c['rho']} m={m}" + (" pr_gated" if c["pr_gated"] else "")


_POOL = None


def _init_worker():
    global _POOL
    _POOL = load_table(ROOT / "data" / "derived" / "cves.csv")


class Labeller:
    """A*-labels states under the per-state and per-instance budgets (D15 §2)."""

    def __init__(self, task, exact):
        self.task, self.exact, self.spent, self.unknown = task, exact, 0, 0

    def __call__(self, s):
        """(h*, h_max, LM-cut) of s, or None if h* is unknown. Cross-checks the enumeration."""
        if self.spent >= LABEL_BUDGET:
            self.unknown += 1
            return None
        hs, r_lm, r_hm = exact_cost(self.task, s, STATE_BUDGET)
        self.spent += r_lm.expanded + r_hm.expanded
        if hs is None:
            self.unknown += 1
            return None
        if self.exact is not None and self.exact[s] != hs:
            raise HardFailure(f"enumeration h*={self.exact[s]} != A* {hs} at {s:#x}")
        return [hs, *check_admissible(self.task, s, hs)]


def expanded_stats(task, trace, exact, label, rng):
    """Gap statistics over the distinct states one A* search expanded (D15 §3 item 3)."""
    states = list(dict.fromkeys(trace))  # distinct, in expansion order
    subsampled = exact is None and len(states) > EXPANDED_CAP
    if exact is not None:
        triples = [[exact[s], *check_admissible(task, s, exact[s])] for s in states]
        unknown = 0
    else:
        chosen = sorted(rng.sample(states, EXPANDED_CAP)) if subsampled else states
        before = label.unknown
        triples = [t for t in map(label, chosen) if t is not None]
        unknown = label.unknown - before
    return {"distinct": len(states), "subsampled": subsampled, "hstar_unknown": unknown, **gap_stats(triples)}


def measure_instance(job):
    idx, cell, seed = job
    c = cell
    base = {"cell": cell_key(c), "family": c["family"], "variant": c["variant"], "n": c["n"], "seed": seed,
            "D": c["D"], "rho": c["rho"], "m": c["m"], "pr_gated": c["pr_gated"], "exposed_level0": c["e0"]}
    t0 = time.perf_counter()
    try:
        inst = make_instance(c["family"], seed, c["n"], _POOL, pr_gated=c["pr_gated"], cred_levels=c["D"],
                             coupling=c["rho"], share_pool=c["m"], exposed_level0=c["e0"], **c["params"])
    except UnreachableGoal as e:
        return idx, {**base, "status": "unreachable", "reason": str(e)}
    except KnobInfeasible as e:
        return idx, {**base, "status": "generation_failure", "reason": str(e)}
    task, where = inst.task, f"{cell_key(c)} seed={seed}"
    try:
        rec = {**base, "status": "ok", "facts": len(task.facts), "actions": len(task.actions)}
        init_set = task.init
        rec["structure"] = {
            # Actions needing two or more facts the attacker does not start with: the conjunctions.
            "multi_pre_actions": sum(sum(not init_set >> f & 1 for f in a.pre) >= 2 for a in task.actions),
            "target_hop_depth": hop_distances(inst.network)[inst.target],
            "coupled_exploits": len(inst.coupled or {}), "coupled_unchanged": inst.coupled_unchanged,
        }

        tr_lm, tr_hm = [], []
        hstar0, r_lm, r_hm = exact_cost(task, task.init, BUDGET, traces=(tr_lm, tr_hm))
        r_h0 = uniform_cost(task, max_expansions=BUDGET)
        rec["init"] = {  # the [S] block, unchanged
            "hstar": hstar0,
            "plan_len": len(r_lm.plan) if hstar0 is not None else None,
            "expanded": {"h0": r_h0.expanded, "hmax": r_hm.expanded, "lmcut": r_lm.expanded},
            "budget_hit": {"h0": r_h0.budget_hit, "hmax": r_hm.budget_hit, "lmcut": r_lm.budget_hit},
        }
        if hstar0 is not None and not r_h0.budget_hit and r_h0.cost != hstar0:
            raise HardFailure(f"UCS {r_h0.cost} != h* {hstar0}")
        # R from LM-cut alone: LM-cut is admissible, so its plan is optimal even if h_max was censored.
        plan_lm = len(r_lm.plan) if r_lm.solved else None
        rec["effort"] = {
            "censored": r_lm.budget_hit,
            "R": r_lm.expanded / plan_lm if plan_lm else None,
            "R_hmax": r_hm.expanded / len(r_hm.plan) if r_hm.solved else None,
            "plan_len_lmcut": plan_lm, "hstar_lmcut": r_lm.cost if r_lm.solved else None,
            "cross_checked": hstar0 is not None,
            "cred_chain_len": sum(task.actions[a].name.startswith("harvest cred") for a in r_lm.plan or []),
            "seconds": {"h0": round(r_h0.seconds, 4), "hmax": round(r_hm.seconds, 4), "lmcut": round(r_lm.seconds, 4)},
        }

        rng = random.Random(f"landscape:{c['family']}:{c['n']}:{seed}")  # the [S] stream (D15 §3)
        states, cap_bound = sample_states(task, rng, SAMPLE_CAP, WALKS_PER_SAMPLE)
        exact = enumerate_exact(task, ENUM_CAP)
        label = Labeller(task, exact)
        triples = []
        for s in states:
            t = label(s)
            if t is not None:
                triples.append(t)
        rec["sampled"] = {"states": triples, "cap_bound": cap_bound, "hstar_unknown": label.unknown}

        if exact is None:
            rec["enumeration"] = None
        else:
            non_goal = [(hs, s) for s, hs in exact.items() if hs != 0]
            if any(hs == INF for hs, _ in non_goal):
                raise HardFailure("enumerated state cannot reach the goal")
            if hstar0 is not None and exact[task.init] != hstar0:
                raise HardFailure("enumeration h*(init) != A*")
            full = [[hs, *check_admissible(task, s, hs)] for hs, s in non_goal]
            rec["enumeration"] = {"reachable": len(exact), **gap_stats(full)}

        erng = random.Random(f"expanded:{cell_key(c)}:{seed}")
        rec["expanded_states"] = {"lmcut": expanded_stats(task, tr_lm, exact, label, erng),
                                  "hmax": expanded_stats(task, tr_hm, exact, label, erng)}
        rec["label_expansions"] = label.spent

        # Independent oracle (D15 §5): shares no code with search.py or the bitmask methods.
        checks = []
        # Reference h*(init): the enumeration, else UCS where it finished (checked = A* above).
        init_ref = exact[task.init] if exact is not None else (r_h0.cost if r_h0.solved else None)
        if init_ref is not None:
            checks.append([task.init, optimal_cost(task), init_ref])
        if exact is not None:
            ostates = sorted(set(states) | set(tr_lm) | set(tr_hm))
            orng = random.Random(f"oracle:{cell_key(c)}:{seed}")
            for s in sorted(orng.sample(ostates, min(ORACLE_STATES, len(ostates)))):
                checks.append([s, optimal_cost(task, s), exact[s]])
        for s, o, ref in checks:
            if o != ref:
                raise HardFailure(f"oracle {o} != h* {ref} at {s:#x}")
        rec["oracle"] = checks
        rec["seconds"] = round(time.perf_counter() - t0, 3)
        return idx, rec
    except HardFailure as e:
        raise HardFailure(f"{where}: {e}") from None


def compare_anchors(instances):
    """Anchor records must equal [S] on every field [S] has (seconds excluded). Returns mismatches."""
    (ref_path,) = glob.glob(str(ROOT / "results/landscape/landscape_small_n/*/"))
    ref = {(r["family"], r["n"], r["seed"]): r for r in load_raw(ref_path)["instances"]}
    bad, n = [], 0
    for r in instances:
        if not r["pr_gated"]:
            continue
        n += 1
        want = ref[(r["family"], r["n"], r["seed"])]
        got = {k: r[k] for k in want if k != "seconds" and k in r}
        if json.loads(json.dumps(got)) != {k: v for k, v in want.items() if k != "seconds"}:
            bad.append(f"{r['family']} n={r['n']} seed={r['seed']}")
    return {"reference": str(Path(ref_path).relative_to(ROOT)), "compared": n, "mismatches": bad}


def median_r(rs):
    """Median of R with censored instances as +inf (D15 §6)."""
    return statistics.median(rs) if rs else None


def bootstrap_lower(rs, key):
    rng = random.Random(f"bootstrap:{key}")
    meds = sorted(statistics.median(rng.choices(rs, k=len(rs))) for _ in range(BOOTSTRAP))
    return meds[int(0.025 * BOOTSTRAP)]


def summarise(cell_recs, seeds_per_cell):
    ok = [r for r in cell_recs if r["status"] == "ok"]
    rs = [INF if r["effort"]["censored"] else r["effort"]["R"] for r in ok]
    solved_len = [r["effort"]["plan_len_lmcut"] for r in ok if not r["effort"]["censored"]]
    med_len = statistics.median(solved_len) if solved_len else None
    s = {"seeds": len(cell_recs), "reachable": len(ok),
         "unreachable": sum(r["status"] == "unreachable" for r in cell_recs),
         "generation_failure": sum(r["status"] == "generation_failure" for r in cell_recs),
         "censored": sum(r["effort"]["censored"] for r in ok), "median_R": median_r(rs),
         "median_plan_len": med_len,
         "eligible": bool(cell_recs) and cell_recs[0]["n"] >= 12 and len(ok) >= 10 and med_len is not None
                     and med_len >= 3}
    s["R_ci_lower"] = bootstrap_lower(rs, cell_recs[0]["cell"]) if len(ok) >= 10 else None
    s["criterion_1"] = (s["eligible"] and s["median_R"] >= R_THRESHOLD and s["R_ci_lower"] >= R_CI_LOWER)
    return s


def fmt(x, nd=2):
    if x is None:
        return "—"
    if x == INF:
        return "+∞"
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def render(raw):
    """report.md from raw.json alone."""
    cfg = raw["config"]
    cells = {}
    for r in raw["instances"]:
        cells.setdefault(r["cell"], []).append(r)
    L = [f"# {cfg['name']}", "",
         f"Mode **{cfg['mode']}**" + (" — a pilot for timing and tooling, not a result (D15 §7)." if cfg["mode"] == "pilot" else "."),
         f"D12 schema (pr_gated off) with the D15 knobs" + (", depth knob in its D16 variant (internet-exposed hosts at level 0)"
         if cfg.get("exposed_level0") else ", depth knob as registered in D15") + "; anchor cells are pr_gated with knobs off. "
         f"Init budget {cfg['budget']:,} expansions; per-state labelling budget {cfg['state_budget']:,}, "
         f"per-instance {cfg['label_budget']:,}. Costs in D9 units (38 per effort unit).", "",
         "h* checks passed on every instance (any failure would have aborted the run): A*+LM-cut = A*+h_max, "
         "enumeration = A* where enumerated, UCS = h* where UCS finished, no admissible h above h*, "
         "independent oracle = h* on every oracle-checked state.", ""]
    if "anchor_check" in raw:
        a = raw["anchor_check"]
        L += [f"**Anchor reproduction of [S]** (`{a['reference']}`): {a['compared']} instances compared, "
              f"{len(a['mismatches'])} mismatches — **{'PASS' if not a['mismatches'] else 'FAIL'}**.", ""]
    L += ["## Effort (D15 §4, §6)", "",
          "R = A*+LM-cut expansions from the initial state / optimal plan length. Censored = LM-cut hit the "
          "budget; it counts as R = +∞. `elig.` and `crit. 1` apply the D15 §6 rules (n ≥ 12, ≥ 10 reachable, "
          "median solved plan length ≥ 3; median R ≥ 5 with bootstrap CI lower bound ≥ 3); both need 20 seeds, "
          "so they are always `no` in a pilot.", "",
          "| cell | reachable | gen. fail | censored | median R | R CI low | median R_hmax | median plan len "
          "| median exp. h0 / h_max / LM-cut | h0 at budget | elig. | crit. 1 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for key, rs in cells.items():
        s = summarise(rs, cfg["seeds_per_cell"])
        ok = [r for r in rs if r["status"] == "ok"]
        rh = [INF if r["effort"]["R_hmax"] is None else r["effort"]["R_hmax"] for r in ok]
        e = {h: [r["init"]["expanded"][h] for r in ok] for h in ("h0", "hmax", "lmcut")}
        med = lambda xs: fmt(statistics.median(xs), 1) if xs else "—"
        h0_cap = sum(r["init"]["budget_hit"]["h0"] for r in ok)
        L.append(f"| {key} | {s['reachable']}/{s['seeds']} | {s['generation_failure']} | {s['censored']} "
                 f"| {fmt(s['median_R'])} | {fmt(s['R_ci_lower'])} | {fmt(median_r(rh))} | {fmt(s['median_plan_len'])} "
                 f"| {med(e['h0'])} / {med(e['hmax'])} / {med(e['lmcut'])} | {h0_cap}/{len(ok)} "
                 f"| {'yes' if s['eligible'] else 'no'} | {'**YES**' if s['criterion_1'] else 'no'} |")

    def pooled(stats):
        n = sum(x["n"] for x in stats)
        out = {"n": n}
        for h in ("hmax", "lmcut"):
            lt = sum(x[h]["lt"] for x in stats)
            out[h] = (f"{lt / n:.3f}" if n else "—", max((x[h]["gap_max"] for x in stats), default=0))
        return out

    L += ["", "## Exactness: fraction of states with h < h* (max gap in D9 units)", "",
          "Sampled = [S] random walks; expanded = distinct states the A* search with that heuristic expanded "
          "from the initial state; all = every reachable non-goal state, enumerated instances only.", "",
          "| cell | LM-cut: sampled | LM-cut: LM-cut-expanded | LM-cut: all | h_max: sampled | h_max: h_max-expanded "
          "| h_max: all | enumerated | h* unknown (sampled + expanded) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for key, rs in cells.items():
        ok = [r for r in rs if r["status"] == "ok"]
        sm = pooled([gap_stats(r["sampled"]["states"]) for r in ok])
        el = pooled([r["expanded_states"]["lmcut"] for r in ok])
        eh = pooled([r["expanded_states"]["hmax"] for r in ok])
        en = pooled([r["enumeration"] for r in ok if r["enumeration"] is not None])
        unk = sum(r["sampled"]["hstar_unknown"] + r["expanded_states"]["lmcut"]["hstar_unknown"]
                  + r["expanded_states"]["hmax"]["hstar_unknown"] for r in ok)
        c = lambda st, h: f"{st[h][0]} ({st[h][1]})" if st["n"] else "—"
        L.append(f"| {key} | {c(sm, 'lmcut')} | {c(el, 'lmcut')} | {c(en, 'lmcut')} | {c(sm, 'hmax')} "
                 f"| {c(eh, 'hmax')} | {c(en, 'hmax')} | {sum(r['enumeration'] is not None for r in ok)}/{len(ok)} | {unk} |")

    L += ["", "## Oracle coverage (independent UCS, src/ahg/oracle.py)", "",
          "| cell | instances checked | states checked |", "|---|---|---|"]
    for key, rs in cells.items():
        ok = [r for r in rs if r["status"] == "ok"]
        L.append(f"| {key} | {sum(bool(r['oracle']) for r in ok)}/{len(ok)} | {sum(len(r['oracle']) for r in ok)} |")
    L += ["", "Per instance, `raw.json` lists every oracle-checked state as [state, oracle h*, reference h*].", ""]

    L += ["## Time per instance (s, wall-clock in a worker; diagnostic)", "",
          "| cell | median | max | total |", "|---|---|---|---|"]
    for key, rs in cells.items():
        t = [r["seconds"] for r in rs if r["status"] == "ok"]
        L.append(f"| {key} | {fmt(statistics.median(t), 2) if t else '—'} | {fmt(max(t), 2) if t else '—'} "
                 f"| {fmt(sum(t), 1) if t else '—'} |")

    fails = [r for r in raw["instances"] if r["status"] != "ok"]
    L += ["", "## Unreachable goals and generation failures", ""]
    L += [f"- {r['cell']} seed={r['seed']}: {r['status']} — {r['reason']}" for r in fails] or ["- none"]
    return "\n".join(L) + "\n"


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("pilot", "full", "confirm", "replicate"):
        sys.exit(__doc__)
    mode, d16 = sys.argv[1], "--d16" in sys.argv
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    grid = grid_cells(d16)
    if mode == "confirm":
        wanted = sys.argv[sys.argv.index("--cells") + 1].split(";")
        by_key = {cell_key(c): c for c in grid}
        missing = [k for k in wanted if k not in by_key]
        if missing:
            sys.exit(f"unknown cells: {missing}")
        jobs = [(by_key[k], s) for k in wanted for s in CONFIRM_SEEDS]
    else:
        seeds = {"pilot": [0], "full": SEEDS, "replicate": CONFIRM_SEEDS}[mode]
        jobs = [(c, s) for c in grid for s in seeds]
    if mode == "pilot":
        jobs += [(c, s) for c in anchor_cells() for s in SEEDS]
    jobs = [(i, c, s) for i, (c, s) in enumerate(jobs)]
    print(f"{len(jobs)} instances on {workers} workers", flush=True)
    t0, out = time.perf_counter(), [None] * len(jobs)
    with Pool(workers, initializer=_init_worker) as pool:
        for done, (i, rec) in enumerate(pool.imap_unordered(measure_instance, jobs), 1):
            out[i] = rec
            print(f"[{done}/{len(jobs)} {time.perf_counter() - t0:7.0f}s] {rec['cell']} seed={rec['seed']} "
                  f"{rec['status']} {rec.get('seconds', 0):.2f}s", flush=True)
    config = {"name": f"depth_coupling_sweep/{mode}" + ("_d16" if d16 else ""), "mode": mode,
              "decision": ("D15+D16" if d16 else "D15") + (" replication" if mode == "replicate" else ""), "exposed_level0": d16, "workers": workers,
              "cells": wanted if mode == "confirm" else None,
              "levels": LEVELS, "couplings": COUPLINGS, "variants": VARIANTS, "sizes": SIZES,
              "seeds_per_cell": 1 if mode == "pilot" else len(CONFIRM_SEEDS if mode in ("confirm", "replicate") else SEEDS),
              "anchor": {"sizes": ANCHOR_SIZES, "seeds": list(SEEDS)} if mode == "pilot" else None,
              "budget": BUDGET, "state_budget": STATE_BUDGET, "label_budget": LABEL_BUDGET,
              "sample_cap": SAMPLE_CAP, "walks_per_sample": WALKS_PER_SAMPLE, "expanded_cap": EXPANDED_CAP,
              "enum_cap": ENUM_CAP, "oracle_states": ORACLE_STATES, "bootstrap": BOOTSTRAP,
              "r_threshold": R_THRESHOLD, "r_ci_lower": R_CI_LOWER,
              "rng_streams": {"sampling": "landscape:{family}:{n}:{seed}", "expanded": "expanded:{cell}:{seed}",
                              "oracle": "oracle:{cell}:{seed}", "bootstrap": "bootstrap:{cell}"},
              "elapsed_seconds": round(time.perf_counter() - t0, 1)}
    raw = {"config": config, "instances": out}
    if mode == "pilot":
        raw["anchor_check"] = compare_anchors(out)
        if raw["anchor_check"]["mismatches"]:
            raise HardFailure(f"anchor cells do not reproduce [S]: {raw['anchor_check']['mismatches']}")
    path = write_run(config["name"], raw, render(raw), sorted({s for _, _, s in jobs}), config)
    print(f"wrote {path}")


if __name__ == "__main__":
    try:
        main()
    except HardFailure as e:
        sys.exit(f"HARD FAILURE, nothing written: {e}")
