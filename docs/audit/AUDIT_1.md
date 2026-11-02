# Independent research-codebase audit

## Audit metadata

- Repository: `DevanshSharma867/learned-heuristics-attack-graphs`
- Audited snapshot: uploaded ZIP, archive commit `b728e4bf9cfea92fbda296cffd4bd424d78d5101`
- Working copy: fresh extraction at `/mnt/data/audit-work/repo`; no commits or pushes made
- Live GitHub clone: attempted but unavailable because this environment could not resolve `github.com`; conclusions are scoped to the uploaded snapshot
- Runtime constraint: requested Python 3.12 is not installed; Python 3.13.5 and `uv` 0.10.0 were available. Tests and reproductions were run under Python 3.13.5 where possible and are explicitly labelled; no clean Python 3.12 run was possible.
- Phase A was intended to be blind to `docs/findings.md`, `docs/decisions.md`, `docs/experiment_log.md`, `docs/related_work.md`, and `results/`. A repository-wide grep accidentally emitted a few matching lines from docs/results before Phase A ended; this breach was disclosed and recorded. Phase B subsequently reviewed the specified docs and reports.

## Final summary

### Top 5 issues by severity

1. **MAJOR — BUG:** The D23 residual-ranking GNN is optimized with `h_max + softplus(r)` but searched with `h_max + max(0,r)`; the two can reverse state order, so the learned headline is not evaluating the exact trained ranker.
2. **MAJOR — STATISTICS:** D15/D16 R2/R3 sign-test p-values treat repeated knob-cell observations of the same `(family, seed)` network/CVE assignment as independent, inflating the effective sample size.
3. **MAJOR — BUG:** NVD CPE parsing ignores node negation and fails to recurse into nested configuration nodes; derived CVE membership can be both over- and under-included.
4. **MAJOR — MODELLING:** CVEs are assigned to services by family only, without concrete vendor/product/version compatibility; this is a synthetic family-level proxy, not realistic vulnerability applicability.
5. **MAJOR — TEST-GAP:** The D23 decision claims GBFS/weighted-A* h_add comparators and nested-bootstrap/Holm/Wilcoxon analysis are implemented, but they are absent from the checked-in evaluator/source; no held-out test-evaluation reports or final frozen manifest are present in this snapshot.

### Headline result risk

The **0.595× h_max node-expansion** number is a real D22 validation statistic for 82 instances and one training seed, not a test/generalization result. It is validation-selected, affected by the train/inference score-transform mismatch, and the same report measures **5.30× h_max end-to-end time**. The classical near-plan-length A* result is substantially better supported for the measured synthetic delete-free generator, but “near-exact” must refer to search effort, not pointwise h-value exactness: D16 records large h* gaps on many states A* expands.

### Before publication

Fix and test the full NVD applicability traversal; either implement product/version-specific service matching or explicitly limit the claim to family-level synthetic assignment; align training and inference score transforms and retrain; reanalyse the depth/coupling sign tests with topology-seed clustering; implement and test the declared h_add/GBFS/weighted-A* comparators and nested multi-seed statistics; complete all planned seeds and one-shot held-out evaluations; report end-to-end time against h_max as well as LM-cut; provide the raw NVD snapshot (or permanent immutable artifact), label batches, frozen model manifest and clean Python 3.12 reproduction.

### Reviewer objections to answer

- **CVE validity:** rerun with product/version-specific installed software and full NVD nested AND/OR/negation semantics.
- **Synthetic-task external validity:** validate on a richer independent attack-graph benchmark with realistic conjunctions and, where relevant, delete effects.
- **Statistics:** repeat R2/R3 inference with topology/seed clusters and multiplicity control.
- **Baseline fairness:** compare against A*+h_add, GBFS+h_add and weighted A*+h_add at w=1.5,2 under identical search budgets and tie/reopen rules.
- **Generalization and uncertainty:** finish multi-seed training and the five held-out test splits; use nested instance/seed bootstrap and Holm-corrected paired tests.
- **Practical speed:** measure counterbalanced end-to-end wall time including GNN inference on a fixed quiet machine.
- **Sensitivity:** rerun with alternative monotone and uniform cost maps, plus alternate CVE/product sampling.
- **Reproducibility:** provide the immutable raw NVD input, derived/label artifacts, checkpoints and complete source/data hashes.

**Scope and limits:** no CRITICAL issue was established. Audit ran against the uploaded ZIP (archive metadata commit `b728e4bf9cfea92fbda296cffd4bd424d78d5101`), not a live Git clone; GitHub DNS resolution failed. Python 3.12 was unavailable, so code/test runs used Python 3.13.5 with temporary external shims for Git/distribution metadata where needed. No files were committed or pushed. The Phase A blind breach is disclosed in the body.

---

# Phase A — Blind module sweep

## 1. Data pipeline

### Finding D1 — NVD applicability negation is ignored

- **Location:** `src/ahg/cve.py:116-121`
- **Type / severity:** BUG / MAJOR
- **Problem:** `vulnerable_products()` treats every `cpeMatch` with `vulnerable: true` as a positive affected-product match, but never checks the containing node's `negate` field. NVD's CVE API 2.0 schema includes `node.negate` (current schema 2.2.4, `node` definition), and NVD's API documentation describes this as a logical negation flag. A product match inside a negated node cannot safely be interpreted as an unconditional positive applicability match.
- **Why it matters:** A CVE can be incorrectly assigned to a product family, changing the CVE pool and downstream action costs/features. The bug is in the parser irrespective of whether the selected snapshot happens to contain affected examples.
- **Verification:** Ran a throwaway fixture under `PYTHONPATH=src python3` with one `negate: true` node containing a matching `vulnerable: true` CPE. `vulnerable_products()` returned `{'acme:widget'}`. No branch in lines 116-121 reads `negate`. The raw NVD pages are absent from this snapshot, so the number of affected rows in the committed CSV could not be measured.
- **Reference:** NVD CVE API 2.0 schema: <https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema> (the `node` definition has `negate`, lines 437-460); NVD applicability statement explanation: <https://nvd.nist.gov/developers/vulnerabilities-1>.
- **Remediation:** Evaluate the logical applicability statement rather than scanning for matching CPE strings independently of node semantics; add tests for positive, negated, AND, and OR configurations. At minimum, explicitly reject or separately handle negated nodes rather than counting their CPEs as positive matches.

### Finding D2 — The raw NVD snapshot required to reproduce the derived table is absent from the repository

- **Location:** `.gitignore:5-7`; `scripts/derive_cves.py:33-44`; derived artifact `data/derived/build_log.json:93-100`
- **Type / severity:** REPRODUCIBILITY / MAJOR
- **Problem:** The repository ignores all of `data/*` except `data/derived/`, so `data/raw/nvd/<snapshot>/manifest.json` and the compressed NVD page files are not present in the supplied repository snapshot. `derive_cves.py` requires those files and validates their hashes before regenerating `data/derived/cves.csv`.
- **Why it matters:** A fresh checkout cannot rebuild the committed CVE table or independently verify its inclusion counts from the referenced NVD snapshot. A manifest hash and snapshot date in `build_log.json` are not substitutes for distributing or making the exact immutable input data retrievable.
- **Verification:** `find data -maxdepth 3 -type d -name '2026-*'` found no raw snapshot directory. Ran `PYTHONPATH=src python3 scripts/derive_cves.py 2026-10-21`; it exited with `FileNotFoundError` for `data/raw/nvd/2026-10-21/manifest.json`. `.gitignore` explicitly excludes the raw data. The build log records snapshot date `2026-10-21` and manifest SHA-256 `0e5a3b...cb387e`, but the manifest itself is absent.
- **Remediation:** Publish the immutable snapshot in an artifact store/release (with stable URL and checksum) or provide a deterministic retrieval script and the exact manifest. Make the rebuild instructions fetch/verify it before deriving the CSV.

