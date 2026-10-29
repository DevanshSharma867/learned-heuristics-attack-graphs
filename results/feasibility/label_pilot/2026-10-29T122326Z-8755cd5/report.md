# label_pilot

D19 label pilot. Feasibility and sizing only; no model is trained.

## train-677e9fe4-8755cd5-pilot (train; 1 worker(s); commit 8755cd5)

- instances: 84, labelled 58; failures {'unreachable': 26}
- states: 9588 (61 goal states); per labelled instance mean 165.3, median 154, max 348
- mean states per instance by source (a state counts once per source): optimal_path 9.2, walk 96.1, expanded_lmcut 9.6, expanded_hmax 21.7, successor 80.8
- successors before the cap: median 61; capped on 7 instances
- init expansions, median: LM-cut 8, h_max 11
- oracle: 3915 states checked, 0 over its pop budget; enumeration on 30 instances

h\* in effort units (quantiles 0, 0.1, 0.25, 0.5, 0.75, 0.9, 1):

| states | q0 | q0.1 | q0.25 | q0.5 | q0.75 | q0.9 | q1 |
|---|---|---|---|---|---|---|---|
| all | 0.00 | 2.00 | 3.61 | 6.45 | 9.79 | 14.00 | 32.61 |
| optimal_path | 0.00 | 0.00 | 3.00 | 7.03 | 11.21 | 16.58 | 32.61 |
| walk | 1.00 | 1.00 | 3.61 | 6.00 | 9.45 | 13.21 | 32.61 |
| expanded_lmcut | 1.00 | 2.89 | 5.00 | 8.97 | 13.58 | 19.89 | 32.61 |
| expanded_hmax | 1.00 | 4.00 | 6.61 | 10.63 | 16.29 | 20.61 | 32.61 |
| successor | 0.00 | 2.00 | 4.00 | 7.50 | 11.21 | 15.63 | 32.61 |

- time per instance (s): mean 1.79, median 0.68, max 14.59
- time per state (s): 0.0109 mean (search 0.0083, cross-checks 0.0022); per-instance median 0.0045
- disk: 103.9 kB (38.2 kB labels); elapsed 104.2 s

## val-677e9fe4-8755cd5-pilot (val; 1 worker(s); commit 8755cd5)

- instances: 28, labelled 24; failures {'unreachable': 4}
- states: 3669 (27 goal states); per labelled instance mean 152.9, median 147, max 292
- mean states per instance by source (a state counts once per source): optimal_path 8.8, walk 92.4, expanded_lmcut 8.7, expanded_hmax 18.6, successor 76.1
- successors before the cap: median 61; capped on 1 instances
- init expansions, median: LM-cut 8, h_max 10.5
- oracle: 1620 states checked, 0 over its pop budget; enumeration on 13 instances

h\* in effort units (quantiles 0, 0.1, 0.25, 0.5, 0.75, 0.9, 1):

| states | q0 | q0.1 | q0.25 | q0.5 | q0.75 | q0.9 | q1 |
|---|---|---|---|---|---|---|---|
| all | 0.00 | 1.00 | 3.00 | 5.03 | 8.61 | 13.05 | 27.95 |
| optimal_path | 0.00 | 0.00 | 2.00 | 6.00 | 10.03 | 15.05 | 27.95 |
| walk | 1.00 | 1.00 | 2.00 | 5.00 | 8.39 | 13.42 | 27.95 |
| expanded_lmcut | 1.00 | 2.00 | 4.00 | 7.03 | 11.61 | 15.21 | 27.95 |
| expanded_hmax | 1.00 | 3.00 | 6.00 | 10.61 | 14.21 | 19.50 | 27.95 |
| successor | 0.00 | 2.00 | 3.00 | 6.03 | 9.61 | 14.21 | 27.95 |

- time per instance (s): mean 1.30, median 0.75, max 6.28
- time per state (s): 0.0085 mean (search 0.0064, cross-checks 0.0018); per-instance median 0.0046
- disk: 41.1 kB (14.6 kB labels); elapsed 31.3 s

## Projection (pooled pilot rates)

Labelled fraction 0.732; 161.7 states and 1.65 s per labelled instance; 4.0 bytes per label (gzip).

| split | seeds | labelled (exp.) | states | CPU-hours | labels MB |
|---|---|---|---|---|---|
| train | 600 | 439 | 71,020 | 0.20 | 0.28 |
| val | 100 | 73 | 11,837 | 0.03 | 0.05 |
| test_id | 100 | 73 | 11,837 | 0.03 | 0.05 |
| test_vuln | 100 | 73 | 11,837 | 0.03 | 0.05 |
| test_vuln_cost | 100 | 73 | 11,837 | 0.03 | 0.05 |
| total |  | 732 | 118,366 | 0.34 | 0.47 |

test_size (n = 30) and test_structure (hub_and_spoke) are outside the pilot distribution and are not projected here.
