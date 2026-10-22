# landscape_small_n

PR-gated attack graphs, families flat, tiered, hub_and_spoke, n in [6, 8, 12]. Costs in D9 integer units (38 per effort unit). Expansion budget 200,000; up to 300 sampled non-goal states per instance.

h* is from A*+LM-cut, cross-checked against A*+h_max on every state and against full enumeration on every enumerated instance. No mismatch and no admissible heuristic above h* occurred (either would have aborted the run).

**Gap columns.** `h<h*` is the fraction of states where the heuristic is strictly below h*. `mean gap` is the mean of h* − h over *all* evaluated states (zeros included); `max gap` is the largest.

## Instances and initial-state search

| family | n | seeds | reachable | unreachable | h* unknown | median plan len | median h* | median exp. h0 | h0 at budget | median exp. h_max | median exp. LM-cut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flat | 6 | 20 | 18 | 2 | 0 | 3 | 267 | 10 | 0/18 | 3 | 3 |
| tiered | 6 | 20 | 12 | 8 | 0 | 4 | 325.5 | 9.5 | 0/12 | 4 | 4 |
| hub_and_spoke | 6 | 20 | 13 | 7 | 0 | 4 | 267 | 6 | 0/13 | 4 | 4 |
| flat | 8 | 20 | 19 | 1 | 0 | 3 | 213 | 23 | 0/19 | 3 | 3 |
| tiered | 8 | 20 | 15 | 5 | 0 | 4 | 442 | 14 | 0/15 | 5 | 4 |
| hub_and_spoke | 8 | 20 | 15 | 5 | 0 | 4 | 404 | 20 | 0/15 | 4 | 4 |
| flat | 12 | 20 | 18 | 2 | 0 | 3 | 182.5 | 20.5 | 0/18 | 3 | 3 |
| tiered | 12 | 20 | 19 | 1 | 0 | 5 | 478 | 57 | 0/19 | 6 | 5 |
| hub_and_spoke | 12 | 20 | 17 | 3 | 0 | 4 | 251 | 55 | 0/17 | 4 | 4 |

`h0 at budget` counts instances where uniform-cost search stopped at the budget; their expansion count is a lower bound. The median is marked as a lower bound when at least half the cell hit the budget.

## Sampled states: h_max and LM-cut versus h*

| family | n | states | instances at cap | h* unknown | h_max h<h* | h_max mean gap | h_max max gap | LM-cut h<h* | LM-cut mean gap | LM-cut max gap |
|---|---|---|---|---|---|---|---|---|---|---|
| flat | 6 | 567 | 0/18 | 0 | 0.035 | 1.3 | 38 | 0.000 | 0.0 | 0 |
| tiered | 6 | 212 | 0/12 | 0 | 0.071 | 2.3 | 38 | 0.000 | 0.0 | 0 |
| hub_and_spoke | 6 | 312 | 0/13 | 0 | 0.032 | 1.2 | 38 | 0.000 | 0.0 | 0 |
| flat | 8 | 2300 | 0/19 | 0 | 0.011 | 0.4 | 38 | 0.000 | 0.0 | 0 |
| tiered | 8 | 842 | 0/15 | 0 | 0.070 | 5.2 | 191 | 0.019 | 1.0 | 85 |
| hub_and_spoke | 8 | 1073 | 0/15 | 0 | 0.001 | 0.0 | 38 | 0.000 | 0.0 | 0 |
| flat | 12 | 5389 | 17/18 | 0 | 0.032 | 1.2 | 76 | 0.000 | 0.0 | 0 |
| tiered | 12 | 4882 | 10/19 | 0 | 0.042 | 1.6 | 76 | 0.000 | 0.0 | 27 |
| hub_and_spoke | 12 | 4983 | 15/17 | 0 | 0.005 | 0.2 | 38 | 0.000 | 0.0 | 0 |

`instances at cap` counts instances that yielded the full 300 distinct states; the rest exhausted the walk budget first, i.e. the sample is every distinct state the walks found.

## Sampled versus exact (full enumeration of reachable non-goal states)

