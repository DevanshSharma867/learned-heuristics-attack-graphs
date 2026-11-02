# AUDIT_2 — Why are `h_max` and LM-cut near-exact?

**Scope:** targeted follow-up to AUDIT_1. AUDIT_1 was not edited. This pass examines the heuristic values themselves, not only A* solution costs.

## Executive conclusion

The measurements support a mixed answer:

1. **No heuristic implementation bug was found.** In 61 train-style generated tasks, an independently implemented frozenset-based dynamic program reproduced the repository's exact cost-to-go labels for all 61,873 reachable states. Across those states, neither `h_max` nor LM-cut ever exceeded the exact remaining cost. A separate 1,000-task admissibility stress test also found no overestimation. This is strong evidence against a bug in the tested code paths, not a proof for every possible task.
2. **LM-cut really is very close to exact on the generated attack tasks.** It was exact on 99.81% of all reachable states in the train-style sample, and on 86.9% of the sampled initial states. It is not universally exact: 116/61,873 reachable states had a positive gap, with a maximum gap of 148 cost units.
3. **The result is materially model-dependent.** The tasks are delete-free, have one target fact, represent control as a binary per-host `execCode` fact, and fold intermediate attack facts into actions. These restrictions remove many interactions present in operational attack scenarios. The more constrained D2/D3 and coupling variants still have LM-cut near-exactness, but `h_max` becomes much weaker.
4. **The headline depends on which states are measured.** On the same train-style sample, `h_max` was exact at only 10/61 initial states, despite being exact on 92.75% of all reachable states. LM-cut was exact at 53/61 initial states. A pooled all-state percentage must not be presented as the expected accuracy at A* start states or at the states selected by the label pipeline.

| Question | Classification | Confidence | Finding |
|---|---|---:|---|
| Is there evidence of a bug in `h_max` or LM-cut? | **BUG — not observed** | High for tested states; not universal proof | No overestimation or DP/oracle disagreement found in the tested attack tasks. |
| Is near-exactness a property of the task formulation? | **MODELLING CHOICE** | High | Monotone, delete-free, single-goal, binary-host facts substantially simplify the planning problem. |
| Can the aggregate exactness rate mislead? | **METRIC ISSUE** | High | Initial states, uniformly pooled reachable states, and label-pipeline states have materially different heuristic-gap distributions. |
| Are small positive LM-cut gaps themselves defects? | **FINE** | High | They are expected for an admissible approximation; they do not indicate overestimation or incorrect search. |

---

## 1. What the code actually asks the heuristics to estimate

### 1.1 The task is monotone and single-goal

`src/ahg/attack_graph.py:1-20` defines the main facts as `attackerLocated(internet)` and one `execCode(host)` fact per internal host. The goal built at `src/ahg/attack_graph.py:176` is the single fact `execCode(target)`. The comments at lines 17-20 explain that intermediate MulVAL-style facts such as `netAccess`, `canAccessHost`, and `principalCompromised` are folded into the actions that consume them.

All useful actions add facts and never delete them. `src/ahg/task.py:1-10` describes this delete-free state representation; `src/ahg/task.py:78-86` emits only applicable actions that add something new. As a consequence, every useful transition strictly increases the number of facts held, and the reachable state graph is a DAG.

Delete-free does **not** mean that `h_max` or LM-cut must be exact. It means that the delete relaxation is identical to the original task, so the optimal relaxed cost `h+` equals `h*`; `src/ahg/heuristics.py:13-15` says this explicitly. The heuristic implementations are still approximations to that optimal relaxed cost.

### 1.2 Action structure in the generated attack model

`src/ahg/attack_graph.py:147-154` creates one exploit action per reach edge. It normally requires only control of the source host and adds control of one destination host. Optional PR, coupling, and depth settings add further conjunctive prerequisites.

Login actions are different: `src/ahg/attack_graph.py:155-162` requires both a trust-source host and a host with network access to the destination login service (deduplicated when they are the same host), plus a depth credential when enabled. Credential-harvesting actions are unary (`src/ahg/attack_graph.py:171-175`).

