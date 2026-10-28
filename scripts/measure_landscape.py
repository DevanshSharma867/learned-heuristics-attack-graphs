"""Measure the heuristic landscape of PR-gated attack graphs (D13 variant).

Usage: python scripts/measure_landscape.py small|large [--pilot]

  small  -> run "landscape_small_n": n in {6, 8, 12}, seeds 0-19 per cell,
            plus full enumeration of the reachable state space where it fits.
  large  -> run "landscape_large_n": n in {20, 30, 40}, seeds from 0 upwards
            until 15 reachable instances per cell (at most 60 seeds tried).
  --pilot   one seed per cell, written nowhere; prints timings only.

Per instance it records:
  - UnreachableGoal (counted, never dropped: CLAUDE.md rule 10);
  - nodes expanded from the initial state by A* with h0, h_max and LM-cut,
    each capped at BUDGET expansions (a capped count is a lower bound);
  - h* and the optimal plan length from the initial state;
  - up to SAMPLE_CAP sampled reachable non-goal states, with h*(s), h_max(s)
    and LM-cut(s) for each;
  - (small only) the same h_max/LM-cut gap statistics over every reachable
    non-goal state, so sampler bias is visible next to the sampled numbers.

h* is computed by A* + LM-cut and cross-checked against A* + h_max. Both are
admissible, so the two optimal costs must be equal. A mismatch, or an
admissible heuristic exceeding h*, aborts the run before anything is written.
In the small run, the enumeration computes h* a third, independent way and
must agree with A* on every sampled state. The helpers live in ahg.measure.

The output goes through ahg.runlog into results/landscape/<run>/ as raw.json,
report.md (rendered from raw.json by render()) and provenance.json.
"""

import random
import statistics
import sys
import time
from pathlib import Path

from ahg.attack_graph import UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.measure import HardFailure, check_admissible, enumerate_exact, exact_cost, gap_stats, sample_states
from ahg.runlog import write_run
from ahg.search import INF, uniform_cost
from ahg.topology import GENERATORS

BUDGET = 200_000  # max expansions per search
SAMPLE_CAP = 300  # sampled non-goal states per instance
WALKS_PER_SAMPLE = 10  # random walks tried per wanted sample before giving up
ENUM_CAP = 50_000  # small run: enumerate the reachable space only up to this many states

RUNS = {
    "small": dict(name="landscape_small_n", sizes=[6, 8, 12], seeds=20, reachable_target=None, enumerate=True),
    "large": dict(name="landscape_large_n", sizes=[20, 30, 40], seeds=60, reachable_target=15, enumerate=False),
}


def measure_instance(family, seed, n, pool, do_enum):
    try:
        task = make_instance(family, seed, n, pool, pr_gated=True).task
    except UnreachableGoal as e:
        return {"family": family, "n": n, "seed": seed, "status": "unreachable", "reason": str(e)}
    t0 = time.perf_counter()
    rec = {"family": family, "n": n, "seed": seed, "status": "ok",
           "facts": len(task.facts), "actions": len(task.actions)}

    hstar0, r_lm, r_hm = exact_cost(task, task.init, BUDGET)
    r_h0 = uniform_cost(task, max_expansions=BUDGET)
    rec["init"] = {
        "hstar": hstar0,
        "plan_len": len(r_lm.plan) if hstar0 is not None else None,
        "expanded": {"h0": r_h0.expanded, "hmax": r_hm.expanded, "lmcut": r_lm.expanded},
        "budget_hit": {"h0": r_h0.budget_hit, "hmax": r_hm.budget_hit, "lmcut": r_lm.budget_hit},
    }
    if hstar0 is not None and not r_h0.budget_hit and r_h0.cost != hstar0:
        raise HardFailure(f"{family} n={n} seed={seed}: UCS {r_h0.cost} != h* {hstar0}")

    rng = random.Random(f"landscape:{family}:{n}:{seed}")
    states, cap_bound = sample_states(task, rng, SAMPLE_CAP, WALKS_PER_SAMPLE)
    exact = enumerate_exact(task, ENUM_CAP) if do_enum else None
    triples, unknown = [], 0
    for s in states:
        hs, _, _ = exact_cost(task, s, BUDGET)
        if hs is None:
            unknown += 1
            continue
        if exact is not None and exact[s] != hs:
            raise HardFailure(f"{family} n={n} seed={seed}: enumeration h*={exact[s]} != A* {hs} at {s:#x}")
        triples.append([hs, *check_admissible(task, s, hs)])
    rec["sampled"] = {"states": triples, "cap_bound": cap_bound, "hstar_unknown": unknown}

    if do_enum:
        if exact is None:
            rec["enumeration"] = None  # infeasible: more than ENUM_CAP reachable states
        else:
            non_goal = [(hs, s) for s, hs in exact.items() if hs != 0]
            if any(hs == INF for hs, _ in non_goal):
                raise HardFailure(f"{family} n={n} seed={seed}: enumerated state cannot reach the goal")
            if exact[task.init] != hstar0:
                raise HardFailure(f"{family} n={n} seed={seed}: enumeration h*(init) != A*")
            full = [[hs, *check_admissible(task, s, hs)] for hs, s in non_goal]
            rec["enumeration"] = {"reachable": len(exact), **gap_stats(full)}
    rec["seconds"] = round(time.perf_counter() - t0, 3)
    return rec


