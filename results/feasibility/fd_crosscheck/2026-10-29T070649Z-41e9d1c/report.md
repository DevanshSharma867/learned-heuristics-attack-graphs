# fd_crosscheck

Fast Downward release-24.06.1 (1eef26b); 20 instances from `results/feasibility/inference_microbench/2026-10-29T062211Z-1627e16` (D15+D16, D = 3, n = 20); 200 states (initial + 9 sampled per instance).

## Values

- h_max: FD = ours on **200/200** states.
- LM-cut: FD = ours on **169/200** states; every value of both is ≤ h\* (checked; the run aborts otherwise). Mismatch gaps (FD − ours, D9 units): -38, -3, -38, 18, -4, 23, -38, 38, 38, 38, 38, 38, 38, 38, 38, 23, -38, -38, -38, -38, -38, -38, -110, -110, -38, -38, -38, -38, -38, -38, -38.
- FD A\*+LM-cut plan cost = our h\* on **200/200** states where h\* is known (any mismatch aborts).

## Per-state cost from the initial-state search (ms)

FD: search time / evaluations, minus the blind search's per-evaluation overhead. Python and learned: the feasibility run's per-state medians on the same instances.

| method | median per state | min | max |
|---|---|---|---|
| FD hmax (C++) | 0.0015 | 0.0000 | 0.0023 |
| FD lmcut (C++) | 0.0072 | 0.0035 | 0.0142 |
| FD search overhead per evaluation | 0.0009 | | |
| hmax (this repo) | 0.0392 | 0.0176 | 0.1137 |
| lmcut (this repo) | 0.6587 | 0.2940 | 1.8133 |
| mlp/cpu1/batched (this repo) | 0.0412 | 0.0183 | 0.0981 |
| gnn64x3/cpu1/batched (this repo) | 0.1123 | 0.0575 | 0.2866 |
| gnn128x6/cpu1/batched (this repo) | 0.4111 | 0.1489 | 1.1843 |

Median FD search time from the initial state (ms): A\*+hmax 0.2465 (15 expansions), A\*+lmcut 0.5595 (9.5 expansions), A\*+blind 3.0585 (811.5 expansions).

## Break-even against FD

E\* = the largest expansion count at which the learned heuristic (per-expansion cost p from the feasibility run) still beats FD's A\* on time. `py loop` adds this repo's Python search overhead per expansion; `C++ loop` assumes zero loop overhead (optimistic). Median over instances; `≥ plan` = fraction of instances where E\* ≥ the optimal plan length (a perfect heuristic of that cost would win).

| method | p (ms) | E\* vs FD h_max, py loop | C++ loop | E\* vs FD LM-cut, py loop | C++ loop | ≥ plan vs FD LM-cut, C++ loop |
|---|---|---|---|---|---|---|
| mlp/cpu1/batched | 0.259 | 0.87 | 0.90 | 1.85 | 1.93 | 0% |
| gnn64x3/cpu1/batched | 0.696 | 0.31 | 0.32 | 0.66 | 0.67 | 0% |
| gnn128x6/cpu1/batched | 2.471 | 0.09 | 0.10 | 0.20 | 0.20 | 0% |

Median optimal plan length on these instances: 8; median FD A\*+LM-cut expansions 9.5.
