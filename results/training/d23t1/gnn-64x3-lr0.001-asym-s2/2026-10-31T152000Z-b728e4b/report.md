# training d23t1/gnn-64x3-lr0.001-asym-s2

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "gnn", "lam": 1.0, "layers": 3, "loss": "asym", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 2, "target": "hstar", "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 5.6606 at epoch 9 of 15; wall time 3692.8 s (encoding 0.4 s); torch threads 1.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 23.4381 | 25.6523 | 247.22 |
| 1 | 15.4667 | 13.0994 | 262.36 |
| 2 | 12.4101 | 9.5580 | 270.88 |
| 3 | 10.6768 | 8.1814 | 285.85 |
| 4 | 9.2708 | 11.7594 | 289.47 |
| 5 | 9.1389 | 7.9461 | 297.68 |
| 6 | 8.0733 | 7.6444 | 307.71 |
| 7 | 7.4627 | 7.7398 | 231.50 |
| 8 | 7.1339 | 6.0307 | 211.13 |
| 9 | 7.4140 | 5.6606 | 212.44 |
| 10 | 6.8711 | 8.1712 | 209.70 |
| 11 | 6.6904 | 6.1541 | 206.47 |
| 12 | 6.5401 | 7.4378 | 207.40 |
| 13 | 5.6148 | 7.9995 | 201.91 |
| 14 | 5.2322 | 5.6680 | 202.99 |
