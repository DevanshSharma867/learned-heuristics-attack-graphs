# hyperparameter search (D21 §5)

Budget 3.0 h; elapsed 3.02 h. Seed 0, MSE, selection by val MSE.

| kind | overrides | status | best val MSE | epochs | seconds |
|---|---|---|---|---|---|
| wl | `{"lam": 0.1}` | ok | 11.7125 | 1 | 373 |
| wl | `{"lam": 1.0}` | ok | 11.7356 | 1 | 109 |
| wl | `{"lam": 10.0}` | ok | 11.7482 | 1 | 102 |
| mlp | `{"lr": 0.001, "hidden": 64}` | ok | 9.7971 | 16 | 6 |
| mlp | `{"lr": 0.003, "hidden": 64}` | ok | 10.0106 | 12 | 4 |
| mlp | `{"lr": 0.001, "hidden": 128}` | ok | 9.8809 | 16 | 7 |
| mlp | `{"lr": 0.003, "hidden": 128}` | ok | 9.8246 | 10 | 4 |
| gnn | `{"lr": 0.001, "hidden": 64, "layers": 3}` | ok | 3.1518 | 21 | 2152 |
| gnn | `{"lr": 0.003, "hidden": 64, "layers": 3}` | ok | 3.9871 | 18 | 2003 |
| gnn | `{"lr": 0.001, "hidden": 128, "layers": 3}` | ok | 2.8164 | 18 | 4415 |
| gnn | `{"lr": 0.003, "hidden": 128, "layers": 3}` | stopped (budget) | 4.7593 | 8 | 1697 |
| gnn | `{"lr": 0.001, "hidden": 64, "layers": 6}` | not run (budget) | — | — | 0 |
| gnn | `{"lr": 0.003, "hidden": 64, "layers": 6}` | not run (budget) | — | — | 0 |
| gnn | `{"lr": 0.001, "hidden": 128, "layers": 6}` | not run (budget) | — | — | 0 |
| gnn | `{"lr": 0.003, "hidden": 128, "layers": 6}` | not run (budget) | — | — | 0 |

Selected: wl {"lam": 0.1}, mlp {"lr": 0.001, "hidden": 64}, gnn {"lr": 0.001, "hidden": 128, "layers": 3}