def render(raw):
    """report.md from raw.json alone, so the report can always be regenerated from it."""
    cfg = raw["config"]
    L = [f"# {cfg['name']}", "",
         f"PR-gated attack graphs, families {', '.join(cfg['families'])}, n in {cfg['sizes']}. "
         f"Costs in D9 integer units (38 per effort unit). Expansion budget {cfg['budget']:,}; "
         f"up to {cfg['sample_cap']} sampled non-goal states per instance.", "",
         "h* is from A*+LM-cut, cross-checked against A*+h_max on every state"
         + (" and against full enumeration on every enumerated instance. " if cfg["enumerate"] else ". ")
         + "No mismatch and no admissible heuristic above h* occurred (either would have aborted the run).", "",
         "**Gap columns.** `h<h*` is the fraction of states where the heuristic is strictly below h*. "
         "`mean gap` is the mean of h* − h over *all* evaluated states (zeros included); `max gap` is the largest.", ""]

    cells = {}
    for r in raw["instances"]:
        cells.setdefault((r["family"], r["n"]), []).append(r)

    def frac(st, h):
        return f"{st[h]['lt'] / st['n']:.3f}" if st["n"] else "—"

    def mean(st, h):
        return f"{st[h]['gap_sum'] / st['n']:.1f}" if st["n"] else "—"

    def med(xs):
        return f"{statistics.median(xs):g}" if xs else "—"

    L += ["## Instances and initial-state search", "",
          "| family | n | seeds | reachable | unreachable | h* unknown | median plan len | median h* "
          "| median exp. h0 | h0 at budget | median exp. h_max | median exp. LM-cut |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (fam, n), rs in cells.items():
        ok = [r for r in rs if r["status"] == "ok"]
        known = [r for r in ok if r["init"]["hstar"] is not None]
        e = {h: [r["init"]["expanded"][h] for r in ok] for h in ("h0", "hmax", "lmcut")}
        h0_cap = sum(r["init"]["budget_hit"]["h0"] for r in ok)
        h0_med = med(e["h0"]) + (" (≥, lower bound)" if h0_cap and h0_cap >= len(ok) / 2 else "")
        L.append(f"| {fam} | {n} | {len(rs)} | {len(ok)} | {len(rs) - len(ok)} | {len(ok) - len(known)} "
                 f"| {med([r['init']['plan_len'] for r in known])} | {med([r['init']['hstar'] for r in known])} "
                 f"| {h0_med} | {h0_cap}/{len(ok)} | {med(e['hmax'])} | {med(e['lmcut'])} |")
    L += ["", "`h0 at budget` counts instances where uniform-cost search stopped at the budget; their "
          "expansion count is a lower bound. The median is marked as a lower bound when at least half "
          "the cell hit the budget.", ""]

    L += ["## Sampled states: h_max and LM-cut versus h*", "",
          "| family | n | states | instances at cap | h* unknown | h_max h<h* | h_max mean gap | h_max max gap "
          "| LM-cut h<h* | LM-cut mean gap | LM-cut max gap |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for (fam, n), rs in cells.items():
        ok = [r for r in rs if r["status"] == "ok"]
        st = gap_stats([t for r in ok for t in r["sampled"]["states"]])
        cap = sum(r["sampled"]["cap_bound"] for r in ok)
        unk = sum(r["sampled"]["hstar_unknown"] for r in ok)
        L.append(f"| {fam} | {n} | {st['n']} | {cap}/{len(ok)} | {unk} | {frac(st, 'hmax')} | {mean(st, 'hmax')} "
                 f"| {st['hmax']['gap_max']} | {frac(st, 'lmcut')} | {mean(st, 'lmcut')} | {st['lmcut']['gap_max']} |")
    L += ["", f"`instances at cap` counts instances that yielded the full {cfg['sample_cap']} distinct states; "
          "the rest exhausted the walk budget first, i.e. the sample is every distinct state the walks found.", ""]

    if cfg["enumerate"]:
        L += ["## Sampled versus exact (full enumeration of reachable non-goal states)", "",
              "| family | n | enumerated | states (sampled / all) | h_max h<h* (sampled / all) "
              "| h_max mean gap (s / all) | LM-cut h<h* (sampled / all) | LM-cut mean gap (s / all) |",
              "|---|---|---|---|---|---|---|---|"]
        for (fam, n), rs in cells.items():
            ok = [r for r in rs if r["status"] == "ok"]
            en = [r for r in ok if r["enumeration"] is not None]
            # Compare on the same instances only, so the difference is sampler bias, not instance mix.
            s = gap_stats([t for r in en for t in r["sampled"]["states"]])
            a = {"n": sum(r["enumeration"]["n"] for r in en)}
            for h in ("hmax", "lmcut"):
                a[h] = {"lt": sum(r["enumeration"][h]["lt"] for r in en),
                        "gap_sum": sum(r["enumeration"][h]["gap_sum"] for r in en),
                        "gap_max": max((r["enumeration"][h]["gap_max"] for r in en), default=0)}
            L.append(f"| {fam} | {n} | {len(en)}/{len(ok)} | {s['n']} / {a['n']} | {frac(s, 'hmax')} / {frac(a, 'hmax')} "
                     f"| {mean(s, 'hmax')} / {mean(a, 'hmax')} | {frac(s, 'lmcut')} / {frac(a, 'lmcut')} "
                     f"| {mean(s, 'lmcut')} / {mean(a, 'lmcut')} |")
        L += ["", f"Enumeration is attempted up to {cfg['enum_cap']:,} reachable states per instance. "
              "Both columns use only the enumerated instances. Fractions are pooled over states, so "
              "instances with many states weigh more in the `all` column.", ""]

    unreach = [r for r in raw["instances"] if r["status"] == "unreachable"]
    L += ["## Generation failures (UnreachableGoal)", ""]
    L += [f"- {r['family']} n={r['n']} seed={r['seed']}: {r['reason']}" for r in unreach] or ["- none"]
    return "\n".join(L) + "\n"


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in RUNS:
        sys.exit(__doc__)
    spec, pilot = RUNS[sys.argv[1]], "--pilot" in sys.argv
    pool = load_table(Path(__file__).resolve().parent.parent / "data" / "derived" / "cves.csv")
    instances, seeds_used = [], set()
    for n in spec["sizes"]:
        for family in GENERATORS:
            reachable = 0
            for seed in range(1 if pilot else spec["seeds"]):
                if spec["reachable_target"] and reachable >= spec["reachable_target"]:
                    break
                rec = measure_instance(family, seed, n, pool, spec["enumerate"])
                instances.append(rec)
                seeds_used.add(seed)
                reachable += rec["status"] == "ok"
                print(f"{family:14s} n={n:2d} seed={seed:2d} {rec['status']:11s} {rec.get('seconds', 0):8.2f}s", flush=True)
    config = {"name": spec["name"], "variant": "pr_gated", "families": list(GENERATORS), "sizes": spec["sizes"],
              "seeds_per_cell": spec["seeds"], "reachable_target": spec["reachable_target"], "budget": BUDGET,
              "sample_cap": SAMPLE_CAP, "walks_per_sample": WALKS_PER_SAMPLE,
              "enumerate": spec["enumerate"], "enum_cap": ENUM_CAP if spec["enumerate"] else None,
              "sampling_rng": "random.Random('landscape:{family}:{n}:{seed}')"}
    raw = {"config": config, "instances": instances}
    if pilot:
        print(render(raw))
        return
    out = write_run(spec["name"], raw, render(raw), sorted(seeds_used), config)
    print(f"wrote {out}")


if __name__ == "__main__":
    try:
        main()
    except HardFailure as e:
        sys.exit(f"HARD FAILURE, nothing written: {e}")
