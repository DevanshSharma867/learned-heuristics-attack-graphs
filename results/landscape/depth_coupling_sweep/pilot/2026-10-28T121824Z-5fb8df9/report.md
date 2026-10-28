# depth_coupling_sweep/pilot

Mode **pilot** — a pilot for timing and tooling, not a result (D15 §7).
D12 schema (pr_gated off) with the D15 knobs; anchor cells are pr_gated with knobs off. Init budget 200,000 expansions; per-state labelling budget 20,000, per-instance 2,000,000. Costs in D9 units (38 per effort unit).

h* checks passed on every instance (any failure would have aborted the run): A*+LM-cut = A*+h_max, enumeration = A* where enumerated, UCS = h* where UCS finished, no admissible h above h*, independent oracle = h* on every oracle-checked state.

**Anchor reproduction of [S]** (`results/landscape/landscape_small_n/2026-10-22T114620Z-4f00c1b/raw.json`): 120 instances compared, 0 mismatches — **PASS**.

## Effort (D15 §4, §6)

R = A*+LM-cut expansions from the initial state / optimal plan length. Censored = LM-cut hit the budget; it counts as R = +∞. `elig.` and `crit. 1` apply the D15 §6 rules (n ≥ 12, ≥ 10 reachable, median solved plan length ≥ 3; median R ≥ 5 with bootstrap CI lower bound ≥ 3); both need 20 seeds, so they are always `no` in a pilot.

| cell | reachable | gen. fail | censored | median R | R CI low | median R_hmax | median plan len | median exp. h0 / h_max / LM-cut | h0 at budget | elig. | crit. 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flat n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 11 / 4 / 4 | 0/1 | no | no |
| flat n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 9 / 4 / 4 | 0/1 | no | no |
| flat n=8 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 8 / 4 / 4 | 0/1 | no | no |
| flat n=8 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 9 / 4 / 4 | 0/1 | no | no |
| flat n=8 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 11 / 7 / 6 | 0/1 | no | no |
| flat n=8 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 6 / 5 / 5 | 0/1 | no | no |
| flat n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 18 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 27 / 5 / 5 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 29 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 23 / 5 / 5 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 24 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 14 / 5 / 5 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 19 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 26 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.29 | 7 | 24 / 9 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 22 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 19 / 7 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 14 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 15 / 7 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 20 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 13 / 7 / 7 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 13 / 7 / 7 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 13 / 7 / 7 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 12 / 7 / 7 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 13 / 7 / 7 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 18 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 9 / 6 / 6 | 0/1 | no | no |
| flat n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 8 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 8 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 6 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 7 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 18 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 7 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 9 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 20 / 5 / 5 | 0/1 | no | no |
| flat n=12 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 16 / 5 / 5 | 0/1 | no | no |
| flat n=12 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 12 / 5 / 5 | 0/1 | no | no |
| flat n=12 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 14 / 6 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.40 | — | 1.80 | 5 | 45 / 9 / 7 | 0/1 | no | no |
| flat n=12 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 8 / 6 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 28 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 104 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 17 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 84 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 25 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 29 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 88 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 23 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 48 / 6 / 6 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 30 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 56 / 4 / 4 | 0/1 | no | no |
| tiered3 n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 38 / 4 / 4 | 0/1 | no | no |
| tiered3 n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 30 / 4 / 4 | 0/1 | no | no |
| tiered3 n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 20 / 4 / 4 | 0/1 | no | no |
| tiered3 n=12 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 42 / 9 / 8 | 0/1 | no | no |
| tiered3 n=12 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 10 | 22 / 10 / 10 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 52 / 5 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 32 / 5 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 39 / 5 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 20 / 5 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 9 | 35 / 9 / 9 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 11 | 19 / 11 / 11 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 68 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 33 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 68 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 25 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 1267 / 3 / 3 | 0/1 | no | no |
| flat n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 846 / 3 / 3 | 0/1 | no | no |
| flat n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 2 | 1512 / 2 / 2 | 0/1 | no | no |
| flat n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.50 | 2 | 2739 / 5 / 2 | 0/1 | no | no |
| flat n=20 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 650 / 3 / 3 | 0/1 | no | no |
| flat n=20 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.67 | 3 | 2214 / 5 / 3 | 0/1 | no | no |
| flat n=20 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.60 | 5 | 1583 / 13 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 1346 / 5 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 933 / 5 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 1019 / 3 / 3 | 0/1 | no | no |
| flat n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.00 | 3 | 1592 / 6 / 3 | 0/1 | no | no |
| flat n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 685 / 5 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 1163 / 5 / 4 | 0/1 | no | no |
| flat n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.33 | 6 | 1323 / 14 / 6 | 0/1 | no | no |
| flat n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.40 | 5 | 1368 / 7 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.71 | 7 | 3204 / 12 / 7 | 0/1 | no | no |
| flat n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.29 | 7 | 1849 / 9 / 7 | 0/1 | no | no |
| flat n=20 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.60 | 5 | 2780 / 8 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.40 | 5 | 522 / 7 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.60 | 5 | 2594 / 8 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.38 | 8 | 1110 / 19 / 8 | 0/1 | no | no |
| flat n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.25 | — | 1.62 | 8 | 1273 / 13 / 10 | 0/1 | no | no |
| flat n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 951 / 8 / 8 | 0/1 | no | no |
| flat n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.44 | 9 | 1280 / 13 / 9 | 0/1 | no | no |
| flat n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 1469 / 10 / 7 | 0/1 | no | no |
| flat n=20 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.25 | — | 1.62 | 8 | 713 / 13 / 10 | 0/1 | no | no |
| flat n=20 D=3 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 1076 / 10 / 7 | 0/1 | no | no |
| flat n=20 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.78 | 9 | 1055 / 25 / 9 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 10 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 9 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 485 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 17 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 177 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 57 / 5 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.50 | 4 | 58 / 6 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 581 / 6 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 32 / 6 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 29 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.43 | 7 | 598 / 17 / 7 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 52 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 50 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 391 / 6 / 6 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 44 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 40 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.75 | 8 | 406 / 14 / 8 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 62 / 8 / 8 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 61 / 8 / 8 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 9 | 658 / 9 / 9 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 59 / 8 / 8 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 59 / 8 / 8 | 0/1 | no | no |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 9 | 227 / 9 / 9 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 904 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 717 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 735 / 5 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 359 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 529 / 3 / 3 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.86 | 7 | 238 / 13 / 7 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 432 / 6 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 301 / 5 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 384 / 5 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 257 / 5 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 280 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.44 | 9 | 224 / 13 / 9 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.83 | 6 | 488 / 11 / 6 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 6 | 363 / 8 / 6 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.83 | 6 | 450 / 11 / 6 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 6 | 315 / 8 / 6 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 256 / 6 / 5 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=2 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.10 | 10 | 128 / 11 / 10 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.62 | 8 | 582 / 13 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.62 | 8 | 481 / 13 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.62 | 8 | 533 / 13 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.38 | 8 | 329 / 11 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.88 | 8 | 687 / 15 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.36 | 11 | 271 / 26 / 11 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.33 | 9 | 8210 / 21 / 9 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.67 | 9 | 4734 / 15 / 9 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.62 | 8 | 5470 / 13 / 8 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.90 | 10 | 2128 / 29 / 10 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.60 | 10 | 4767 / 16 / 10 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.50 | 10 | 3268 / 15 / 10 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.40 | 10 | 3159 / 14 / 10 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.73 | 11 | 1750 / 30 / 11 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 6.36 | 14 | 3160 / 89 / 14 | 0/1 | no | no |
| tiered5 n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 3.29 | 14 | 1555 / 46 / 14 | 0/1 | no | no |
| tiered5 n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.75 | 12 | 2019 / 33 / 12 | 0/1 | no | no |
| tiered5 n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.27 | 15 | 746 / 34 / 15 | 0/1 | no | no |
| tiered5 n=20 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=0 rho=0.0 m=all pr_gated | 19/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 3 | 23 / 3 / 3 | 0/19 | no | no |
| hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated | 15/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 4 | 20 / 4 / 4 | 0/15 | no | no |
| tiered3 n=8 D=0 rho=0.0 m=all pr_gated | 15/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 4 | 14 / 5 / 4 | 0/15 | no | no |
| flat n=12 D=0 rho=0.0 m=all pr_gated | 18/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 3.00 | 20.5 / 3.0 / 3.0 | 0/18 | yes | no |
| hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated | 17/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 4 | 55 / 4 / 4 | 0/17 | yes | no |
| tiered3 n=12 D=0 rho=0.0 m=all pr_gated | 19/20 | 0 | 0 | 1.00 | 1.00 | 1.00 | 5 | 57 / 6 / 5 | 0/19 | yes | no |

