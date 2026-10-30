# training-cost projection (D17 seed plan)

Priced at the mean training wall time (label loading excluded; encoding included where it was not cached yet) of the pilot runs of each config, sequential on one M4 CPU process.

| item | runs | h per run (pilot) | hours |
|---|---|---|---|
| gnn | 10 | 1.31 | 13.1 |
| mlp | 10 | 0.00 | 0.0 |
| wl | 2 | 0.10 | 0.2 |
| gnn_ablation | 30 | 0.61 | 18.4 |

Total: 31.7 h.

Seconds per epoch, train + val (timing run):

- gnn on cpu: 101.5
- gnn on mps: 83.3
- mlp on cpu: 0.3
- mlp on mps: 1.5
