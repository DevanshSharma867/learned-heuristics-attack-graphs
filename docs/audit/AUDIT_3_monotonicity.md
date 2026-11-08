# AUDIT_3: Monotonicity and modelling-assumption dependency map

**Date:** 2026-11-08. **Code audited:** commit `192b7b4128b3bd8b67a25ce0a18c1b18289f282c`, tagged locally as
`monotonic-study-frozen`. **Scope:** `src/ahg/`, `scripts/`, `tests/`.

**Nature of this audit.**
- It is a read-only map, and no code was changed.
- It lists where the frozen monotonic study (D1–D24) depends on seven modelling assumptions, what breaks if each is relaxed,
  and a verdict for each place.
- It does **not** propose the revised attack model, which D25 leaves to later D-entries.

**Verdicts.** The verdicts are written against "the assumption is relaxed", not against any particular new model.
- **REUSE AS-IS:** the code does not depend on the assumption. At most a comment or docstring would become wrong.
- **NEEDS CHANGE:** the code structure stays, but specific lines, a justification or a test must change.
- **REWRITE:** the algorithm or schema is built on the assumption and does not survive it.

Where a verdict depends on semantics the new model has not fixed yet, the entry says so. Typical cases are
negative preconditions, conditional effects and disjunctive goals. Anything not confirmed by reading or running
code is marked **UNVERIFIED**.

**Check performed for this audit (not a code change).** Over the raw NVD snapshot
(`data/raw/nvd/2026-10-21/`, 38 pages), the NVD Primary v3.x metric of every CVE in `data/derived/cves.csv`
was read to count fields the derived table drops. The script was run ad hoc and is not in the repo. Results are in §6.

---

## Summary table (assumption × file × verdict)