## Exactness: fraction of states with h < h* (max gap in D9 units)

Sampled = [S] random walks; expanded = distinct states the A* search with that heuristic expanded from the initial state; all = every reachable non-goal state, enumerated instances only.

| cell | LM-cut: sampled | LM-cut: LM-cut-expanded | LM-cut: all | h_max: sampled | h_max: h_max-expanded | h_max: all | enumerated | h* unknown (sampled + expanded) |
|---|---|---|---|---|---|---|---|---|
| flat n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.160 (38) | 0.000 (0) | 0.148 (38) | 1/1 | 0 |
| flat n=8 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.200 (245) | 0.714 (245) | 0.238 (245) | 1/1 | 0 |
| flat n=8 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.294 (38) | 0.667 (38) | 0.308 (38) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.025 (38) | 0.333 (38) | 0.049 (38) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.207 (38) | 0.000 (0) | 0.194 (38) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.167 (38) | 0.030 (38) | 1/1 | 0 |
| tiered3 n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.064 (38) | 0.667 (38) | 0.082 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.333 (76) | 0.778 (76) | 0.349 (76) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.071 (38) | 0.667 (38) | 0.089 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.062 (38) | 0.429 (38) | 0.091 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.222 (38) | 0.667 (38) | 0.250 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.5 m=all | 0.036 (81) | 0.000 (0) | 0.019 (81) | 0.048 (119) | 0.000 (0) | 0.025 (119) | 1/1 | 0 |
| flat n=12 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.167 (38) | 0.018 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.004 (38) | 0.500 (38) | 0.003 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.006 (38) | 0.500 (38) | 0.005 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.006 (38) | 0.500 (38) | 0.007 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.006 (38) | 0.500 (38) | 0.005 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.5 m=all | 0.015 (43) | 0.000 (0) | 0.008 (43) | 0.038 (81) | 0.500 (38) | 0.024 (81) | 1/1 | 0 |
| flat n=12 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.006 (38) | 0.500 (38) | 0.005 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.057 (76) | 0.600 (76) | 0.028 (76) | 1/1 | 0 |
| flat n=12 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.031 (76) | 0.600 (76) | 0.017 (76) | 1/1 | 0 |
| flat n=12 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.047 (38) | 0.000 (0) | 0.029 (38) | 1/1 | 0 |
| flat n=12 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.073 (38) | 0.333 (38) | 0.045 (38) | 1/1 | 0 |
| flat n=12 D=2 rho=0.5 m=all | 0.038 (99) | 0.286 (99) | 0.023 (99) | 0.091 (157) | 0.889 (144) | 0.058 (157) | 1/1 | 0 |
| flat n=12 D=2 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.004 (38) | 0.333 (38) | 0.004 (38) | 1/1 | 0 |
| flat n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.003 (38) | 0.500 (38) | 0.004 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.003 (38) | 0.400 (38) | 0.004 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.004 (38) | 0.500 (38) | 0.005 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.022 (38) | 0.600 (38) | 0.025 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=12 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.197 (38) | 0.444 (76) | 0.155 (76) | 1/1 | 0 |
| tiered3 n=12 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=0 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.105 (38) | 0.100 (38) | 0.130 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.0 m=all | 0.013 (22) | 0.000 (0) | 0.013 (22) | 0.080 (38) | 0.600 (38) | 0.066 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.068 (38) | 0.600 (38) | 0.069 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.25 m=all | 0.018 (22) | 0.000 (0) | 0.015 (22) | 0.096 (38) | 0.600 (38) | 0.077 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.057 (38) | 0.600 (38) | 0.057 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.149 (38) | 0.444 (38) | 0.171 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.254 (76) | 0.000 (0) | 0.278 (76) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.172 (76) | 0.000 (0) | 0.167 (76) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.120 (16) | 0.000 (0) | 0.133 (16) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=0 rho=0.5 m=1 | 0.007 (13) | 0.000 (0) | — | 0.033 (18) | 0.800 (18) | — | 0/1 | 0 |
| flat n=20 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=0 rho=1.0 m=1 | 0.013 (18) | 0.000 (0) | — | 0.070 (18) | 0.800 (18) | — | 0/1 | 0 |
| flat n=20 D=0 rho=1.0 m=all | 0.037 (38) | 0.200 (36) | — | 0.180 (123) | 0.846 (123) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.027 (38) | 0.200 (15) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.017 (38) | 0.200 (33) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.027 (38) | 0.333 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.5 m=1 | 0.007 (13) | 0.333 (27) | — | 0.037 (56) | 0.667 (56) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.020 (38) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | — | 0.073 (56) | 0.800 (56) | — | 0/1 | 0 |
| flat n=20 D=1 rho=1.0 m=all | 0.023 (36) | 0.167 (36) | — | 0.193 (161) | 0.857 (161) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.0 m=all | 0.020 (20) | 0.000 (0) | — | 0.063 (38) | 0.286 (38) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.25 m=1 | 0.007 (18) | 0.000 (0) | — | 0.290 (56) | 0.667 (56) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.143 (76) | 0.778 (76) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.5 m=1 | 0.057 (18) | 0.000 (0) | — | 0.240 (56) | 0.875 (18) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.5 m=all | 0.090 (20) | 0.000 (0) | — | 0.163 (38) | 0.286 (38) | — | 0/1 | 0 |
| flat n=20 D=2 rho=1.0 m=1 | 0.060 (18) | 0.000 (0) | — | 0.200 (56) | 0.875 (18) | — | 0/1 | 0 |
| flat n=20 D=2 rho=1.0 m=all | 0.100 (58) | 0.125 (18) | — | 0.357 (114) | 0.895 (114) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.0 m=all | 0.030 (38) | 0.800 (38) | — | 0.087 (56) | 0.846 (56) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.25 m=1 | 0.007 (18) | 0.375 (18) | — | 0.183 (56) | 0.750 (56) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.25 m=all | 0.013 (38) | 0.333 (20) | — | 0.047 (91) | 0.692 (91) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.5 m=1 | 0.027 (21) | 0.429 (21) | — | 0.157 (132) | 0.800 (132) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.5 m=all | 0.103 (38) | 0.800 (38) | — | 0.313 (56) | 0.846 (56) | — | 0/1 | 0 |
| flat n=20 D=3 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | — | 0.183 (132) | 0.800 (132) | — | 0/1 | 0 |
| flat n=20 D=3 rho=1.0 m=all | 0.063 (38) | 0.444 (34) | — | 0.217 (199) | 0.920 (199) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.020 (38) | 0.333 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 0.003 (11) | 0.000 (0) | — | 0.160 (76) | 0.400 (69) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.053 (38) | 0.600 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.063 (38) | 0.667 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.083 (38) | 0.500 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.027 (38) | 0.333 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.080 (38) | 0.500 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.230 (76) | 0.824 (76) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.030 (38) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.023 (38) | 0.200 (27) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.207 (76) | 0.667 (65) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.060 (69) | 0.200 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.087 (38) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.113 (107) | 0.643 (107) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 0.020 (31) | 0.000 (0) | — | 0.040 (38) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 0.003 (40) | 0.000 (0) | 0.000 (40) | 0.100 (175) | 0.000 (0) | 0.004 (175) | 1/1 | 0 |
| tiered3 n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.017 (38) | 0.200 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.043 (16) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=0 rho=1.0 m=all | 0.027 (38) | 0.000 (0) | — | 0.297 (76) | 0.769 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.0 m=all | 0.017 (6) | 0.000 (0) | — | 0.053 (38) | 0.500 (22) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.25 m=1 | 0.020 (6) | 0.000 (0) | — | 0.027 (38) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.25 m=all | 0.003 (16) | 0.000 (0) | — | 0.050 (38) | 0.400 (22) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.010 (38) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.5 m=all | 0.007 (16) | 0.000 (0) | — | 0.107 (38) | 0.500 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=1 rho=1.0 m=all | 0.030 (38) | 0.000 (0) | 0.002 (38) | 0.350 (76) | 0.769 (76) | 0.066 (76) | 1/1 | 0 |
| tiered3 n=20 D=2 rho=0.0 m=all | 0.007 (22) | 0.000 (0) | — | 0.147 (38) | 0.727 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.25 m=1 | 0.007 (22) | 0.000 (0) | — | 0.147 (38) | 0.625 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.25 m=all | 0.007 (22) | 0.000 (0) | — | 0.143 (38) | 0.727 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.097 (38) | 0.625 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.113 (38) | 0.167 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=2 rho=1.0 m=all | 0.007 (38) | 0.000 (0) | 0.002 (38) | 0.217 (76) | 0.727 (38) | 0.063 (76) | 1/1 | 0 |
| tiered3 n=20 D=3 rho=0.0 m=all | 0.010 (22) | 0.000 (0) | — | 0.300 (38) | 0.846 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.25 m=1 | 0.007 (22) | 0.000 (0) | — | 0.317 (38) | 0.846 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.25 m=all | 0.020 (22) | 0.000 (0) | — | 0.370 (38) | 0.846 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.203 (76) | 0.818 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.5 m=all | 0.070 (38) | 0.000 (0) | — | 0.290 (92) | 0.867 (55) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=3 rho=1.0 m=all | 0.033 (38) | 0.000 (0) | 0.001 (38) | 0.430 (152) | 0.923 (152) | 0.085 (152) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.710 (38) | 0.905 (38) | — | 0/1 | 0 |
| tiered5 n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.703 (38) | 0.867 (38) | 0.300 (38) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.647 (38) | 0.692 (38) | 0.226 (38) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.653 (76) | 0.931 (76) | 0.290 (76) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=0.0 m=all | 0.007 (38) | 0.000 (0) | 0.000 (38) | 0.743 (76) | 0.875 (76) | 0.299 (76) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 0.010 (38) | 0.000 (0) | 0.000 (38) | 0.720 (76) | 0.867 (76) | 0.300 (76) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.25 m=all | 0.010 (38) | 0.000 (0) | 0.000 (38) | 0.607 (76) | 0.714 (60) | 0.222 (76) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 0.003 (38) | 0.000 (0) | 0.000 (38) | 0.650 (114) | 0.933 (114) | 0.290 (114) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.0 m=all | 0.083 (61) | 0.214 (15) | 0.004 (61) | 0.750 (152) | 0.978 (152) | 0.301 (152) | 1/1 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=1 | 0.040 (76) | 0.000 (0) | 0.004 (76) | 0.740 (152) | 0.957 (152) | 0.309 (152) | 1/1 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=all | 0.040 (38) | 0.000 (0) | 0.002 (38) | 0.617 (114) | 0.848 (114) | 0.216 (114) | 1/1 | 0 |
| tiered5 n=20 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.599 (190) | 0.941 (190) | 0.300 (190) | 1/1 | 0 |
| tiered5 n=20 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=0 rho=0.0 m=all pr_gated | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.011 (38) | 0.081 (38) | 0.009 (38) | 19/19 | 0 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.001 (38) | 0.019 (38) | 0.002 (38) | 15/15 | 0 |
| tiered3 n=8 D=0 rho=0.0 m=all pr_gated | 0.019 (85) | 0.110 (85) | 0.017 (85) | 0.070 (191) | 0.365 (191) | 0.072 (191) | 15/15 | 0 |
| flat n=12 D=0 rho=0.0 m=all pr_gated | 0.000 (0) | 0.016 (38) | 0.000 (38) | 0.032 (76) | 0.203 (76) | 0.020 (76) | 18/18 | 0 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.005 (38) | 0.162 (38) | 0.001 (38) | 17/17 | 0 |
| tiered3 n=12 D=0 rho=0.0 m=all pr_gated | 0.000 (27) | 0.000 (0) | 0.000 (27) | 0.042 (76) | 0.327 (76) | 0.032 (76) | 19/19 | 0 |

