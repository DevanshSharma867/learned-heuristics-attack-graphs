# training search/wl-lam0.1-mse-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "wl", "lam": 0.1, "layers": 3, "loss": "mse", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 0, "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 11.7125 at epoch 0 of 1; wall time 372.8 s (encoding 341.2 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 0.5210 | 11.7125 | 31.60 |