| # | Assumption | File (lines) | Verdict |
|---|---|---|---|
| 1 | Delete-free | `src/ahg/task.py` (1-10, 22-43, 78-86, 125-137, 140-144) | **REWRITE** (Action/Task schema, successor function, plan_cost, digest) |
| 1 | Delete-free | `src/ahg/search.py` (1, 41-96; D4 reopening at 83-94) | REUSE AS-IS (docstring line 1 only) |
| 1 | Delete-free | `src/ahg/heuristics.py` (13-15, 29-87, 107-124, 127-205, 208-209) | NEEDS CHANGE (h+ = h\* and h_FF ≥ h\* claims; code reusable if the new model stays STRIPS with positive pre/goal) |
| 1 | Delete-free | `src/ahg/oracle.py` (42-46) | NEEDS CHANGE |
| 1 | Delete-free | `src/ahg/measure.py` (31-33 dead-end check; 45-69 sampler; 72-93 enumeration) | **REWRITE** `enumerate_exact`; NEEDS CHANGE `exact_cost`, `sample_states` |
| 1 | Delete-free | `src/ahg/labels.py` (72-79, 103-107, 115-119) | NEEDS CHANGE |
| 1 | Delete-free | `src/ahg/attack_graph.py` (1, 176-179) | NEEDS CHANGE (reachability test via h_max) |
| 1 | Delete-free | `src/ahg/pddl.py` (1-8, 21-24) | NEEDS CHANGE (no delete effects emitted) |
| 1 | Delete-free | `src/ahg/learning/encode.py` (117-121, 128) | NEEDS CHANGE |
| 1 | Delete-free | `src/ahg/learning/train.py` (74-86 residual h\* − h_max ≥ 0) | REUSE AS-IS (conditional on STRIPS semantics) |
| 1 | Delete-free | `src/ahg/dataset.py` (118-130 static graph, 141) | NEEDS CHANGE (graph has no delete edges) |
| 1 | Delete-free | `scripts/measure_landscape.py` (76-77, 94-95), `scripts/measure_depth_coupling.py` (182-183, 196-197), `scripts/measure_exactness.py` (59-60), `scripts/check_size_shift.py` (74), `scripts/gen_attack_graphs.py` (28-37), `scripts/bench_inference.py` (146) | NEEDS CHANGE (inherit measure.py) |
| 1 | Delete-free | `scripts/fd_crosscheck.py` (87-102) | NEEDS CHANGE |
| 1 | Delete-free | `tests/helpers.py` (7-22, 25-50) | **REWRITE** `brute_force_optimal`; NEEDS CHANGE `random_task` |
| 1 | Delete-free | `tests/test_core.py` (59-60), `tests/test_attack_graph.py` (232), `tests/test_pddl.py` (22), `tests/test_labels.py` (26-36) | NEEDS CHANGE |
| 2 | Single goal fact | `src/ahg/attack_graph.py` (17, 109-117, 176, 183-193) | NEEDS CHANGE |
| 2 | Single goal fact | `src/ahg/task.py`, `heuristics.py`, `oracle.py`, `pddl.py`, `search.py`, `dataset.py`, `learning/encode.py`, `learning/models.py` | REUSE AS-IS (goal is a conjunctive tuple) |
| 2 | Single goal fact | `tests/test_attack_graph.py` (86) | NEEDS CHANGE |
| 3 | Single init at attackerLocated(internet) | `src/ahg/network.py` (8-9, 25, 86-87, 113-126), `src/ahg/topology.py` (44, 83-87, 150, 184, 197, 227) | NEEDS CHANGE |
| 3 | Single init | `src/ahg/attack_graph.py` (6, 120-121, 176, 183-193, 206, 236) | NEEDS CHANGE |
| 3 | Single init | `src/ahg/labels.py` (56-79, 135-138), `src/ahg/evaluate.py` (95, 100-104), `src/ahg/measure.py` (56-65) | NEEDS CHANGE |
| 3 | Single init | `src/ahg/task.py`, `search.py` (`start=`), `oracle.py` (`start`), `pddl.py` (`state`) | REUSE AS-IS |
| 4 | One execCode per host | `src/ahg/attack_graph.py` (3-7, 120-180, 223-244) | **REWRITE** (fact index = host id throughout) |
| 4 | One execCode per host | `src/ahg/cve.py` (42, 51-59, 197-209) | NEEDS CHANGE (no impact/scope columns) |
| 4 | One execCode per host | `src/ahg/dataset.py` (36-38, 102-115, 156) | NEEDS CHANGE |
| 4 | One execCode per host | `tests/test_attack_graph.py` (84-103, 154-178), `tests/test_knobs.py` (73-82, 110-113, 200) | NEEDS CHANGE |
| 5 | Single-pre exploits / folded MulVAL facts | `src/ahg/attack_graph.py` (9-20, 147-162) | NEEDS CHANGE (fold justification relies on delete-free) |
| 5 | Single-pre / folding | `tests/test_attack_graph.py` (91-94), `tests/test_knobs.py` (113), `scripts/gen_attack_graphs.py` (48-49), `scripts/measure_depth_coupling.py` (152-153) | NEEDS CHANGE |
| 5 | Single-pre / folding | `heuristics.py`, `search.py`, `task.py`, `learning/models.py` (56-61) | REUSE AS-IS (arbitrary arity) |
| 6 | Every service vulnerable, one family-level CVE per service | `src/ahg/assign.py` (1-41) | **REWRITE** |
| 6 | Every service vulnerable | `src/ahg/attack_graph.py` (147-154) | NEEDS CHANGE |
| 6 | CVE filters (1,473 CVEs) | `src/ahg/cve.py` (26-48, 62-189), `scripts/fetch_nvd.py`, `scripts/derive_cves.py` | NEEDS CHANGE if the CVE set changes; REUSE AS-IS for the frozen table |
| 6 | CVE pools | `src/ahg/splits.py` (27-28, 86-98) | REUSE AS-IS (mechanism); NEEDS CHANGE if pools are redefined |
| 6 | Every service vulnerable | `tests/test_assign.py` (57-68), `tests/test_splits.py` (56-64) | NEEDS CHANGE |
| 7 | Learning assumes 1–6 | `src/ahg/dataset.py` (35-38, 102-164) | NEEDS CHANGE |
| 7 | Learning assumes 1–6 | `src/ahg/learning/encode.py` (28-30, 61-87, 108-136) | NEEDS CHANGE |
| 7 | Learning assumes 1–6 | `src/ahg/learning/models.py` (16, 33-64) | NEEDS CHANGE (no delete-edge channel; FACT_DIM = 2) |
| 7 | Learning assumes 1–6 | `src/ahg/learning/heuristic.py`, `learning/train.py`, `learning/runs.py`, `src/ahg/evaluate.py`, `src/ahg/stats.py` | REUSE AS-IS |

---

## 1. Delete-free / monotonic states

### What the assumption is
- `Action` has `pre`, `add` and `cost`, and there is **no delete list** (`src/ahg/task.py:21-36`).
- The module docstring states the assumption: "There are no delete effects: once the attacker holds a privilege it
  is never lost" (`task.py:1-10`).

### Dependencies

**`src/ahg/task.py`**
- **Lines 22-36 (`Action`).** There is no field for deletes or for negative preconditions. `__post_init__` builds
  only `pre_mask` and `add_mask`.
  - *Breaks:* deletes cannot be represented at all. → **REWRITE** (schema).
- **Lines 41-43 (`useful`) and 78-86 (`successors`).**
  - Actions whose adds are all already held are skipped, and the successor is `state | add_mask`.
  - The docstring (81-82) gives the justification: "Skipping useless actions is safe only because the task is
    delete-free: such an action would lead back to the same state."
  - *Breaks if relaxed:*
    - `state | add_mask` ignores deletes, so successors are wrong.
    - The pruning justification no longer holds as written. Whether pruning stays cost-safe depends on the new
      model's semantics: it does with positive preconditions and goals only, and does not in general with negative
      preconditions or goals. This needs a new argument (**UNVERIFIED** until those semantics are fixed).
  - → **REWRITE.**