## Oracle coverage (independent UCS, src/ahg/oracle.py)

| cell | instances checked | states checked |
|---|---|---|
| flat n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| flat n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| flat n=8 D=0 rho=0.25 m=all | 1/1 | 21 |
| flat n=8 D=0 rho=0.5 m=1 | 1/1 | 21 |
| flat n=8 D=0 rho=0.5 m=all | 1/1 | 21 |
| flat n=8 D=0 rho=1.0 m=1 | 1/1 | 21 |
| flat n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=1 rho=0.0 m=all | 0/0 | 0 |
| flat n=8 D=1 rho=0.25 m=1 | 0/0 | 0 |
| flat n=8 D=1 rho=0.25 m=all | 0/0 | 0 |
| flat n=8 D=1 rho=0.5 m=1 | 0/0 | 0 |
| flat n=8 D=1 rho=0.5 m=all | 0/0 | 0 |
| flat n=8 D=1 rho=1.0 m=1 | 0/0 | 0 |
| flat n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=2 rho=0.0 m=all | 0/0 | 0 |
| flat n=8 D=2 rho=0.25 m=1 | 0/0 | 0 |
| flat n=8 D=2 rho=0.25 m=all | 0/0 | 0 |
| flat n=8 D=2 rho=0.5 m=1 | 0/0 | 0 |
| flat n=8 D=2 rho=0.5 m=all | 0/0 | 0 |
| flat n=8 D=2 rho=1.0 m=1 | 0/0 | 0 |
| flat n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=3 rho=0.0 m=all | 0/0 | 0 |
| flat n=8 D=3 rho=0.25 m=1 | 0/0 | 0 |
| flat n=8 D=3 rho=0.25 m=all | 0/0 | 0 |
| flat n=8 D=3 rho=0.5 m=1 | 0/0 | 0 |
| flat n=8 D=3 rho=0.5 m=all | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=1 | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=8 D=0 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=8 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=8 D=0 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=8 D=0 rho=1.0 m=1 | 1/1 | 21 |
| tiered3 n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=1 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=8 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=8 D=1 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=8 D=1 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=8 D=1 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=8 D=1 rho=1.0 m=1 | 1/1 | 21 |
| tiered3 n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=1 | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=1 | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=1 | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=all | 0/0 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.5 m=all | 1/1 | 21 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.0 m=all | 1/1 | 18 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 1/1 | 18 |
| tiered5 n=8 D=1 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=1 | 1/1 | 18 |
| tiered5 n=8 D=1 rho=0.5 m=all | 1/1 | 17 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 1/1 | 18 |
| tiered5 n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| flat n=12 D=0 rho=0.0 m=all | 1/1 | 21 |
| flat n=12 D=0 rho=0.25 m=1 | 1/1 | 21 |
| flat n=12 D=0 rho=0.25 m=all | 1/1 | 21 |
| flat n=12 D=0 rho=0.5 m=1 | 1/1 | 21 |
| flat n=12 D=0 rho=0.5 m=all | 1/1 | 21 |
| flat n=12 D=0 rho=1.0 m=1 | 1/1 | 21 |
| flat n=12 D=0 rho=1.0 m=all | 1/1 | 21 |
| flat n=12 D=1 rho=0.0 m=all | 1/1 | 21 |
| flat n=12 D=1 rho=0.25 m=1 | 1/1 | 21 |
| flat n=12 D=1 rho=0.25 m=all | 1/1 | 21 |
| flat n=12 D=1 rho=0.5 m=1 | 1/1 | 21 |
| flat n=12 D=1 rho=0.5 m=all | 1/1 | 21 |
| flat n=12 D=1 rho=1.0 m=1 | 1/1 | 21 |
| flat n=12 D=1 rho=1.0 m=all | 1/1 | 21 |
| flat n=12 D=2 rho=0.0 m=all | 1/1 | 21 |
| flat n=12 D=2 rho=0.25 m=1 | 1/1 | 21 |
| flat n=12 D=2 rho=0.25 m=all | 1/1 | 21 |
| flat n=12 D=2 rho=0.5 m=1 | 1/1 | 21 |
| flat n=12 D=2 rho=0.5 m=all | 1/1 | 21 |
| flat n=12 D=2 rho=1.0 m=1 | 1/1 | 21 |
| flat n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| flat n=12 D=3 rho=0.0 m=all | 0/0 | 0 |
| flat n=12 D=3 rho=0.25 m=1 | 0/0 | 0 |
| flat n=12 D=3 rho=0.25 m=all | 0/0 | 0 |
| flat n=12 D=3 rho=0.5 m=1 | 0/0 | 0 |
| flat n=12 D=3 rho=0.5 m=all | 0/0 | 0 |
| flat n=12 D=3 rho=1.0 m=1 | 0/0 | 0 |
| flat n=12 D=3 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 1/1 | 21 |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 1/1 | 21 |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 1/1 | 21 |
| hub_and_spoke n=12 D=1 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=1 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=12 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=12 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=12 D=0 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=12 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=12 D=0 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=12 D=0 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=0 rho=1.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=1 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=12 D=1 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=12 D=1 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=12 D=1 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=12 D=1 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=1 rho=1.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=2 rho=0.0 m=all | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=1 | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.0 m=all | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=1 | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=1 | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=all | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=12 D=1 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=12 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=12 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=12 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=12 D=3 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=12 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=12 D=3 rho=1.0 m=all | 0/0 | 0 |
| flat n=20 D=0 rho=0.0 m=all | 1/1 | 1 |
| flat n=20 D=0 rho=0.25 m=1 | 1/1 | 1 |
| flat n=20 D=0 rho=0.25 m=all | 1/1 | 1 |
| flat n=20 D=0 rho=0.5 m=1 | 1/1 | 1 |
| flat n=20 D=0 rho=0.5 m=all | 1/1 | 1 |
| flat n=20 D=0 rho=1.0 m=1 | 1/1 | 1 |
| flat n=20 D=0 rho=1.0 m=all | 1/1 | 1 |
| flat n=20 D=1 rho=0.0 m=all | 1/1 | 1 |
| flat n=20 D=1 rho=0.25 m=1 | 1/1 | 1 |
| flat n=20 D=1 rho=0.25 m=all | 1/1 | 1 |
| flat n=20 D=1 rho=0.5 m=1 | 1/1 | 1 |
| flat n=20 D=1 rho=0.5 m=all | 1/1 | 1 |
| flat n=20 D=1 rho=1.0 m=1 | 1/1 | 1 |
| flat n=20 D=1 rho=1.0 m=all | 1/1 | 1 |
| flat n=20 D=2 rho=0.0 m=all | 1/1 | 1 |
| flat n=20 D=2 rho=0.25 m=1 | 1/1 | 1 |
| flat n=20 D=2 rho=0.25 m=all | 1/1 | 1 |
| flat n=20 D=2 rho=0.5 m=1 | 1/1 | 1 |
| flat n=20 D=2 rho=0.5 m=all | 1/1 | 1 |
| flat n=20 D=2 rho=1.0 m=1 | 1/1 | 1 |
| flat n=20 D=2 rho=1.0 m=all | 1/1 | 1 |
| flat n=20 D=3 rho=0.0 m=all | 1/1 | 1 |
| flat n=20 D=3 rho=0.25 m=1 | 1/1 | 1 |
| flat n=20 D=3 rho=0.25 m=all | 1/1 | 1 |
| flat n=20 D=3 rho=0.5 m=1 | 1/1 | 1 |
| flat n=20 D=3 rho=0.5 m=all | 1/1 | 1 |
| flat n=20 D=3 rho=1.0 m=1 | 1/1 | 1 |
| flat n=20 D=3 rho=1.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 1/1 | 1 |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 1/1 | 21 |
| tiered3 n=20 D=0 rho=0.0 m=all | 1/1 | 1 |
| tiered3 n=20 D=0 rho=0.25 m=1 | 1/1 | 1 |
| tiered3 n=20 D=0 rho=0.25 m=all | 1/1 | 1 |
| tiered3 n=20 D=0 rho=0.5 m=1 | 1/1 | 1 |
| tiered3 n=20 D=0 rho=0.5 m=all | 1/1 | 1 |
| tiered3 n=20 D=0 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=20 D=0 rho=1.0 m=all | 1/1 | 1 |
| tiered3 n=20 D=1 rho=0.0 m=all | 1/1 | 1 |
| tiered3 n=20 D=1 rho=0.25 m=1 | 1/1 | 1 |
| tiered3 n=20 D=1 rho=0.25 m=all | 1/1 | 1 |
| tiered3 n=20 D=1 rho=0.5 m=1 | 1/1 | 1 |
| tiered3 n=20 D=1 rho=0.5 m=all | 1/1 | 1 |
| tiered3 n=20 D=1 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=20 D=1 rho=1.0 m=all | 1/1 | 21 |
| tiered3 n=20 D=2 rho=0.0 m=all | 1/1 | 1 |
| tiered3 n=20 D=2 rho=0.25 m=1 | 1/1 | 1 |
| tiered3 n=20 D=2 rho=0.25 m=all | 1/1 | 1 |
| tiered3 n=20 D=2 rho=0.5 m=1 | 1/1 | 1 |
| tiered3 n=20 D=2 rho=0.5 m=all | 1/1 | 1 |
| tiered3 n=20 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=20 D=2 rho=1.0 m=all | 1/1 | 21 |
| tiered3 n=20 D=3 rho=0.0 m=all | 1/1 | 1 |
| tiered3 n=20 D=3 rho=0.25 m=1 | 1/1 | 1 |
| tiered3 n=20 D=3 rho=0.25 m=all | 1/1 | 1 |
| tiered3 n=20 D=3 rho=0.5 m=1 | 1/1 | 1 |
| tiered3 n=20 D=3 rho=0.5 m=all | 1/1 | 1 |
| tiered3 n=20 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=20 D=3 rho=1.0 m=all | 1/1 | 21 |
| tiered5 n=20 D=0 rho=0.0 m=all | 1/1 | 1 |
| tiered5 n=20 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=20 D=0 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=20 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=20 D=0 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=1 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=20 D=3 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=20 D=3 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=20 D=3 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=20 D=3 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=3 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=0 rho=0.0 m=all pr_gated | 19/19 | 399 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated | 15/15 | 315 |
| tiered3 n=8 D=0 rho=0.0 m=all pr_gated | 15/15 | 304 |
| flat n=12 D=0 rho=0.0 m=all pr_gated | 18/18 | 378 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated | 17/17 | 357 |
| tiered3 n=12 D=0 rho=0.0 m=all pr_gated | 19/19 | 399 |