### Finding D3 — CVE-to-service assignment is family-only, not product- or version-valid

- **Location:** `src/ahg/network.py:36-41`; `src/ahg/assign.py:3-8,33-40`
- **Type / severity:** MODELLING / MAJOR
- **Problem:** A `Service` records only a family label (for example, `sql` or `http`). `assign_cves()` samples any CVE in that family uniformly, even though the derived CVE table distinguishes vendor/product and NVD match criteria can include version ranges. No service has a concrete product/version identity, and assignment never checks the CVE's applicable version range.
- **Why it matters:** The generated attack graphs represent family-level vulnerability exposure, not a realistic mapping from installed software inventory to applicable CVEs. A generated `sql` service can receive a CVE for PostgreSQL, Oracle MySQL, MariaDB, or Microsoft SQL Server without the service being tied to any of those products. Claims about product-realistic vulnerability assignment or real-world applicability would be unsupported. This may be acceptable as an explicit synthetic abstraction, but it materially limits the external validity of conclusions.
- **Verification:** Inspected the `Service` dataclass (`family` is its only software identity field) and `assign_cves()` (candidate pool filtered only by `r.family == s.family`, then `rng.choice`). The committed table itself includes multiple distinct vendor/product identities per family; for example, `sql` contains `oracle:mysql`, `mariadb:mariadb`, `postgresql:postgresql`, and `microsoft:sql_server` rows.
- **Remediation:** Either add a product/version identity to generated services and sample only matching product/version CVEs, or state clearly that service families are abstract vulnerability buckets and avoid interpreting generated CVE assignments as concrete software vulnerability exposure.

### Data checks with no issue found

- **CVSS version mixing:** No v2 exploitability values are fed into the cost pipeline. `nvd_primary_v3()` selects NVD Primary v3.1 first, then NVD Primary v3.0 (`src/ahg/cve.py:62-76`); v2-only and v4-only records are classified as exclusions (`src/ahg/cve.py:90-105`). In the committed table, 1,056 records use v3.1 and 417 use v3.0.
- **Publication window:** `derive()` applies an inclusive `2016-01-01` through `2023-12-31` publication-date filter (`src/ahg/cve.py:40,166-169`). The committed table ranges from `2016-01-13` to `2023-12-24`.
- **Derived-table uniqueness and counts:** The table contains 1,473 rows and 1,473 unique CVE IDs, with no duplicate `(CVE, family)` assignments. The build-log inclusion counts sum to 1,473. These checks establish internal consistency, not independent correctness of the unavailable raw snapshot.
- **Score/PR pairing:** Score and `Privileges Required` are read from the same NVD Primary v3 metric, and the PR vector component is checked against `cvssData.privilegesRequired` (`src/ahg/cve.py:62-87`).

---

## 2. Cost model

### Cost-distribution measurements

The frozen mapping in `src/ahg/cost.py:3-7,16-32` is internally consistent:

- `k = round(10E)` for NVD exploitability score `E` on the one-decimal grid;
- `x = (k - 1) / 38`;
- effort cost `c = 1 + 9(1 - x)`;
- stored integer cost `C = 38c = 389 - 9k`.

Measured on the committed 1,473-row CVE table:

- Stored-cost range: **38–362** units; effort range: **1.000–9.526**.
- Mean effort cost: **4.201**; median: **3.605**.
- **22 distinct** cost values occur in the table (39 grid values are mathematically possible).
- 472/1,473 records (**32.0%**) are at the minimum cost of 1.0; 310 (**21.0%**) cost 3.605; 265 (**18.0%**) cost 7.395.
- Family means vary materially: DNS 2.40, FTP 2.80, HTTP 2.47, mail 3.30, RDP 3.35, SMB 3.96, SQL 5.65, SSH 3.48 effort units. This reflects the CVE score mix and the family-specific sampling pools.

### Checks with no issue found

- The integer formula matches the stated continuous mapping exactly on all 39 allowed `k` values; costs remain positive and in the intended [1, 10] effort range.
- The one-decimal input check rejects off-grid/out-of-range values. The `round()` path avoids the demonstrated floating-point truncation case.
- Integer units preserve exact path-cost comparisons; the scale factor is consistently 38 in the core task/search/training paths inspected.
- The actual distribution is discrete and skewed, not close to uniform. However, it is **not** so uniform that the model collapses to hop-count planning: 68% of the table's CVEs have costs above the minimum, and the maximum is over 9.5 times the minimum. There is a substantial minimum-cost atom that should be disclosed, but no cost-arithmetic defect was found.

**Verification:** Ran `PYTHONPATH=src pytest -q tests/test_cost.py` — 49 passed. Independently loaded `data/derived/cves.csv`, recomputed every cost using `ahg.cost.cost_units`, and computed the range, moments, unique-value count, mass at the minimum, and per-family summaries. Raw NVD pages were not needed for these calculations.

---

## 3. Topology generators and CVE assignment

### Checks with no issue found

- **Seed determinism:** all topology randomness is local to a `random.Random` seeded from the topology family and integer seed (`src/ahg/topology.py:121-126`). Service-family sampling is sorted before storage; repair candidates are created in deterministic list order. The cross-process test also varies `PYTHONHASHSEED` (`tests/test_topology.py:25-35`).
- **Connectivity:** every generated internal host is reachable from the internet over host/service reachability edges. Flat and tiered repair unreachable hosts using only allowed sources; hub-and-spoke repairs only through the assigned hub/spokes structure. This property held in the test suite and in 500 seeds per family at 30 hosts (1,500 networks total).
- **Family semantics:** flat permits arbitrary internal source/destination pairs; tiered permits same-tier and one-tier-down edges with only tier 0 exposed; hub-and-spoke restricts spokes to their assigned hub and connects hubs to hubs. Tests cover these invariants (`tests/test_topology.py:78-114`).
- **Variation:** over 500 seeds at 30 hosts, mean network summaries were distinct: flat had about 534 reach edges and depth 2.22; tiered about 251 reach edges and depth 3.41; hub-and-spoke about 76 reach edges and depth exactly 3. All had 30/30 reachable hosts. The default hub-and-spoke configuration is a single-hub star, so its structure is intentionally very distinctive (`hub_share=1.0`).
- **Randomness stream separation:** CVE assignment sorts each family pool and uses a separate `cves:<family>:<seed>` RNG stream from the topology generator (`src/ahg/assign.py:18-40`). Deterministic, pool-order-independent, family-consistent assignment is covered by `tests/test_assign.py`.

### Topology limitations to disclose (not implementation bugs)

- The connectivity repair deliberately forces every host to be reachable, so the benchmark does not sample arbitrary partially disconnected enterprise networks. It models reachable, attackable hosts by construction (`src/ahg/topology.py:15-18,89-109`). This is a scope restriction rather than a defect in the stated generator.
- The default family parameters differ along more than one dimension (e.g. exposure probabilities, reach probabilities, trust probabilities, and allowed edge patterns). A held-out-family result therefore generalizes to the bundled family distribution as a whole, not to an isolated causal effect of one structural feature.
- Hub-and-spoke defaults to one hub (`src/ahg/topology.py:205-213`), making the family close to a star and easy to distinguish structurally. The default topology split should not be described as a broad sample of multi-hub enterprise networks without separate parameterized coverage.

**Verification:** `PYTHONPATH=src pytest -q tests/test_topology.py tests/test_assign.py` — 447 passed. Separately generated 500 seeds per family at 30 hosts and measured service counts, reach/trust edges, exposure, reachability, BFS depth, deep-host share, and hub share. Every sampled topology had all 30 internal hosts reachable. No additional generator or deterministic-seed bug found.

---

## 4. Attack-graph generator and generation knobs

### Finding G1 — Every generated service is assumed vulnerable, and every reach edge becomes an exploit