- **Lines 125-137 (`plan_cost`).** `state |= a.add_mask`.
  - *Breaks:* plan validation ignores deletes. Every search result goes through `evaluate._run` (`evaluate.py:80`),
    so the check there would not validate plans. → NEEDS CHANGE.
- **Lines 140-144 (`task_digest`).** It hashes `[name, pre, add, cost]`.
  - *Breaks:* tasks differing only in deletes get the same digest. `dataset.open_batch` (`dataset.py:95`) relies
    on this digest to bind labels to graphs. → NEEDS CHANGE.
- **Lines 18, 107-122 (bitmask `State`, `to_mask`, `facts_of`).** A state stays a set of facts.
  → REUSE AS-IS.

**`src/ahg/search.py`**
- **Lines 41-96, `best_first_search`.**
  - It is generic: it only calls `task.successors`, `task.is_goal`, `h`, and `task.actions[ai].cost`.
  - Duplicate detection uses `g_best`/`closed` and handles cycles, which can arise once states can shrink.
- **D4 reopening** (lines 83-94: push on strictly cheaper g, reopen if already closed; stale skip at 69-70).
  The policy is independent of monotonicity.
- *Breaks:* only the docstring at line 1 ("delete-free task").
- → **REUSE AS-IS.**

**`src/ahg/heuristics.py`**
- **Lines 13-15, docstring.** "Our tasks are already delete-free, so the 'relaxed' problem is the real problem:
  h+ … equals h\*."
  - *Breaks:* with deletes, h+ ≤ h\* only, not equality. This is the h\* = h+ result of Contribution 1 (CLAUDE.md
    §0), which is specific to the frozen model. → NEEDS CHANGE (claim).
- **Lines 29-87 (`relaxed_costs`) and 95-104 (`hmax`, `hadd`, `hsp`).**
  - These read only `pre`, `add` and `cost`, so they compute the delete relaxation of whatever task they are given.
  - For STRIPS with positive preconditions and goals, the delete relaxation is admissible (h+ ≤ h\*). So
    `ADMISSIBLE = {"h0","hsp","hmax","lmcut"}` (line 209, D7) stays valid **under that semantics**.
  - With negative preconditions or conditional effects, these functions would silently ignore them.
    **UNVERIFIED** until the new semantics are fixed.
  - → REUSE AS-IS, conditional.
- **Lines 107-124 (`hff`).** The code works as a relaxed-plan heuristic.
  - D7's note "on our delete-free tasks h_FF's relaxed plan is a real plan, so h_FF ≥ h\* always"
    (decisions.md D7) no longer holds: with deletes, h_FF can fall below h\*.
  - → NEEDS CHANGE (claim and the tests asserting it, below).
- **Lines 127-205 (`lmcut`).**
  - It is a standard LM-cut on the relaxed task (Helmert & Domshlak 2009, cited in the docstring) and reads only
    `pre`, `add`, `costs` and `goal`.
  - LM-cut is admissible for STRIPS with action costs. Its correctness does not use delete-freeness.
  - With multiple goals, the goal zone is grown from the costliest goal (163-165). That is equivalent to the usual
    artificial-goal construction, and it is already exercised by `tests/test_core.py` with `goal_size=2`.
  - → REUSE AS-IS, conditional on positive preconditions and goals.

**`src/ahg/oracle.py`**
- **Lines 41-46.** `if pre <= s and not add <= s:` then `s | add`. It has the same useless-action skip and the same
  union successor as `Task.successors`, in independent code.
  - *Breaks:* the oracle (CLAUDE.md rule 6) would agree with a wrong search. → NEEDS CHANGE.
  - Its independence from `search.py` (docstring 3-7) must be preserved by whatever change is made.

**`src/ahg/measure.py`**
- **Lines 31-33 (`exact_cost`).** It raises `HardFailure` if a reachable state cannot reach the goal: "Delete-free
  with a reachable goal: every reachable state reaches it (D14 §1)."
  - *Breaks:* with deletes, dead ends become possible, and this check would abort valid runs. → NEEDS CHANGE.
- **Lines 45-69 (`sample_states`).**
  - The walk-length bound is `max_depth = facts not held initially` (56), justified by "each useful action adds at
    least one fact" (docstring 49-51).
  - *Breaks:* the bound is invalid and walks can cycle. The sampler's D14 §2 / D19 §2 semantics change.
    → NEEDS CHANGE.