| family | n | enumerated | states (sampled / all) | h_max h<h* (sampled / all) | h_max mean gap (s / all) | LM-cut h<h* (sampled / all) | LM-cut mean gap (s / all) |
|---|---|---|---|---|---|---|---|
| flat | 6 | 18/18 | 567 / 597 | 0.035 / 0.037 | 1.3 / 1.4 | 0.000 / 0.000 | 0.0 / 0.0 |
| tiered | 6 | 12/12 | 212 / 230 | 0.071 / 0.078 | 2.3 / 2.7 | 0.000 / 0.000 | 0.0 / 0.0 |
| hub_and_spoke | 6 | 13/13 | 312 / 325 | 0.032 / 0.037 | 1.2 / 1.4 | 0.000 / 0.000 | 0.0 / 0.0 |
| flat | 8 | 19/19 | 2300 / 2847 | 0.011 / 0.009 | 0.4 / 0.4 | 0.000 / 0.000 | 0.0 / 0.0 |
| tiered | 8 | 15/15 | 842 / 982 | 0.070 / 0.072 | 5.2 / 5.3 | 0.019 / 0.017 | 1.0 / 0.9 |
| hub_and_spoke | 8 | 15/15 | 1073 / 1245 | 0.001 / 0.002 | 0.0 / 0.1 | 0.000 / 0.000 | 0.0 / 0.0 |
| flat | 12 | 18/18 | 5389 / 50335 | 0.032 / 0.020 | 1.2 / 0.8 | 0.000 / 0.000 | 0.0 / 0.0 |
| tiered | 12 | 19/19 | 4882 / 20230 | 0.042 / 0.032 | 1.6 / 1.3 | 0.000 / 0.000 | 0.0 / 0.0 |
| hub_and_spoke | 12 | 17/17 | 4983 / 26136 | 0.005 / 0.001 | 0.2 / 0.0 | 0.000 / 0.000 | 0.0 / 0.0 |

Enumeration is attempted up to 50,000 reachable states per instance. Both columns use only the enumerated instances. Fractions are pooled over states, so instances with many states weigh more in the `all` column.

## Generation failures (UnreachableGoal)

- flat n=6 seed=13: execCode(lan-2) unreachable in {'family': 'flat', 'seed': 13, 'params': {'n_hosts': 6, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=6 seed=14: execCode(lan-6) unreachable in {'family': 'flat', 'seed': 14, 'params': {'n_hosts': 6, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=0: execCode(tier2-5) unreachable in {'family': 'tiered', 'seed': 0, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=1: execCode(tier2-5) unreachable in {'family': 'tiered', 'seed': 1, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=5: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 5, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=8: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 8, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=9: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 9, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=13: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 13, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=17: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 17, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=6 seed=19: execCode(tier2-6) unreachable in {'family': 'tiered', 'seed': 19, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=6 seed=0: execCode(spoke-5) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=2: execCode(spoke-4) unreachable in {'family': 'hub_and_spoke', 'seed': 2, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=10: execCode(spoke-5) unreachable in {'family': 'hub_and_spoke', 'seed': 10, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=12: execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 12, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=14: execCode(spoke-5) unreachable in {'family': 'hub_and_spoke', 'seed': 14, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=16: execCode(spoke-3) unreachable in {'family': 'hub_and_spoke', 'seed': 16, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=6 seed=17: execCode(spoke-4) unreachable in {'family': 'hub_and_spoke', 'seed': 17, 'params': {'n_hosts': 6, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- flat n=8 seed=0: execCode(lan-8) unreachable in {'family': 'flat', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=8 seed=1: execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 1, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=8 seed=5: execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 5, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=8 seed=9: execCode(tier2-7) unreachable in {'family': 'tiered', 'seed': 9, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=8 seed=11: execCode(tier2-7) unreachable in {'family': 'tiered', 'seed': 11, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=8 seed=17: execCode(tier2-8) unreachable in {'family': 'tiered', 'seed': 17, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=8 seed=0: execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 0, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 seed=12: execCode(spoke-3) unreachable in {'family': 'hub_and_spoke', 'seed': 12, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 seed=14: execCode(spoke-6) unreachable in {'family': 'hub_and_spoke', 'seed': 14, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 seed=16: execCode(spoke-8) unreachable in {'family': 'hub_and_spoke', 'seed': 16, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=8 seed=17: execCode(spoke-2) unreachable in {'family': 'hub_and_spoke', 'seed': 17, 'params': {'n_hosts': 8, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- flat n=12 seed=7: execCode(lan-10) unreachable in {'family': 'flat', 'seed': 7, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- flat n=12 seed=11: execCode(lan-12) unreachable in {'family': 'flat', 'seed': 11, 'params': {'n_hosts': 12, 'services': [1, 3], 'p_exposed': 0.2, 'p_reach': 0.3, 'p_trust': 0.05}, 'schema_version': 1}
- tiered n=12 seed=1: execCode(tier2-9) unreachable in {'family': 'tiered', 'seed': 1, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_tiers': 3, 'p_exposed': 0.5, 'p_intra': 0.3, 'p_down': 0.2, 'p_trust': 0.05}, 'schema_version': 1}
- hub_and_spoke n=12 seed=16: execCode(spoke-7) unreachable in {'family': 'hub_and_spoke', 'seed': 16, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 seed=17: execCode(spoke-2) unreachable in {'family': 'hub_and_spoke', 'seed': 17, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
- hub_and_spoke n=12 seed=18: execCode(spoke-7) unreachable in {'family': 'hub_and_spoke', 'seed': 18, 'params': {'n_hosts': 12, 'services': [1, 3], 'n_hubs': 1, 'p_exposed': 0.2, 'p_link': 0.5, 'p_trust': 0.3}, 'schema_version': 1}