- **Location:** `src/ahg/assign.py:18-40`; `src/ahg/attack_graph.py:146-154`
- **Type / severity:** MODELLING / MAJOR
- **Problem:** `assign_cves()` assigns exactly one CVE to every service. `build_task()` then emits an exploit action for every network reach edge, using the CVE attached to that service. There is no probability that a service has no known applicable vulnerability, no patch/mitigation state, and no unaffected service. Therefore every permitted network connection to a service is an exploit transition in the base graph.
- **Why it matters:** The generator makes the environment fully vulnerable by construction. Combined with topology repair (every host reachable), it guarantees a route to every host in the ungated base model. It removes the important real-world distinction between network reachability and vulnerability/exploitability. This materially simplifies attack planning and makes the base results conditional on a 100%-vulnerable service model.
- **Verification:** `assign_cves()` iterates every `net.services` entry and always assigns one record; `build_task()` iterates every `net.reach` entry and unconditionally appends an `exploit` action. The base-generation sample at 12 hosts had 100/100 reachable tasks in each family; no base instance raised `UnreachableGoal`.
- **Remediation:** Model vulnerability prevalence explicitly (including services with no assigned CVE and patched/unaffected versions), or state that the benchmark assumes every modeled service has one known vulnerability and restrict all external-validity claims accordingly.

### Finding G2 — Default attack tasks are almost entirely unary weighted-reachability problems

- **Location:** `src/ahg/attack_graph.py:146-162,247-261`
- **Type / severity:** MODELLING / MAJOR
- **Problem:** With default arguments (`pr_gated=False`, `cred_levels=0`, `coupling=0.0`), every exploit action has exactly one host precondition and one host effect. The only conjunctive actions are optional login alternatives; in the observed baseline sample they were rare, and the optimal plans almost never used them. The more demanding PR, credential-depth, and coupling preconditions are opt-in knobs, not part of the default formulation.
- **Why it matters:** Most baseline instances reduce to weighted directed reachability / shortest-path planning over hosts, not a general conjunctive attack-planning problem. This gives h_max little room to improve over the exact relaxed graph distance and weakens claims about learning a heuristic for complex conjunctive planning. The effect is visible in exact small-instance measurements below.
- **Verification:** Built 30 real-pool instances per family at 8 hosts using defaults. Compared uniform-cost search against A*+h_max. Mean optimal plan lengths were flat 3.0 (range 1–5), tiered 3.8 (3–5), and hub-and-spoke 3.0 (always 3). `h_max(start) == UCS optimal cost` in 29/30 flat, 27/30 tiered, and 30/30 hub-and-spoke tasks. Across the 90 chosen plans, only 8 actions were `login`; the remaining 286 were `exploit`. In the full action sets, all exploit actions were unary; multi-precondition actions came only from logins. These are small-instance measurements, not a claim about the uninspected primary result dataset.
- **Remediation:** Make the conjunctive attack prerequisites central to the primary benchmark rather than optional, and/or add realistic exploit prerequisites such as service-specific credentials, lateral-movement material, multi-host conditions, and partial vulnerability coverage. Report separate results for unary baseline and conjunctive variants.

### Finding G3 — The coupling parameter is not validated as a probability

- **Location:** `src/ahg/attack_graph.py:223-244,247-261`
- **Type / severity:** BUG / MINOR
- **Problem:** `coupling` is used as a Bernoulli probability but is never checked to be in [0, 1]. Negative values are silently accepted and produce no coupled exploits; values above 1 silently select every eligible internal exploit (and may make the goal unreachable). `make_instance()` routes any truthy value into `couple_exploits()`.
- **Why it matters:** A malformed experiment config can silently run a different setting from the one intended, or produce avoidable unreachable instances instead of a clear configuration error.
- **Verification:** Ran `make_instance("flat", 0, 8, pool, coupling=-0.5)`; it returned successfully with zero coupled actions. `coupling=1.5` was also accepted by the knob code and proceeded to an `UnreachableGoal`, not an invalid-parameter error.
- **Remediation:** Validate finite `0 <= coupling <= 1` at the public entry point and add tests for values below 0, above 1, NaN, and valid endpoints.

### Checks with no issue found

- **Initial state:** `Task` starts with exactly `1 << INTERNET`; no internal host, user capability, admin capability, or credential fact is initially held (`src/ahg/attack_graph.py:163-176`).
- **Goal selection:** the target is an internal host selected among those at maximum BFS hop distance from the internet (`src/ahg/attack_graph.py:183-193`). This is deterministic for a given topology family and seed.
- **Action semantics:** default exploit actions have a single source-host precondition and add the destination host. Login actions require both the network-access source and the trust/credential source (deduplicated when identical), and add the trusted destination (`src/ahg/attack_graph.py:155-162`). The tests exercise a hand-checked conjunctive login case.
- **Knob failure handling:** PR gating, credential levels, and coupled exploits can make a goal unreachable; `build_task()` checks `h_max(init)` and raises `UnreachableGoal` instead of pretending the instance is solved. In a 100-seed, 12-host probe, base tasks were all reachable; PR gating produced 4–11% unreachability, D=2 credential levels 16–31%, and coupling=1/share_pool=1 7–54%, depending on family. These failures are detectable by the caller, though their treatment by dataset/evaluation scripts is audited later.
- **Depth/coupling semantics:** the existing tests check credential level facts, level occupancy, coupling holder exclusion, and `exposed_level0` placement. No additional semantic defect was demonstrated in this module.

**Verification:** Inspected `attack_graph.py`, `task.py`, `assign.py`, and generator tests. Ran throwaway probes with the committed CVE pool: 30 seeds/family at 8 hosts with A*+h_max and UCS; 100 seeds/family at 12 hosts for base, PR-gated, D=2, D=2+exposed-level0, coupling=0.5, and coupling=1/share_pool=1. The primary result paths and label-generation scripts have not yet been read; the base-task findings must be reconciled with the actual labelled experiment variants in later modules.

---

## Phase A — Module 5: Task model and search

**No defect found in the inspected task/search core.** `Task.successors` implements the delete-free transition relation directly: an action is emitted exactly when its conjunctive preconditions hold and it adds at least one new fact. Search applies the corresponding add effects, tracks best `g`, discards stale queue entries, and reopens a closed state when a cheaper path is found. Goal testing is on dequeue (before the budget check), avoiding premature goal-on-generation termination. Expansion counts exclude goal states and stale entries; trace length is explicitly kept equal to expanded count. Tie-breaking is fixed as `(f, h, insertion_order)` for all wrappers.

**Verification:** `PYTHONPATH=src pytest -q tests/test_core.py` (485 passed) and `PYTHONPATH=src pytest -q tests/test_attack_graph.py` (349 passed, 3 skipped). A throwaway four-fact task with an admissible but inconsistent heuristic caused state `{s,a}` to be expanded twice; A* reopened it and returned cost 12, matching UCS. The core test suite also checks weighted-A*'s 2x bound on 60 generated tasks and trace/budget invariance across algorithms and heuristics. No finding filed. Residual test gap noted for Module 11: direct reopening is not in the committed test suite, despite the targeted throwaway check passing.

## Phase A — Module 6: Heuristic correctness

**No defect found in the inspected heuristic implementations.** h-sp uses the cheapest reached precondition (relaxing conjunction to OR); h-max uses max; h-add uses sum; h-FF extracts a shared relaxed supporter plan; LM-cut iteratively subtracts action-cost landmarks. For the modeled delete-free task, the relaxed planning problem is the original task, so the distinction is between optimal relaxed planning and polynomial approximations, not a discrepancy between the planning model and its delete relaxation.

