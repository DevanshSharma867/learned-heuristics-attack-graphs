# training search/mlp-64-mse-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "mlp", "lam": 1.0, "layers": 3, "loss": "mse", "lr": 0.003, "max_epochs": 30, "patience": 5, "seed": 0, "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 10.0106 at epoch 6 of 12; wall time 3.6 s (encoding 0.0 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 10.7301 | 10.5527 | 0.30 |
| 1 | 9.4777 | 10.6417 | 0.30 |
| 2 | 9.2665 | 10.5515 | 0.30 |
| 3 | 9.1298 | 10.6193 | 0.30 |
| 4 | 8.9706 | 10.1660 | 0.30 |
| 5 | 8.8359 | 10.2887 | 0.30 |
| 6 | 8.7023 | 10.0106 | 0.30 |
| 7 | 8.5660 | 10.7199 | 0.30 |
| 8 | 8.4600 | 10.5598 | 0.30 |
| 9 | 8.3533 | 10.3253 | 0.30 |
| 10 | 8.2708 | 10.1617 | 0.31 |
| 11 | 8.1984 | 10.2523 | 0.30 |
