# Exactness of h_max and LM-cut by state population (val-677e9fe4-72e8821)

82 labelled instances. Each cell: fraction with h = h\* (mean gap; max gap, effort units; states). All reachable states: the 36 instances with at most 2,000 reachable states (state-weighted; instance-weighted in its own column).

| heuristic | initial states | all reachable (state-wt.) | all reachable (inst.-wt.) | label states (all) | label: optimal_path | label: walk | label: expanded_lmcut | label: expanded_hmax | label: successor |
|---|---|---|---|---|---|---|---|---|---|
| hmax | 0.256 (1.97; 8.87; 82) | 0.828 (0.34; 9.87; 18,327) | 0.802 | 0.652 (0.62; 9.87; 12,402) | 0.627 (0.63; 8.87; 721) | 0.727 (0.46; 9.87; 7,637) | 0.513 (0.94; 8.87; 721) | 0.216 (2.04; 9.87; 1,432) | 0.491 (0.96; 9.87; 6,114) |
| lmcut | 0.732 (0.29; 2.00; 82) | 0.993 (0.01; 2.00; 18,327) | 0.986 | 0.939 (0.06; 2.00; 12,402) | 0.904 (0.10; 2.00; 721) | 0.956 (0.04; 2.00; 7,637) | 0.791 (0.22; 2.00; 721) | 0.806 (0.20; 2.00; 1,432) | 0.898 (0.10; 2.00; 6,114) |

By cell (initial states; fraction exact, h_max / LM-cut):

| variant | n | D | instances | h_max | LM-cut |
|---|---|---|---|---|---|
| flat | 12 | 2 | 13 | 5/13 | 12/13 |
| flat | 12 | 3 | 12 | 2/12 | 5/12 |
| flat | 20 | 2 | 9 | 3/9 | 5/9 |
| flat | 20 | 3 | 7 | 3/7 | 5/7 |
| tiered3 | 12 | 2 | 7 | 4/7 | 6/7 |
| tiered3 | 12 | 3 | 4 | 0/4 | 3/4 |
| tiered3 | 20 | 2 | 7 | 1/7 | 5/7 |
| tiered3 | 20 | 3 | 7 | 1/7 | 7/7 |
| tiered5 | 12 | 2 | 5 | 2/5 | 4/5 |
| tiered5 | 12 | 3 | 3 | 0/3 | 2/3 |
| tiered5 | 20 | 2 | 4 | 0/4 | 3/4 |
| tiered5 | 20 | 3 | 4 | 0/4 | 3/4 |
