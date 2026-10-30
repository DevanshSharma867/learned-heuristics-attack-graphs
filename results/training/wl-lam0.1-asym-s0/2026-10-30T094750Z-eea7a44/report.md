# training wl-lam0.1-asym-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "wl", "lam": 0.1, "layers": 3, "loss": "asym", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 0, "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 22.2077 at epoch 2 of 10; wall time 363.1 s (encoding 72.9 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 1.3035 | 24.5444 | 29.37 |
| 1 | 1.0805 | 22.4311 | 28.77 |
| 2 | 1.0135 | 22.2077 | 28.79 |
| 3 | 1.0104 | 22.2729 | 28.96 |
| 4 | 1.0166 | 22.2507 | 29.03 |
| 5 | 1.0184 | 22.3283 | 28.86 |
| 6 | 1.0179 | 22.2175 | 29.19 |
| 7 | 1.0149 | 22.3366 | 29.09 |
| 8 | 1.0260 | 22.3231 | 29.01 |
| 9 | 1.0220 | 22.3337 | 29.14 |