**Verification:** an independent throwaway generator built 20,000 random delete-free tasks (2–7 facts, 1–18 actions, conjunctive preconditions, multi-fact add effects, positive integer costs). For each task, a separate frozenset/UCS oracle checked `hsp <= h*`, `hmax <= h*`, `lmcut <= h*`, h-max's unreachable detection, and `h* <= hff <= hadd` for reachable starts. All 20,000 passed. Existing `tests/test_core.py` additionally checks all reachable states over 60 random tasks; `tests/test_attack_graph.py` checks the attack-graph-specific cases. No finding filed. The throwaway check supplements, but does not replace, a committed exhaustive/property-based heuristic test.

## Phase A — Module 7: Oracle, label generation and splits

**No oracle-independence or split-overlap defect found in the inspected code.** The production oracle in `src/ahg/oracle.py` uses `frozenset` fact sets, independent applicability tests (`pre <= state`) and its own Dijkstra loop; it does not call the production search or `Task.successors`. The labeler cross-checks A*+LM-cut labels with A*+h-max, `check_admissible`, backward exact enumeration when the reachable state space is under `enum_cap`, and the independent UCS oracle (with skipped budget-limited checks counted separately). Optimal-path suffix labels are valid because actions are delete-free and path costs are additive. Random walks, expanded-state traces and successors have deterministic, separate RNG streams.

**Split verification:** train has 3,000 seeds, val and each test split have 100; all seed sets are disjoint and none intersects reserved seeds 0–19 or 100–119. The configured cell counts are 84 for train/val/test-ID/test-vuln, 42 for test-size, and 28 for test-structure. CVE hash pools partition the 1,473-record table into 988 train-pool and 485 heldout records; the costly-heldout subset has 344. All eight families remain represented in each pool. Train and validation deliberately share the train CVE pool (topology-level validation); test-vuln/test-vuln-cost use the disjoint heldout CVE pool.

**Verification:** inspected `src/ahg/oracle.py`, `labels.py`, `measure.py`, `splits.py`, `dataset.py`; ran split-range/CVE-pool intersection checks; `tests/test_labels.py` produced 3 passes, 4 setup errors and 2 failures because the ZIP has no `.git` directory and `runlog.provenance()` calls `git rev-parse HEAD` before creating test batches. The label tests that do not require Git metadata passed. The failure is an audit-environment limitation caused by using the provided ZIP after the live clone failed, not a finding against a normal Git checkout. No actual `data/labels/` batches are included in the ZIP, so batch-level label coverage and failure rates cannot be re-counted from the artifact.

## Phase A — Module 8: Learning, features, models and training

### Finding L1 — Residual-ranking model is trained with softplus residuals but evaluated with ReLU-clipped residuals

- **Location:** `src/ahg/learning/train.py:92-95`; `src/ahg/learning/heuristic.py:43-50`
- **Type / severity:** BUG / MAJOR
- **Problem:** For `target="residual", loss="rank"`, `group_rank_loss()` ranks `h_max + softplus(r)` where `r` is the model's raw output. The deployed `Learned` heuristic instead returns `h_max + max(0, r)`. These are not equivalent transformations in the presence of varying h-max values: softplus distinguishes negative residuals, while `max(0,r)` collapses every negative residual to zero. The ordering of two states can reverse between the score optimized by training and the score used by A*.
- **Why it matters:** The D23 primary model A is explicitly configured as a residual-target, ranking-loss GNN. Its ranking objective is therefore not the ranking function actually used in the headline evaluation. This weakens interpretation of the ranking-training result and could explain or alter its measured search performance.
- **Verification:** Read `configs/training/d23.json` (primary model A uses `target: residual`, `loss: rank`); traced `new_gnn()` (`positive=False`), `group_rank_loss()`, and inference. A throwaway two-state numeric check with h-max values `[10.0, 9.8]` and raw residuals `[-10.0, -1.0]` gives training scores `[10.000045, 10.313262]` (state 1 ranks higher), but inference scores `[10.0, 9.8]` (state 0 ranks higher). The order reverses.
- **Remediation:** Use the same residual transform in rank loss and inference. Either deploy `softplus(r)` or train against `max(0,r)` with an explicit treatment of its zero-gradient negative region; then retrain all affected ranking models and rerun evaluation.

### Finding L2 — Encoded-feature cache is not versioned by the encoder implementation

- **Location:** `src/ahg/learning/encode.py:24-33`
- **Type / severity:** REPRODUCIBILITY / MINOR
- **Problem:** Cache keys contain the label-batch content hash and feature family (`mlp`, `wl`, `gnn`, etc.), but not an encoder/schema version or code hash. A cache built by an earlier implementation is silently reused after feature-generation code changes, as long as the label batch content is unchanged.
- **Why it matters:** A rerun from a later checkout can train on stale encodings while the recorded repository commit points to the new encoder code. This is a silent reproducibility hazard, especially for a research pipeline where feature definitions may evolve.
- **Verification:** Inspected `_cached()`: it loads an existing `<batch-content-sha>/<kind>.pt` without checking the encoder version, preprocessing hash, tensor schema or source commit. `data/cache/` is ignored and not included in the supplied archive, so no stale-cache instance could be confirmed.
- **Remediation:** Add an explicit feature-schema/version token (or deterministic encoder source/config hash) to the cache key and validate the loaded tensor schema. Consider atomic writes to avoid leaving a partial `.pt` file after interruption.

### Finding L3 — WL training ignores the shared wall-clock deadline

- **Location:** `src/ahg/learning/train.py:169-192`
- **Type / severity:** BUG / MINOR
- **Problem:** `_train_wl()` accepts `deadline` but never checks it; its own comment says “no deadline check”. `scripts/train.py`'s budgeted grid/sequence runner passes a shared deadline and describes the budget as hard, with running configurations stopping at an epoch boundary. A WL fit can therefore continue past the deadline and delay or prevent subsequent configurations from starting.
- **Why it matters:** Hyperparameter-search budget accounting and run scheduling are not hard-bounded for WL. This does not directly affect the D23 multi-seed plan (which has no deadline), but it affects the training search/sequence commands and their declared budget semantics.
- **Verification:** Traced `run_budgeted()` → `train_run()` → `train_model()` → `_train_wl()`; the `deadline` parameter is passed through but unused in all WL rounds. The MLP/GNN early-stop path checks it between epochs (`_early_stop`, lines 148-150).
- **Remediation:** Check the deadline between WL/IRLS rounds and record an explicit partial/stopped status, or describe the budget as soft and reserve time for a running WL fit.

### Learning checks with no leakage found

- No input tensor is derived directly from `h*`: MLP inputs are graph size, held-fact count, h-sp, and applicable-action cost summaries; GNN inputs are held/goal fact bits plus static action graph/features; residual variants additionally receive h-max-derived fact/global features; WL colours use held/goal status, action kind and cost. The label `h*` is used as target (or to form `h* - h_max` residuals), not as an input.
- MLP standardisation and WL vocabulary are fitted on train batches only. `train_model()` rejects batches whose manifest split is not `train` or `val`; validation is used for early stopping / WL model selection. Train/val seed ranges are disjoint, though their CVE pool is intentionally shared for topology-level validation.
- Seed handling is explicit: `torch.manual_seed(cfg["seed"])`, a seeded CPU `torch.Generator` for MLP shuffling, and a seeded `random.Random` for GNN instance order. D23 sets PyTorch thread count explicitly.

## Phase A — Module 9: Evaluation harness and statistics

### Finding E1 — No paired Wilcoxon/Holm implementation exists for model-comparison inference

