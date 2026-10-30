# epoch timing (D21 §5)

torch threads 4; 391736 train states.

| model | device | train s/epoch (each epoch) | val s |
|---|---|---|---|
| gnn 64 | cpu | 99.1, 101.3 | 1.2, 1.4 |
| gnn 64 | mps | 92.7, 71.9 | 0.8, 1.1 |
| mlp 64 | cpu | 0.3, 0.3 | 0.0, 0.0 |
| mlp 64 | mps | 1.5, 1.4 | 0.0, 0.0 |