The current train split uses flat, tiered3, and tiered5 families; host counts 12 and 20; D2/D3 credential depth; and the coupling grid (`src/ahg/splits.py:22-27, 57-80`). Its `instance_spec` sets `exposed_level0=True` (`src/ahg/splits.py:62-68`). `label_seed` passes those settings to `make_instance` but does not pass `pr_gated` (`src/ahg/labels.py:145-150`); `make_instance` defaults `pr_gated=False` (`src/ahg/attack_graph.py:247-261`). Thus the active train-style model in this pass includes depth and coupling prerequisites, but not the optional PR capability gates.

### 1.3 Why the two heuristics behave differently

- `h_max` computes a fact cost from the **maximum** cost of an action's prerequisites (`src/ahg/heuristics.py:29-40, 81-86, 95-96`). For an action requiring two independently obtained facts, this can charge the more expensive prerequisite while failing to charge the other one. That is the expected weakness of `h_max` on AND-preconditions, not a coding error.
- LM-cut repeatedly computes `h_max`, constructs a zero-cost goal zone, extracts a cut of actions that every solution must cross, charges the minimum residual cut cost, and reduces those action costs (`src/ahg/heuristics.py:127-140, 145-205`). It can therefore account additively for multiple required action landmarks that `h_max` merges with a maximum.

A small hand-built AND-fan-in task demonstrates the distinction. Two independent prerequisites each cost 10, and the final action costs 1: exact cost `h* = 21`, `h_max = 11`, LM-cut `= 21`. With three prerequisite branches costing 7, 9, and 11 and a final action costing 2: `h* = 29`, `h_max = 13`, LM-cut `= 29`. This is the expected mathematical behavior of the algorithms.

---

## 2. Measurement design

### 2.1 Train-style controlled sample

I generated the same *cell structure* as the current train split, but with a small reproducible seed sample:

- 12 hosts; flat, tiered3, and tiered5 topology families.
- Credential depth D=2 and D=3.
- Coupling `rho` in {0, 0.25, 0.5, 1.0}; share-pool `m` in {1, all hosts}.
- `exposed_level0=True`; `pr_gated=False`.
- Seeds 0 and 1 per cell: 96 generation attempts, 61 reachable tasks, and 35 `UnreachableGoal` generation outcomes. Unreachable tasks were not counted as solved instances.

The CVE records were synthetic: eight service families with a deliberately mixed set of exploitability scores and PR values. The actual CVE CSV was not read, so the cost formula and action-generation code are exercised, but these results do not claim to represent the empirical CVE distribution.

For each successful task, I enumerated every reachable state and computed exact `h*` by backward induction over the monotonic state DAG. I then independently reimplemented the enumeration using frozenset states and direct action-precondition/effect checks, without the repository's bitmask successor routine. The two exact label maps agreed on **all 61,873 states across all 61 tasks**. The independent uniform-cost oracle also agreed with the enumerated initial-state optimal cost on all 61 tasks.

### 2.2 Simpler baseline

To isolate the effect of the added constraints, I also tested the unconstrained model (`D=0`, no coupling, no PR gates): three topology families (flat, tiered, hub-and-spoke), 8 and 12 hosts, six seeds per cell. This produced 36 tasks and 33,307 reachable states.

### 2.3 Additional checks

- A 1,000-task random acyclic, delete-free planning stress test enumerated 17,954 reachable states and found zero `h_max` or LM-cut overestimations.
- A separate 5,000-task random one-goal planning sample found LM-cut exact on 4,976/5,000 initial states, with a maximum underestimation gap of 7 units. This confirms that LM-cut is not mathematically exact for arbitrary delete-free tasks.
- `pytest tests/test_core.py`: 485 passed.

---

## 3. Results

### 3.1 Unconstrained baseline: almost exact by construction of this task family

| Topology | Hosts | Tasks | Reachable states | `h_max` exact | LM-cut exact |
|---|---:|---:|---:|---:|---:|
| Flat | 8 | 6 | 901 | 100.00% | 100.00% |
| Flat | 12 | 6 | 13,322 | 99.80% | 100.00% |
| Tiered | 8 | 6 | 390 | 98.72% | 100.00% |
| Tiered | 12 | 6 | 7,272 | 98.10% | 100.00% |
| Hub-and-spoke | 8 | 6 | 574 | 100.00% | 100.00% |
| Hub-and-spoke | 12 | 6 | 10,848 | 100.00% | 100.00% |
| **Total** | — | **36** | **33,307** | **99.49%** | **100.00%** |

