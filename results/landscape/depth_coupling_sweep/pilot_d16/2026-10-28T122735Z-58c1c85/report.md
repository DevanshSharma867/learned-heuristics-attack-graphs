# depth_coupling_sweep/pilot_d16

Mode **pilot** — a pilot for timing and tooling, not a result (D15 §7).
D12 schema (pr_gated off) with the D15 knobs, depth knob in its D16 variant (internet-exposed hosts at level 0); anchor cells are pr_gated with knobs off. Init budget 200,000 expansions; per-state labelling budget 20,000, per-instance 2,000,000. Costs in D9 units (38 per effort unit).

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
| flat n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 14 / 5 / 5 | 0/1 | no | no |
| flat n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 12 / 5 / 5 | 0/1 | no | no |
| flat n=8 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 11 / 5 / 5 | 0/1 | no | no |
| flat n=8 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 12 / 5 / 5 | 0/1 | no | no |
| flat n=8 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.29 | 7 | 13 / 9 / 7 | 0/1 | no | no |
| flat n=8 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 7 / 6 / 6 | 0/1 | no | no |
| flat n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 14 / 6 / 6 | 0/1 | no | no |
| flat n=8 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 12 / 6 / 6 | 0/1 | no | no |
| flat n=8 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 9 / 6 / 6 | 0/1 | no | no |
| flat n=8 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 12 / 6 / 6 | 0/1 | no | no |
| flat n=8 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 13 / 9 / 8 | 0/1 | no | no |
| flat n=8 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 11 / 7 / 7 | 0/1 | no | no |
| flat n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 11 / 8 / 8 | 0/1 | no | no |
| flat n=8 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 13 / 8 / 7 | 0/1 | no | no |
| flat n=8 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 14 / 8 / 8 | 0/1 | no | no |
| flat n=8 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 13 / 8 / 7 | 0/1 | no | no |
| flat n=8 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 9 | 10 / 9 / 9 | 0/1 | no | no |
| flat n=8 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 18 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 11 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 11 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 23 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 16 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 16 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 6 | 26 / 8 / 6 | 0/1 | no | no |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 18 / 7 / 7 | 0/1 | no | no |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 18 / 7 / 7 | 0/1 | no | no |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 8 | 30 / 8 / 8 | 0/1 | no | no |
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
| tiered3 n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 38 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 43 / 8 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 34 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 38 / 8 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 24 / 6 / 6 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 29 / 8 / 7 | 0/1 | no | no |
| tiered3 n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 44 / 7 / 7 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 43 / 9 / 8 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 40 / 8 / 7 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 35 / 9 / 8 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 25 / 7 / 7 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 31 / 9 / 8 | 0/1 | no | no |
| tiered3 n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=8 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 43 / 9 / 8 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.22 | 9 | 38 / 11 / 9 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.22 | 9 | 42 / 11 / 9 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.22 | 9 | 30 / 11 / 9 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.18 | — | 2.27 | 11 | 28 / 25 / 13 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.22 | 9 | 30 / 11 / 9 | 0/1 | no | no |
| tiered3 n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 20 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 22 / 5 / 5 | 0/1 | no | no |
| tiered5 n=8 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 27 / 7 / 6 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 27 / 7 / 6 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 27 / 7 / 6 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 25 / 7 / 6 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 27 / 7 / 6 | 0/1 | no | no |
| tiered5 n=8 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 23 / 8 / 7 | 0/1 | no | no |
| tiered5 n=8 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 23 / 8 / 7 | 0/1 | no | no |
| tiered5 n=8 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 23 / 8 / 7 | 0/1 | no | no |
| tiered5 n=8 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 21 / 8 / 7 | 0/1 | no | no |
| tiered5 n=8 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 23 / 8 / 7 | 0/1 | no | no |
| tiered5 n=8 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 27 / 10 / 8 | 0/1 | no | no |
| tiered5 n=8 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 27 / 10 / 8 | 0/1 | no | no |
| tiered5 n=8 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=8 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 27 / 10 / 8 | 0/1 | no | no |
| tiered5 n=8 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 23 / 9 / 8 | 0/1 | no | no |
| tiered5 n=8 D=3 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 27 / 10 / 8 | 0/1 | no | no |
| tiered5 n=8 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 18 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 5 / 3 / 3 | 0/1 | no | no |
| flat n=12 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 9 / 6 / 6 | 0/1 | no | no |
| flat n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 14 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 14 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 10 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 10 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 27 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 10 / 4 / 4 | 0/1 | no | no |
| flat n=12 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.14 | 7 | 13 / 8 / 7 | 0/1 | no | no |
| flat n=12 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.50 | 6 | 26 / 9 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.67 | 6 | 28 / 10 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 6 | 23 / 6 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 57 / 7 / 6 | 0/1 | no | no |
| flat n=12 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 2.40 | — | 2.80 | 5 | 61 / 14 / 12 | 0/1 | no | no |
| flat n=12 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| flat n=12 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 19 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 19 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 14 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 19 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 29 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 19 / 7 / 7 | 0/1 | no | no |
| flat n=12 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 9 | 15 / 12 / 9 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 28 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 104 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 17 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 84 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 25 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 39 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 125 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 27 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 99 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 38 / 5 / 5 | 0/1 | no | no |
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
| tiered3 n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 74 / 6 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 49 / 6 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 48 / 6 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 38 / 6 / 5 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.44 | 9 | 63 / 13 / 9 | 0/1 | no | no |
| tiered3 n=12 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.09 | 11 | 32 / 12 / 11 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 83 / 10 / 7 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 56 / 10 / 7 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 50 / 10 / 7 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.17 | 6 | 27 / 7 / 6 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.89 | 9 | 60 / 17 / 9 | 0/1 | no | no |
| tiered3 n=12 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.38 | 8 | 99 / 11 / 8 | 0/1 | no | no |
| tiered3 n=12 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.38 | 8 | 63 / 11 / 8 | 0/1 | no | no |
| tiered3 n=12 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 65 / 9 / 8 | 0/1 | no | no |
| tiered3 n=12 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.33 | 9 | 109 / 21 / 9 | 0/1 | no | no |
| tiered3 n=12 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.45 | 11 | 66 / 16 / 11 | 0/1 | no | no |
| tiered3 n=12 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=12 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 68 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 33 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 68 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 25 / 7 / 7 | 0/1 | no | no |
| tiered5 n=12 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=12 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 75 / 9 / 8 | 0/1 | no | no |
| tiered5 n=12 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 40 / 9 / 8 | 0/1 | no | no |
| tiered5 n=12 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 75 / 9 / 8 | 0/1 | no | no |
| tiered5 n=12 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 32 / 9 / 8 | 0/1 | no | no |
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
| flat n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.25 | — | 2.00 | 4 | 1712 / 8 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.50 | 4 | 1143 / 6 / 4 | 0/1 | no | no |
| flat n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.67 | 3 | 1886 / 5 / 3 | 0/1 | no | no |
| flat n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 3.33 | 3 | 3037 / 10 / 3 | 0/1 | no | no |
| flat n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.25 | — | 1.75 | 4 | 951 / 7 / 5 | 0/1 | no | no |
| flat n=20 D=1 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.00 | 4 | 2336 / 8 / 4 | 0/1 | no | no |
| flat n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 5.67 | 6 | 2038 / 34 / 6 | 0/1 | no | no |
| flat n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.20 | — | 2.00 | 5 | 3232 / 10 / 6 | 0/1 | no | no |
| flat n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 2223 / 6 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.14 | — | 2.71 | 7 | 4816 / 19 / 8 | 0/1 | no | no |
| flat n=20 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.80 | — | 4.00 | 5 | 5973 / 20 / 9 | 0/1 | no | no |
| flat n=20 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.60 | 5 | 1579 / 8 / 5 | 0/1 | no | no |
| flat n=20 D=2 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.80 | — | 2.20 | 5 | 4377 / 11 / 9 | 0/1 | no | no |
| flat n=20 D=2 rho=1.0 m=all | 1/1 | 0 | 0 | 1.29 | — | 5.57 | 7 | 2746 / 39 / 9 | 0/1 | no | no |
| flat n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.43 | — | 1.86 | 7 | 3478 / 13 / 10 | 0/1 | no | no |
| flat n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.43 | 7 | 2906 / 10 / 7 | 0/1 | no | no |
| flat n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.50 | 8 | 3235 / 12 / 8 | 0/1 | no | no |
| flat n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 5947 / 7 / 7 | 0/1 | no | no |
| flat n=20 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.14 | — | 1.57 | 7 | 2548 / 11 / 8 | 0/1 | no | no |
| flat n=20 D=3 rho=1.0 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 7 | 5463 / 7 / 7 | 0/1 | no | no |
| flat n=20 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 2.80 | — | 4.80 | 10 | 3743 / 48 / 28 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 10 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 9 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 485 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 7 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 17 / 3 / 3 | 0/1 | no | no |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 5 | 177 / 5 / 5 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 54 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 54 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.00 | 4 | 903 / 8 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 37 / 4 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 57 / 5 / 4 | 0/1 | no | no |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 6 | 388 / 8 / 6 | 0/1 | no | no |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 904 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 717 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 735 / 5 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 4 | 359 / 4 / 4 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.00 | 3 | 529 / 3 / 3 | 0/1 | no | no |
| tiered3 n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=0 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.86 | 7 | 238 / 13 / 7 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.20 | 5 | 1105 / 11 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.20 | 5 | 870 / 11 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.80 | 5 | 913 / 14 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.60 | 5 | 474 / 8 / 5 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 4 | 731 / 5 / 4 | 0/1 | no | no |
| tiered3 n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=1 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 3.75 | 8 | 358 / 30 / 8 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.40 | 5 | 1244 / 12 / 5 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.80 | 5 | 874 / 9 / 5 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.40 | 5 | 1041 / 12 / 5 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.14 | 7 | 572 / 15 / 7 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=0.5 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.20 | 5 | 484 / 6 / 5 | 0/1 | no | no |
| tiered3 n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=2 rho=1.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.33 | 9 | 338 / 12 / 9 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 2136 / 9 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.12 | 8 | 1480 / 9 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 1769 / 10 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.25 | 8 | 837 / 10 / 8 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=0.5 m=all | 1/1 | 0 | 0 | 1.12 | — | 1.88 | 8 | 1948 / 15 / 9 | 0/1 | no | no |
| tiered3 n=20 D=3 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered3 n=20 D=3 rho=1.0 m=all | 1/1 | 0 | 0 | 3.75 | — | 9.83 | 12 | 1115 / 118 / 45 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.33 | 9 | 8210 / 21 / 9 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.67 | 9 | 4734 / 15 / 9 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 1.62 | 8 | 5470 / 13 / 8 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 2.90 | 10 | 2128 / 29 / 10 | 0/1 | no | no |
| tiered5 n=20 D=0 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=0 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=0 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.50 | 10 | 8441 / 25 / 10 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 1.90 | 10 | 4933 / 19 / 10 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.00 | 9 | 5681 / 18 / 9 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.5 m=1 | 1/1 | 0 | 0 | 1.00 | — | 3.55 | 11 | 2183 / 39 / 11 | 0/1 | no | no |
| tiered5 n=20 D=1 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=1 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.0 m=all | 1/1 | 0 | 0 | 1.00 | — | 6.00 | 10 | 2092 / 60 / 10 | 0/1 | no | no |
| tiered5 n=20 D=2 rho=0.25 m=1 | 1/1 | 0 | 0 | 1.00 | — | 6.00 | 10 | 1889 / 60 / 10 | 0/1 | no | no |
| tiered5 n=20 D=2 rho=0.25 m=all | 1/1 | 0 | 0 | 1.00 | — | 2.10 | 10 | 880 / 21 / 10 | 0/1 | no | no |
| tiered5 n=20 D=2 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=0.5 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=1.0 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=2 rho=1.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=0.0 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=0.25 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=0.25 m=all | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
| tiered5 n=20 D=3 rho=0.5 m=1 | 0/1 | 0 | 0 | — | — | — | — | — / — / — | 0/0 | no | no |
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
| flat n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.023 (38) | 0.000 (0) | 0.022 (38) | 1/1 | 0 |
| flat n=8 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.023 (38) | 0.000 (0) | 0.022 (38) | 1/1 | 0 |
| flat n=8 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.185 (76) | 0.000 (0) | 0.200 (76) | 1/1 | 0 |
| flat n=8 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.023 (38) | 0.000 (0) | 0.022 (38) | 1/1 | 0 |
| flat n=8 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.273 (245) | 0.778 (245) | 0.304 (245) | 1/1 | 0 |
| flat n=8 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.157 (76) | 0.500 (76) | 0.164 (76) | 1/1 | 0 |
| flat n=8 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.170 (76) | 0.500 (76) | 0.170 (76) | 1/1 | 0 |
| flat n=8 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.056 (38) | 0.333 (38) | 0.105 (38) | 1/1 | 0 |
| flat n=8 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.170 (76) | 0.500 (76) | 0.170 (76) | 1/1 | 0 |
| flat n=8 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.273 (175) | 0.778 (175) | 0.304 (175) | 1/1 | 0 |
| flat n=8 D=2 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.174 (38) | 0.714 (38) | 0.191 (38) | 1/1 | 0 |
| flat n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.208 (38) | 0.750 (38) | 0.231 (38) | 1/1 | 0 |
| flat n=8 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.217 (38) | 0.750 (38) | 0.231 (38) | 1/1 | 0 |
| flat n=8 D=3 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.217 (58) | 0.750 (58) | 0.250 (58) | 1/1 | 0 |
| flat n=8 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.217 (38) | 0.750 (38) | 0.231 (38) | 1/1 | 0 |
| flat n=8 D=3 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=8 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.026 (38) | 0.500 (38) | 0.051 (38) | 1/1 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.026 (38) | 0.500 (38) | 0.051 (38) | 1/1 | 0 |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.026 (38) | 0.400 (38) | 0.051 (38) | 1/1 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.143 (38) | 0.750 (38) | 0.163 (38) | 1/1 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
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
| tiered3 n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.153 (38) | 0.000 (0) | 0.123 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.25 m=1 | 0.016 (38) | 0.143 (38) | 0.015 (38) | 0.429 (76) | 0.750 (38) | 0.418 (76) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.158 (38) | 0.000 (0) | 0.130 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.5 m=1 | 0.019 (38) | 0.143 (38) | 0.018 (38) | 0.204 (38) | 0.500 (38) | 0.214 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.351 (76) | 0.000 (0) | 0.310 (76) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.190 (38) | 0.375 (38) | 0.205 (38) | 1/1 | 0 |
| tiered3 n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.020 (38) | 0.000 (0) | 0.014 (38) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=1 | 0.059 (38) | 0.250 (38) | 0.048 (38) | 0.333 (38) | 0.778 (38) | 0.365 (38) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.061 (38) | 0.125 (38) | 0.045 (38) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=1 | 0.047 (38) | 0.250 (38) | 0.041 (38) | 0.116 (38) | 0.556 (38) | 0.122 (38) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=0.5 m=all | 0.114 (38) | 0.000 (0) | 0.098 (38) | 0.229 (76) | 0.000 (0) | 0.195 (76) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.103 (38) | 0.333 (38) | 0.116 (38) | 1/1 | 0 |
| tiered3 n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.093 (38) | 0.111 (38) | 0.077 (38) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=1 | 0.024 (38) | 0.000 (0) | 0.018 (38) | 0.310 (38) | 0.364 (38) | 0.382 (76) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.308 (76) | 0.727 (76) | 0.254 (76) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.162 (38) | 0.364 (38) | 0.175 (38) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=0.5 m=all | 0.222 (38) | 0.538 (38) | 0.250 (38) | 0.778 (114) | 0.880 (152) | 0.786 (152) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.162 (38) | 0.364 (38) | 0.175 (38) | 1/1 | 0 |
| tiered3 n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=8 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.032 (38) | 0.143 (38) | 0.029 (38) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.032 (38) | 0.143 (38) | 0.029 (38) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.032 (38) | 0.143 (38) | 0.029 (38) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.031 (38) | 0.143 (38) | 0.030 (38) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.032 (38) | 0.143 (38) | 0.029 (38) | 1/1 | 0 |
| tiered5 n=8 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.038 (38) | 0.125 (38) | 0.032 (38) | 1/1 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.038 (38) | 0.125 (38) | 0.032 (38) | 1/1 | 0 |
| tiered5 n=8 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.038 (38) | 0.125 (38) | 0.032 (38) | 1/1 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.036 (38) | 0.125 (38) | 0.034 (38) | 1/1 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.038 (38) | 0.125 (38) | 0.032 (38) | 1/1 | 0 |
| tiered5 n=8 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.375 (76) | 0.600 (76) | 0.333 (76) | 1/1 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.375 (76) | 0.600 (76) | 0.333 (76) | 1/1 | 0 |
| tiered5 n=8 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.375 (76) | 0.600 (76) | 0.333 (76) | 1/1 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.320 (76) | 0.556 (76) | 0.333 (76) | 1/1 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.375 (76) | 0.600 (76) | 0.333 (76) | 1/1 | 0 |
| tiered5 n=8 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=0.5 m=all | 0.036 (81) | 0.000 (0) | 0.019 (81) | 0.048 (119) | 0.000 (0) | 0.025 (119) | 1/1 | 0 |
| flat n=12 D=0 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=0 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.167 (38) | 0.018 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.021 (38) | 0.500 (38) | 0.006 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.029 (38) | 0.500 (38) | 0.009 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.015 (38) | 0.500 (38) | 0.008 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.015 (38) | 0.500 (38) | 0.006 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=0.5 m=all | 0.041 (81) | 0.000 (0) | 0.018 (81) | 0.088 (119) | 0.500 (38) | 0.042 (119) | 1/1 | 0 |
| flat n=12 D=1 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.018 (38) | 0.500 (38) | 0.007 (38) | 1/1 | 0 |
| flat n=12 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.056 (38) | 0.500 (76) | 0.068 (76) | 1/1 | 0 |
| flat n=12 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.166 (114) | 0.667 (114) | 0.069 (114) | 1/1 | 0 |
| flat n=12 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.157 (175) | 0.800 (175) | 0.045 (175) | 1/1 | 0 |
| flat n=12 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.109 (38) | 0.333 (38) | 0.071 (38) | 1/1 | 0 |
| flat n=12 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.007 (38) | 0.286 (38) | 0.004 (38) | 1/1 | 0 |
| flat n=12 D=2 rho=0.5 m=all | 0.100 (124) | 0.833 (99) | 0.056 (124) | 0.186 (182) | 0.929 (207) | 0.109 (207) | 1/1 | 0 |
| flat n=12 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| flat n=12 D=3 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=3 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=3 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.080 (58) | 0.429 (20) | 0.052 (58) | 1/1 | 0 |
| flat n=12 D=3 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| flat n=12 D=3 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.191 (76) | 0.833 (114) | 0.192 (114) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.010 (38) | 0.500 (38) | 0.005 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.047 (38) | 0.600 (38) | 0.020 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.010 (38) | 0.500 (38) | 0.007 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.037 (38) | 0.600 (38) | 0.029 (38) | 1/1 | 0 |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.011 (38) | 0.400 (38) | 0.011 (38) | 1/1 | 0 |
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
| tiered3 n=12 D=1 rho=0.0 m=all | 0.021 (22) | 0.000 (0) | 0.013 (22) | 0.050 (38) | 0.500 (38) | 0.052 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.071 (38) | 0.500 (38) | 0.062 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.25 m=all | 0.040 (22) | 0.000 (0) | 0.018 (22) | 0.091 (38) | 0.500 (38) | 0.074 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.5 m=1 | 0.033 (22) | 0.000 (0) | 0.024 (22) | 0.133 (38) | 0.667 (38) | 0.121 (38) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.268 (76) | 0.615 (76) | 0.217 (76) | 1/1 | 0 |
| tiered3 n=12 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.345 (76) | 0.333 (76) | 0.333 (76) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.0 m=all | 0.017 (22) | 0.000 (0) | 0.006 (22) | 0.040 (38) | 0.300 (38) | 0.014 (38) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.056 (38) | 0.300 (38) | 0.045 (38) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.031 (38) | 0.300 (38) | 0.011 (38) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.056 (38) | 0.143 (38) | 0.030 (38) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.300 (114) | 0.824 (114) | 0.248 (114) | 1/1 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.0 m=all | 0.045 (22) | 0.000 (0) | 0.025 (22) | 0.545 (76) | 0.818 (76) | 0.310 (76) | 1/1 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.624 (76) | 0.818 (76) | 0.454 (76) | 1/1 | 0 |
| tiered3 n=12 D=3 rho=0.25 m=all | 0.034 (22) | 0.000 (0) | 0.024 (22) | 0.435 (76) | 0.778 (76) | 0.306 (76) | 1/1 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=1 | 0.026 (22) | 0.000 (0) | 0.021 (22) | 0.570 (152) | 0.905 (152) | 0.426 (152) | 1/1 | 0 |
| tiered3 n=12 D=3 rho=0.5 m=all | 0.008 (38) | 0.000 (0) | 0.004 (38) | 0.331 (76) | 0.750 (76) | 0.198 (76) | 1/1 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.254 (76) | 0.000 (0) | 0.278 (76) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.172 (76) | 0.000 (0) | 0.167 (76) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.120 (16) | 0.000 (0) | 0.133 (16) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 1/1 | 0 |
| tiered5 n=12 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.317 (76) | 0.444 (38) | 0.313 (76) | 1/1 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.257 (76) | 0.444 (38) | 0.255 (76) | 1/1 | 0 |
| tiered5 n=12 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.196 (38) | 0.444 (38) | 0.186 (38) | 1/1 | 0 |
| tiered5 n=12 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.161 (38) | 0.444 (38) | 0.133 (38) | 1/1 | 0 |
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
| flat n=20 D=1 rho=0.0 m=all | 0.043 (20) | 0.400 (18) | — | 0.083 (38) | 0.750 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.153 (38) | 0.667 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.25 m=all | 0.003 (23) | 0.333 (23) | — | 0.023 (38) | 0.600 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.5 m=1 | 0.013 (13) | 0.333 (12) | — | 0.127 (38) | 0.800 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=0.5 m=all | 0.073 (20) | 0.400 (18) | — | 0.207 (38) | 0.714 (38) | — | 0/1 | 0 |
| flat n=20 D=1 rho=1.0 m=1 | 0.010 (18) | 0.000 (0) | — | 0.143 (56) | 0.875 (18) | — | 0/1 | 0 |
| flat n=20 D=1 rho=1.0 m=all | 0.027 (38) | 0.167 (38) | — | 0.303 (161) | 0.941 (161) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.0 m=all | 0.007 (18) | 0.167 (18) | — | 0.033 (38) | 0.500 (38) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.117 (38) | 0.333 (38) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.25 m=all | 0.007 (38) | 0.375 (38) | — | 0.047 (91) | 0.895 (91) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.5 m=1 | 0.070 (38) | 0.778 (23) | — | 0.183 (76) | 0.950 (87) | — | 0/1 | 0 |
| flat n=20 D=2 rho=0.5 m=all | 0.060 (20) | 0.000 (0) | — | 0.237 (38) | 0.375 (38) | — | 0/1 | 0 |
| flat n=20 D=2 rho=1.0 m=1 | 0.083 (18) | 0.778 (18) | — | 0.227 (56) | 0.909 (18) | — | 0/1 | 0 |
| flat n=20 D=2 rho=1.0 m=all | 0.157 (76) | 0.556 (76) | — | 0.367 (167) | 0.949 (167) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.0 m=all | 0.023 (38) | 0.300 (18) | — | 0.033 (38) | 0.462 (38) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.25 m=1 | 0.040 (15) | 0.000 (0) | — | 0.177 (56) | 0.600 (56) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.25 m=all | 0.043 (38) | 0.375 (38) | — | 0.057 (76) | 0.833 (76) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.5 m=1 | 0.043 (38) | 0.000 (0) | — | 0.090 (109) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=3 rho=0.5 m=all | 0.333 (38) | 0.250 (38) | — | 0.450 (56) | 0.818 (56) | — | 0/1 | 0 |
| flat n=20 D=3 rho=1.0 m=1 | 0.000 (0) | 0.000 (0) | — | 0.133 (114) | 0.000 (0) | — | 0/1 | 0 |
| flat n=20 D=3 rho=1.0 m=all | 0.237 (105) | 0.857 (89) | — | 0.347 (190) | 0.958 (190) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.020 (38) | 0.333 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 0.003 (11) | 0.000 (0) | — | 0.160 (76) | 0.400 (69) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.117 (38) | 0.500 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.143 (38) | 0.500 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.220 (76) | 0.750 (76) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.167 (38) | 0.500 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.173 (38) | 0.600 (38) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.253 (114) | 0.750 (107) | — | 0/1 | 0 |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.017 (38) | 0.200 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.000 (0) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.043 (16) | 0.000 (0) | — | 0/1 | 0 |
| tiered3 n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=0 rho=1.0 m=all | 0.027 (38) | 0.000 (0) | — | 0.297 (76) | 0.769 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.113 (38) | 0.727 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.150 (38) | 0.727 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.25 m=all | 0.003 (16) | 0.000 (0) | — | 0.167 (76) | 0.786 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.150 (38) | 0.625 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.173 (54) | 0.200 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=1 rho=1.0 m=all | 0.070 (38) | 0.000 (0) | — | 0.400 (114) | 0.900 (114) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.467 (54) | 0.917 (54) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.507 (54) | 0.889 (54) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | — | 0.477 (54) | 0.917 (54) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.450 (76) | 0.867 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=0.5 m=all | 0.000 (0) | 0.000 (0) | — | 0.047 (38) | 0.167 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=2 rho=1.0 m=all | 0.050 (38) | 0.000 (0) | 0.004 (38) | 0.260 (76) | 0.583 (76) | 0.054 (76) | 1/1 | 0 |
| tiered3 n=20 D=3 rho=0.0 m=all | 0.003 (38) | 0.000 (0) | — | 0.027 (38) | 0.111 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | — | 0.050 (38) | 0.111 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.25 m=all | 0.013 (38) | 0.000 (0) | — | 0.043 (38) | 0.200 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | — | 0.107 (38) | 0.200 (38) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=0.5 m=all | 0.147 (38) | 0.333 (38) | — | 0.303 (76) | 0.733 (76) | — | 0/1 | 0 |
| tiered3 n=20 D=3 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered3 n=20 D=3 rho=1.0 m=all | 0.253 (114) | 0.911 (114) | 0.031 (114) | 0.650 (190) | 0.975 (152) | 0.126 (190) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.710 (38) | 0.905 (38) | — | 0/1 | 0 |
| tiered5 n=20 D=0 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.703 (38) | 0.867 (38) | 0.300 (38) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.647 (38) | 0.692 (38) | 0.226 (38) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.653 (76) | 0.931 (76) | 0.290 (76) | 1/1 | 0 |
| tiered5 n=20 D=0 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=0 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | — | 0.730 (76) | 0.920 (76) | — | 0/1 | 0 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.687 (76) | 0.895 (76) | 0.304 (76) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.25 m=all | 0.013 (22) | 0.000 (0) | 0.000 (22) | 0.627 (76) | 0.778 (76) | 0.231 (76) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.637 (114) | 0.949 (114) | 0.294 (114) | 1/1 | 0 |
| tiered5 n=20 D=1 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.0 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.363 (114) | 0.967 (114) | 0.259 (114) | 1/1 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=1 | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.300 (114) | 0.967 (114) | 0.260 (114) | 1/1 | 0 |
| tiered5 n=20 D=2 rho=0.25 m=all | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.250 (76) | 0.905 (76) | 0.166 (76) | 1/1 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.0 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=1 | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=all | — | — | — | — | — | — | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.5 m=1 | — | — | — | — | — | — | 0/0 | 0 |
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
| flat n=8 D=1 rho=0.0 m=all | 1/1 | 21 |
| flat n=8 D=1 rho=0.25 m=1 | 1/1 | 21 |
| flat n=8 D=1 rho=0.25 m=all | 1/1 | 21 |
| flat n=8 D=1 rho=0.5 m=1 | 1/1 | 21 |
| flat n=8 D=1 rho=0.5 m=all | 1/1 | 21 |
| flat n=8 D=1 rho=1.0 m=1 | 1/1 | 21 |
| flat n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=2 rho=0.0 m=all | 1/1 | 21 |
| flat n=8 D=2 rho=0.25 m=1 | 1/1 | 21 |
| flat n=8 D=2 rho=0.25 m=all | 1/1 | 20 |
| flat n=8 D=2 rho=0.5 m=1 | 1/1 | 21 |
| flat n=8 D=2 rho=0.5 m=all | 1/1 | 21 |
| flat n=8 D=2 rho=1.0 m=1 | 1/1 | 21 |
| flat n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| flat n=8 D=3 rho=0.0 m=all | 1/1 | 21 |
| flat n=8 D=3 rho=0.25 m=1 | 1/1 | 21 |
| flat n=8 D=3 rho=0.25 m=all | 1/1 | 21 |
| flat n=8 D=3 rho=0.5 m=1 | 1/1 | 21 |
| flat n=8 D=3 rho=0.5 m=all | 1/1 | 15 |
| flat n=8 D=3 rho=1.0 m=1 | 0/0 | 0 |
| flat n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 1/1 | 21 |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 1/1 | 21 |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 1/1 | 21 |
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
| tiered3 n=8 D=2 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=8 D=2 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=8 D=2 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=8 D=2 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=8 D=2 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=8 D=2 rho=1.0 m=1 | 1/1 | 21 |
| tiered3 n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=8 D=3 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=8 D=3 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=8 D=3 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=8 D=3 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=8 D=3 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=8 D=3 rho=1.0 m=1 | 1/1 | 21 |
| tiered3 n=8 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=0.5 m=all | 1/1 | 21 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 1/1 | 21 |
| tiered5 n=8 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=8 D=1 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=1 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=8 D=1 rho=0.5 m=all | 1/1 | 21 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 1/1 | 21 |
| tiered5 n=8 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=8 D=2 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=8 D=2 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=2 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=8 D=2 rho=0.5 m=all | 1/1 | 21 |
| tiered5 n=8 D=2 rho=1.0 m=1 | 1/1 | 21 |
| tiered5 n=8 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=8 D=3 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=8 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=8 D=3 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=8 D=3 rho=0.5 m=all | 1/1 | 21 |
| tiered5 n=8 D=3 rho=1.0 m=1 | 1/1 | 21 |
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
| flat n=12 D=2 rho=1.0 m=1 | 0/0 | 0 |
| flat n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| flat n=12 D=3 rho=0.0 m=all | 1/1 | 21 |
| flat n=12 D=3 rho=0.25 m=1 | 1/1 | 21 |
| flat n=12 D=3 rho=0.25 m=all | 1/1 | 21 |
| flat n=12 D=3 rho=0.5 m=1 | 1/1 | 21 |
| flat n=12 D=3 rho=0.5 m=all | 1/1 | 21 |
| flat n=12 D=3 rho=1.0 m=1 | 1/1 | 21 |
| flat n=12 D=3 rho=1.0 m=all | 1/1 | 21 |
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
| tiered3 n=12 D=2 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=2 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=12 D=2 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=12 D=2 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=12 D=2 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=12 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered3 n=12 D=3 rho=0.0 m=all | 1/1 | 21 |
| tiered3 n=12 D=3 rho=0.25 m=1 | 1/1 | 21 |
| tiered3 n=12 D=3 rho=0.25 m=all | 1/1 | 21 |
| tiered3 n=12 D=3 rho=0.5 m=1 | 1/1 | 21 |
| tiered3 n=12 D=3 rho=0.5 m=all | 1/1 | 21 |
| tiered3 n=12 D=3 rho=1.0 m=1 | 0/0 | 0 |
| tiered3 n=12 D=3 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=0 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=12 D=0 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=12 D=0 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=12 D=1 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=12 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=12 D=1 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=12 D=1 rho=0.5 m=1 | 1/1 | 21 |
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
| hub_and_spoke n=20 D=2 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | 0/0 | 0 |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | 0/0 | 0 |
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
| tiered3 n=20 D=1 rho=1.0 m=all | 1/1 | 1 |
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
| tiered5 n=20 D=1 rho=0.0 m=all | 1/1 | 1 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 1/1 | 21 |
| tiered5 n=20 D=1 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=1 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.0 m=all | 1/1 | 21 |
| tiered5 n=20 D=2 rho=0.25 m=1 | 1/1 | 21 |
| tiered5 n=20 D=2 rho=0.25 m=all | 1/1 | 21 |
| tiered5 n=20 D=2 rho=0.5 m=1 | 0/0 | 0 |
| tiered5 n=20 D=2 rho=0.5 m=all | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=1 | 0/0 | 0 |
| tiered5 n=20 D=2 rho=1.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.0 m=all | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=1 | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.25 m=all | 0/0 | 0 |
| tiered5 n=20 D=3 rho=0.5 m=1 | 0/0 | 0 |
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
| flat n=8 D=0 rho=0.0 m=all | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=0.25 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=0.25 m=all | 0.06 | 0.06 | 0.1 |
| flat n=8 D=0 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=0.5 m=all | 0.06 | 0.06 | 0.1 |
| flat n=8 D=0 rho=1.0 m=1 | 0.07 | 0.07 | 0.1 |
| flat n=8 D=0 rho=1.0 m=all | — | — | — |
| flat n=8 D=1 rho=0.0 m=all | 0.09 | 0.09 | 0.1 |
| flat n=8 D=1 rho=0.25 m=1 | 0.11 | 0.11 | 0.1 |
| flat n=8 D=1 rho=0.25 m=all | 0.08 | 0.08 | 0.1 |
| flat n=8 D=1 rho=0.5 m=1 | 0.09 | 0.09 | 0.1 |
| flat n=8 D=1 rho=0.5 m=all | 0.09 | 0.09 | 0.1 |
| flat n=8 D=1 rho=1.0 m=1 | 0.08 | 0.08 | 0.1 |
| flat n=8 D=1 rho=1.0 m=all | — | — | — |
| flat n=8 D=2 rho=0.0 m=all | 0.14 | 0.14 | 0.1 |
| flat n=8 D=2 rho=0.25 m=1 | 0.13 | 0.13 | 0.1 |
| flat n=8 D=2 rho=0.25 m=all | 0.08 | 0.08 | 0.1 |
| flat n=8 D=2 rho=0.5 m=1 | 0.11 | 0.11 | 0.1 |
| flat n=8 D=2 rho=0.5 m=all | 0.10 | 0.10 | 0.1 |
| flat n=8 D=2 rho=1.0 m=1 | 0.13 | 0.13 | 0.1 |
| flat n=8 D=2 rho=1.0 m=all | — | — | — |
| flat n=8 D=3 rho=0.0 m=all | 0.08 | 0.08 | 0.1 |
| flat n=8 D=3 rho=0.25 m=1 | 0.12 | 0.12 | 0.1 |
| flat n=8 D=3 rho=0.25 m=all | 0.10 | 0.10 | 0.1 |
| flat n=8 D=3 rho=0.5 m=1 | 0.10 | 0.10 | 0.1 |
| flat n=8 D=3 rho=0.5 m=all | 0.09 | 0.09 | 0.1 |
| flat n=8 D=3 rho=1.0 m=1 | — | — | — |
| flat n=8 D=3 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=0 rho=0.0 m=all | 0.03 | 0.03 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=1 | 0.04 | 0.04 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.25 m=all | 0.05 | 0.05 | 0.0 |
| hub_and_spoke n=8 D=0 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=0 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=0 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.0 m=all | 0.06 | 0.06 | 0.1 |
| hub_and_spoke n=8 D=1 rho=0.25 m=1 | 0.05 | 0.05 | 0.1 |
| hub_and_spoke n=8 D=1 rho=0.25 m=all | 0.06 | 0.06 | 0.1 |
| hub_and_spoke n=8 D=1 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=1 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=1 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=1 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.0 m=all | 0.05 | 0.05 | 0.1 |
| hub_and_spoke n=8 D=2 rho=0.25 m=1 | 0.05 | 0.05 | 0.1 |
| hub_and_spoke n=8 D=2 rho=0.25 m=all | 0.07 | 0.07 | 0.1 |
| hub_and_spoke n=8 D=2 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=2 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=2 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=2 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.0 m=all | 0.07 | 0.07 | 0.1 |
| hub_and_spoke n=8 D=3 rho=0.25 m=1 | 0.06 | 0.06 | 0.1 |
| hub_and_spoke n=8 D=3 rho=0.25 m=all | 0.08 | 0.08 | 0.1 |
| hub_and_spoke n=8 D=3 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=8 D=3 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=8 D=3 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=8 D=3 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=0 rho=0.0 m=all | 0.05 | 0.05 | 0.0 |
| tiered3 n=8 D=0 rho=0.25 m=1 | 0.06 | 0.06 | 0.1 |
| tiered3 n=8 D=0 rho=0.25 m=all | 0.05 | 0.05 | 0.1 |
| tiered3 n=8 D=0 rho=0.5 m=1 | 0.05 | 0.05 | 0.0 |
| tiered3 n=8 D=0 rho=0.5 m=all | 0.04 | 0.04 | 0.0 |
| tiered3 n=8 D=0 rho=1.0 m=1 | 0.04 | 0.04 | 0.0 |
| tiered3 n=8 D=0 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=1 rho=0.0 m=all | 0.08 | 0.08 | 0.1 |
| tiered3 n=8 D=1 rho=0.25 m=1 | 0.09 | 0.09 | 0.1 |
| tiered3 n=8 D=1 rho=0.25 m=all | 0.07 | 0.07 | 0.1 |
| tiered3 n=8 D=1 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| tiered3 n=8 D=1 rho=0.5 m=all | 0.07 | 0.07 | 0.1 |
| tiered3 n=8 D=1 rho=1.0 m=1 | 0.06 | 0.06 | 0.1 |
| tiered3 n=8 D=1 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=2 rho=0.0 m=all | 0.10 | 0.10 | 0.1 |
| tiered3 n=8 D=2 rho=0.25 m=1 | 0.10 | 0.10 | 0.1 |
| tiered3 n=8 D=2 rho=0.25 m=all | 0.09 | 0.09 | 0.1 |
| tiered3 n=8 D=2 rho=0.5 m=1 | 0.10 | 0.10 | 0.1 |
| tiered3 n=8 D=2 rho=0.5 m=all | 0.08 | 0.08 | 0.1 |
| tiered3 n=8 D=2 rho=1.0 m=1 | 0.08 | 0.08 | 0.1 |
| tiered3 n=8 D=2 rho=1.0 m=all | — | — | — |
| tiered3 n=8 D=3 rho=0.0 m=all | 0.11 | 0.11 | 0.1 |
| tiered3 n=8 D=3 rho=0.25 m=1 | 0.11 | 0.11 | 0.1 |
| tiered3 n=8 D=3 rho=0.25 m=all | 0.12 | 0.12 | 0.1 |
| tiered3 n=8 D=3 rho=0.5 m=1 | 0.09 | 0.09 | 0.1 |
| tiered3 n=8 D=3 rho=0.5 m=all | 0.10 | 0.10 | 0.1 |
| tiered3 n=8 D=3 rho=1.0 m=1 | 0.10 | 0.10 | 0.1 |
| tiered3 n=8 D=3 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=0 rho=0.0 m=all | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=0.25 m=1 | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=0 rho=0.5 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=0 rho=0.5 m=all | 0.03 | 0.03 | 0.0 |
| tiered5 n=8 D=0 rho=1.0 m=1 | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=1 rho=0.0 m=all | 0.05 | 0.05 | 0.0 |
| tiered5 n=8 D=1 rho=0.25 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=1 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=1 rho=0.5 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=1 rho=0.5 m=all | 0.05 | 0.05 | 0.1 |
| tiered5 n=8 D=1 rho=1.0 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=1 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=2 rho=0.0 m=all | 0.04 | 0.04 | 0.0 |
| tiered5 n=8 D=2 rho=0.25 m=1 | 0.05 | 0.05 | 0.0 |
| tiered5 n=8 D=2 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=2 rho=0.5 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=2 rho=0.5 m=all | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=2 rho=1.0 m=1 | 0.05 | 0.05 | 0.1 |
| tiered5 n=8 D=2 rho=1.0 m=all | — | — | — |
| tiered5 n=8 D=3 rho=0.0 m=all | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=3 rho=0.25 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=3 rho=0.25 m=all | — | — | — |
| tiered5 n=8 D=3 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| tiered5 n=8 D=3 rho=0.5 m=all | 0.07 | 0.07 | 0.1 |
| tiered5 n=8 D=3 rho=1.0 m=1 | 0.06 | 0.06 | 0.1 |
| tiered5 n=8 D=3 rho=1.0 m=all | — | — | — |
| flat n=12 D=0 rho=0.0 m=all | 0.59 | 0.59 | 0.6 |
| flat n=12 D=0 rho=0.25 m=1 | 0.38 | 0.38 | 0.4 |
| flat n=12 D=0 rho=0.25 m=all | 0.43 | 0.43 | 0.4 |
| flat n=12 D=0 rho=0.5 m=1 | 0.52 | 0.52 | 0.5 |
| flat n=12 D=0 rho=0.5 m=all | 0.39 | 0.39 | 0.4 |
| flat n=12 D=0 rho=1.0 m=1 | 0.43 | 0.43 | 0.4 |
| flat n=12 D=0 rho=1.0 m=all | 0.19 | 0.19 | 0.2 |
| flat n=12 D=1 rho=0.0 m=all | 0.64 | 0.64 | 0.6 |
| flat n=12 D=1 rho=0.25 m=1 | 0.47 | 0.47 | 0.5 |
| flat n=12 D=1 rho=0.25 m=all | 0.50 | 0.50 | 0.5 |
| flat n=12 D=1 rho=0.5 m=1 | 0.56 | 0.56 | 0.6 |
| flat n=12 D=1 rho=0.5 m=all | 0.47 | 0.47 | 0.5 |
| flat n=12 D=1 rho=1.0 m=1 | 0.49 | 0.49 | 0.5 |
| flat n=12 D=1 rho=1.0 m=all | 0.26 | 0.26 | 0.3 |
| flat n=12 D=2 rho=0.0 m=all | 1.03 | 1.03 | 1.0 |
| flat n=12 D=2 rho=0.25 m=1 | 0.51 | 0.51 | 0.5 |
| flat n=12 D=2 rho=0.25 m=all | 0.81 | 0.81 | 0.8 |
| flat n=12 D=2 rho=0.5 m=1 | 0.80 | 0.80 | 0.8 |
| flat n=12 D=2 rho=0.5 m=all | 0.64 | 0.64 | 0.6 |
| flat n=12 D=2 rho=1.0 m=1 | — | — | — |
| flat n=12 D=2 rho=1.0 m=all | — | — | — |
| flat n=12 D=3 rho=0.0 m=all | 0.67 | 0.67 | 0.7 |
| flat n=12 D=3 rho=0.25 m=1 | 0.70 | 0.70 | 0.7 |
| flat n=12 D=3 rho=0.25 m=all | 0.43 | 0.43 | 0.4 |
| flat n=12 D=3 rho=0.5 m=1 | 0.70 | 0.70 | 0.7 |
| flat n=12 D=3 rho=0.5 m=all | 0.50 | 0.50 | 0.5 |
| flat n=12 D=3 rho=1.0 m=1 | 0.73 | 0.73 | 0.7 |
| flat n=12 D=3 rho=1.0 m=all | 0.34 | 0.34 | 0.3 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all | 0.19 | 0.19 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.25 m=1 | 0.28 | 0.28 | 0.3 |
| hub_and_spoke n=12 D=0 rho=0.25 m=all | 0.20 | 0.20 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.5 m=1 | 0.25 | 0.25 | 0.2 |
| hub_and_spoke n=12 D=0 rho=0.5 m=all | 0.23 | 0.23 | 0.2 |
| hub_and_spoke n=12 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=12 D=0 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=12 D=1 rho=0.0 m=all | 0.26 | 0.26 | 0.3 |
| hub_and_spoke n=12 D=1 rho=0.25 m=1 | 0.37 | 0.37 | 0.4 |
| hub_and_spoke n=12 D=1 rho=0.25 m=all | 0.28 | 0.28 | 0.3 |
| hub_and_spoke n=12 D=1 rho=0.5 m=1 | 0.31 | 0.31 | 0.3 |
| hub_and_spoke n=12 D=1 rho=0.5 m=all | 0.32 | 0.32 | 0.3 |
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
| tiered3 n=12 D=0 rho=0.25 m=all | 0.25 | 0.25 | 0.2 |
| tiered3 n=12 D=0 rho=0.5 m=1 | 0.17 | 0.17 | 0.2 |
| tiered3 n=12 D=0 rho=0.5 m=all | 0.28 | 0.28 | 0.3 |
| tiered3 n=12 D=0 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=0 rho=1.0 m=all | 0.12 | 0.12 | 0.1 |
| tiered3 n=12 D=1 rho=0.0 m=all | 0.58 | 0.58 | 0.6 |
| tiered3 n=12 D=1 rho=0.25 m=1 | 0.30 | 0.30 | 0.3 |
| tiered3 n=12 D=1 rho=0.25 m=all | 0.39 | 0.39 | 0.4 |
| tiered3 n=12 D=1 rho=0.5 m=1 | 0.28 | 0.28 | 0.3 |
| tiered3 n=12 D=1 rho=0.5 m=all | 0.42 | 0.42 | 0.4 |
| tiered3 n=12 D=1 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=1 rho=1.0 m=all | 0.23 | 0.23 | 0.2 |
| tiered3 n=12 D=2 rho=0.0 m=all | 0.53 | 0.53 | 0.5 |
| tiered3 n=12 D=2 rho=0.25 m=1 | 0.31 | 0.31 | 0.3 |
| tiered3 n=12 D=2 rho=0.25 m=all | 0.38 | 0.38 | 0.4 |
| tiered3 n=12 D=2 rho=0.5 m=1 | 0.22 | 0.22 | 0.2 |
| tiered3 n=12 D=2 rho=0.5 m=all | 0.32 | 0.32 | 0.3 |
| tiered3 n=12 D=2 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=2 rho=1.0 m=all | — | — | — |
| tiered3 n=12 D=3 rho=0.0 m=all | 0.74 | 0.74 | 0.7 |
| tiered3 n=12 D=3 rho=0.25 m=1 | 0.40 | 0.40 | 0.4 |
| tiered3 n=12 D=3 rho=0.25 m=all | 0.55 | 0.55 | 0.6 |
| tiered3 n=12 D=3 rho=0.5 m=1 | 0.50 | 0.50 | 0.5 |
| tiered3 n=12 D=3 rho=0.5 m=all | 0.62 | 0.62 | 0.6 |
| tiered3 n=12 D=3 rho=1.0 m=1 | — | — | — |
| tiered3 n=12 D=3 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=0 rho=0.0 m=all | 0.13 | 0.13 | 0.1 |
| tiered5 n=12 D=0 rho=0.25 m=1 | 0.08 | 0.08 | 0.1 |
| tiered5 n=12 D=0 rho=0.25 m=all | 0.11 | 0.11 | 0.1 |
| tiered5 n=12 D=0 rho=0.5 m=1 | 0.07 | 0.07 | 0.1 |
| tiered5 n=12 D=0 rho=0.5 m=all | — | — | — |
| tiered5 n=12 D=0 rho=1.0 m=1 | — | — | — |
| tiered5 n=12 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=12 D=1 rho=0.0 m=all | 0.19 | 0.19 | 0.2 |
| tiered5 n=12 D=1 rho=0.25 m=1 | 0.14 | 0.14 | 0.1 |
| tiered5 n=12 D=1 rho=0.25 m=all | 0.19 | 0.19 | 0.2 |
| tiered5 n=12 D=1 rho=0.5 m=1 | 0.14 | 0.14 | 0.1 |
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
| flat n=20 D=0 rho=0.0 m=all | 3.48 | 3.48 | 3.5 |
| flat n=20 D=0 rho=0.25 m=1 | 4.59 | 4.59 | 4.6 |
| flat n=20 D=0 rho=0.25 m=all | 3.80 | 3.80 | 3.8 |
| flat n=20 D=0 rho=0.5 m=1 | 4.70 | 4.70 | 4.7 |
| flat n=20 D=0 rho=0.5 m=all | 4.00 | 4.00 | 4.0 |
| flat n=20 D=0 rho=1.0 m=1 | 4.42 | 4.42 | 4.4 |
| flat n=20 D=0 rho=1.0 m=all | 6.92 | 6.92 | 6.9 |
| flat n=20 D=1 rho=0.0 m=all | 5.67 | 5.67 | 5.7 |
| flat n=20 D=1 rho=0.25 m=1 | 6.63 | 6.63 | 6.6 |
| flat n=20 D=1 rho=0.25 m=all | 5.31 | 5.31 | 5.3 |
| flat n=20 D=1 rho=0.5 m=1 | 7.16 | 7.16 | 7.2 |
| flat n=20 D=1 rho=0.5 m=all | 6.17 | 6.17 | 6.2 |
| flat n=20 D=1 rho=1.0 m=1 | 6.95 | 6.95 | 6.9 |
| flat n=20 D=1 rho=1.0 m=all | 10.57 | 10.57 | 10.6 |
| flat n=20 D=2 rho=0.0 m=all | 10.22 | 10.22 | 10.2 |
| flat n=20 D=2 rho=0.25 m=1 | 10.50 | 10.50 | 10.5 |
| flat n=20 D=2 rho=0.25 m=all | 11.71 | 11.71 | 11.7 |
| flat n=20 D=2 rho=0.5 m=1 | 12.63 | 12.63 | 12.6 |
| flat n=20 D=2 rho=0.5 m=all | 9.93 | 9.93 | 9.9 |
| flat n=20 D=2 rho=1.0 m=1 | 10.72 | 10.72 | 10.7 |
| flat n=20 D=2 rho=1.0 m=all | 20.23 | 20.23 | 20.2 |
| flat n=20 D=3 rho=0.0 m=all | 17.84 | 17.84 | 17.8 |
| flat n=20 D=3 rho=0.25 m=1 | 17.73 | 17.73 | 17.7 |
| flat n=20 D=3 rho=0.25 m=all | 17.00 | 17.00 | 17.0 |
| flat n=20 D=3 rho=0.5 m=1 | 16.77 | 16.77 | 16.8 |
| flat n=20 D=3 rho=0.5 m=all | 19.78 | 19.78 | 19.8 |
| flat n=20 D=3 rho=1.0 m=1 | 17.05 | 17.05 | 17.1 |
| flat n=20 D=3 rho=1.0 m=all | 39.72 | 39.72 | 39.7 |
| hub_and_spoke n=20 D=0 rho=0.0 m=all | 1.11 | 1.11 | 1.1 |
| hub_and_spoke n=20 D=0 rho=0.25 m=1 | 1.20 | 1.20 | 1.2 |
| hub_and_spoke n=20 D=0 rho=0.25 m=all | 1.55 | 1.55 | 1.6 |
| hub_and_spoke n=20 D=0 rho=0.5 m=1 | 1.17 | 1.17 | 1.2 |
| hub_and_spoke n=20 D=0 rho=0.5 m=all | 1.16 | 1.16 | 1.2 |
| hub_and_spoke n=20 D=0 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=0 rho=1.0 m=all | 1.78 | 1.78 | 1.8 |
| hub_and_spoke n=20 D=1 rho=0.0 m=all | 1.68 | 1.68 | 1.7 |
| hub_and_spoke n=20 D=1 rho=0.25 m=1 | 1.71 | 1.71 | 1.7 |
| hub_and_spoke n=20 D=1 rho=0.25 m=all | 2.31 | 2.31 | 2.3 |
| hub_and_spoke n=20 D=1 rho=0.5 m=1 | 1.91 | 1.91 | 1.9 |
| hub_and_spoke n=20 D=1 rho=0.5 m=all | 1.90 | 1.90 | 1.9 |
| hub_and_spoke n=20 D=1 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=1 rho=1.0 m=all | 2.69 | 2.69 | 2.7 |
| hub_and_spoke n=20 D=2 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=20 D=2 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=20 D=2 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=20 D=2 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=20 D=2 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=20 D=2 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=2 rho=1.0 m=all | — | — | — |
| hub_and_spoke n=20 D=3 rho=0.0 m=all | — | — | — |
| hub_and_spoke n=20 D=3 rho=0.25 m=1 | — | — | — |
| hub_and_spoke n=20 D=3 rho=0.25 m=all | — | — | — |
| hub_and_spoke n=20 D=3 rho=0.5 m=1 | — | — | — |
| hub_and_spoke n=20 D=3 rho=0.5 m=all | — | — | — |
| hub_and_spoke n=20 D=3 rho=1.0 m=1 | — | — | — |
| hub_and_spoke n=20 D=3 rho=1.0 m=all | — | — | — |
| tiered3 n=20 D=0 rho=0.0 m=all | 2.47 | 2.47 | 2.5 |
| tiered3 n=20 D=0 rho=0.25 m=1 | 2.62 | 2.62 | 2.6 |
| tiered3 n=20 D=0 rho=0.25 m=all | 2.45 | 2.45 | 2.4 |
| tiered3 n=20 D=0 rho=0.5 m=1 | 2.48 | 2.48 | 2.5 |
| tiered3 n=20 D=0 rho=0.5 m=all | 2.82 | 2.82 | 2.8 |
| tiered3 n=20 D=0 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=0 rho=1.0 m=all | 4.66 | 4.66 | 4.7 |
| tiered3 n=20 D=1 rho=0.0 m=all | 3.85 | 3.85 | 3.9 |
| tiered3 n=20 D=1 rho=0.25 m=1 | 4.07 | 4.07 | 4.1 |
| tiered3 n=20 D=1 rho=0.25 m=all | 4.06 | 4.06 | 4.1 |
| tiered3 n=20 D=1 rho=0.5 m=1 | 4.00 | 4.00 | 4.0 |
| tiered3 n=20 D=1 rho=0.5 m=all | 4.31 | 4.31 | 4.3 |
| tiered3 n=20 D=1 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=1 rho=1.0 m=all | 7.35 | 7.35 | 7.3 |
| tiered3 n=20 D=2 rho=0.0 m=all | 4.91 | 4.91 | 4.9 |
| tiered3 n=20 D=2 rho=0.25 m=1 | 4.84 | 4.84 | 4.8 |
| tiered3 n=20 D=2 rho=0.25 m=all | 4.80 | 4.80 | 4.8 |
| tiered3 n=20 D=2 rho=0.5 m=1 | 5.68 | 5.68 | 5.7 |
| tiered3 n=20 D=2 rho=0.5 m=all | 5.10 | 5.10 | 5.1 |
| tiered3 n=20 D=2 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=2 rho=1.0 m=all | 14.49 | 14.49 | 14.5 |
| tiered3 n=20 D=3 rho=0.0 m=all | 8.51 | 8.51 | 8.5 |
| tiered3 n=20 D=3 rho=0.25 m=1 | 8.23 | 8.23 | 8.2 |
| tiered3 n=20 D=3 rho=0.25 m=all | 8.35 | 8.35 | 8.4 |
| tiered3 n=20 D=3 rho=0.5 m=1 | 7.73 | 7.73 | 7.7 |
| tiered3 n=20 D=3 rho=0.5 m=all | 9.82 | 9.82 | 9.8 |
| tiered3 n=20 D=3 rho=1.0 m=1 | — | — | — |
| tiered3 n=20 D=3 rho=1.0 m=all | 23.35 | 23.35 | 23.4 |
| tiered5 n=20 D=0 rho=0.0 m=all | 4.14 | 4.14 | 4.1 |
| tiered5 n=20 D=0 rho=0.25 m=1 | 10.97 | 10.97 | 11.0 |
| tiered5 n=20 D=0 rho=0.25 m=all | 10.19 | 10.19 | 10.2 |
| tiered5 n=20 D=0 rho=0.5 m=1 | 6.52 | 6.52 | 6.5 |
| tiered5 n=20 D=0 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=0 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=0 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=1 rho=0.0 m=all | 5.53 | 5.53 | 5.5 |
| tiered5 n=20 D=1 rho=0.25 m=1 | 13.64 | 13.64 | 13.6 |
| tiered5 n=20 D=1 rho=0.25 m=all | 12.58 | 12.58 | 12.6 |
| tiered5 n=20 D=1 rho=0.5 m=1 | 8.04 | 8.04 | 8.0 |
| tiered5 n=20 D=1 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=1 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=1 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=2 rho=0.0 m=all | 6.76 | 6.76 | 6.8 |
| tiered5 n=20 D=2 rho=0.25 m=1 | 6.27 | 6.27 | 6.3 |
| tiered5 n=20 D=2 rho=0.25 m=all | 4.91 | 4.91 | 4.9 |
| tiered5 n=20 D=2 rho=0.5 m=1 | — | — | — |
| tiered5 n=20 D=2 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=2 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=2 rho=1.0 m=all | — | — | — |
| tiered5 n=20 D=3 rho=0.0 m=all | — | — | — |
| tiered5 n=20 D=3 rho=0.25 m=1 | — | — | — |
| tiered5 n=20 D=3 rho=0.25 m=all | — | — | — |
| tiered5 n=20 D=3 rho=0.5 m=1 | — | — | — |
| tiered5 n=20 D=3 rho=0.5 m=all | — | — | — |
| tiered5 n=20 D=3 rho=1.0 m=1 | — | — | — |
| tiered5 n=20 D=3 rho=1.0 m=all | — | — | — |
| flat n=8 D=0 rho=0.0 m=all pr_gated | 0.17 | 0.52 | 4.1 |
| hub_and_spoke n=8 D=0 rho=0.0 m=all pr_gated | 0.09 | 0.18 | 1.4 |
| tiered3 n=8 D=0 rho=0.0 m=all pr_gated | 0.10 | 0.17 | 1.5 |
| flat n=12 D=0 rho=0.0 m=all pr_gated | 1.81 | 3.10 | 33.3 |
| hub_and_spoke n=12 D=0 rho=0.0 m=all pr_gated | 0.49 | 0.81 | 9.5 |
| tiered3 n=12 D=0 rho=0.0 m=all pr_gated | 0.75 | 1.46 | 14.2 |

## Unreachable goals and generation failures

- flat n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=0.5 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- tiered3 n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=0 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=1 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=1 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=8 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier4-8) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(lan-5) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
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
- tiered3 n=12 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered3 n=12 D=3 rho=1.0 m=all seed=0: unreachable — execCode(tier2-10) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=0.5 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=12 D=0 rho=1.0 m=all seed=0: unreachable — execCode(tier4-11) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
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
- hub_and_spoke n=20 D=2 rho=0.0 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=0.25 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=0.5 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=2 rho=1.0 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=0.0 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=0.25 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=0.5 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=1.0 m=1 seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=20 D=3 rho=1.0 m=all seed=0: unreachable — execCode(spoke-18) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
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
- tiered5 n=20 D=2 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=0.5 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=1.0 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=2 rho=1.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=0.0 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=0.25 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=0.25 m=all seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered5 n=20 D=3 rho=0.5 m=1 seed=0: unreachable — execCode(tier4-17) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_tiers': 5, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
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
