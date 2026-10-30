# training search/mlp-128-mse-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 128, "irls_rounds": 10, "kind": "mlp", "lam": 1.0, "layers": 3, "loss": "mse", "lr": 0.003, "max_epochs": 30, "patience": 5, "seed": 0, "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 9.8246 at epoch 4 of 10; wall time 4.4 s (encoding 0.0 s); torch threads 4.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 10.3285 | 10.6002 | 0.44 |
| 1 | 9.4109 | 10.4522 | 0.43 |
| 2 | 9.1381 | 10.3301 | 0.42 |
| 3 | 8.9152 | 10.4308 | 0.44 |
| 4 | 8.6595 | 9.8246 | 0.43 |
| 5 | 8.4038 | 9.9838 | 0.44 |
| 6 | 8.2241 | 9.9123 | 0.43 |
| 7 | 8.0893 | 10.3888 | 0.43 |
| 8 | 7.9648 | 10.5197 | 0.42 |
| 9 | 7.8913 | 10.0934 | 0.44 |