Per instance, `raw.json` lists every oracle-checked state as [state, oracle h*, reference h*].

## Time per instance (s, wall-clock in a worker; diagnostic)

| cell | median | max | total |
|---|---|---|---|
| flat n=8 D=0 rho=0.0 m=all | 0.09 | 0.09 | 0.1 |
| flat n=8 D=0 rho=0.25 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=0.25 m=all | 0.05 | 0.05 | 0.1 |
| flat n=8 D=0 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=0.5 m=all | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=1.0 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=1.0 m=all | — | — | — |
| flat n=8 D=1 rho=0.0 m=all | — | — | — |
| flat n=8 D=1 rho=0.25 m=1 | — | — | — |
| flat n=8 D=1 rho=0.25 m=all | — | — | — |
| flat n=8 D=1 rho=0.5 m=1 | — | — | — |
| flat n=8 D=1 rho=0.5 m=all | — | — | — |
| flat n=8 D=1 rho=1.0 m=1 | — | — | — |
| flat n=8 D=1 rho=1.0 m=all | — | — | — |
| flat n=8 D=2 rho=0.0 m=all | — | — | — |
| flat n=8 D=2 rho=0.25 m=1 | — | — | — |
| flat n=8 D=2 rho=0.25 m=all | — | — | — |
| flat n=8 D=2 rho=0.5 m=1 | — | — | — |
| flat n=8 D=2 rho=0.5 m=all | — | — | — |
| flat n=8 D=2 rho=1.0 m=1 | — | — | — |
| flat n=8 D=2 rho=1.0 m=all | — | — | — |
| flat n=8 D=3 rho=0.0 m=all | — | — | — |
| flat n=8 D=3 rho=0.25 m=1 | — | — | — |
| flat n=8 D=3 rho=0.25 m=all | — | — | — |
| flat n=8 D=3 rho=0.5 m=1 | — | — | — |
| flat n=8 D=3 rho=0.5 m=all | — | — | — |
| flat n=8 D=3 rho=1.0 m=1 | — | — | — |
| flat n=8 D=3 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 0.04 | 0.04 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 0.03 | 0.03 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 0.04 | 0.04 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=3 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=0 rho=0.0 m=all | 0.05 | 0.05 | 0.1 |
| tiered3 n=8 D=0 rho=0.25 m=1 | 0.05 | 0.05 | 0.1 |
| tiered3 n=8 D=0 rho=0.25 m=all | 0.04 | 0.04 | 0.0 |
| tiered3 n=8 D=0 rho=0.5 m=1 | 0.04 | 0.04 | 0.0 |
| tiered3 n=8 D=0 rho=0.5 m=all | 0.05 | 0.05 | 0.1 |
| tiered3 n=8 D=0 rho=1.0 m=1 | 0.05 | 0.05 | 0.0 |
| tiered3 n=8 D=0 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=1 rho=0.0 m=all | 0.06 | 0.06 | 0.1 |
| tiered3 n=8 D=1 rho=0.25 m=1 | 0.06 | 0.06 | 0.1 |
| tiered3 n=8 D=1 rho=0.25 m=all | 0.06 | 0.06 | 0.1 |
| tiered3 n=8 D=1 rho=0.5 m=1 | 0.05 | 0.05 | 0.1 |
| tiered3 n=8 D=1 rho=0.5 m=all | 0.04 | 0.04 | 0.0 |
| tiered3 n=8 D=1 rho=1.0 m=1 | 0.05 | 0.05 | 0.0 |
| tiered3 n=8 D=1 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=2 rho=0.0 m=all | — | — | — |
| tiered3 n=8 D=2 rho=0.25 m=1 | — | — | — |
| tiered3 n=8 D=2 rho=0.25 m=all | — | — | — |
| tiered3 n=8 D=2 rho=0.5 m=1 | — | — | — |
| tiered3 n=8 D=2 rho=0.5 m=all | — | — | — |
| tiered3 n=8 D=2 rho=1.0 m=1 | — | — | — |
| tiered3 n=8 D=2 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=3 rho=0.0 m=all | — | — | — |
| tiered3 n=8 D=3 rho=0.25 m=1 | — | — | — |
| tiered3 n=8 D=3 rho=0.25 m=all | — | — | — |
| tiered3 n=8 D=3 rho=0.5 m=1 | — | — | — |
| tiered3 n=8 D=3 rho=0.5 m=all | — | — | — |
| tiered3 n=8 D=3 rho=1.0 m=1 | — | — | — |
| tiered3 n=8 D=3 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=0 rho=0.0 m=all | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=0 rho=0.5 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=0 rho=0.5 m=all | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=1 rho=0.0 m=all | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=1 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=1 rho=0.5 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=1 rho=0.5 m=all | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=1 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=2 rho=0.0 m=all | — | — | — |
| tiered5 n=8 D=2 rho=0.25 m=1 | — | — | — |
| tiered5 n=8 D=2 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=2 rho=0.5 m=1 | — | — | — |
| tiered5 n=8 D=2 rho=0.5 m=all | — | — | — |
| tiered5 n=8 D=2 rho=1.0 m=1 | — | — | — |
| tiered5 n=8 D=2 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=3 rho=0.0 m=all | — | — | — |
| tiered5 n=8 D=3 rho=0.25 m=1 | — | — | — |
| tiered5 n=8 D=3 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=3 rho=0.5 m=1 | — | — | — |
| tiered5 n=8 D=3 rho=0.5 m=all | — | — | — |
| tiered5 n=8 D=3 rho=1.0 m=1 | — | — | — |
| tiered5 n=8 D=3 rho=1.0 m=all | — | — | — |
| flat n=12 D=0 rho=0.0 m=all | 0.59 | 0.59 | 0.6 |
| flat n=12 D=0 rho=0.25 m=1 | 0.39 | 0.39 | 0.4 |
| flat n=12 D=0 rho=0.25 m=all | 0.42 | 0.42 | 0.4 |
| flat n=12 D=0 rho=0.5 m=1 | 0.51 | 0.51 | 0.5 |
| flat n=12 D=0 rho=0.5 m=all | 0.38 | 0.38 | 0.4 |
| flat n=12 D=0 rho=1.0 m=1 | 0.42 | 0.42 | 0.4 |
| flat n=12 D=0 rho=1.0 m=all | 0.19 | 0.19 | 0.2 |
| flat n=12 D=1 rho=0.0 m=all | 0.52 | 0.52 | 0.5 |
| flat n=12 D=1 rho=0.25 m=1 | 0.40 | 0.40 | 0.4 |
| flat n=12 D=1 rho=0.25 m=all | 0.36 | 0.36 | 0.4 |
| flat n=12 D=1 rho=0.5 m=1 | 0.46 | 0.46 | 0.5 |
| flat n=12 D=1 rho=0.5 m=all | 0.36 | 0.36 | 0.4 |
| flat n=12 D=1 rho=1.0 m=1 | 0.39 | 0.39 | 0.4 |
| flat n=12 D=1 rho=1.0 m=all | 0.22 | 0.22 | 0.2 |
| flat n=12 D=2 rho=0.0 m=all | 0.95 | 0.95 | 1.0 |
| flat n=12 D=2 rho=0.25 m=1 | 0.79 | 0.79 | 0.8 |
| flat n=12 D=2 rho=0.25 m=all | 0.89 | 0.89 | 0.9 |
| flat n=12 D=2 rho=0.5 m=1 | 1.00 | 1.00 | 1.0 |
| flat n=12 D=2 rho=0.5 m=all | 0.68 | 0.68 | 0.7 |
| flat n=12 D=2 rho=1.0 m=1 | 0.79 | 0.79 | 0.8 |
| flat n=12 D=2 rho=1.0 m=all | — | — | — |
| flat n=12 D=3 rho=0.0 m=all | — | — | — |
| flat n=12 D=3 rho=0.25 m=1 | — | — | — |
| flat n=12 D=3 rho=0.25 m=all | — | — | — |
| flat n=12 D=3 rho=0.5 m=1 | — | — | — |
| flat n=12 D=3 rho=0.5 m=all | — | — | — |
| flat n=12 D=3 rho=1.0 m=1 | — | — | — |
| flat n=12 D=3 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 0.19 | 0.19 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 0.28 | 0.28 | 0.3 |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 0.20 | 0.20 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 0.24 | 0.24 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 0.23 | 0.23 | 0.2 |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 0.24 | 0.24 | 0.2 |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 0.34 | 0.34 | 0.3 |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 0.23 | 0.23 | 0.2 |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 0.20 | 0.20 | 0.2 |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 0.20 | 0.20 | 0.2 |
| hub_and_spoke n=12 D=1 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=12 D=1 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=12 D=2 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=12 D=2 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=12 D=2 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=12 D=2 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=12 D=2 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=12 D=2 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=12 D=2 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=12 D=3 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=12 D=3 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=12 D=3 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=12 D=3 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=12 D=3 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=12 D=3 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=12 D=3 rho=1.0 m=all | — | — | — |
| tiered3 n=12 D=0 rho=0.0 m=all | 0.43 | 0.43 | 0.4 |
| tiered3 n=12 D=0 rho=0.25 m=1 | 0.23 | 0.23 | 0.2 |
| tiered3 n=12 D=0 rho=0.25 m=all | 0.26 | 0.26 | 0.3 |
| tiered3 n=12 D=0 rho=0.5 m=1 | 0.15 | 0.15 | 0.2 |
| tiered3 n=12 D=0 rho=0.5 m=all | 0.28 | 0.28 | 0.3 |
| tiered3 n=12 D=0 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=0 rho=1.0 m=all | 0.12 | 0.12 | 0.1 |
| tiered3 n=12 D=1 rho=0.0 m=all | 0.51 | 0.51 | 0.5 |
| tiered3 n=12 D=1 rho=0.25 m=1 | 0.21 | 0.21 | 0.2 |
| tiered3 n=12 D=1 rho=0.25 m=all | 0.47 | 0.47 | 0.5 |
| tiered3 n=12 D=1 rho=0.5 m=1 | 0.20 | 0.20 | 0.2 |
| tiered3 n=12 D=1 rho=0.5 m=all | 0.28 | 0.28 | 0.3 |
| tiered3 n=12 D=1 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=1 rho=1.0 m=all | 0.14 | 0.14 | 0.1 |
| tiered3 n=12 D=2 rho=0.0 m=all | — | — | — |
| tiered3 n=12 D=2 rho=0.25 m=1 | — | — | — |
| tiered3 n=12 D=2 rho=0.25 m=all | — | — | — |
| tiered3 n=12 D=2 rho=0.5 m=1 | — | — | — |
| tiered3 n=12 D=2 rho=0.5 m=all | — | — | — |
| tiered3 n=12 D=2 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=2 rho=1.0 m=all | — | — | — |
| tiered3 n=12 D=3 rho=0.0 m=all | — | — | — |
| tiered3 n=12 D=3 rho=0.25 m=1 | — | — | — |
| tiered3 n=12 D=3 rho=0.25 m=all | — | — | — |
| tiered3 n=12 D=3 rho=0.5 m=1 | — | — | — |
| tiered3 n=12 D=3 rho=0.5 m=all | — | — | — |
| tiered3 n=12 D=3 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=3 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=0 rho=0.0 m=all | 0.12 | 0.12 | 0.1 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 0.08 | 0.08 | 0.1 |
| tiered5 n=12 D=0 rho=0.25 m=all | 0.12 | 0.12 | 0.1 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| tiered5 n=12 D=0 rho=0.5 m=all | — | — | — |
| tiered5 n=12 D=0 rho=1.0 m=1 | — | — | — |
| tiered5 n=12 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=1 rho=0.0 m=all | — | — | — |
| tiered5 n=12 D=1 rho=0.25 m=1 | — | — | — |
| tiered5 n=12 D=1 rho=0.25 m=all | — | — | — |
| tiered5 n=12 D=1 rho=0.5 m=1 | — | — | — |
| tiered5 n=12 D=1 rho=0.5 m=all | — | — | — |
| tiered5 n=12 D=1 rho=1.0 m=1 | — | — | — |
| tiered5 n=12 D=1 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=2 rho=0.0 m=all | — | — | — |
| tiered5 n=12 D=2 rho=0.25 m=1 | — | — | — |
| tiered5 n=12 D=2 rho=0.25 m=all | — | — | — |
| tiered5 n=12 D=2 rho=0.5 m=1 | — | — | — |
| tiered5 n=12 D=2 rho=0.5 m=all | — | — | — |
| tiered5 n=12 D=2 rho=1.0 m=1 | — | — | — |
| tiered5 n=12 D=2 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=3 rho=0.0 m=all | — | — | — |
| tiered5 n=12 D=3 rho=0.25 m=1 | — | — | — |
| tiered5 n=12 D=3 rho=0.25 m=all | — | — | — |
| tiered5 n=12 D=3 rho=0.5 m=1 | — | — | — |
| tiered5 n=12 D=3 rho=0.5 m=all | — | — | — |
| tiered5 n=12 D=3 rho=1.0 m=1 | — | — | — |
| tiered5 n=12 D=3 rho=1.0 m=all | — | — | — |
| flat n=20 D=0 rho=0.0 m=all | 3.42 | 3.42 | 3.4 |
| flat n=20 D=0 rho=0.25 m=1 | 4.53 | 4.53 | 4.5 |
| flat n=20 D=0 rho=0.25 m=all | 3.72 | 3.72 | 3.7 |
| flat n=20 D=0 rho=0.5 m=1 | 4.64 | 4.64 | 4.6 |
| flat n=20 D=0 rho=0.5 m=all | 3.91 | 3.91 | 3.9 |
| flat n=20 D=0 rho=1.0 m=1 | 4.39 | 4.39 | 4.4 |
| flat n=20 D=0 rho=1.0 m=all | 6.91 | 6.91 | 6.9 |
| flat n=20 D=1 rho=0.0 m=all | 4.68 | 4.68 | 4.7 |
| flat n=20 D=1 rho=0.25 m=1 | 5.09 | 5.09 | 5.1 |
| flat n=20 D=1 rho=0.25 m=all | 4.54 | 4.54 | 4.5 |
| flat n=20 D=1 rho=0.5 m=1 | 5.40 | 5.40 | 5.4 |
| flat n=20 D=1 rho=0.5 m=all | 4.81 | 4.81 | 4.8 |
| flat n=20 D=1 rho=1.0 m=1 | 5.35 | 5.35 | 5.4 |
| flat n=20 D=1 rho=1.0 m=all | 7.64 | 7.64 | 7.6 |
| flat n=20 D=2 rho=0.0 m=all | 6.46 | 6.46 | 6.5 |
| flat n=20 D=2 rho=0.25 m=1 | 10.28 | 10.28 | 10.3 |
| flat n=20 D=2 rho=0.25 m=all | 6.54 | 6.54 | 6.5 |
| flat n=20 D=2 rho=0.5 m=1 | 7.28 | 7.28 | 7.3 |
| flat n=20 D=2 rho=0.5 m=all | 6.21 | 6.21 | 6.2 |
| flat n=20 D=2 rho=1.0 m=1 | 6.76 | 6.76 | 6.8 |
| flat n=20 D=2 rho=1.0 m=all | 11.59 | 11.59 | 11.6 |
| flat n=20 D=3 rho=0.0 m=all | 11.05 | 11.05 | 11.1 |
| flat n=20 D=3 rho=0.25 m=1 | 11.28 | 11.28 | 11.3 |
| flat n=20 D=3 rho=0.25 m=all | 9.92 | 9.92 | 9.9 |
| flat n=20 D=3 rho=0.5 m=1 | 10.72 | 10.72 | 10.7 |
| flat n=20 D=3 rho=0.5 m=all | 10.67 | 10.67 | 10.7 |
| flat n=20 D=3 rho=1.0 m=1 | 10.35 | 10.35 | 10.3 |
| flat n=20 D=3 rho=1.0 m=all | 10.74 | 10.74 | 10.7 |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 1.09 | 1.09 | 1.1 |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 1.11 | 1.11 | 1.1 |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 1.50 | 1.50 | 1.5 |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 1.17 | 1.17 | 1.2 |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 1.15 | 1.15 | 1.2 |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 1.78 | 1.78 | 1.8 |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 1.40 | 1.40 | 1.4 |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 1.44 | 1.44 | 1.4 |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 2.05 | 2.05 | 2.1 |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 1.45 | 1.45 | 1.4 |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 1.35 | 1.35 | 1.3 |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 2.56 | 2.56 | 2.6 |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 1.66 | 1.66 | 1.7 |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 1.67 | 1.67 | 1.7 |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 2.01 | 2.01 | 2.0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 1.71 | 1.71 | 1.7 |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 1.63 | 1.63 | 1.6 |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 2.38 | 2.38 | 2.4 |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 1.75 | 1.75 | 1.8 |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 1.77 | 1.77 | 1.8 |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 2.39 | 2.39 | 2.4 |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 1.81 | 1.81 | 1.8 |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 1.75 | 1.75 | 1.8 |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 9.95 | 9.95 | 10.0 |
| tiered3 n=20 D=0 rho=0.0 m=all | 2.36 | 2.36 | 2.4 |
| tiered3 n=20 D=0 rho=0.25 m=1 | 2.49 | 2.49 | 2.5 |
| tiered3 n=20 D=0 rho=0.25 m=all | 2.47 | 2.47 | 2.5 |
| tiered3 n=20 D=0 rho=0.5 m=1 | 2.44 | 2.44 | 2.4 |
| tiered3 n=20 D=0 rho=0.5 m=all | 2.75 | 2.75 | 2.7 |
| tiered3 n=20 D=0 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=0 rho=1.0 m=all | 4.59 | 4.59 | 4.6 |
| tiered3 n=20 D=1 rho=0.0 m=all | 3.08 | 3.08 | 3.1 |
| tiered3 n=20 D=1 rho=0.25 m=1 | 2.98 | 2.98 | 3.0 |
| tiered3 n=20 D=1 rho=0.25 m=all | 3.13 | 3.13 | 3.1 |
| tiered3 n=20 D=1 rho=0.5 m=1 | 2.83 | 2.83 | 2.8 |
| tiered3 n=20 D=1 rho=0.5 m=all | 3.19 | 3.19 | 3.2 |
| tiered3 n=20 D=1 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=1 rho=1.0 m=all | 13.77 | 13.77 | 13.8 |
| tiered3 n=20 D=2 rho=0.0 m=all | 2.92 | 2.92 | 2.9 |
| tiered3 n=20 D=2 rho=0.25 m=1 | 2.97 | 2.97 | 3.0 |
| tiered3 n=20 D=2 rho=0.25 m=all | 2.99 | 2.99 | 3.0 |
| tiered3 n=20 D=2 rho=0.5 m=1 | 2.71 | 2.71 | 2.7 |
| tiered3 n=20 D=2 rho=0.5 m=all | 3.00 | 3.00 | 3.0 |
| tiered3 n=20 D=2 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=2 rho=1.0 m=all | 8.97 | 8.97 | 9.0 |
| tiered3 n=20 D=3 rho=0.0 m=all | 4.12 | 4.12 | 4.1 |
| tiered3 n=20 D=3 rho=0.25 m=1 | 4.31 | 4.31 | 4.3 |
| tiered3 n=20 D=3 rho=0.25 m=all | 4.12 | 4.12 | 4.1 |
| tiered3 n=20 D=3 rho=0.5 m=1 | 3.88 | 3.88 | 3.9 |
| tiered3 n=20 D=3 rho=0.5 m=all | 5.01 | 5.01 | 5.0 |
| tiered3 n=20 D=3 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=3 rho=1.0 m=all | 13.68 | 13.68 | 13.7 |
| tiered5 n=20 D=0 rho=0.0 m=all | 4.06 | 4.06 | 4.1 |
| tiered5 n=20 D=0 rho=0.25 m=1 | 10.84 | 10.84 | 10.8 |
| tiered5 n=20 D=0 rho=0.25 m=all | 9.99 | 9.99 | 10.0 |
| tiered5 n=20 D=0 rho=0.5 m=1 | 6.36 | 6.36 | 6.4 |
| tiered5 n=20 D=0 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=0 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=1 rho=0.0 m=all | 12.93 | 12.93 | 12.9 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 11.12 | 11.12 | 11.1 |
| tiered5 n=20 D=1 rho=0.25 m=all | 8.69 | 8.69 | 8.7 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 6.23 | 6.23 | 6.2 |
| tiered5 n=20 D=1 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=1 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=1 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=2 rho=0.0 m=all | — | — | — |
| tiered5 n=20 D=2 rho=0.25 m=1 | — | — | — |
| tiered5 n=20 D=2 rho=0.25 m=all | — | — | — |
| tiered5 n=20 D=2 rho=0.5 m=1 | — | — | — |
| tiered5 n=20 D=2 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=2 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=2 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=3 rho=0.0 m=all | 9.31 | 9.31 | 9.3 |
| tiered5 n=20 D=3 rho=0.25 m=1 | 6.50 | 6.50 | 6.5 |
| tiered5 n=20 D=3 rho=0.25 m=all | 7.20 | 7.20 | 7.2 |
| tiered5 n=20 D=3 rho=0.5 m=1 | 4.76 | 4.76 | 4.8 |
| tiered5 n=20 D=3 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=3 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=3 rho=1.0 m=all | — | — | — |
| flat n=8 D=0 rho=0.0 m=all pr_gated | 0.17 | 0.48 | 4.1 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated | 0.09 | 0.17 | 1.4 |
| tiered3 n=8 D=0 rho=0.0 m=all pr_gated | 0.10 | 0.17 | 1.5 |
| flat n=12 D=0 rho=0.0 m=all pr_gated | 1.81 | 3.04 | 32.9 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated | 0.49 | 0.83 | 9.4 |
| tiered3 n=12 D=0 rho=0.0 m=all pr_gated | 0.76 | 1.47 | 14.5 |