- **Location:** `src/ahg/evaluate.py:113-154`; `scripts/evaluate.py:51-72`; `scripts/summarize_depth_coupling.py:206-237`
- **Type / severity:** TEST-GAP / MAJOR
- **Problem:** The main evaluation code computes per-instance geometric-mean ratios with percentile bootstrap CIs, plus counts and descriptive overestimation/sibling-order statistics. It does not compute paired Wilcoxon signed-rank tests or Holm-adjusted p-values. The only inferential test implementation found in the runnable source/scripts is an exact sign test in `summarize_depth_coupling.py`; it emits unadjusted p-values across multiple groups/heuristics.
- **Why it matters:** A research claim that depends on a paired significance threshold or family-wise error control cannot be independently regenerated from the committed analysis code. Bootstrap CIs are not a substitute for a specified paired test plus multiplicity correction. If the paper reports no p-values, this is a reporting/reproducibility gap rather than a claim error.
- **Verification:** Searched all `src/ahg/` and `scripts/` Python sources for `wilcoxon`, `wilcox`, `holm`, `multipletests`, and related code. No Wilcoxon or Holm implementation was found. `summarize_depth_coupling.sign_test()` implements only the binomial sign test and the caller prints its raw p-value.
- **Remediation:** Add a deterministic analysis script that consumes frozen per-instance paired records, computes the pre-specified Wilcoxon tests, applies Holm correction over the stated comparison family, and emits all raw and adjusted p-values with effect sizes. If inference is deliberately CI-only, state that and remove any unsupported significance wording.

### Evaluation checks with no issue found

- Every baseline and learned model is run through the same `astar()` / `best_first_search()` implementation, with fixed `(f, h, insertion-order)` tie-breaking, the same duplicate detection/reopening semantics, and the same expansion budget. The wrappers and a structural spy test make this shared harness explicit (`tests/test_attack_graph.py` around the node-counting wrapper test).
- The evaluation verifies that admissible baselines return the stored optimal initial-state label when not budget-limited; executable learned plans are cost-checked with `plan_cost()`. The report separately displays solved coverage, budget hits, optimal plans and plan-cost ratios, so a plan-cost aggregate is not presented without its solved count.
- The geometric mean is correctly computed as `exp(mean(log(per-instance ratio)))`. Bootstrap resampling is paired at the instance level because it resamples each already-computed model/baseline ratio, rather than independently resampling numerator and denominator. The bootstrap seed is deterministic per model/comparator/metric.
- End-to-end timing includes heuristic feature computation and lazy graph construction; `scripts/evaluate.py` pins PyTorch intra-op threads to one, matching the single-threaded Python search baselines. No timing fairness defect was established from the source alone. The timing estimates remain less robust than expansion counts because the harness records one sequential timing per algorithm/instance without repeated counterbalanced runs.

### Statistical caveats to disclose

- Bootstrap CIs are over instances for one trained checkpoint at a time. They do not by themselves capture between-training-seed variability; a multi-seed headline needs a seed-aware aggregation procedure rather than treating checkpoint-specific intervals as a multi-seed interval.
- Test splits distribute seeds round-robin across knob cells, so cell counts are not always exactly equal (for example, 100 seeds over 84 cells gives 16 cells two observations and 68 cells one). The current bootstrap resamples instances without stratifying by cell. The effect may be modest, but the target estimand should be specified (seed-weighted versus equal-cell-weighted).

## Phase A — Module 10: Provenance, run logs and test-access log

### Finding P1 — Run provenance marks a tree clean while ignoring untracked source files

- **Location:** `src/ahg/runlog.py:62-67`
- **Type / severity:** REPRODUCIBILITY / MAJOR
- **Problem:** `provenance()` computes `git_dirty` with `git status --porcelain --untracked-files=no`. This deliberately suppresses all untracked files. An untracked Python module, config, or script can be imported or invoked by a run while the run manifest reports `git_dirty: false` and identifies only the unchanged HEAD commit. The label-batch identity (`src/ahg/labels.py:184-190`) uses that commit and the config hash, not a source-tree hash, so such a run is not uniquely attributable to the code that executed.
- **Why it matters:** Provenance can falsely certify a run as clean and reproducible even when its actual implementation includes uncommitted, untracked code. This is especially material for generated labels and trained models whose provenance is used to assert which implementation produced them.
- **Verification:** In an isolated temporary Git repository, created and committed `tracked.py`, then created untracked `new_module.py`. `git status --porcelain` reported `?? new_module.py`, while `git status --porcelain --untracked-files=no` returned empty. The provenance implementation uses the latter exact command. `scripts/fetch_nvd.py:114-119` uses a different source/script status check which does include untracked paths, confirming inconsistent dirty-tree semantics within the project.
- **Remediation:** Include untracked files in dirty detection (`git status --porcelain`, with intentional exclusions explicitly documented), and preferably stamp a deterministic source/config tree hash in addition to the commit. Ensure generated batches and model runs capture the same code identity.

### Finding P2 — Test-access guard is bypassable by changing the free-form purpose label

- **Location:** `src/ahg/splits.py:101-116`; caller `src/ahg/dataset.py:69-77`; CLI `scripts/evaluate.py:11-13,81-86`
- **Type / severity:** LEAKAGE / MINOR
- **Problem:** `record_test_access()` only blocks a second read if `purpose == "evaluation"` exactly. `purpose` is any non-empty string, and `scripts/evaluate.py --purpose` accepts any text. Repeated access to the same test split under `purpose="diagnostic"`, `"analysis"`, or another label is therefore accepted without a `permitted_by` decision entry. The log records these accesses, but the code does not enforce a closed purpose vocabulary or prevent test-driven iterative analysis under alternate labels.
- **Why it matters:** The once-only evaluation guard is an advisory convention rather than a robust protocol boundary. If an experiment workflow relies on the code to prevent repeated test-set use, a caller can bypass that check without modifying code. The log does preserve evidence of those reads; I found no evidence in this audit that the test split was actually accessed this way.
- **Verification:** Against a temporary JSONL log, called `record_test_access()` twice for `test_id` with purpose `diagnostic`; both calls succeeded. A later `evaluation` call succeeded once and a second exact `evaluation` call was refused. `dataset.open_batch()` calls this guard before reading the labels, and `scripts/evaluate.py` forwards the free-form CLI value.
- **Remediation:** Use an explicit enum of allowed purposes and define which purposes consume the once-only test budget. For final evaluation, require a registered experiment/decision identifier and fail closed on an unknown purpose. Keep an append-only access log, but do not treat the present guard as an access-control guarantee.

### Provenance checks with no issue found

- `write_run()` uses `mkdir(..., exist_ok=False)` and therefore refuses to overwrite a same-named run directory (`src/ahg/runlog.py:80-93`). Gzip output uses `mtime=0`, making the compressed raw payload deterministic for identical JSON bytes. `load_raw()` accepts old `raw.json` and new `raw.json.gz`, and rejects ambiguous directories containing both (`src/ahg/runlog.py:96-107`).
- Label-batch directories are also append-only: an existing batch ID raises `FileExistsError` (`src/ahg/labels.py:187-192`). The batch manifest records config and CVE-table hashes, per-instance task digests, label/failure content hashes, seed ranges and RNG-stream names.
- Provenance records Python, platform, hardware and installed distribution versions. A commit hash alone is not enough to compensate for P1's dirty-tree gap, but the other recorded fields are useful.

**Phase A process note:** The blind-phase breach reported during the sweep remains in force. While locating statistical-test implementations, one repository-wide `grep` emitted a small number of matching lines from `docs/experiment_log.md`, `docs/decisions.md` and one report under `results/` before the Phase A sweep was complete. No further docs/results content was inspected during Modules 10–12. I will treat those accidentally surfaced snippets as unavailable evidence until Phase B and will not claim that the Phase A pass was perfectly blind.

## Phase A — Module 11: Test suite and test quality

### Test execution

The ZIP has no `.git` metadata and the package is not installed as a distribution. I used a temporary `git` shim outside the repository, returning the archive's recorded commit and a clean status, solely to let provenance-dependent tests execute; I also supplied temporary `ahg` distribution metadata because offline installation could not fetch the `hatchling` build dependency. This does not emulate a real repository's Git status and must not be mistaken for validating provenance under a real checkout.

