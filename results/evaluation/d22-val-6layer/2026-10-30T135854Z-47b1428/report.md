# evaluation on val (D21 §4)

82 labelled instances; budget 200,000 expansions; torch threads 1. Ratios are model / baseline, geometric mean [bootstrap 95% CI over instances]; < 1 means the model expands fewer nodes or is faster.

## Expansions

| model | h0 | hmax | hsp | hadd | lmcut |
|---|---|---|---|---|---|
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 | 0.039 [0.029, 0.053] | 0.595 [0.524, 0.667] | 0.094 [0.073, 0.121] | 1.010 [0.988, 1.033] | 0.943 [0.893, 0.990] |

## End-to-end time

| model | h0 | hmax | hsp | hadd | lmcut |
|---|---|---|---|---|---|
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 | 10.025 [7.520, 13.156] | 8.531 [7.624, 9.515] | 2.627 [2.029, 3.343] | 15.371 [14.611, 16.175] | 0.952 [0.873, 1.038] |

## Plan cost and coverage

| model | solved | budget hits | optimal | plan cost / h* | fewer / more expansions than LM-cut | sibling order acc. (tie rate, pairs) |
|---|---|---|---|---|---|---|
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 | 82/82 | 0 | 52 | 1.054 [1.033, 1.077] | 20 / 15 | 0.921 (0.000, 15605) |

## Overestimation (effort units)

| model | states | rate h_θ > h* | mean violation | max violation | mean abs error |
|---|---|---|---|---|---|
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 (walk) | 7637 | 1.000 | 98.129 | 179.888 | 98.129 |
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 (astar_expanded) | 1509 | 1.000 | 136.975 | 189.393 | 136.975 |
| d22-6layer/gnnres-64x6-lr0.001-rank-s0 (successor) | 6114 | 1.000 | 125.790 | 179.888 | 125.790 |
