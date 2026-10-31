# evaluation on val (D21 §4)

82 labelled instances; budget 200,000 expansions; torch threads 1. Ratios are model / baseline, geometric mean [bootstrap 95% CI over instances]; < 1 means the model expands fewer nodes or is faster.

## Expansions

| model | h0 | hmax | hsp | hadd | lmcut |
|---|---|---|---|---|---|
| d23/gnnres-64x3-lr0.001-rank-s0 | 0.039 [0.029, 0.052] | 0.590 [0.521, 0.662] | 0.093 [0.072, 0.120] | 1.002 [0.983, 1.021] | 0.935 [0.889, 0.976] |
| d22/gnnres-64x3-lr0.001-rank-s0 | 0.039 [0.029, 0.053] | 0.595 [0.526, 0.665] | 0.094 [0.073, 0.121] | 1.011 [0.990, 1.033] | 0.944 [0.900, 0.985] |

## End-to-end time

| model | h0 | hmax | hsp | hadd | lmcut |
|---|---|---|---|---|---|
| d23/gnnres-64x3-lr0.001-rank-s0 | 6.250 [4.728, 8.214] | 5.308 [4.737, 5.923] | 1.637 [1.263, 2.092] | 9.693 [9.213, 10.216] | 0.600 [0.549, 0.655] |
| d22/gnnres-64x3-lr0.001-rank-s0 | 6.286 [4.697, 8.308] | 5.339 [4.761, 5.971] | 1.646 [1.280, 2.118] | 9.749 [9.199, 10.325] | 0.604 [0.550, 0.660] |

## Plan cost and coverage

| model | solved | budget hits | optimal | plan cost / h* | fewer / more expansions than LM-cut | sibling order acc. (tie rate, pairs) |
|---|---|---|---|---|---|---|
| d23/gnnres-64x3-lr0.001-rank-s0 | 82/82 | 0 | 63 | 1.028 [1.014, 1.045] | 20 / 8 | 0.934 (0.000, 15605) |
| d22/gnnres-64x3-lr0.001-rank-s0 | 82/82 | 0 | 61 | 1.039 [1.022, 1.059] | 18 / 8 | 0.931 (0.000, 15605) |

## Overestimation (effort units)

| model | states | rate h_θ > h* | mean violation | max violation | mean abs error |
|---|---|---|---|---|---|
| d23/gnnres-64x3-lr0.001-rank-s0 (walk) | 7637 | 1.000 | 47.704 | 132.022 | 47.704 |
| d23/gnnres-64x3-lr0.001-rank-s0 (astar_expanded) | 1509 | 1.000 | 79.988 | 142.110 | 79.988 |
| d23/gnnres-64x3-lr0.001-rank-s0 (successor) | 6114 | 0.999 | 67.850 | 132.022 | 67.750 |
| d22/gnnres-64x3-lr0.001-rank-s0 (walk) | 7637 | 1.000 | 38.392 | 115.250 | 38.392 |
| d22/gnnres-64x3-lr0.001-rank-s0 (astar_expanded) | 1509 | 1.000 | 67.714 | 123.999 | 67.714 |
| d22/gnnres-64x3-lr0.001-rank-s0 (successor) | 6114 | 1.000 | 56.421 | 115.250 | 56.411 |