Tests were run in module/file-sized batches rather than one monolithic invocation. A broad run initially completed 1,377 tests with 3 skips and one environment-only failure (`test_provenance_records_hardware_and_libraries`: `ahg` distribution metadata absent under `PYTHONPATH` source import). With temporary distribution metadata, larger all-suite invocations repeatedly stalled around the learning/late-suite boundary and timed out without a pytest summary. The files were therefore isolated:

- `tests/test_core.py`: 485 passed.
- `tests/test_attack_graph.py`: 349 passed, 3 skipped.
- `tests/test_topology.py tests/test_assign.py`: 447 passed.
- `tests/test_cost.py tests/test_cve.py`: 54 passed.
- `tests/test_knobs.py -k 'not test_d15_mode_unchanged_by_d16'`: 331 passed, 8 skipped; six parameterized checks that read a committed pilot under `results/` were deferred until Phase A closed.
- `tests/test_labels.py`: 9 passed.
- `tests/test_learning.py` with `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`: 20 passed.
- `tests/test_pddl.py tests/test_runlog.py tests/test_splits.py -k 'not test_committed_pre_d18_run_still_loads'`: 14 passed; the single runlog test reading an existing `results/` artifact was deferred until Phase A closed.
- `tests/test_topology.py` separately: 437 passed.

The project declares `requires-python = ">=3.12,<3.13"` (`pyproject.toml:1-3`), but only Python 3.13.5 is installed here. `uv sync`/a real Python 3.12 run could not be performed offline. Results above are therefore Python 3.13.5 smoke/regression evidence, not a clean run under the declared interpreter.

### Test quality assessment

The suite is not generally superficial. Strong checks include: a separate brute-force optimal-cost routine for tiny generated tasks; a separate UCS oracle on generated graphs; checks over all reachable states on small tasks; label cross-checks against brute force, enumeration, admissibility and the second A* heuristic; seeded model/checkpoint comparisons; and golden structural digests for previously frozen generator outputs. I did not find a broad pattern of tests merely asserting a function equals itself.

However, important behavioural coverage is missing:

1. **NVD applicability semantics:** `tests/test_cve.py`'s `cve()` fixture builds only a simple configurations→nodes→cpeMatch tree; it has no nested AND/OR or `negate` cases. Thus the parser defect in D1 has no regression test.
2. **Real service/CVE compatibility:** the family-mapping test checks only that mapping keys equal service-family names. There is no test that generated services carry product/version identities or that assigned CVEs match an installed product/version. This leaves D3/G1 unchallenged.
3. **Training/evaluation objective parity:** learning tests cover residual variants and ranking-pair arithmetic but never assert that the score used by `group_rank_loss()` has the same state ordering as the `Learned` heuristic deployed in A*. L1 therefore escapes the suite.
4. **Cache invalidation:** no test changes encoder implementation/schema while keeping the same label-batch hash, so L2 is untested.
5. **Provenance and test protocol:** no tests add an untracked importable source file and assert the run is marked dirty; the access-log test checks only a second exact `evaluation` string, not alternate purpose labels. P1/P2 are consequently untested.
6. **Search reopening:** there is no committed regression test that forces an admissible but inconsistent heuristic to improve and reopen an already expanded state. My separate throwaway case passed, but future regressions would not be caught by the suite.
7. **Invalid experiment knobs:** the knob tests check share-pool bounds but not that `coupling` is finite and lies in [0, 1], leaving G3 untested.

The tests around the shared A* harness verify that all algorithms are routed through the same implementation; they do not independently validate every semantic detail of the common engine. That is supplemented by the core toy/brute-force tests, but a direct reopening test and explicit expansion-count contract tests would improve confidence.

**Conclusion:** The suite has significant useful coverage and strong independent checks for search/heuristic correctness, but the specific defects found in the data parser, ranking pipeline, provenance and experimental protocol are exactly the kind of cross-module behaviour not covered by existing tests. No separate defect was filed solely because of test style; the gaps above are recorded as part of the relevant findings.

## Phase A — Module 12: Small reproduction

### Measurement-script slice

- **Command/entry point:** imported `scripts/measure_landscape.py` and called `measure_instance("flat", 0, 6, pool, do_enum=True)` twice with the committed derived CVE table.
- **Result:** the instance was reachable, with 9 facts, 30 actions, `h* = 568` integer cost units and a 5-action optimal plan. Uniform-cost expanded 18 nodes; A*+h-max and A*+LM-cut each expanded 5. Full enumeration covered 30 reachable states, of which 22 were non-goal; both h-max and LM-cut had zero gap on this particular tiny instance.
- **Determinism:** all result fields except elapsed seconds were exactly identical across the two runs. This checks a single generator/measurement cell; it is not a reproduction of the complete historical sweep.

### Training-config slice

- **Command/entry point:** generated one real train batch (`train`, seed 1000) and one validation batch (`val`, seed 1600) using `write_batch()` and `configs/labels/d19.json`, reopened them through `open_batch()`, then called `train_model()` twice with a one-epoch version of D23 primary model A's configuration (`kind=gnn`, `target=residual`, `loss=rank`, 64 hidden units, 3 layers, seed 0). All temporary labels and encoder caches were written under `/tmp`, not into the repository.
- **Batch output:** 120 train states and 124 validation states. Both batch manifests identified the expected flat, n=12, D=2, rho=0 cells and `open_batch()` rebuilt their tasks with matching task digests.
- **Training output:** one epoch completed in each run; train loss 13.6186 and validation loss 20.5284 (effort-scale loss units); the weights were bitwise identical and non-timing history fields matched. A bound learned heuristic returned a finite nonnegative prediction for a training state.
- **Interpretation:** the narrow pipeline slice executes and reproduces for this seed/config on the available CPU runtime. It does not validate the headline multi-seed D23 results, and the deterministic run does not cure the train/inference ranking mismatch in L1.

**Phase A complete.** No further blind-phase restrictions apply from this point. Phase B below compares the source-level audit with the author’s documentation and committed reports. The process note above still applies: Phase A was not fully blind because of the accidental grep exposure already disclosed.
---

# Phase B — Comparison with author claims and committed reports

## 1. Additional findings exposed by claim review

### Finding D4 — NVD applicability parser does not recurse into nested configuration nodes

- **Location:** `src/ahg/cve.py:116-122`
- **Type / severity:** BUG / MAJOR
- **Problem:** `vulnerable_products()` scans only each configuration's immediate `nodes` and immediate `cpeMatch` arrays. NVD configuration nodes can contain nested `nodes`; the implementation never recursively visits them. A vulnerable product recorded only in a nested node is therefore omitted from the returned product set and may be excluded from the derived CVE table.
- **Why it matters:** This compounds D1: the extractor is not evaluating the complete NVD applicability tree. CVE inclusion counts and product/family membership can be wrong in both directions (negation ignored, nested positives omitted). Since raw NVD pages are not included, the number of affected committed rows cannot be quantified.
- **Verification:** Ran a throwaway nested `AND -> OR -> cpeMatch` fixture with `vulnerable: true` and a matching `apache:http_server` criterion. `vulnerable_products()` returned `set()`; expected product was absent. Source lines 116-122 show only one level of `cfg.nodes -> node.cpeMatch` traversal.
- **Remediation:** Recursively traverse all child nodes and correctly evaluate node operators/negation, or use a tested NVD applicability evaluator. Add fixtures for root and nested positive matches, nested AND/OR, `negate`, and mixed platform/vulnerable matches.

### Finding S1 — D15/D16 R2/R3 sign-test p-values treat repeated topology seeds as independent