- **Lines 72-93 (`enumerate_exact`).**
  - It does backward induction, processing states in order of decreasing popcount (88). The docstring (75-77) says
    this is valid because "states of a delete-free task form a DAG (every useful action strictly grows the state)".
  - *Breaks:* with deletes the state graph can have cycles and successors with fewer facts. The order is then wrong,
    and the single pass gives wrong h\*.
  - This is the third, independent label check (D19 §3).
  - → **REWRITE.**

**`src/ahg/labels.py`**
- **Lines 72-79 and 103-107.** Suffix costs along an optimal plan are propagated with
  `s | task.actions[ai].add_mask`.
  - The principle (every suffix of an optimal plan is optimal) holds generally. The state transition does not.
  - → NEEDS CHANGE (use the task's transition function).
- **Line 82.** It uses `sample_states` (above).
- **Lines 115-119.** It uses `enumerate_exact` (above), and it is a HardFailure cross-check.
- **Lines 61-64.** "Goal unreachable from the initial state" is a HardFailure, and A\*+h_max = A\*+LM-cut is
  checked. Both remain valid.
- → NEEDS CHANGE overall.

**`src/ahg/attack_graph.py`**
- **Lines 176-179.** `if hmax(task, task.init) == INF: raise UnreachableGoal`, commented "The task is delete-free,
  so hmax is finite exactly when the goal is reachable."
  - *Breaks:* with deletes, a finite h_max is necessary but not sufficient for reachability. Unreachable goals would
    pass generation and surface later as HardFailure in `labels.py:60-62` instead of being logged as generation
    failures (rule 10).
  - → NEEDS CHANGE.
- **Line 1 docstring.** "delete-free Task (D12)".

**`src/ahg/pddl.py`**
- **Lines 1-8 and 21-24.** "There are no delete effects, exactly as in the Task". The effect is
  `(and <adds> (increase …))`.
  - *Breaks:* the export would drop deletes, and FD would solve a different (relaxed) task. → NEEDS CHANGE.

**`scripts/fd_crosscheck.py`**
- It depends on `exact_cost` (91), `sample_states` (87) and the delete-free PDDL export (68-74).
- The h_max equality check (docstring 11-12: "h_max is unique, so it must match exactly") stays meaningful under
  deletes, because both sides compute the relaxation.
- The plan-cost abort (96-97) depends on correct export and h\*.
- It is hard-wired to the D15+D16 feasibility run `[B]` (`BENCH`, line 49) and to `make_instance(...,
  exposed_level0=True)` (84-85).
- → NEEDS CHANGE.

**Other scripts inheriting `measure.py`**
- `scripts/measure_landscape.py`: 76-77, and the dead-end HardFailure at 94-95.
- `scripts/measure_depth_coupling.py`: 182-183, the dead-end HardFailure at 196-197, and `Labeller` at 98-117.
- `scripts/measure_exactness.py`: 59-60. It also asserts `h* − h ≥ 0` (39), which stays valid if h_max and LM-cut
  stay admissible.
- `scripts/check_size_shift.py`: 74.
- `scripts/gen_attack_graphs.py`: 28-37. The reachable-state count is generic and needs only correct successors.
- `scripts/bench_inference.py`: 146. Its MLP features use `a.useful(s)`.
- → NEEDS CHANGE (all inherit the fix in `measure.py` and `task.py`).

**`src/ahg/learning/`, `src/ahg/dataset.py`** (see also §7)
- `encode.py:117-121`: `plan_open_pairs` builds plan states with `| add_mask`. `encode.py:128` calls
  `task.successors`. → NEEDS CHANGE.
- `dataset.py:118-130` (`static_graph`): only precondition and add edges. A delete has no edge type, so the GNN
  could not see it. → NEEDS CHANGE.
- `train.py:74-86` (`residual_h`): it relies on `h* − h_max ≥ 0`, which holds wherever h_max is admissible (see the
  heuristics item above). → REUSE AS-IS, conditional.

**Tests**
- `tests/helpers.py:25-50` (`brute_force_optimal`).
  - The docstring says "In a delete-free task order only matters for applicability, so a subset S is a valid plan
    iff repeatedly applying applicable actions of S … reaches the goal."
  - This subset argument is false with deletes. It is the brute-force ground truth in `test_core.py:25-60`,
    `test_attack_graph.py:145, 220` and `test_labels.py:26-36`.
  - → **REWRITE.**
- `tests/helpers.py:7-22` (`random_task`): it generates delete-free tasks only. → NEEDS CHANGE.
- `tests/helpers.py:53-62` (`reachable_states`): generic. → REUSE AS-IS.
- `tests/test_core.py:59-60` and `tests/test_attack_graph.py:232` assert `hstar <= hff`. → NEEDS CHANGE.
- `tests/test_pddl.py:22` asserts `"(not " not in d`, commented "delete-free". → NEEDS CHANGE.
- `tests/test_knobs.py:137-146` and `tests/test_attack_graph.py:203-241` are generic oracle-vs-search checks.
  They stay valid once the oracle and successors are fixed.

---

## 2. Single goal fact

**Current state.**
- `Task.goal` is a tuple, interpreted **conjunctively** (`task.py:51, 53-55, 75-76`).
- The generator always builds a one-element goal, `(target,)` (`attack_graph.py:176`).
- A disjunctive goal ("any one of several assets") cannot be expressed in `Task`. Whether that matters depends on
  the new model.

**Generator-side dependencies**
- `src/ahg/attack_graph.py:183-193` (`choose_target`): one target, drawn among the hosts deepest from the internet
  (rng stream `goal:family:seed`).
- `attack_graph.py:109-117`: `Instance.target` is a single int.
- `attack_graph.py:206-208` (D16): raises `KnobInfeasible` if *the* target is internet-exposed.
- `attack_graph.py:214`: the target is placed at the top credential level.
- *Breaks:* every place that treats "the target" as one host. → NEEDS CHANGE.

**Code already goal-set generic** (→ REUSE AS-IS)
- `heuristics.py:69-70, 90-92, 110-114, 147, 163` (`_goal_value` combines with max or sum, and LM-cut uses the
  costliest goal).
- `oracle.py:26`.
- `pddl.py:33` (`_conj(task.goal)`).
- `dataset.py:130, 135, 155` (an `is_goal` bit per fact).
- `learning/encode.py:66, 77`.
- `learning/models.py:62` (the pooling `f[:, g["goal"]].mean(1)` averages over goal facts).
- `tests/test_core.py` already uses `goal_size=2` (`helpers.py:7, 16`).

**Tests**
- `tests/test_attack_graph.py:86`: `t.goal == (i.target,)`. → NEEDS CHANGE.

---

## 3. Single initial state at attackerLocated(internet)

**Task layer: generic** (→ REUSE AS-IS)
- `Task.init` is any bitmask.
- `best_first_search(start=…)` (`search.py:41, 51`), `oracle.optimal_cost(start=…)` (`oracle.py:18, 24`) and
  `problem_pddl(state=…)` (`pddl.py:28-30`) all take arbitrary start states.
- A *set* or *distribution* of initial states is not representable as one `Task`.

**Network and generator**
- `src/ahg/network.py`:
  - 8-9 and 25: host 0 is the internet, `INTERNET = 0`, and it runs no services.
  - 86-87: validation requires host 0 to be the internet.
  - 113-126: `hop_distances` measures distance from the internet.
- `src/ahg/topology.py`:
  - 44: the internet host is created first.
  - 83-87: `ensure_exposed`.
  - 150, 184, 227: `link(INTERNET, …)`.
  - 197: repair edges start from the internet.
- `src/ahg/attack_graph.py`:
  - 6: "the only initial fact".
  - 120-121: `fact_name`.
  - 176: `init = 1 << INTERNET`.
  - 183-193: the target is chosen by hop distance from the internet.
  - 206: D16 "exposed" means reachable from the internet.
  - 236: "Exploits from the internet are never coupled".
- *Breaks:* any other entry point (an insider, a phished workstation, several footholds) changes reachability
  repair, target choice and both D15/D16 knobs. → NEEDS CHANGE.

**Labels, evaluation and sampling**
- `src/ahg/labels.py:56-79`: the init-state A\* runs, `hstar_init` and the optimal-path source all start at
  `task.init`.
- `labels.py:135-138`: `stats["hstar_init"]`.
- `src/ahg/evaluate.py:95, 100-104`: every comparison runs A\* from `task.init` against `stats["hstar_init"]`.
- `src/ahg/measure.py:56-65`: walks start at `task.init`.
- `scripts/measure_exactness.py:56` and `scripts/measure_depth_coupling.py:159, 211-213` use the initial-state
  population.
- *Breaks:* with several initial states, every per-instance number (one h\*(init), one search per instance) would
  need a per-start definition. → NEEDS CHANGE.

**Tests**
- `tests/test_attack_graph.py:84, 86`; `tests/test_knobs.py:110, 178`; `tests/test_topology.py:70, 90, 106`.
  → NEEDS CHANGE.

---

## 4. One execCode fact per host (no user/root split)

**Generator**
- `src/ahg/attack_graph.py:3-7, 120-180`: **fact index = host id**. A state's bitmask is "the set of hosts the
  attacker controls" (docstring 3-4, D12).
- Places that use this identity:
  - exploit `pre (r.src, …)`, `add (s.host,)` (152-154);
  - login `pre {t.src, r.src}`, `add (t.dst,)` (161-162);
  - harvest preconditions `(h.id,)` and `(t,)` (167, 170, 175);
  - capability facts at the fixed indices `n`, `n+1` (135);
  - `cred0 = n + (2 if pr_gated)` (138);
  - `cred_gate(h)` keyed by host (141-144);
  - `couple_exploits` stores a host id as the extra precondition (223-244, used at 150).
- *Breaks:* two privilege levels per host break every index computation and every action template.
  → **REWRITE** (fact schema).
- D12 ("Why one privilege level") records the reason: `cves.csv` holds no impact metrics.

**CVE data** (`src/ahg/cve.py`)
- `CSV_FIELDS` (42) and `CveRecord` (51-59) keep only id, family, products, version, exploitability, published
  date and PR.
- Impact, scope and attack vector are **not** stored. `write_table` and `load_table` (192-209) follow this schema.
- The raw snapshot does contain them. For all 1,473 included CVEs the NVD Primary metric carries `impactScore`,
  `confidentialityImpact`, `integrityImpact`, `availabilityImpact`, `scope` and `attackVector` (counted for this
  audit, see the header).
- → NEEDS CHANGE if privilege outcome is derived from CVSS. The table must be re-derived from the pinned snapshot.

**Learning features** (`src/ahg/dataset.py`)
- `ACTION_KINDS = ("exploit","login","harvest")` and `ACTION_DIM` (36-38).
- `action_features` (102-115) parses the action *name*: the kind is the first token, and the CVE id is token 1 for
  exploits.
- `wl_colours` (156) uses the kind and cost.
- → NEEDS CHANGE if action kinds or name formats change.

**Scripts**
- `scripts/measure_depth_coupling.py:177`: `name.startswith("harvest cred")`.
- `scripts/gen_attack_graphs.py:48`: `startswith("login")`.

**Tests**
- `tests/test_attack_graph.py:84-103, 154-178` (exact fact lists and action tuples).
- `tests/test_knobs.py:73-82, 110-113, 200` (`f >= len(net.hosts)` identifies non-host facts).
- `tests/data/golden_tasks.json` and `golden_d15_tasks.json`, via `tests/golden.py`. These are byte-identity
  digests of the frozen schema, and by design they must not be regenerated (golden.py docstring).
- → NEEDS CHANGE (the new schema needs its own tests; the golden files stay as the record of the frozen schema).

---

## 5. Single-precondition exploits / folded MulVAL intermediate facts

**Generator**
- `src/ahg/attack_graph.py:9-20, 147-154`. An exploit's base precondition is the single fact `fact(src)`.
- The gates add more facts only when the knobs are on: PR gating, coupling and credential level, at 153.
- Logins have one or two preconditions (161-162).

**Folding**
- MulVAL's `netAccess`, `canAccessHost` and `principalCompromised` are folded into the actions (docstring 17-20,
  D12 "Why fold the intermediate facts").
