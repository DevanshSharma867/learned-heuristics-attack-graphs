# d22: 3 runs under one 5.0 h budget

Elapsed 1.29 h.

| overrides | status | best val loss | epochs | seconds | run |
|---|---|---|---|---|---|
| `{"kind": "gnn", "hidden": 64, "layers": 3, "lr": 0.001, "target": "residual", "loss": "mse"}` | ok | 0.6799 | 23 | 2328 | results/training/d22/gnnres-64x3-lr0.001-mse-s0/2026-10-30T124719Z-27adeb9 |
| `{"kind": "gnn", "hidden": 64, "layers": 3, "lr": 0.001, "loss": "rank"}` | ok | 4.6615 | 30 | 1169 | results/training/d22/gnn-64x3-lr0.001-rank-s0/2026-10-30T130648Z-27adeb9 |
| `{"kind": "gnn", "hidden": 64, "layers": 3, "lr": 0.001, "target": "residual", "loss": "rank"}` | ok | 3.6036 | 28 | 1134 | results/training/d22/gnnres-64x3-lr0.001-rank-s0/2026-10-30T132542Z-27adeb9 |