- **Location:** `scripts/summarize_depth_coupling.py:212-239`; `scripts/measure_depth_coupling.py:65-77,134-142,181-205`; `src/ahg/attack_graph.py:256-260`; `src/ahg/topology.py:121-126`; `src/ahg/assign.py:21-40`
- **Type / severity:** STATISTICS / MAJOR
- **Problem:** The per-instance sign test pools every eligible `(variant, n, D, rho, m, seed)` row in the `n=20, D>=2` group and computes an exact binomial p-value as if every row were an independent replicate. They are not. `make_instance()` calls `generate(family, seed, n_hosts)` and `assign_cves(net, pool, seed)` independently of D, coupling, and share-pool settings. Thus each `(family/variant, seed)` produces the same base topology and CVE assignment across multiple knob settings; only the credential/coupling overlays change. In the `n=20, D>=2` sign-test group, the same base network is observed under up to 14 settings (D=2/3 × seven coupling/share-pool settings). The F16r headline has 886 non-tied signs, but at most 80 distinct base `(variant, seed)` networks (four variants × 20 seeds).
- **Why it matters:** The exact sign-test p-value assumes independent signs. Repeated observations of the same base network inflate the effective sample size and make the reported p-values too small. The counts (higher/equal/lower) are valid descriptive summaries of the tested grid, but `p=3.4e-131` for h_max and `p=2.0e-7` for LM-cut do not have the advertised independent-instance interpretation without accounting for clustering.
- **Verification:** Inspected the sign-test aggregation (`sampling_bias_table()` iterates all run records and increments `hi/eq/lo`; `sign_test()` treats the pooled counts as independent). Inspected generation code: topology RNG is keyed only by family and seed; CVE RNG is keyed only by family and seed; `make_instance()` then applies D and coupling via separately seeded streams. Confirmed the replication report's 782/3/101 h_max and 295/410/181 LM-cut counts in `docs/findings.md:337-347`.
- **Remediation:** Reanalyse using the base topology/seed as the clustering unit (cluster bootstrap or cluster-level permutation/sign test), or fit a repeated-measures/mixed-effects model with knob cell within topology. Report the number of independent base networks, not just the number of cell-level rows. Preserve the descriptive fractions separately from inferential p-values.

### Finding E2 — The D23 confirmatory evaluator and statistics described in the decision are absent from the submitted source tree

- **Location:** `src/ahg/evaluate.py:22-30,71-76,79-102,114-120`; `scripts/evaluate.py:1-17,75-119`; missing from `scripts/` and `src/ahg/`
- **Type / severity:** TEST-GAP / MAJOR
- **Problem:** D23 says the val-tested harness includes A*+h_add, GBFS+h_add, weighted A*+h_add at weights 1.5 and 2, and a nested bootstrap + Holm-corrected Wilcoxon + matched-pairs rank-biserial statistics script (`docs/decisions.md:2189-2214,2313-2333`). The checked-in evaluator instead imports only `astar`, loops five A* baselines (`h0`, `hmax`, `hsp`, `hadd`, `lmcut`), and evaluates learned models via the same A* call. There are no GBFS or weighted-A* calls in the evaluator. A repository-wide source/script/test search for `wilcoxon`, `holm`, `rank-biserial`, `nested bootstrap`, and `multipletests` found no implementation. The only inference procedures in the checked-in experiment scripts are instance bootstrap CIs and sign tests.
- **Why it matters:** The planned comparator family and confirmatory inference cannot be reproduced from this snapshot. A result claiming the D23 14-test Holm family, weighted/GBFS h_add comparisons, or nested seed/instance uncertainty would not be supported by the submitted code. This is a code/documentation reproducibility gap, not proof that no private/untracked script was used elsewhere.
- **Verification:** `BASELINES` in `src/ahg/evaluate.py:28` has only five heuristics; `_run()` calls only `astar()` at lines 71-76; `evaluate()` only calls `_run()` for those baselines and learned models. `scripts/evaluate.py` exposes no algorithm selector for GBFS/weighted A*. Searched all `.py` files in `src`, `scripts`, and `tests`; no Wilcoxon/Holm implementation exists.
- **Remediation:** Add the exact declared comparator/evaluation/statistics code to the repository, with unit tests for pairing, seed aggregation, nested resampling, Holm correction, and effect size. Regenerate a val analysis report from committed raw per-instance results before using it for any test claim.

### Finding E3 — The D22 learned-heuristic headline is a validation-only, one-training-seed result and is slower than h_max end-to-end

- **Location:** `results/evaluation/d22-val/2026-10-30T132843Z-fa3a3a6/report.md`; evaluation implementation `src/ahg/evaluate.py:123-153`
- **Type / severity:** METRIC / MAJOR
- **Problem:** The often-quoted residual/ranking GNN ratio of `0.595 [0.526, 0.665]` expansions versus h_max is measured on 82 validation instances, with one trained seed. D22 documentation itself marks this result as validation and selected-on-validation. The same report gives a **5.302×** end-to-end time ratio versus h_max (95% CI [4.720, 5.940]); it is faster than LM-cut in that run (0.595×), but not faster than h_max. It also finds 61/82 optimal plans (plan-cost ratio 1.039 [1.022, 1.059]) and an overestimation rate of 1.00 on both walk and A*-expanded validation states for the rank-residual model.
- **Why it matters:** “0.6× nodes” is a real descriptive statistic for this validation run, but it is not evidence of test-set generalization or a practical speedup over the strongest fast baseline. The confidence interval is conditional on a single fitted model and resamples instances only; it does not include training-seed uncertainty. Selection on val makes the reported ratio optimistic.
- **Verification:** Read the committed D22 evaluation report and its raw-derived summary. `summarise()` in `src/ahg/evaluate.py:123-153` bootstraps per-instance log ratios; it does not resample training seeds. The D22 report lists 82/82 solved, 61 optimal plans, 1.039 plan-cost ratio, 0.595 expansions vs LM-cut and h_max respectively as noted above; time-vs-h_max is 5.302.
- **Remediation:** Report this as a one-seed validation result only. Complete the registered multi-seed test evaluation and report both node expansions and end-to-end time against h_max and LM-cut. Use the committed nested cluster/seed bootstrap implementation once it exists.

## 2. Claim-by-claim assessment