At the initial state, `h_max` was exact on 33/36 tasks and LM-cut on 36/36. The median number of multi-precondition actions in an optimal plan was zero; only 2/36 selected optimal plans used a multi-precondition action. This is a strong explanation for the near-exact `h_max` result in this simplified configuration: most optimal routes do not force the search to pay for multiple independent prerequisites at once.

### 3.2 Train-style D2/D3 plus coupling sample

| Heuristic | Exact states | Inexact states | Exact fraction | Maximum gap | Overestimates |
|---|---:|---:|---:|---:|---:|
| `h_max` | 57,388 | 4,485 | 92.751% | 278 units (7.32 effort units) | 0 |
| LM-cut | 61,757 | 116 | 99.813% | 148 units (3.89 effort units) | 0 |

The cost model stores 38 units per effort unit (`src/ahg/cost.py:1-13`), so gaps above are converted using that scale. Both heuristics remained admissible throughout the sweep. LM-cut was much closer to `h*`, but it was not exact everywhere.

The pooled state exactness differs by topology:

| Family | Tasks | Reachable states | `h_max` exact | LM-cut exact |
|---|---:|---:|---:|---:|
| Flat | 30 | 46,712 | 97.58% | 99.95% |
| Tiered3 | 24 | 13,474 | 77.85% | 99.32% |
| Tiered5 | 7 | 1,687 | 78.13% | 100.00% |

Tiered5 has only seven successful tasks in this small seed sample, so its 100% LM-cut result is weak evidence about that family in general. The tiered3 result is more informative: it contains most of the observed LM-cut misses and a substantial fraction of the `h_max` misses.

### 3.3 Initial-state values are a different story

Across the same 61 tasks:

| Heuristic | Exact initial states | Exact fraction | Median gap | Mean gap | Maximum gap |
|---|---:|---:|---:|---:|---:|
| `h_max` | 10/61 | 16.39% | 76 units | 92.67 units | 234 units |
| LM-cut | 53/61 | 86.89% | 0 units | 8.69 units | 83 units |

Initial-state breakdown:

| Family | Tasks | `h_max` exact | LM-cut exact |
|---|---:|---:|---:|
| Flat | 30 | 10/30 | 29/30 |
| Tiered3 | 24 | 0/24 | 17/24 |
| Tiered5 | 7 | 0/7 | 7/7 |

This is the most important correction to a single pooled exactness percentage. `h_max` being exact on 92.75% of reachable states does **not** mean it is close to exact at the start of these tasks. The full-state denominator contains many states after some prerequisite facts have already been acquired; those states are often easier for the heuristic. The initial state has not yet acquired any of those prerequisites.

The sampled optimal plans had a median length of 8 actions; a median of 4 actions in those plans had multiple preconditions. Median fraction of all actions with multiple preconditions was 0.60, with median maximum precondition arity 3. This is materially different from the unconstrained baseline, where optimal plans rarely used multi-precondition actions.

### 3.4 LM-cut misses are real but small

One initial-state example from the train-style sample:

- Topology: tiered3, 12 hosts, D=3, `rho=0.25`, `m=1`, seed 1.
- 16 facts, 40 actions, maximum precondition arity 3; selected optimal plan length 11.
- Exact `h* = 1,615` units; `h_max = 1,456`; LM-cut `= 1,532`.
- LM-cut gap: 83 units (2.18 effort units, about 5.1% of `h*`).

Across all reachable states, the largest LM-cut gap was 148 units in a tiered3 D=3 coupled instance. That gap is evidence against a claim of universal exactness, but not evidence of a bug: LM-cut is an admissible lower bound, not an exact solver for arbitrary tasks.

### 3.5 A small reproduction of the label-state sampler

`src/ahg/labels.py:1-12, 35-36, 72-91` says the label pipeline samples optimal-path states, random-walk states, states expanded by both A* searches, and their successors. It explicitly notes that random walks under-represent states where classical heuristics err.

I ran `label_instance` on four reachable representative tasks using a reduced diagnostic configuration (walk cap 60, three walks per sample, successor cap 200), with one additional tiered5 attempt failing as unreachable. The four tasks yielded 317 unique labelled states; LM-cut was exact on 298/317 (94.0%) and `h_max` on 204/317 (64.4%). Three tasks had exact LM-cut labels throughout; the tiered3 D=3 coupled task had LM-cut exact on 67/86 labels and `h_max` exact on 35/86.

