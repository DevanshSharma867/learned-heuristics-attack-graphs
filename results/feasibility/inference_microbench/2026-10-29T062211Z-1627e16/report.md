# inference_microbench

**Speed only: untrained, randomly initialised models. Nothing here is a result about learning.**

Instances: the 391 reachable D15+D16 instances at D = 3, n = 20, from `results/landscape/depth_coupling_sweep/full_d16/2026-10-28T142309Z-ab208e3`. Rerun expansions equal the run's on every instance. States: successors of the first 20 distinct A*+LM-cut-expanded states per instance (4084 expanded nodes, 32250 successor states; median 7 successors per node). torch 2.15.0; devices cpu1, cpu, mps.

## Per-state cost (ms)

Median over instances of the per-instance median time per successor state, and the 90th percentile over instances. Feature extraction included; `feat.` is its median share of that time.

| method | per state | p90 | feat. |
|---|---|---|---|
| hmax | 0.041 | 0.093 | — |
| lmcut | 0.701 | 1.490 | — |
| mlp/cpu1/single | 0.053 | 0.092 | 81% |
| mlp/cpu1/batched | 0.040 | 0.078 | 96% |
| gnn64x3/cpu1/single | 0.282 | 0.418 | 2% |
| gnn64x3/cpu1/batched | 0.112 | 0.210 | 3% |
| gnn128x6/cpu1/single | 1.037 | 1.235 | 0% |
| gnn128x6/cpu1/batched | 0.395 | 0.988 | 1% |
| mlp/cpu/single | 0.053 | 0.091 | 82% |
| mlp/cpu/batched | 0.041 | 0.077 | 96% |
| gnn64x3/cpu/single | 0.378 | 0.678 | 1% |
| gnn64x3/cpu/batched | 0.188 | 0.257 | 2% |
| gnn128x6/cpu/single | 1.109 | 1.758 | 1% |
| gnn128x6/cpu/batched | 0.501 | 0.828 | 1% |
| mlp/mps/single | 0.406 | 0.458 | 51% |
| mlp/mps/batched | 0.105 | 0.142 | 62% |
| gnn64x3/mps/single | 0.857 | 1.004 | 23% |
| gnn64x3/mps/batched | 0.202 | 0.293 | 15% |
| gnn128x6/mps/single | 1.499 | 2.676 | 14% |
| gnn128x6/mps/batched | 0.546 | 1.305 | 6% |

## Break-even from the full run's timings (`results/landscape/depth_coupling_sweep/full_d16/2026-10-28T142309Z-ab208e3`)