- D12's justification is explicitly delete-free: "Folding preserves reachability and optimal cost. The task is
  delete-free and the folded steps are free, so every plan in one representation maps to a plan of equal cost in
  the other."
- *Breaks:* if intermediate facts (e.g. network access or a session) can be lost, this equivalence is no longer
  established. Folding would need a new argument, or the facts would need to be materialised.
- → NEEDS CHANGE.
- The MulVAL correspondence is still marked `[VERIFY rule names against MulVAL's interaction_rules.P]` in D12, and
  is **UNVERIFIED**.

**Measurement**
- `scripts/measure_depth_coupling.py:152-153` counts "multi_pre_actions".
- `scripts/gen_attack_graphs.py:49` counts conjunctive logins.
- Both are descriptive, and correct for any arity.

**Tests**
- `tests/test_attack_graph.py:91-94` asserts `a.pre == (r.src,)` for every default exploit.
- `tests/test_knobs.py:113` asserts the same for uncoupled exploits.
- → NEEDS CHANGE.

**Arity-generic code** (→ REUSE AS-IS)
- `heuristics.relaxed_costs` (`need = len(a.pre)`, line 50).
- `task.py`, `search.py`, `oracle.py`.
- `learning/models.py:56-58`: an action aggregates the *mean* of its preconditions, for any number of them.