This is only a small sampler spot-check, not a train-set estimate. It demonstrates why the uniform-all-reachable-state percentage and the actual label-state percentage should be reported separately.

---

## 4. Is the near-exactness an artefact or a bug?

### BUG — no defect demonstrated

I found no evidence that either implementation is returning values above `h*`, mishandling the conjunctions in the sampled tasks, or relying on a shared bitmask error to make the exactness result look better. The repository's `enumerate_exact` computes `h*` by backward induction (`src/ahg/measure.py:72-93`); the independent frozenset DP reproduced every state label in the 61-task sample. The separate `oracle.optimal_cost` uses frozenset states and direct action checks (`src/ahg/oracle.py:1-8, 18-47`) and matched all 61 initial costs.

There is one important interpretation trap in the existing measurement code: `src/ahg/measure.py:18-34` checks that A* with LM-cut and A* with `h_max` return the same **optimal solution cost**. That verifies search optimality agreement; it does not establish that the heuristic values themselves equal `h*` at every state. The state-by-state comparisons in this audit are the relevant test for heuristic exactness.

### MODELLING CHOICE — strong contributor

The generated task removes delete effects, uses one binary `execCode(host)` fact per host, has one goal fact, folds several intermediate attack predicates into actions, and uses fixed additive action costs. These choices make the state graph monotone and remove many sources of interaction. The active train-style depth and coupling gates do add conjunctions, but they do not introduce fact deletion or non-monotonic effects.

This is a legitimate abstraction for a controlled planning benchmark. It is not a faithful model of every operational attack-response environment. In particular, these measurements say nothing about state changes such as patching/removing vulnerabilities, privilege revocation, credential expiry, session invalidation, defensive actions that undo attacker progress, or action costs that depend on the evolving state.

### METRIC ISSUE — the denominator and sampled state distribution matter

Report at least three quantities separately:

1. Heuristic exactness at the **initial state** of each instance.
2. Exactness across **all reachable states**, with the state-weighted aggregation explicitly identified.
3. Exactness across the **actual label/search state sample**, which is intentionally biased toward A*-expanded states and their successors.

Do not use equal A* solution costs as a proxy for heuristic exactness. Both admissible heuristics can return the same optimal plan cost while having different—and inexact—values on the states they evaluated.

### FINE — a positive LM-cut gap is not a bug

LM-cut is designed to remain admissible; it is not guaranteed to recover `h*` for every delete-free task. The sampled attack tasks show 116 underestimates, and generic random delete-free tasks also produced cases where LM-cut was below `h*`. The relevant correctness condition is `h(s) <= h*(s)`, which held for every state tested here.

---

## 5. Limits and reproducibility notes

- The actual CVE table was not read. All experiment costs came from synthetic CVE records, passed through the repository's actual assignment and `cost_units` code. This isolates graph/search structure but does not validate the empirical cost distribution.
- The train-style sample covers 12-host cells and seeds 0/1, not the full train seed range or the 20-host train cells. The results should not be promoted to a full-split estimate.
- State-weighted rates give more weight to tasks with larger reachable state spaces. Per-family and initial-state rates are included to reduce this aggregation ambiguity.
- The label sampler spot-check uses the repository's `label_instance` implementation but deliberately smaller sampling caps than a production label run. Its percentages are illustrative only.
- The environment ran Python 3.13.5, while `pyproject.toml:5` declares `>=3.12,<3.13`. The heuristic and core tests executed successfully, but a strict reproducibility run should use the declared interpreter range.
- Excluded files and directories were not opened: `docs/findings.md`, `docs/decisions.md`, `docs/experiment_log.md`, `docs/related_work.md`, and `results/`.

## Final assessment

**LM-cut's near-exactness is a measured property of these generated attack tasks, not a demonstrated implementation bug. It is also model-dependent, and its apparent accuracy rises or falls substantially with the state population being measured.** For the unconstrained D=0 baseline, both heuristics are almost exact on the enumerated states. For the D2/D3-plus-coupling train-style sample, LM-cut remains close to exact (99.81% of reachable states; 86.9% of initial states), while `h_max` is exact on only 16.4% of initial states. Neither should be described simply as “near-exact” without stating the model variant and evaluation distribution.

**AUDIT_1 integrity:** unchanged. SHA-256 at completion: `e6b87128bba130a6c85ffe7b7a9384eaf6e2c16ece9a9fa41cc50faecf5ddf39`.