| Author claim | Assessment | Evidence and qualification |
|---|---|---|
| Classical h_max and LM-cut are near-optimal on the measured attack graphs (C1). | **Supported for the tested synthetic generator and registered ranges.** | D12 and PR-gated [S]/[L] measurements show A*+h_max/LM-cut usually expands close to optimal-plan length. The D15/D16 grid and fresh-seed replication have zero eligible cells meeting the registered hard-regime criterion; in F16r the highest eligible median `R` is 1.89 and pooled median `R` is 1.00 in every `(D,n)` row (`docs/findings.md:337-347,349-365`). This is not evidence for arbitrary real attack graphs or richer delete-effect models. |
| “h_max and LM-cut are near-exact.” | **Needs qualification; not true as a pointwise heuristic-value claim.** | In F16 at n=20,D=3, h_max is below h* on 84.2% of h_max-expanded states and LM-cut on 36.9% of LM-cut-expanded states; at ρ=1,m=all,D=3 the corresponding within-heuristic expanded-state fractions are 94.4% and 65.1% (`docs/findings.md:460-510`). The supported claim is near-plan-length A* expansion effort despite substantial state-wise heuristic gaps, not numerical equality h(s)=h*(s). The findings document itself makes this distinction. |
| Random-walk samples under-represent heuristic error on A*-expanded states. | **Supported descriptively on the D15/D16 grid; inferential p-values are compromised.** | F16 n=20,D=3: LM-cut is below h* on 6.5% of walk states vs 36.9% of LM-cut-expanded states; h_max is 25.8% vs 84.2% on h_max-expanded states (`docs/findings.md:460-467`). The comparison is each heuristic's own A*-expanded set, not a shared state set. R2/R3 direction counts support the descriptive pattern, but the sign-test p-values are anti-conservative because of repeated base seeds (S1). |
| Residual+ranking GNN expands about 0.6× h_max nodes. | **Supported only as a selected, one-seed validation statistic; not as a test result.** | D22 validation report: 0.595 [0.526,0.665] vs h_max on 82 instances. D23 reproduction-val report shows a similar 0.590 ratio for the retrain. Both are validation. The rank-residual train/inference transformation mismatch (L1) remains; no test evaluation or final D23 frozen manifest is in the ZIP. |
| The learned model is faster in practice. | **Not supported against h_max; partially supported against LM-cut in the D22 val run.** | D22 val end-to-end time is 5.302× h_max and 0.595× LM-cut for the residual/ranking model. The report's node-count win does not equal a general runtime win. The D23 decision predicts the GNN loses to all h_add methods on time, but those comparators are not implemented in this snapshot. |
| H1/H2/H3 generalization to held-out topology, size, and vulnerability splits. | **No supporting test evidence in this snapshot.** | `results/test_access_log.jsonl` contains five label-generation reads and no `purpose: evaluation` entries. `results/evaluation/` contains only validation/pilot reports (five reports; no test_id/test_size/test_structure/test_vuln/test_vuln_cost reports). Test labels being precomputed is disclosed and does not itself show model leakage; the models' test performance simply remains unmeasured here. |
| D23's planned five-seed A/B primary model and three-seed ablations are complete. | **Not complete in this snapshot.** | `configs/training/d23.json` declares A/B seeds 0–4 and five ablation groups, but available D23t1 artifacts contain only the two seed-0 A/B models and their gate copies. `results/training/d23t1/frozen.json` is absent, and `scripts/d23_local.sh` log says the 23-run rest phase had only just started. Treat this as in-progress at snapshot time, not a completed result. |
| D23 includes the four h_add search comparators and nested statistical tests. | **Contradicted by the checked-in source snapshot.** | The decision says these were implemented and val-tested (`docs/decisions.md:2328-2333`), but the evaluator is A*-only and there is no Wilcoxon/Holm/effect-size script (E2). |

## 3. Model selection, preregistration and leakage assessment

- **No evidence of test-set model selection or test-result cherry-picking in the supplied snapshot.** The access log shows test label generation only; the D23 decision explicitly states that no evaluation read had occurred. It is appropriate to describe the test evaluation as pending, not to imply test performance.
- **Validation selection is real and disclosed.** D22 chooses variants using validation metrics; the selected validation score is therefore not an unbiased estimate of generalization. One seed also provides no estimate of seed-to-seed training variance.
- **D23 amendment 2 is a post-failure protocol change.** The first gate failed because model B's new validation plan-cost CI was `[1.0000, 1.0013]` while the reference CI was degenerate `[1.0000, 1.0000]`. The rule was then changed to CI overlap and the gate passed. The decision and experiment log disclose this happened before any test evaluation (`docs/decisions.md:2384-2403`; `results/training/d23t1-gate/`). This is not test leakage, but it weakens the strict preregistration claim; show both gate outcomes and call the second criterion amended/post hoc.
- **The access log is a useful audit trail but not a hard security barrier.** Phase A finding P2 remains: alternate purpose strings can bypass the exact `evaluation` repeat guard. No bypass was observed in the supplied log.
- **No direct h* feature leakage was found in the model inputs.** h* is the target/label; the learned GNN receives graph/state features, and the residual construction uses h_max. That is a valid use of an admissible baseline, not leakage. The train/inference score-transform inconsistency L1 is a separate issue.

## 4. Documentation and provenance consistency

- `docs/status_report.md` is explicitly dated 2026-10-19 and describes the early core-only repository; it is stale but timestamped, so it should not be presented as current project status.
- `docs/hpc.md` still says `scripts/train.py` is “not runnable yet”, while the training script exists and D23 has run. It also contains unfilled QoS/template placeholders. Update or mark this operational note historical.
- `docs/decisions.md` calls the D23 h_add comparators and statistics script implemented and tested, but they are absent from this archive (E2). This is the most material document/source mismatch.
- The archive has no `.git` directory, raw NVD snapshot, label batches, D23 `frozen.json`, or test-evaluation reports. This audit cannot verify that the archive exactly corresponds to the recorded commit or reconstruct D22/D23 training from raw data and full label artifacts. The live remote clone was unavailable in this environment; this report is scoped to the supplied ZIP.
- All 48 committed `results/*/report.md` files were inventoried. The small evaluation/feasibility/training reports were inspected, and the large landscape reports were checked for configuration, summary tables, oracle coverage, reachability/generation failures, and terminal instance listings. The main result claims cross-check against `docs/findings.md` and `docs/experiment_log.md`.

## 5. Reviewer objections and the experiment that answers each

1. **Are the CVEs actually applicable to the software in each generated service?** Build product- and version-specific services, recursively evaluate NVD CPE applicability (including nested AND/OR and negation), and rerun derivation/assignment. Publish exact snapshot artifacts and counts.
2. **Does the result survive beyond this delete-free, synthetic attack-graph construction?** Add a second generator or imported benchmark with realistic multi-prerequisite rules, versioned software inventory, exploit preconditions, and (where appropriate) delete effects; report results separately rather than pooling with the current generator.
3. **Are R2/R3 sampling-bias inferences statistically valid?** Reanalyse at the topology-seed cluster level, account for repeated measures across the 14 knob cells, and report cluster-aware effect sizes/CIs and adjusted p-values. Keep per-cell descriptive counts.
4. **Does the learned model beat strong classical and greedy baselines under the same algorithm/budget?** Implement A*+h_add, GBFS+h_add, and weighted A*+h_add (w=1.5,2) in the same evaluation harness; verify identical reopening, tie-breaking, and budget semantics; report expansions, solution cost and wall time.
5. **Is the 0.6× expansion result robust across training randomness and held-out data?** Complete all declared A/B and ablation seeds, freeze model hashes, evaluate each of the five test splits once, and use a nested bootstrap over instances and seeds plus Holm-corrected paired tests.
6. **Does ranking training optimize the heuristic actually searched with?** Make training and inference use the exact same score transform or prove ranking equivalence; test pairwise-order parity over real validation states and rerun training/evaluation.
7. **Is the node reduction useful once inference overhead is counted?** Measure repeated, counterbalanced end-to-end timings on a quiet fixed machine for GNN, h_max, LM-cut, h_add and the planned GBFS/weighted-A* baselines; report median/CI and inference cost per evaluated state.
8. **How sensitive are results to the arbitrary CVSS-to-cost map and sampling assumptions?** Rerun with at least uniform costs and multiple monotone CVSS cost transforms; compare family-balanced vs uniform-CVE and product-specific assignment. State which conclusions depend on the cost model.
9. **Are the reported claims reproducible from an immutable source/data package?** Supply the raw NVD snapshot/manifest or permanent artifact URL, label-batch manifests and data, frozen model manifest/checkpoints, full run provenance, correct working-tree checks including untracked files, and a clean Python 3.12/uv reproduction command.

## 6. Overall conclusion

The core delete-free planning/search implementation and the classical heuristic calculations are strong relative to the tests run: no correctness defect was found in the best-first-search engine, reopening, h_max/h_sp/LM-cut admissibility, or the independent oracle checks on the tested tiny/generated instances. The main threats to the paper are higher in the experimental/data layers: incomplete NVD applicability parsing; family-only CVE assignment; the train/inference ranking mismatch; pseudo-replicated sign-test inference; and a D23 protocol whose promised comparator/statistics code and test evaluation are not present in this snapshot.

No CRITICAL issue was established. The single-seed, validation-only 0.595× h_max expansion result is not demonstrated to be numerically fabricated, but it is not a test/generalization result, has an implementation mismatch in the learned score, and is not an end-to-end speedup over h_max. The classical near-plan-length expansion finding is better supported within the synthetic delete-free generator, but it should not be described as pointwise near-exact heuristic values or generalized to realistic attack graphs without additional validation.

