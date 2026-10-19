# Status report: Learned Heuristics for A* over Attack Graphs

- **Audit date:** 2026-10-19 (week 3 of the ~10-week plan that started the week of 5 Oct 2026)
- **Auditor:** Claude Code (Opus 5.5), read-only audit. No source, test, or config file was modified. Only this file was created.
- **Repo:** `/Users/devanshsharma/projects/learned-heuristics-attack-graphs` (remote `origin` = https://github.com/DevanshSharma867/learned-heuristics-attack-graphs.git)

**Summary.** The repo holds a small, clean, well-tested core: a delete-free planning task model, one best-first search routine (UCS / A* / weighted A* / GBFS), and six classical heuristics (h0, h_sp, h_max, h_add, h_FF, LM-cut). All 125 tests pass. Nothing past that exists yet: no topology generator, no CVE/NVD data, no attack-graph generator, no implemented cost model, no labels, no splits, no learning code, no evaluation harness, and no results. **The git repository has zero commits.** Every file is untracked.

---

## 1. Inventory

### 1.1 Directory tree

Excluded: `.git/`, `__pycache__/`, `.pytest_cache/`. The `.venv/` directory exists (9.6 MB, contents not listed). No `data/`, `results/` or `runs/` directories exist.

```
.
├── .DS_Store                     (6 KB, macOS junk, untracked and NOT in .gitignore)
├── .gitignore                    (.venv/, __pycache__/, *.pyc, .pytest_cache/, data/, runs/)
├── .python-version               ("3.12")
├── AI_Project_Guidelines.v1.md   (course guidelines, 13.5 KB)
├── CLAUDE.md                     (project instructions, 13 KB)
├── ai_porject_proposal.md        (proposal text, 19 KB; filename has a typo "porject")
├── pyproject.toml
├── uv.lock
├── docs/
│   └── learn/
│       └── README.md             (learning-guide index, 52 lines)
├── scripts/
│   └── toy_demo.py               (21 lines)
├── src/
│   └── ahg/
│       ├── __init__.py           (1 line, docstring only)
│       ├── task.py               (135 lines)
│       ├── search.py             (113 lines)
│       ├── heuristics.py         (209 lines)
│       └── examples.py           (25 lines)
└── tests/
    ├── conftest.py               (4 lines, adds tests/ to sys.path)
    ├── helpers.py                (62 lines)
    └── test_core.py              (86 lines)
```

Missing from the layout in CLAUDE.md §6: `configs/`, `data/`, `results/`, `docs/decisions.md`, `docs/experiment_log.md`, `docs/ai_usage_log.md`, `docs/paper/`, and the subpackages `generators/`, `cve/`, `attackgraph/`, `learning/`, `eval/`. The package is flat (`src/ahg/*.py`), not split into the subpackages CLAUDE.md suggests. CLAUDE.md says to adapt to what exists, so this is not a problem.

`docs/learn/README.md` links to chapter files `01-the-problem.md` … `05-research-method.md` and `glossary.md`, and marks chapters 01–03 as "written". **None of those files exist in the repo.** It also mentions `PREREG.md` and `src/ahg/models/`, which do not exist either.

### 1.2 Source modules

| Module | What it does | Key items | Status |
|---|---|---|---|
| `src/ahg/task.py` | Delete-free planning task. Facts are indices, a state is an `int` bitmask, and actions have conjunctive preconditions and add effects, with no deletes. | `Action` (frozen dataclass: `name, pre, add, cost`, cached `pre_mask/add_mask`, `applicable`, `useful`), `Task` (`facts, actions, init, goal`, cached `goal_mask, pre_of, achievers`, `is_goal`, `successors`, `describe`, `from_names`), `to_mask`, `facts_of`, `plan_cost` (validates a plan) | Complete for its scope |
| `src/ahg/search.py` | A single best-first search parameterised by `f = w_g·g + w_h·h` | `SearchResult` (plan, cost, expanded, generated, evaluations, seconds, budget_hit), `best_first_search`, wrappers `astar`, `uniform_cost`, `weighted_astar`, `gbfs` | Complete for its scope |
| `src/ahg/heuristics.py` | Classical delete-relaxation heuristics | `relaxed_costs` (generalised Dijkstra over facts, modes `max`/`add`/`min`), `h0`, `hsp`, `hmax`, `hadd`, `hff`, `lmcut`, dicts `HEURISTICS`, `ADMISSIBLE` | Complete for its scope |
| `src/ahg/examples.py` | One hand-built 3-host toy network (7 facts, 7 actions, goal `root@db`) | `toy_network()` | Complete (toy only) |
| `src/ahg/__init__.py` | Package docstring | — | Stub (intentionally empty) |
| `scripts/toy_demo.py` | Prints every heuristic's value and every search result on the toy network | — | Complete |
| `tests/helpers.py` | Independent test oracles | `random_task(seed, …)` (random delete-free task, may be unsolvable), `brute_force_optimal` (enumerates every action subset; does not use the search code), `reachable_states` (DFS) | Complete |
| `tests/test_core.py` | Correctness tests | see §3.1 | Complete for current code |

### 1.3 Dependencies, Python, hardware

- `pyproject.toml`: `requires-python = ">=3.12,<3.13"`, **runtime `dependencies = []`**, dev group `pytest>=8`, build backend hatchling.
- `uv.lock` pins `pytest 9.1.1`, `pluggy 1.7.0`, `iniconfig 2.3.1`, `packaging 26.3`, `pygments 2.21.0`, `colorama 0.4.6`. Nothing else is pinned.
- `.venv` Python: **3.12.13**. Tool: `uv 0.11.7`.
- **PyTorch, PyTorch Geometric, numpy and scipy are not installed** and are not declared anywhere.
- Hardware: Apple M4, 10 cores, 16 GB RAM (macOS, Darwin 24.6.0). `nvidia-smi` is not present, so there is **no NVIDIA GPU**. `torch.cuda.is_available()` could not be run because torch is not installed. Whether Apple MPS would work is **not verified**.

### 1.4 Git history

```
$ git log --oneline | head -50
fatal: your current branch 'master' does not have any commits yet
```

- Total commits: **0**. First and latest commit dates: **none**.
- Current branch: `master` (unborn). The harness reports `main` as the main branch, but no `main` branch exists locally. Remote `origin` is configured. Whether anything has been pushed to GitHub was **not verified**.
- File modification times show the code was written on 17 Oct 2026 (11:58–12:02). `CLAUDE.md` was edited on 19 Oct.

---

## 2. Pipeline status

| Stage | Status | Evidence |
|---|---|---|
| a. Synthetic topology generators | **NOT STARTED** | No generator code. The only network is the hand-written `examples.toy_network()`. No flat, tiered, or hub-and-spoke family exists. |
| b. CVE/NVD assignment | **NOT STARTED** | No NVD cache, no `data/` directory, no CPE matching, no CVSS handling. CVE count: 0. Snapshot date: none. |
| c. Attack-graph generation | **NOT STARTED** | No MulVAL integration and no native generator. Nothing in the repo records a MulVAL go/no-go decision (proposal week 2 milestone). Whether MulVAL is installed on this machine was **not verified**. |
| d. Fact–action representation | **DONE (core)** | `task.py`. See details below. |
| e. Cost model | **NOT IMPLEMENTED** | No code computes `c(a) = 1 + 9·(1 − x_a)`. Costs are set by hand: the toy uses 10–90, random test tasks use `randint(1, 20)`. `Action.cost` is annotated `int`. |
| f. Search (A*, UCS) | **DONE** | `search.py`. See details below. |
| g. Heuristics | **DONE**: h0, h_sp, h_max, h_add, h_FF, LM-cut | `heuristics.py`. See details below. |
| h. Exact solver and labels | **PARTIAL** | There is no label-generation code. The exact solver is in practice UCS or A* with an admissible heuristic. Brute-force enumeration is used as an independent oracle in the tests. No separate UCS implementation exists (see rule 6). |
| i. Splits | **NOT STARTED** | No split code and no seed management. |
| j. GNN and MLP | **NOT STARTED** | No model code. torch and PyG are not installed. |
| k. Training loop, checkpoints, logging | **NOT STARTED** | — |
| l. Evaluation harness, statistics, tables and figures | **NOT STARTED** | `SearchResult` already records the raw per-run metrics: expanded, generated, evaluations, seconds, cost, budget_hit. There are no evaluation scripts, statistics, tables, or plots. |

### d. Fact–action representation (`src/ahg/task.py`)

- Facts are integer indices with string names. A **state is an `int` bitmask** (bit i = fact i held). This makes states hashable, and duplicate detection uses them directly as dict keys.
- **AND preconditions:** `Action.pre_mask`. `applicable(state)` is `pre_mask & ~state == 0`, meaning every precondition is held. **OR over achievers** is implicit: several actions can add the same fact. `Task.achievers[f]` and `Task.pre_of[f]` are the adjacency lists of the bipartite fact–action graph.
- `successors` yields only actions that are applicable **and useful** (they add at least one new fact). This is safe because the task is delete-free; the docstring says so.
- No explicit graph or PyG export exists yet. A GNN input would have to be built from `pre_of` and `achievers`.
- Goals are conjunctive (`goal_mask`), which is more general than the single target privilege in CLAUDE.md.

### e. Cost model

Not implemented, so it cannot match CLAUDE.md §1 rule 5 yet. One technical point is relevant later (see §6): the frozen formula gives real-valued costs, while the code is written and tested for integer costs.

### f. Search (`src/ahg/search.py`)

- One function, `best_first_search(task, h, w_g=1, w_h=1, start=None, max_expansions=None)`:
  - UCS: `h = 0`
  - A*: `w_g = w_h = 1`
  - weighted A*: `w_h = w`
  - GBFS: `w_g = 0`
- **Priority / tie-breaking** (lines 51, 86): the heap key is `(f, h, insertion counter, g, state)`. Ties on f go to lower h, then to the earliest-generated node (FIFO). This rule is documented in the module docstring.
- **Duplicate detection:** the `g_best` dict over states. A successor is pushed only if its g is strictly better than the best known (line 75). Stale heap entries are skipped on pop (line 63).
- **Reopening policy:** closed states **are reopened** if a strictly cheaper g is found (lines 77–78). The same policy applies to every heuristic because there is only one code path. It is documented in a code comment but not yet in `docs/decisions.md`, which does not exist.
- **Goal test** happens on expansion (pop), not on generation (line 66).
- **Counting:**
  - `expanded` is incremented for each non-stale popped node that is not a goal (line 71). **The goal node itself is not counted.**
  - `generated` counts every successor produced, including duplicates that get pruned.
  - `evaluations` is `len(h_cache)`, the number of distinct states whose h was computed. h is computed lazily and cached per state.
  - The counting code is shared by all heuristics, so it is identical across them.
- **Dead ends:** if h = INF, the node is never pushed. If h(s0) = INF, the search returns unsolved with `expanded = 0`.
- **Budget:** `max_expansions` returns unsolved with `budget_hit=True`. Otherwise, an unsolved result means the space was exhausted, i.e. the goal is unreachable. `SearchResult` has no explicit flag for "proved unreachable"; it has to be inferred from `not solved and not budget_hit`.
- **Timing:** `seconds` is wall-clock from the start of the call and includes every heuristic call, so heuristic computation time is counted.
- h is called **one state at a time** (`h(task, state)`). Batched heuristic evaluation is not supported.

### g. Heuristics (`src/ahg/heuristics.py`)

`relaxed_costs(task, state, mode, costs=None, stop_at_goal=True)` is a generalised Dijkstra over facts. Facts held in `state` cost 0. An action fires once its preconditions are reached, and it sets each add effect to `cost(a) + combine(precondition costs)`:

| ID | Code | Combine over preconditions | Combine over goals | Admissible? | Tested |
|---|---|---|---|---|---|
| h0 | `h0` | — | — | yes | yes |
| h_sp | `hsp` | `min` (an action fires as soon as its **first, cheapest** precondition is reached, i.e. AND treated as OR) | `max` | **yes** | `hsp ≤ hmax ≤ h*` on every reachable state of 60 random tasks |
| h_max | `hmax` | `max` | `max` | yes | as above |
| h_add | `hadd` | `sum` | `sum` | no | `h* ≤ hff ≤ hadd` checked |
| h_FF | `hff` | relaxed plan extracted backwards from h_add best supporters, summing distinct action costs | — | no | as above |
| LM-cut | `lmcut` | iterative h_max with cost reduction (Helmert & Domshlak 2009) | — | yes | `hmax ≤ lmcut ≤ h*` on every reachable state of 60 random tasks |

**How h_sp is computed and why it is admissible as implemented.** h_sp is a shortest-path relaxation: each action is treated as reachable once any one of its preconditions is reached, and the goal value is the max over goal facts. Every fact's h_sp value is therefore ≤ its h_max value, by induction over the Dijkstra order, because min ≤ max. Since h_max is admissible, h_sp is admissible too. The tests confirm h_sp ≤ h_max ≤ h* empirically. The word "cost-weighted" in CLAUDE.md matches this: edges carry action costs. The specific choice to combine over goals with **max** (rather than sum) is what keeps it admissible, and it should be written down in `decisions.md`.

**Observation (delete-free specific).** In a delete-free task, h+ = h*. h_FF's relaxed plan is therefore a real plan, so **h_FF ≥ h\*** always holds, and h_add ≥ h_FF in these tests. Both "inadmissible" references are upper bounds on h* here, never under it. This is worth stating in the paper.

**Missing relative to CLAUDE.md:** nothing at the heuristic level. LM-cut and h_FF are already implemented, which ticks part of the §5 checklist item on baselines. Fast Downward/PDDL export does not exist. Note that `HEURISTICS` also includes LM-cut and h_FF, while CLAUDE.md's definition of "normal A*" lists only h_max, h_add, and h_sp.

### h. Exact solver and label cross-check

- There is no `labels.py` and no label dataset. The exact solver would be `uniform_cost` or `astar(…, lmcut)` run from each sampled state (`start=` is supported).
- **Cross-check that exists (tests):** `brute_force_optimal` enumerates all action subsets. It is independent of the search code and only feasible for about 13 actions. Tests compare UCS, A* with every admissible heuristic, and GBFS plan validity against it on 60 random tasks (9 facts, 13 actions).
- An "independent UCS implementation" as required by CLAUDE.md rule 6 does **not** exist. UCS is the same `best_first_search` code that A* uses.

### i–l. Splits, models, training, evaluation

Not started. Nothing to report.

---

## 3. Runs performed during this audit

All runs used `.venv/bin/python` (Python 3.12.13) on an Apple M4. Probe scripts were placed in the session scratchpad, **not in the repo**, so the numbers in §3.3–3.4 are diagnostic and not reproducible from the repo as it stands.

### 3.1 Test suite

`python -m pytest -q`: **125 passed, 0 failed, in 7.33 s.**

| Test | Instances | Result |
|---|---|---|
| `test_toy_heuristic_values` | 1 | PASS |
| `test_toy_optimal_plan` | 1 | PASS |
| `test_search_matches_brute_force[seed]` | 60 (seeds 0–59) | 60 PASS |
| `test_admissibility_and_dominance_on_every_state[seed]` | 60 | 60 PASS |
| `test_random_tasks_are_not_trivial` | 1 | PASS |
| `test_weighted_astar_bound_with_admissible_h` | 1 | PASS |
| `test_budget` | 1 | PASS |

Slowest test: `test_admissibility_and_dominance_on_every_state[43]`, 0.70 s.

Tests required by CLAUDE.md §6, and whether they exist:

| Required test | Status |
|---|---|
| Labels vs independent UCS | partial: brute-force oracle exists; no label code, no separate UCS |
| Admissible heuristics never exceed h* | yes |
| A* with admissible h returns the optimal cost | yes |
| Identical node counting across heuristics | not tested explicitly; guaranteed structurally by the single code path |
| Split disjointness | not applicable yet |

### 3.2 Smallest end-to-end path: `scripts/toy_demo.py`

The toy network has 7 facts, 7 actions, and **14 reachable states**. True optimal cost h* = 150 (confirmed by brute force in the tests). Runtime was 0.025 s total.

Heuristic values at the initial state: `h0 0, hsp 90, hmax 100, hadd 180, hff 150, lmcut 150`.

| Run | Cost | Expanded | Generated |
|---|---|---|---|
| UCS | 150 | 9 | 16 |
| A*(hsp) | 150 | 8 | 14 |
| A*(hmax) | 150 | 5 | 9 |
| A*(lmcut) | 150 | 5 | 9 |
| A*(hadd) | 150 | 5 | 9 |
| A*(hff) | 150 | 5 | 9 |
| WA*(hmax, w=2) | 150 | 5 | 9 |
| GBFS(hadd) | 150 | 5 | 9 |

This is a hand-built toy graph, not a generated attack graph, so the pipeline from generator to search was not exercised.

### 3.3 Label agreement

For every reachable state of the toy task plus 60 random tasks (`random_task(seed)` for seeds 0–59: 9 facts, 13 actions), UCS cost from that state was compared with brute-force h*. Result: **1726 / 1726 states agree.** 36 of the 60 random tasks are solvable from the initial state. Reachable states per task were min 3, median 24, max 104. Runtime: 6.6 s.

### 3.4 Exact-solver scaling probe (random tasks, not attack graphs)

Random delete-free tasks were generated with `random_task(seed, n_facts=N, n_actions=1.5N, max_pre=3, max_add=2, goal_size=2)`, seeds 1000–1002, with a **30 s cap** per run. `inf` means unsolvable.

| N facts / actions | seed | UCS | A*(hmax) | A*(lmcut) |
|---|---|---|---|---|
| 10/15 | 1000 | 23, exp 17 | 23, exp 4 | 23, exp 2 |
| 10/15 | 1001 | inf, exp 12 | inf, exp 0 | inf, exp 0 |
| 10/15 | 1002 | inf, exp 18 | inf, exp 0 | inf, exp 0 |
| 20/30 | 1000 | inf, exp 7654, 0.03 s | inf, exp 0 | inf, exp 0 |
| 20/30 | 1001 | 42, exp 190 | 42, exp 30 | 42, exp 4 |
| 20/30 | 1002 | 47, exp 105 | 47, exp 21 | 47, exp 3 |
| 30/45 | 1000 | 49, exp 237 | 49, exp 23 | 49, exp 4 |
| 30/45 | 1001 | 37, exp 157 | 37, exp 9 | 37, exp 3 |
| 30/45 | 1002 | 6, exp 15 | 6, exp 4 | 6, exp 2 |
| 40/60 | 1000 | 21, exp 345 | 21, exp 21 | 21, exp 3, 0.01 s |
| 40/60 | 1001 | 154, exp 146357, 1.11 s | 154, exp 46531, 1.87 s | 154, exp 11, 0.05 s |
| 40/60 | 1002 | inf, exp 190080, 1.50 s | inf, exp 0 | inf, exp 0 |
| 60/90 | 1000 | 62, exp 2130, 0.02 s | 62, exp 124, 0.02 s | 62, exp 6, 0.03 s |
| 60/90 | 1001 | **TIMEOUT > 30 s** | **TIMEOUT > 30 s** | 117, exp 18, 0.40 s |
| 60/90 | 1002 | 11, exp 207 | 11, exp 6 | 11, exp 2, 0.01 s |
| 80/120 | 1000 | **TIMEOUT > 30 s** | inf, exp 0 | inf, exp 0 |
| 80/120 | 1001 | **TIMEOUT > 30 s** | inf, exp 0 | inf, exp 0 |
| 80/120 | 1002 | 13, exp 422, 0.01 s | 13, exp 17, 0.01 s | 13, exp 2, 0.02 s |

What this probe shows, with the caveat that random tasks are not structured like attack graphs:

- UCS and A*(hmax) already blow up past 30 s at about 60 facts / 90 actions on some instances.
- A*(LM-cut) solved every instance in ≤ 0.40 s, expanding at most 18 nodes. **LM-cut was nearly perfectly informed on these tasks** (see §6.2).
- The largest graph the exact solver handles within ~1 minute on real attack graphs is **not measurable yet**, because no attack-graph generator exists.

---

## 4. Existing results

**None.** The repo contains no results files, logs, checkpoints, datasets, `results/` or `runs/` directories, or experiment logs. The only numbers in the repo are hard-coded test expectations for the toy network in `tests/test_core.py:13-28` (hsp 90, hmax 100, hadd 180, hff 150, optimal 150), and these match the demo output above.

---

## 5. Integrity check against CLAUDE.md §1

| # | Rule | Verdict | Evidence |
|---|---|---|---|
| 1 | No test leakage | **CANNOT TELL YET** | No splits, data, normalization, or training code exists. |
| 2 | Training-graph results diagnostic only | **CANNOT TELL YET** | No results. |
| 3 | Never fabricate results | **COMPLIANT so far** | No reported results exist. The toy numbers in `test_core.py` are asserted by tests and reproduced by `toy_demo.py`. Note that `docs/learn/README.md` says chapters 01–03 are "written" with "real" numbers, but those files are not in the repo, so their numbers cannot be checked. |
| 4 | Never fabricate citations | **COMPLIANT so far** | The only in-code citation is "Helmert & Domshlak 2009" (`heuristics.py:128`) for LM-cut. It is a real ICAPS 2009 paper; the bibliographic details were not checked in this audit. The repo has no bibliography file. |
| 5 | Cost model frozen, `c = 1 + 9(1 − x)` | **CANNOT TELL YET (not implemented)** | No code computes it. Toy and test costs are arbitrary integers. `Action.cost: int` (`task.py:24`). |
| 6 | Labels verified vs independent UCS and enumeration | **PARTIAL** | Brute-force enumeration oracle (`tests/helpers.py:25-50`) is used in tests (1726/1726 agreement in §3.3). A separate, independent UCS implementation does not exist. No label pipeline exists to verify. |
| 7 | Fair comparison | **COMPLIANT by design (for classical heuristics)** | All algorithms share one `best_first_search` (`search.py:41`), with the same tie-breaking (line 86), duplicate detection (lines 63, 75), and counting (lines 70–73). Timing includes heuristic calls (`t0` at line 44, h called inside the loop at line 82). GNN timing **cannot tell yet**. Risk: the `h(task, state)` interface is per-state, so a GNN cannot be batched without changing the API. |
| 8 | No optimality claims for inadmissible heuristics | **COMPLIANT** | `ADMISSIBLE = {"h0","hsp","hmax","lmcut"}` (`heuristics.py:209`). The weighted-A* bound is only tested with h_max (`test_core.py:73-80`). h_add and h_FF are labelled inadmissible in the docstring. |
| 9 | Seeds and provenance everywhere | **NOT YET IN PLACE (at risk)** | No run-logging code. **Zero commits**, so no commit hash could be recorded for any run today. Test seeds are fixed (`SEEDS = range(60)`). |
| 10 | Unreachable goals logged separately | **CANNOT TELL YET** | No experiment code. `SearchResult` can tell budget exhaustion apart from an exhausted space (`budget_hit`), which is the right building block. |
| 11 | Raw results append-only | **CANNOT TELL YET** | No results directory. `runs/` is git-ignored in `.gitignore` but `results/` is not mentioned. |

Specific checks requested:

- **Test leakage:** none possible yet, because there is no data.
- **Normalization statistics computed on test data:** not applicable yet. No normalization code exists, including normalization of CVSS `x_a` into [0, 1].
- **Inconsistent node counting across heuristics:** not present; the code path is shared.
- **GNN inference time excluded from timing:** not applicable yet. The current design times every h call, but batching would need an API change that keeps the batch inside the timed region.

---

## 6. Problems and risks

### 6.1 Process and grading risks (high)

1. **Zero commits.** The course grades "commit history that reflects work across the semester" and flags last-minute history (`AI_Project_Guidelines.v1.md` around lines 158, 216, 255). Code written on 17 Oct is not yet in git. Nothing is pushed (not verified on GitHub).
2. **Required docs are missing:** `docs/decisions.md`, `docs/experiment_log.md`, `docs/ai_usage_log.md`.
3. **The learning guide references files that don't exist** (chapters 01–05, glossary, `PREREG.md`). They were either never saved or never added to the repo.
4. **Schedule.** The proposal timeline puts the MulVAL go/no-go and cost-model fixing in weeks 1–2 and generators plus CVE assignment in week 3. None of these exist. The week 4 items (classical baselines, cross-check) are largely done early. **The critical path is now the generator.**
5. `.DS_Store` is not git-ignored.

### 6.2 Research-design risks

1. **LM-cut may be close to perfect on delete-free tasks.** In §3.4, A*(LM-cut) expanded 2–18 nodes on every random instance, including ones where UCS and h_max ran out of time. If generated attack graphs behave the same way, then:
   - H1 ("fewer expansions than hand-crafted baselines") will very likely fail against LM-cut, and a reviewer will insist on LM-cut.
   - The honest comparison shifts to **wall-clock time** (per-state LM-cut cost vs GNN inference) and to the weaker baselines.
   - CLAUDE.md's "normal A*" (h_max, h_add, h_sp) excludes LM-cut. Results reported only against that set would look cherry-picked.

   This should be measured on real generated attack graphs before the GNN is built.
2. **h_add and h_FF are upper bounds on h\*** in delete-free tasks (tested: `h* ≤ hff ≤ hadd`). This means GBFS or A* with h_FF is a strong anytime baseline. It also means "inadmissible" here always means overestimating, which shapes the H2 narrative.
3. **Exact alternatives exist.** Optimal delete-free planning, i.e. computing h+, has dedicated exact methods (hitting-set and MIP-based approaches) `[VERIFY: specific papers and venues not checked in this audit]`. Reviewers may ask why search is used at all. The related-work positioning needs to address this.
4. **Random test tasks are not attack-graph-shaped.** All verification so far uses `random_task` and the toy. Admissibility and optimality tests should be re-run on generated attack graphs once they exist.

### 6.3 Code-level issues and divergences (no bugs found in tested behaviour)

1. **Real-valued costs vs integer assumptions.** The frozen model gives real costs in [1, 10], but:
   - `Action.cost: int` (`task.py:24`).
   - LM-cut subtracts costs in floating point (`heuristics.py:205`) and then tests `costs[ai] == 0` exactly (`heuristics.py:170`), followed by `assert m > 0` (line 202). Float residues such as 1e-16 could break the goal-zone construction or trigger the assertion.
   - Exact-equality comparisons in search (`g2 >= g_best`) and in the label cross-check (`==`) are also brittle with floats.

   One option is to store costs as exact integers. For example, with CVSS v3 exploitability `E` (one decimal place, maximum 3.9) normalised as `x = E/3.9`, `39·c = 39 + 9·(39 − 10E)` is an integer. **This depends on the normalization choice, which is not yet defined**, and it must be recorded in `decisions.md` without changing the formula itself.
2. **`successors` scans every action per expansion** (`task.py:82`), which is O(|A|) per state. That is fine now but will matter for large test graphs and for timing fairness. It is the same for all heuristics, so it is fair but slow.
3. **The heuristic API is per-state** (`h(task, state)`). A GNN needs batched evaluation of successors to be competitive in wall-clock time. Any batching change must keep timing and evaluation counting identical across methods.
4. **Expansion counting excludes the goal node** (`search.py:66-71`). It is consistent across methods but should be documented, since papers differ on this.
5. **Reopening policy** (reopen on strictly cheaper g) is documented only in a code comment.
6. **Goals are conjunctive tuples.** CLAUDE.md describes a single target privilege. This is a harmless generalisation.
7. `relaxed_costs` treats any unknown `mode` string as `"add"` (`heuristics.py:83`). This is minor.
8. **Dependencies:** `pyproject.toml` declares no runtime dependencies, so torch, PyG, numpy, scipy, and pyyaml are all missing. There are no configs and there is no run-provenance code.
9. TODO/FIXME/XXX/HACK markers in `src/`, `tests/`, `scripts/`: **none found**.
10. **Hardcoded constants:** toy costs (`examples.py`), test generator defaults (`helpers.py:7`), and `SEEDS = range(60)`. All are test or demo only. No experiment constants exist yet.

### 6.4 Scalability

- On random tasks, UCS and A*(h_max) exceed 30 s at about 60 facts / 90 actions on some seeds. A*(LM-cut) stayed ≤ 0.4 s up to 80 facts / 120 actions (§3.4).
- On attack graphs: **not measurable**, because there is no generator.
- `brute_force_optimal` is exponential in |A| and is only usable up to about 13–15 actions.

---

## 7. Recommendations (ordered by leverage)

1. **Commit and push now, then commit small and often** (≈ 30 min).
   - Add `.DS_Store` (and `results/raw` policy) to `.gitignore`.
   - Make several logical commits: task model, search, heuristics, tests, docs.
   - Create `docs/decisions.md`, `docs/experiment_log.md`, `docs/ai_usage_log.md`.
   - Recover or restore the missing `docs/learn` chapters.

   This protects the course grade (commit-history evidence) and makes rule 9 (commit hash per run) possible.
2. **Record the outstanding formulation decisions in `docs/decisions.md`** (≈ 2–3 h). These should come before any generator output:
   - MulVAL go/no-go.
   - The exact normalization of `x_a` and an exact numeric representation of costs (e.g. integer units, see §6.3.1), so LM-cut and the label checks stay exact.
   - The h_sp definition (AND→OR, max over goals).
   - The reopening policy and the expansion-counting convention.
   - Whether LM-cut and h_FF are part of "normal A*". Recommendation: yes.
3. **Build the native generator end to end** (≈ 1.5–2 weeks; this is the critical path for both the course and the paper):
   - topology families (flat, tiered, hub-and-spoke) with seeds;
   - a pinned local NVD snapshot with CPE-to-service mapping;
   - CVSS → cost;
   - a `Task` builder;
   - logging of unreachable goals.

   Re-run the existing admissibility and optimality tests on generated graphs, and add an independent UCS (a few dozen lines) to fully satisfy rule 6.
4. **Pilot before any learning** (≈ 2–3 days once item 3 is done). On generated graphs across sizes, measure:
   - h* vs h_max, LM-cut, h_FF gaps;
   - expansions and wall-clock time for each baseline;
   - the exact-solver size limit (~1 min).

   This decides the paper's framing. If LM-cut is near-exact, H1 should be judged on wall-clock time and/or GBFS, and the hypothesis wording should be updated *before* experiments via `decisions.md`. It also fixes the label-size limit and the expansion budgets.
5. **Data and learning infrastructure, then models** (≈ 2–3 weeks):
   - topology-level splits from disjoint seeds, with a disjointness test;
   - state sampling and label generation;
   - a run-provenance wrapper that saves config, git hash, seeds, versions, and hardware;
   - a batched heuristic interface in search that keeps timing and counting identical;
   - add torch and PyG to `pyproject.toml`;
   - MLP ablation first (cheap, validates the pipeline), then the GNN, with ≥ 5 seeds.

   CPU or MPS on the M4 should be checked; no CUDA is available locally.

Effort estimates are rough and assume solo work. They are not derived from measured data.