- search overhead per expansion o (UCS): median 0.024 ms
- **c\*_lm, largest per-state cost to tie A*+LM-cut at LM-cut's expansion counts: median 1.342 ms** (p10 0.587, p90 3.142)
- reference medians: A*+LM-cut expands 9, A*+h_max 15; optimal plan length 8 (a lower bound on any A* expansion count); A*+LM-cut evaluations per expansion 8.2
- self-check (the cost model should reproduce the classical searches' own counts): median E\*_hm of h_max = 28.2 vs its actual 15; median E\*_lm of LM-cut = 18.1 vs its actual 9

E\*_hm (E\*_lm): the largest expansion count at which a heuristic with that per-expansion cost p still beats A*+h_max (A*+LM-cut). `≥ plan` = fraction of instances where E\*_hm ≥ optimal plan length, i.e. where even a perfect heuristic of that cost would beat A*+h_max.

| method | p per expansion (ms) | median E\*_hm | median E\*_lm | E\*_hm ≥ plan |
|---|---|---|---|---|
| hmax | 0.312 | 28.2 | 285.8 | 99% |
| lmcut | 5.253 | 1.8 | 18.1 | 2% |
| mlp/cpu1/single | 0.426 | 21.9 | 221.9 | 97% |
| mlp/cpu1/batched | 0.306 | 30.9 | 303.0 | 100% |
| gnn64x3/cpu1/single | 2.154 | 5.2 | 53.3 | 26% |
| gnn64x3/cpu1/batched | 0.786 | 11.6 | 117.5 | 73% |
| gnn128x6/cpu1/single | 8.273 | 1.3 | 13.5 | 2% |
| gnn128x6/cpu1/batched | 2.821 | 3.4 | 31.4 | 9% |
| mlp/cpu/single | 0.434 | 22.3 | 224.5 | 96% |
| mlp/cpu/batched | 0.306 | 31.3 | 304.6 | 100% |
| gnn64x3/cpu/single | 2.998 | 3.4 | 34.7 | 14% |
| gnn64x3/cpu/batched | 1.352 | 7.9 | 80.8 | 42% |
| gnn128x6/cpu/single | 8.785 | 1.2 | 11.3 | 1% |
| gnn128x6/cpu/batched | 3.332 | 2.7 | 27.6 | 8% |
| mlp/mps/single | 3.349 | 3.2 | 33.0 | 16% |
| mlp/mps/batched | 0.715 | 12.9 | 131.1 | 75% |
| gnn64x3/mps/single | 7.261 | 1.6 | 15.5 | 4% |
| gnn64x3/mps/batched | 1.403 | 7.0 | 69.2 | 40% |
| gnn128x6/mps/single | 12.482 | 0.9 | 8.1 | 1% |
| gnn128x6/mps/batched | 3.921 | 2.6 | 26.3 | 7% |

## Break-even from this script's own single-process reruns (consistency check)

- search overhead per expansion o (UCS): median 0.011 ms
- **c\*_lm, largest per-state cost to tie A*+LM-cut at LM-cut's expansion counts: median 0.619 ms** (p10 0.304, p90 1.321)
- reference medians: A*+LM-cut expands 9, A*+h_max 15; optimal plan length 8 (a lower bound on any A* expansion count); A*+LM-cut evaluations per expansion 8.2
- self-check (the cost model should reproduce the classical searches' own counts): median E\*_hm of h_max = 13.1 vs its actual 15; median E\*_lm of LM-cut = 8.1 vs its actual 9

E\*_hm (E\*_lm): the largest expansion count at which a heuristic with that per-expansion cost p still beats A*+h_max (A*+LM-cut). `≥ plan` = fraction of instances where E\*_hm ≥ optimal plan length, i.e. where even a perfect heuristic of that cost would beat A*+h_max.

| method | p per expansion (ms) | median E\*_hm | median E\*_lm | E\*_hm ≥ plan |
|---|---|---|---|---|
| hmax | 0.312 | 13.1 | 132.9 | 83% |
| lmcut | 5.253 | 0.8 | 8.1 | 1% |
| mlp/cpu1/single | 0.426 | 10.0 | 103.5 | 59% |
| mlp/cpu1/batched | 0.306 | 14.4 | 139.4 | 88% |
| gnn64x3/cpu1/single | 2.154 | 2.3 | 24.2 | 7% |
| gnn64x3/cpu1/batched | 0.786 | 5.3 | 53.1 | 24% |
| gnn128x6/cpu1/single | 8.273 | 0.6 | 6.1 | 1% |
| gnn128x6/cpu1/batched | 2.821 | 1.5 | 14.4 | 2% |
| mlp/cpu/single | 0.434 | 10.0 | 104.5 | 59% |
| mlp/cpu/batched | 0.306 | 14.5 | 141.6 | 89% |
| gnn64x3/cpu/single | 2.998 | 1.6 | 15.7 | 2% |
| gnn64x3/cpu/batched | 1.352 | 3.5 | 36.1 | 14% |
| gnn128x6/cpu/single | 8.785 | 0.5 | 5.2 | 1% |
| gnn128x6/cpu/batched | 3.332 | 1.2 | 12.2 | 1% |
| mlp/mps/single | 3.349 | 1.5 | 14.8 | 4% |
| mlp/mps/batched | 0.715 | 6.0 | 59.4 | 32% |
| gnn64x3/mps/single | 7.261 | 0.7 | 6.9 | 1% |
| gnn64x3/mps/batched | 1.403 | 3.1 | 31.0 | 14% |
| gnn128x6/mps/single | 12.482 | 0.4 | 3.7 | 1% |
| gnn128x6/mps/batched | 3.921 | 1.2 | 12.0 | 2% |