---

## 6. Every service vulnerable; one family-level CVE per service; the CVE filters

**Assignment** (`src/ahg/assign.py:18-41`)
- Every service gets exactly one CVE (36-40), drawn uniformly with replacement from the CVEs of its *family*.
- It raises if a family has none (38-39).
- There is no "not vulnerable" outcome, no product or version matching (`CveRecord.products` is recorded but unused
  in assignment), and no multiple-CVE service.
- → **REWRITE** if any of these changes.

**Generator** (`src/ahg/attack_graph.py:147-154`)
- **Every reach edge becomes an exploit**, using `cves[s.id]` (a KeyError if a service had no CVE).
- D12's reachability proof ("Every reach edge yields an exploit action. So … every goal is reachable by
  construction") depends on this.
- → NEEDS CHANGE.

**CVE filters giving 1,473 CVEs** (`src/ahg/cve.py`; D11)
- **Scope.** 8 service families mapped to 35 vendor:product CPE names (`FAMILY_PRODUCTS`, 26-39). The snapshot
  has 38 pages: one per product, plus two extra pages for `oracle:mysql`.
- **Rule order** (`derive`, 141-189):
  1. `platform_only`: no product of the family is marked vulnerable by a positive `vulnerable: true` cpeMatch,
     with negation handled, D24 §3 (108-138).
  2. `multi_family`: vulnerable in more than one family; the CVE is dropped from all of them.
  3. Score: the NVD Primary v3.1, else v3.0, exploitability score must exist (`nvd_primary_v3`, 62-76). CNA-only
     v3, v2-only, v4-only and unscored CVEs are excluded.
  4. `outside_window`: published outside `WINDOW` = 2016-01-01 to 2023-12-31 (40).
