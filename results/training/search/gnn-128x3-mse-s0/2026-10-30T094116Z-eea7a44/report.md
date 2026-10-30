# training search/gnn-128x3-mse-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 128, "irls_rounds": 10, "kind": "gnn", "lam": 1.0, "layers": 3, "loss": "mse", "lr": 0.003, "max_epochs": 30, "patience": 5, "seed": 0, "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 4.7593 at epoch 7 of 8; wall time 1697.3 s (encoding 0.6 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 17.4489 | 12.5694 | 212.21 |
| 1 | 10.9705 | 13.4950 | 210.57 |
| 2 | 9.1698 | 6.0344 | 209.93 |
| 3 | 7.4750 | 7.9851 | 208.35 |
| 4 | 7.2248 | 5.4291 | 210.39 |
| 5 | 5.9194 | 7.2762 | 209.98 |
| 6 | 5.4383 | 10.4737 | 207.41 |
| 7 | 4.9117 | 4.7593 | 207.93 |
