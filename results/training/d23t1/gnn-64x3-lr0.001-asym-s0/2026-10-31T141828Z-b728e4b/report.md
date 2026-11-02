# training d23t1/gnn-64x3-lr0.001-asym-s0

```
{"batch_size": 256, "device": "cpu", "hidden": 64, "irls_rounds": 10, "kind": "gnn", "lam": 1.0, "layers": 3, "loss": "asym", "lr": 0.001, "max_epochs": 30, "patience": 5, "seed": 0, "target": "hstar", "train_batches": ["data/labels/train-677e9fe4-72e8821"], "val_batches": ["data/labels/val-677e9fe4-72e8821"], "w_over": 4.0}
```

Best val loss 6.7373 at epoch 8 of 14; wall time 2826.4 s (encoding 0.4 s); torch threads 1.

| epoch | train loss | val loss | epoch s |
|---|---|---|---|
| 0 | 24.6029 | 15.8535 | 212.43 |
| 1 | 15.2326 | 12.4446 | 203.95 |
| 2 | 12.5900 | 9.4984 | 192.39 |
| 3 | 10.6311 | 10.4366 | 192.60 |
| 4 | 9.9245 | 9.1979 | 189.52 |
| 5 | 8.4814 | 8.5884 | 192.76 |
| 6 | 7.7868 | 11.6923 | 186.75 |
| 7 | 7.5298 | 7.6813 | 192.90 |
| 8 | 7.1040 | 6.7373 | 187.68 |
| 9 | 6.7586 | 7.2639 | 187.77 |
| 10 | 6.5542 | 8.1909 | 192.19 |
| 11 | 5.5815 | 7.5654 | 203.47 |
| 12 | 6.0561 | 7.8953 | 222.17 |
| 13 | 5.9652 | 10.1909 | 232.75 |
