# training d23t1/mlp-64-lr0.001-mse-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "mlp", "lam": 1.0, "layers": 3, "loss": "mse", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 0, "target": "hstar", "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 9.7971 at epoch 10 of 16; wall time 6.1 s (encoding 0.1 s); torch threads 1.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 11.9372 | 10.6259 | 0.36 |
| 1 | 9.6925 | 10.5178 | 0.38 |
| 2 | 9.4344 | 10.3684 | 0.38 |
| 3 | 9.2740 | 10.6372 | 0.38 |
| 4 | 9.1376 | 10.2144 | 0.38 |
| 5 | 9.0169 | 10.4333 | 0.40 |
| 6 | 8.9196 | 10.0790 | 0.37 |
| 7 | 8.8414 | 10.4698 | 0.37 |
| 8 | 8.7733 | 10.2100 | 0.38 |
| 9 | 8.7216 | 10.1383 | 0.38 |
| 10 | 8.6760 | 9.7971 | 0.37 |
| 11 | 8.6315 | 9.8370 | 0.37 |
| 12 | 8.5737 | 9.9394 | 0.37 |
| 13 | 8.5400 | 10.0258 | 0.37 |
| 14 | 8.4939 | 10.2685 | 0.37 |
| 15 | 8.4521 | 9.9434 | 0.37 |