- **PR** is read from the same vector, and cross-checked (79-87).
- **Result.** `data/derived/cves.csv` has 1,473 rows: dns 158, ftp 62, http 189, mail 125, rdp 106, smb 107,
  sql 668, ssh 58. `data/derived/build_log.json` reports `rows: 1473`, `snapshot_date: 2026-10-21` and
  `fetch_git_commit: bcf91c8`.
- **No attack-vector filter.** Of the 1,473 included CVEs, 1,300 are `AV:NETWORK`, 160 are `AV:LOCAL` and 13 are
  `AV:ADJACENT_NETWORK`.
  - All are used as remote exploits from any reach-edge source (`attack_graph.py:147-154`).
  - Scope: 1,406 `UNCHANGED` and 67 `CHANGED`.
  - Counted for this audit from the raw snapshot; see the header.
- findings.md §9 already records "every modelled service is vulnerable" and "CVE assignment is family-level"
  (D24 §8). The AV:LOCAL count is not recorded there (stated as fact, not as a proposal).
- → REUSE AS-IS for the frozen table. NEEDS CHANGE if inclusion rules or stored columns change. A new table must
  be a new derived file, because `cves.csv`'s SHA-256 is pinned in every label manifest (`labels.py:215`) and
  checked by `dataset.open_batch` (`dataset.py:83-84`).

**Pools** (`src/ahg/splits.py:27-28, 86-98`)
- `heldout` is the hash-based ~30% of CVE ids. `heldout_costly` is `heldout` with E ≤ 2.8. `train` is the rest.
- The mechanism is family-agnostic. → REUSE AS-IS (mechanism).

**Tests**
- `tests/test_assign.py:57-68`: the empty-family pool is rejected, and every family is covered with one CVE per
  service.
- `tests/test_splits.py:56-64`: the pools cover every family.
- `tests/test_cve.py`: rule tests, which stay valid for the frozen rules.
- → NEEDS CHANGE (assign and splits tests) if the assignment changes.

---

## 7. `src/ahg/learning/` (and `src/ahg/dataset.py`, which defines its features)

| Location | Relies on | What breaks if relaxed | Verdict |
|---|---|---|---|
| `dataset.py:35` `COST_SCALE = 10*SCALE` | the D9 cost range [38, 380] | nothing, unless the cost model changes (it is frozen, rule 5) | REUSE AS-IS |
| `dataset.py:36-38` `ACTION_KINDS`, `PR`, `ACTION_DIM = 7` | (4) the three action kinds; (6) one CVE per exploit carrying PR | new kinds or several CVEs per action do not fit the one-hot | NEEDS CHANGE |
| `dataset.py:102-115` `action_features` | (4, 6) action **names**: kind = token 0, CVE id = token 1 | a name-format change breaks parsing | NEEDS CHANGE |
| `dataset.py:118-130` `static_graph` | (1) only pre and add edges | deletes are invisible to the GNN | NEEDS CHANGE |
| `dataset.py:133-135` `fact_features` (held, is_goal) | (2) a goal is a set of facts | fine for multiple goals | REUSE AS-IS |
| `dataset.py:138-143` `mlp_features` | (1) `task.successors` (useful-action skip); `#held` = popcount | inherits the successor semantics | NEEDS CHANGE (via task.py) |
| `dataset.py:146-164` `wl_colours` | (4) action kind from the name; (1) pre and add only | the same as above | NEEDS CHANGE |
| `dataset.py:69-99` `open_batch` | rebuilds instances with `make_instance` and checks `task_digest` and the `cves.csv` SHA | a generator change makes old batches unloadable at new commits (by design); they stay loadable at the tag | REUSE AS-IS |
| `learning/encode.py:28-30` `ENCODER_VERSION` | hashes `task.py`, `heuristics.py`, `search.py` and others | any change invalidates caches (by design) | REUSE AS-IS |
| `learning/encode.py:61-67` `fact_bits` | (2) the goal set | — | REUSE AS-IS |
| `learning/encode.py:70-87` `hmax_inputs`, `gnn_inputs` | (1) h_max admissible, so the residual is ≥ 0 | holds if h_max stays admissible (§1) | REUSE AS-IS (conditional) |
| `learning/encode.py:108-136` `plan_open_pairs` | (1) `| add_mask` (120) and `task.successors` (128); (3) a single `task.init` | wrong plan states with deletes | NEEDS CHANGE |
| `learning/encode.py:139-153` `rank_groups` | (3) one plan per instance from `task.init` | needs a per-start definition with several inits | NEEDS CHANGE |
| `learning/models.py:16` `FACT_DIM = 2`; 33-64 `GNN` | (1) two edge types (pre to action: AND mean; action to add: OR mean) | no channel for delete edges | NEEDS CHANGE |
| `learning/models.py:19-30, 67-128` `MLP`, `WLLinear`, `fit_ridge` | input vectors only | — | REUSE AS-IS |
| `learning/heuristic.py:20-65` | `static_graph(inst)`, `fact_bits`, `hmax` | inherits the dataset changes; the logic is generic | REUSE AS-IS |
| `learning/train.py:74-86` `residual_h` | (1) h\* − h_max ≥ 0 | holds while h_max is admissible | REUSE AS-IS (conditional) |
| `learning/train.py` (rest), `learning/runs.py` | train/val batches, seeds, checkpoints | — | REUSE AS-IS |
| `src/ahg/evaluate.py:29-118` | (3) one A\* per instance from `task.init` against `hstar_init`; admissible baselines must hit h\* | multiple inits need per-start records | REUSE AS-IS (logic); NEEDS CHANGE only if init becomes a set |

