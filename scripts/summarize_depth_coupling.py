"""Side-by-side summary of D15 depth-coupling sweep runs, for findings.md.

Usage: python scripts/summarize_depth_coupling.py RUN_DIR [RUN_DIR ...]

Each RUN_DIR is a results/landscape/depth_coupling_sweep/<mode>/<stamp>/ folder.
Prints markdown to stdout, computed from the runs' raw data alone, with the cell-level
D15 §6 rules taken from measure_depth_coupling.summarise so the criterion is
applied exactly as the run's own report.md applies it.

Group tables pool every reachable instance in the group: R uses +inf for
censored instances (D15 §6), so medians and the 90th percentile are robust
to them and stay honest.
"""

import importlib.util
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from ahg.runlog import load_raw

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("dc", ROOT / "scripts" / "measure_depth_coupling.py")
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)
INF = float("inf")


def load(run_dir):
    raw = load_raw(run_dir)
    return raw, [r for r in raw["instances"] if not r["pr_gated"]]


def fmt(x, nd=2):
    if x is None:
        return "—"
    if x == INF:
        return "+∞"
    return f"{x:.{nd}f}"


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None


def r_of(r):
    return INF if r["effort"]["censored"] else r["effort"]["R"]


def rh_of(r):
    return INF if r["effort"]["R_hmax"] is None else r["effort"]["R_hmax"]


def criterion(name, raw, recs):
    cells = defaultdict(list)
    for r in recs:
        cells[r["cell"]].append(r)
    summ = {k: dc.summarise(v, raw["config"]["seeds_per_cell"]) for k, v in cells.items()}
    met = [k for k, s in summ.items() if s["criterion_1"]]
    elig = [k for k, s in summ.items() if s["eligible"]]
    why = defaultdict(int)
    for k, s in summ.items():
        if s["eligible"]:
            continue
        n = cells[k][0]["n"]
        if n < 12:
            why["n < 12 (size rule)"] += 1
        elif s["reachable"] < 10:
            why["n ≥ 12, fewer than 10 of 20 reachable"] += 1
        else:
            why["n ≥ 12, median solved plan length < 3"] += 1
    print(f"### {name}: criterion part 1\n")
    print(f"- cells: {len(summ)}; eligible: **{len(elig)}**; meeting part 1 (median R ≥ {dc.R_THRESHOLD}, "
          f"CI lower ≥ {dc.R_CI_LOWER}): **{len(met)}**" + (f" — {', '.join(met)}" if met else ""))
    for reason, c in why.items():
        print(f"- ineligible, {reason}: {c}")
    fails = sum(r["status"] == "generation_failure" for r in recs)
    print(f"- instances: {len(recs)}; reachable {sum(r['status'] == 'ok' for r in recs)}; unreachable "
          f"{sum(r['status'] == 'unreachable' for r in recs)}; generation failures {fails}")
    top = sorted(((s["median_R"], k) for k, s in summ.items() if s["eligible"]), reverse=True)[:5]
    print("- highest median R among eligible cells: " + "; ".join(f"{k} = {fmt(m)}" for m, k in top))
    print()
    return summ


def group_table(name, runs, key, label, sizes=(12, 20)):
    print(f"### R and R_hmax by {label}\n")
    print("Each entry: median R / 90th-pct R / max R · median R_hmax · reachable/seeds · censored. "
          "Pooled over all other grid factors.\n")
    head = "| " + label + " | n | " + " | ".join(runs) + " |"
    print(head)
    print("|" + "---|" * (2 + len(runs)))
    vals = sorted({key(r) for _, recs in runs.values() for r in recs}, key=str)
    for v in vals:
        for n in sizes:
            row = []
            for _, recs in runs.values():
                g = [r for r in recs if key(r) == v and r["n"] == n]
                ok = [r for r in g if r["status"] == "ok"]
                rs, rh = [r_of(r) for r in ok], [rh_of(r) for r in ok]
                cens = sum(r["effort"]["censored"] for r in ok)
                row.append(f"{fmt(statistics.median(rs)) if rs else '—'} / {fmt(pct(rs, 0.9))} / {fmt(max(rs) if rs else None)} "
                           f"· {fmt(statistics.median(rh)) if rh else '—'} · {len(ok)}/{len(g)} · {cens}")
            print(f"| {v} | {n} | " + " | ".join(row) + " |")
    print()


