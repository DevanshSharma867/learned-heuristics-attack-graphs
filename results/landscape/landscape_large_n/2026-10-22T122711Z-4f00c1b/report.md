# landscape_large_n

PR-gated attack graphs, families flat, tiered, hub_and_spoke, n in [20, 30, 40]. Costs in D9 integer units (38 per effort unit). Expansion budget 200,000; up to 300 sampled non-goal states per instance.

h* is from A*+LM-cut, cross-checked against A*+h_max on every state . No mismatch and no admissible heuristic above h* occurred (either would have aborted the run).

**Gap columns.** `h<h*` is the fraction of states where the heuristic is strictly below h*. `mean gap` is the mean of h* − h over *all* evaluated states (zeros included); `max gap` is the largest.

## Instances and initial-state search

| family | n | seeds | reachable | unreachable | h* unknown | median plan len | median h* | median exp. h0 | h0 at budget | median exp. h_max | median exp. LM-cut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flat | 20 | 15 | 15 | 0 | 0 | 3 | 152 | 566 | 0/15 | 3 | 3 |
| tiered | 20 | 15 | 15 | 0 | 0 | 4 | 240 | 492 | 0/15 | 4 | 4 |
| hub_and_spoke | 20 | 16 | 15 | 1 | 0 | 3 | 251 | 37 | 0/15 | 3 | 3 |
| flat | 30 | 15 | 15 | 0 | 0 | 2 | 114 | 65 | 1/15 | 2 | 2 |
| tiered | 30 | 15 | 15 | 0 | 0 | 4 | 190 | 686 | 0/15 | 5 | 4 |
| hub_and_spoke | 30 | 16 | 15 | 1 | 0 | 4 | 251 | 226 | 2/15 | 4 | 4 |
| flat | 40 | 15 | 15 | 0 | 0 | 2 | 76 | 47 | 2/15 | 2 | 2 |
| tiered | 40 | 15 | 15 | 0 | 0 | 4 | 152 | 421 | 1/15 | 4 | 4 |
| hub_and_spoke | 40 | 15 | 15 | 0 | 0 | 4 | 251 | 236 | 2/15 | 4 | 4 |

`h0 at budget` counts instances where uniform-cost search stopped at the budget; their expansion count is a lower bound. The median is marked as a lower bound when at least half the cell hit the budget.

## Sampled states: h_max and LM-cut versus h*

| family | n | states | instances at cap | h* unknown | h_max h<h* | h_max mean gap | h_max max gap | LM-cut h<h* | LM-cut mean gap | LM-cut max gap |
|---|---|---|---|---|---|---|---|---|---|---|
| flat | 20 | 4500 | 15/15 | 0 | 0.050 | 1.8 | 38 | 0.006 | 0.0 | 38 |
| tiered | 20 | 4500 | 15/15 | 0 | 0.070 | 2.3 | 76 | 0.009 | 0.3 | 38 |
| hub_and_spoke | 20 | 4500 | 15/15 | 0 | 0.001 | 0.0 | 38 | 0.000 | 0.0 | 0 |
| flat | 30 | 4500 | 15/15 | 0 | 0.024 | 0.9 | 38 | 0.010 | 0.4 | 38 |
| tiered | 30 | 4500 | 15/15 | 0 | 0.064 | 2.5 | 76 | 0.006 | 0.2 | 38 |
| hub_and_spoke | 30 | 4500 | 15/15 | 0 | 0.026 | 1.0 | 38 | 0.000 | 0.0 | 0 |
| flat | 40 | 4500 | 15/15 | 0 | 0.020 | 0.8 | 76 | 0.008 | 0.3 | 76 |
| tiered | 40 | 4500 | 15/15 | 0 | 0.033 | 1.2 | 38 | 0.019 | 0.7 | 38 |
| hub_and_spoke | 40 | 4500 | 15/15 | 0 | 0.011 | 0.4 | 38 | 0.000 | 0.0 | 0 |

`instances at cap` counts instances that yielded the full 300 distinct states; the rest exhausted the walk budget first, i.e. the sample is every distinct state the walks found.

## Generation failures (UnreachableGoal)

- hub_and_spoke n=20 seed=1: execCode(spoke-12) unreachable in {'family': 'hub_and_spoke', 'seed': 1, 'params': {'n_hosts': 20, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=30 seed=12: execCode(spoke-30) unreachable in {'family': 'hub_and_spoke', 'seed': 12, 'params': {'n_hosts': 30, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