---

## Fast Downward setup (facts)

- **Setup script** (`scripts/setup_fast_downward.sh`):
  - It runs `git clone --depth 1 --branch release-24.06.1 https://github.com/aibasel/downward.git` into
    `third_party/downward`.
  - It asserts `git describe --tags` = `release-24.06.1`, then runs `python3 build.py release -j 8`.
- **Version and commit:**
  - `third_party/downward` has `git describe --tags` = `release-24.06.1` and `git rev-parse HEAD` =
    `1eef26b2cbf599a1894606aa898d9d49e1034cb9`, both read on 2026-11-08.
  - The recorded run's provenance (`results/feasibility/fd_crosscheck/2026-10-29T070649Z-41e9d1c/provenance.json`)
    has the same tag and commit.
- **Installed on this machine:** yes.
  - `third_party/downward/builds/release/bin/downward` (4,253,800 bytes, built 2026-10-29) and `…/bin/translate/`
    exist.
  - `third_party/` is gitignored (`.gitignore:28`), so FD is not part of the repo.
  - A smoke test on 2026-11-08 ran `fast-downward.py d.pddl p.pddl --search 'astar(lmcut())'` on a one-action
    STRIPS task in the scratchpad. The translator exited with 0, and FD reported "Solution found" and "Plan cost: 1".
  - FD is not on `PATH`. It is invoked as `python fast-downward.py`.
  - Compiler and build flags: **UNVERIFIED**.
- **Configurations `scripts/fd_crosscheck.py` runs:**
  - **Translate:** `fast-downward.py --sas-file task.sas --translate domain.pddl problem.pddl` (72-73), on the
    grounded export from `src/ahg/pddl.py`. It translates once per state.
  - **Searches:** `--search "astar(lmcut())"` and `--search "astar(hmax())"` on every measured state (93). That is
    the initial state plus 9 sampled states per instance, 20 instances, 200 states. The initial-state h values are
    parsed from "Initial heuristic value", and the plan cost from the LM-cut run.
  - **Timing:** `--search "astar(blind())"` on the initial state only (101-102), used to subtract per-evaluation
    search overhead (103-106).
  - **Instances:** 20, evenly spaced, from the D15+D16 feasibility run `[B]`
    (`results/feasibility/inference_microbench/2026-10-29T062211Z-1627e16`), with D = 3, n = 20 and
    `exposed_level0=True`.
- **Recorded result** (`report.md` of the run above, commit `41e9d1c`, clean):
  - h_max: FD equals ours on 200/200 states.
  - LM-cut: FD equals ours on 169/200 states. Both are always ≤ h\* (any LM-cut value above h\* would abort the run).
  - FD's A\*+LM-cut plan cost equals our h\* on 200/200 states.

---

## What this audit does not cover

- Correctness of the frozen code under its own assumptions. That is covered by AUDIT_1, AUDIT_2 and the test suite:
  1750 passed and 11 skipped at `192b7b4` on 2026-11-08.
- Anything about the revised model. Every "breaks if relaxed" above is stated generically.
- `results/`, test splits and label batches. None was read; only the access log was parsed, for the D25 session
  report.