def pooled_gaps(stats):
    n = sum(s["n"] for s in stats)
    out = {}
    for h in ("hmax", "lmcut"):
        lt = sum(s[h]["lt"] for s in stats)
        out[h] = (lt / n if n else None, max((s[h]["gap_max"] for s in stats), default=0), n)
    return out


def exactness_table(name, recs):
    print(f"### Exactness by D — {name}\n")
    print("Fraction of states with h < h* (max gap, D9 units; states). `expanded` = distinct states expanded by "
          "A* with that same heuristic. `all` = every reachable non-goal state of enumerated instances.\n")
    print("| D | n | LM-cut sampled | LM-cut expanded | LM-cut all | h_max sampled | h_max expanded | h_max all |")
    print("|---|---|---|---|---|---|---|---|")
    for D in sorted({r["D"] for r in recs}):
        for n in (8, 12, 20):
            ok = [r for r in recs if r["D"] == D and r["n"] == n and r["status"] == "ok"]
            sm = pooled_gaps([dc.gap_stats(r["sampled"]["states"]) for r in ok])
            ex = {h: pooled_gaps([r["expanded_states"][h] for r in ok])[h] for h in ("lmcut", "hmax")}
            en = pooled_gaps([r["enumeration"] for r in ok if r["enumeration"] is not None])
            c = lambda t: f"{fmt(t[0], 3)} ({t[1]}; {t[2]})" if t[2] else "—"
            print(f"| {D} | {n} | {c(sm['lmcut'])} | {c(ex['lmcut'])} | {c(en['lmcut'])} | {c(sm['hmax'])} "
                  f"| {c(ex['hmax'])} | {c(en['hmax'])} |")
    print()


def interaction_table(name, recs):
    print(f"### LM-cut exactness by (ρ, m) and D — {name}\n")
    print("LM-cut h < h* on LM-cut-expanded states (pooled over variants and n ≥ 12; states), and h_max on "
          "h_max-expanded states for comparison.\n")
    print("| (ρ, m) | D=0 LM-cut | D=0 h_max | D=1 LM-cut | D=1 h_max | D=2 LM-cut | D=2 h_max | D=3 LM-cut | D=3 h_max |")
    print("|---|---|---|---|---|---|---|---|---|")
    for rho, m in dc.COUPLINGS:
        row = []
        for D in dc.LEVELS:
            ok = [r for r in recs if r["rho"] == rho and r["m"] == m and r["D"] == D and r["n"] >= 12 and r["status"] == "ok"]
            for h in ("lmcut", "hmax"):
                t = pooled_gaps([r["expanded_states"][h] for r in ok])[h]
                row.append(f"{fmt(t[0], 3)} ({t[2]})" if t[2] else "—")
        print(f"| ({rho}, {'all' if m is None else m}) | " + " | ".join(row) + " |")
    print()