## Unreachable goals and generation failures

- flat n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=0.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=0.25 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=0.25 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=0.5 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=0.5 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=0.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=0.25 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=0.5 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=0.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=0.25 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=0.5 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.25 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.25 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.25 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=0.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=0.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=0.5 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=0 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=1 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.5 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=0.0 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=0.25 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=0.5 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=3 rho=1.0 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=12 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=0 rho=1.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=1 rho=1.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=0.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=0.25 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=0.5 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=0.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=0.25 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=0.5 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=3 rho=1.0 m=all seed=0: unreachable — execCode(spoke-10) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=12 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=0.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=0.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=0.5 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=0.5 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=0.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=0.25 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=0.5 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=0.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=0.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=0.5 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=20 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=20 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-19) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=20 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-19) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=20 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-19) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=20 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-19) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=0 rho=0.5 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=1 rho=0.5 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=0.5 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=0 rho=0.0 m=all pr_gated seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated seed=12: unreachable — execCode(spoke-3) unreachable in {'family': 'hub_and_spoke', 'seed': 12, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated seed=14: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 14, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated seed=16: unreachable — execCode(spoke-8) unreachable in {'family': 'hub_and_spoke', 'seed': 16, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated seed=17: unreachable — execCode(spoke-2) unreachable in {'family': 'hub_and_spoke', 'seed': 17, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=0.0 m=all pr_gated seed=1: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 1, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=0.0 m=all pr_gated seed=5: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 5, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=0.0 m=all pr_gated seed=9: unreachable — execCode(tier2-7) unreachable in {'family': 'tiered', 'seed': 9, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=0.0 m=all pr_gated seed=11: unreachable — execCode(tier2-7) unreachable in {'family': 'tiered', 'seed': 11, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=0.0 m=all pr_gated seed=17: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 17, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=0 rho=0.0 m=all pr_gated seed=7: unreachable — execCode(lan-10) unreachable in {'family': 'flat', 'seed': 7, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=0 rho=0.0 m=all pr_gated seed=11: unreachable — execCode(lan-12) unreachable in {'family': 'flat', 'seed': 11, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated seed=16: unreachable — execCode(spoke-7) unreachable in {'family': 'hub_and_spoke', 'seed': 16, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated seed=17: unreachable — execCode(spoke-2) unreachable in {'family': 'hub_and_spoke', 'seed': 17, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated seed=18: unreachable — execCode(spoke-7) unreachable in {'family': 'hub_and_spoke', 'seed': 18, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=12 D=0 rho=0.0 m=all pr_gated seed=1: unreachable — execCode(tier2-9) unreachable in {'family': 'tiered', 'seed': 1, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
