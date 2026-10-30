# training d22-6layer/gnnres-64x6-lr0.001-rank-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "gnn", "lam": 1.0, "layers": 6, "loss": "rank", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 0, "target": "residual", "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 3.9730 at epoch 9 of 15; wall time 1099.3 s (encoding 1.0 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 7.1887 | 5.1622 | 64.65 |
| 1 | 5.3568 | 4.8089 | 68.12 |
| 2 | 4.9924 | 4.4076 | 70.55 |
| 3 | 4.8191 | 4.5523 | 71.80 |
| 4 | 4.7258 | 4.3982 | 72.37 |
| 5 | 4.6348 | 4.3198 | 73.51 |
| 6 | 4.5987 | 4.3438 | 71.73 |
| 7 | 4.4659 | 4.2099 | 70.14 |
| 8 | 4.3965 | 4.2657 | 70.03 |
| 9 | 4.3293 | 3.9730 | 70.85 |
| 10 | 4.2882 | 4.0705 | 75.43 |
| 11 | 4.2318 | 4.0434 | 74.95 |
| 12 | 4.1730 | 4.0026 | 76.78 |
| 13 | 4.1098 | 4.1996 | 75.89 |
| 14 | 4.0519 | 4.1947 | 76.29 |