def timing_table(runs):
    print("### Search time from the initial state (s), n = 20\n")
    print("Median per instance of the A* search time (heuristic computation included), and median time per "
          "expanded node. Wall-clock in one of 6 workers; diagnostic.\n")
    print("| run | D | median s LM-cut | median s h_max | median s h0 | ms/expansion LM-cut | ms/expansion h_max | median exp. LM-cut / h_max |")
    print("|---|---|---|---|---|---|---|---|")
    for name, (_, recs) in runs.items():
        for D in dc.LEVELS:
            ok = [r for r in recs if r["D"] == D and r["n"] == 20 and r["status"] == "ok"]
            if not ok:
                continue
            sec = {h: [r["effort"]["seconds"][h] for r in ok] for h in ("lmcut", "hmax", "h0")}
            per = {h: [1000 * r["effort"]["seconds"][h] / max(1, r["init"]["expanded"][h]) for r in ok] for h in ("lmcut", "hmax")}
            ex = {h: statistics.median(r["init"]["expanded"][h] for r in ok) for h in ("lmcut", "hmax")}
            print(f"| {name} | {D} | {fmt(statistics.median(sec['lmcut']), 4)} | {fmt(statistics.median(sec['hmax']), 4)} "
                  f"| {fmt(statistics.median(sec['h0']), 4)} | {fmt(statistics.median(per['lmcut']), 3)} "
                  f"| {fmt(statistics.median(per['hmax']), 3)} | {ex['lmcut']:g} / {ex['hmax']:g} |")
    print()


def extras_table(runs):
    print("### Instance-level facts cited in findings.md\n")
    for name, (_, recs) in runs.items():
        ok = [r for r in recs if r["status"] == "ok"]
        print(f"**{name}**\n")
        hits = {h: sum(r["init"]["budget_hit"][h] for r in ok) for h in ("h0", "hmax", "lmcut")}
        print(f"- init searches at budget: {hits}")
        print(f"- reachable instances with R ≥ 2: {sum(r_of(r) >= 2 for r in ok)}; R ≥ 5: "
              f"{sum(r_of(r) >= 5 for r in ok)}; of {len(ok)}")
        top = max(ok, key=r_of)
        print(f"- max R: {top['cell']} seed={top['seed']}: R = {fmt(r_of(top))}, R_hmax = {fmt(rh_of(top))}, "
              f"expanded {top['init']['expanded']}, plan length {top['effort']['plan_len_lmcut']}, "
              f"seconds {top['effort']['seconds']}")
        for D in dc.LEVELS:
            big = [r for r in recs if r["D"] == D and r["n"] >= 12]
            g = [r for r in big if r["status"] == "ok"]
            print(f"- D={D}, n ≥ 12: reachable {len(g)}/{len(big)}; median plan length "
                  f"{statistics.median(r['effort']['plan_len_lmcut'] for r in g):g}; median credential chain "
                  f"{statistics.median(r['effort']['cred_chain_len'] for r in g):g}")
        for v in sorted({r["variant"] for r in recs}):
            per = [[r["status"] == "ok" for r in recs if r["variant"] == v and r["n"] == 20 and r["D"] == D]
                   for D in dc.LEVELS]
            print(f"- {v} n=20 reachable by D: {' / '.join(f'{sum(g)}/{len(g)}' for g in per)}")
        fails = defaultdict(int)
        for r in recs:
            if r["status"] == "generation_failure":
                fails[f"{r['variant']} n={r['n']} D={r['D']}"] += 1
        print(f"- generation failures: {dict(fails) or 0}\n")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    runs = {}
    for d in sys.argv[1:]:
        raw, recs = load(d)
        runs[raw["config"]["decision"]] = (raw, recs)
        print(f"- **{raw['config']['decision']}**: `{Path(d).resolve().relative_to(ROOT)}`")
    print()
    for name, (raw, recs) in runs.items():
        criterion(name, raw, recs)
    group_table("D", runs, lambda r: r["D"], "D")
    group_table("(ρ, m)", runs, lambda r: f"({r['rho']}, {'all' if r['m'] is None else r['m']})", "(ρ, m)")
    group_table("variant", runs, lambda r: r["variant"], "variant")
    for name, (_, recs) in runs.items():
        exactness_table(name, recs)
    for name, (_, recs) in runs.items():
        interaction_table(name, recs)
    timing_table(runs)
    extras_table(runs)


if __name__ == "__main__":
    main()
