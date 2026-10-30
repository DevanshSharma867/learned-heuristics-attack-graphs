# CLAUDE.md — Learned Heuristics for A* over Attack Graphs

## 0. What this project is (read first)

A research project on learned heuristics for A* search over vulnerability-derived attack graphs. **The product is a publishable paper** (workshop first, then conference/journal if results hold) with a reproducible code artifact to match. Every decision in this repo is made to that standard: if a choice is defensible in peer review, it's right; if it only makes sense as a shortcut to a deadline, it's wrong.

Treat the repo as a research artifact, not a coursework submission — code, experiments, and writing held to the bar a reviewer would apply, not a grader. (It does also satisfy a course requirement, but that follows automatically from doing the paper properly and never drives a decision.)

**Target (set 2026-10-29):** a workshop paper or an arXiv preprint, written for MS applications as well as the course. Every decision must meet that standard. The course requirements are a **subset**, met by doing the paper properly:
- Research track;
- a GNN heuristic, an MLP ablation and the generalisation splits promised in the proposal;
- AI-usage disclosure (`docs/ai_usage_log.md`) and a steady commit history;
- the final report, demo and viva.

If the paper and the course ever pull apart, the paper standard wins. Any course requirement it would drop is named in `docs/decisions.md`.

**Paper framing (D17, adopted 2026-10-29).** Working title: *"Learned heuristics for attack-graph planning: what they can and cannot buy"*.
- **Contribution 2 (learning: informedness and generalisation under shift) is the headline.** It tests H1–H3 below, against the thresholds fixed in D17 §2.
- **Contribution 1 (characterisation) is the motivating study.** It covers near-exact classical A\* on these graphs, h\* = h+ (delete-free), and the walk-vs-A\* sampling bias.
- **The timing result against Fast Downward is a pre-registered negative.** It is reported prominently, not buried.

Author/maintainer: Devansh Sharma (solo). Repo: https://github.com/DevanshSharma867/learned-heuristics-attack-graphs

**Research question.** Compared with A* using classical heuristics, can a neural cost-to-go estimator trained on some attack graphs reduce search effort on attack graphs from *unseen* network topologies, and how much solution quality does it cost?

**Hypotheses (do not silently change these; changes go in `docs/decisions.md`):**
- **H1 (efficiency):** on unseen in-distribution test graphs, A* + learned heuristic expands fewer nodes than A* + hand-crafted baselines.
- **H2 (trade-off):** the learned heuristic reduces effort at a measurable suboptimality cost relative to admissible baselines (which return optimal plans).
- **H3 (generalization):** the advantage shrinks under shifts in (a) graph size, (b) topology family, (c) vulnerability-feature distribution — each measured separately.

Scope tiers: **Core** = GNN heuristic + classical A* baselines + generalization study. **Secondary** = MLP ablation. **Optional** = weighted A*, asymmetric loss, MulVAL validation. If time runs short, the Core alone must be a complete, honest result.

---

## 1. Research integrity rules — NON-NEGOTIABLE

These protect the paper. Violating any of them invalidates results. If a requested change would break one, stop and say so.

1. **No test leakage.** Splits are made at the *topology level* from disjoint seeds *before* any state sampling. Test graphs are never used for training, early stopping, hyperparameter tuning, normalization statistics, or architecture choice. Validation split only for those.
2. **Training-graph results are diagnostic only** and never support a claim in the report/paper.
3. **Never fabricate or "fill in" results.** Every number in a table, plot, or text must be produced by a script in this repo from a logged run. If a run hasn't happened, write `TODO: not yet run`, never a plausible number.
4. **Never fabricate citations.** Any reference added must be real and verifiable (DOI / arXiv / venue URL). If unsure a paper exists or says what we claim, mark it `[VERIFY]` and tell me.
5. **The cost model is frozen** before main experiments: `c(a) = 1 + 9·(1 − x_a)`, `x_a ∈ [0,1]` = normalized CVSS exploitability sub-score. It is an attack-effort proxy, *not* a calibrated probability — never describe it otherwise. "Optimal" always means "optimal under this cost model".
6. **Labels must be verified.** Exact cost-to-go labels are cross-checked against an independent uniform-cost search implementation (and exhaustive enumeration on the smallest graphs). A label-check test must pass before any training run is trusted.
7. **Fair comparison.** All methods run on identical instances, same hardware, same expansion-counting code, same tie-breaking, same duplicate detection. GNN inference time (incl. batching/graph construction) is counted in end-to-end wall-clock. Heuristic computation time for h_max / h_add / h_sp is also counted.
8. **Inadmissible heuristics get no optimality or bounded-suboptimality claims** (including in weighted A*). Report measured suboptimality only.
9. **Seeds everywhere.** Every run records: git commit hash, config, all seeds, library versions, hardware. Report mean ± std across ≥ 5 training seeds, plus per-instance paired comparisons.
10. **Unreachable goals** are logged separately as generation/solver failures, never silently dropped or counted as "solved".
11. **Don't overwrite raw results.** Raw run outputs are append-only; aggregates are regenerated from raw outputs by scripts.

---

## 2. Problem formulation (the source of truth)

- **Attack graph** = fact–action graph with **conjunctive** action preconditions (AND over preconditions; OR over alternative actions achieving a fact).
- **State** = set of privileges/facts held by the attacker. **Action** = exploit whose preconditions ⊆ state; adds its effects. **Goal** = target privilege ∈ state.
- Privileges are **monotonic** (never removed) → **delete-free planning problem**. Delete-relaxation heuristics apply. Optimal delete-free planning is still NP-hard in general — search over states, not over graph edges.
- Search: A* with `f = g + h`. Uniform-cost = `h ≡ 0`. Document whether nodes are reopened when h is inconsistent/inadmissible, and apply the same policy to every heuristic.
- State representation: hashable (frozenset or bitset). Duplicate detection on states.

### Heuristics compared
| ID | Name | Property |
|---|---|---|
| h0 | uniform-cost | admissible (trivially) |
| h_max | delete-relaxation max | admissible |
| h_add | delete-relaxation additive | inadmissible, informative reference |
| h_sp | cost-weighted shortest-path relaxation | document admissibility explicitly and test it empirically |
| h_θ (GNN) | learned cost-to-go | inadmissible; overestimation measured |
| h_θ (MLP) | learned, graph-level features (ablation) | inadmissible |

"Normal A*" in the writing = A* with h_max / h_add / h_sp.

### Learned heuristic
- **GNN:** message passing over the fact–action graph. Privilege nodes: `held_in_state`, `is_goal`. Exploit nodes: normalized cost + CVSS attributes. Pooling → scalar `h_θ(s)`.
- **MLP ablation:** graph-level hand-built features (#privileges, #exploits, #held, h_sp(s), aggregate CVSS cost stats). Tests whether relational structure adds value.
- **Labels:** exact optimal cost-to-go h*(s) from an exact solver on small graphs.
- **Losses:** MSE baseline; asymmetric loss penalizing overestimation (Optional tier). Report overestimation rate `|{s : h_θ(s) > h*(s)}| / |evaluated states|`, mean and max violation.

---

## 3. Data pipeline

synthetic topology → service/CVE assignment → attack-graph generator (MulVAL or native) → fact–action graph → state sampler → (labels via exact solver) → train / evaluate.

- **Topology families:** flat, tiered/segmented, hub-and-spoke (extendable). Hosts, services, reachability/firewall rules, trust relationships.
- **CVEs:** sampled from NVD records matching each service family (product/CPE). CVSS attributes → features. Cache NVD data locally with a pinned snapshot date; never hit the network during experiments.
- **Generator:** MulVAL if operational; otherwise the native generator implementing the same fact–action representation (MulVAL then becomes optional external validation). Record which one produced each dataset.

### Splits / generalization tests
| Test | What changes | Held within training range |
|---|---|---|
| In-distribution | fresh unseen graphs | everything |
| Size shift | #hosts (larger) | topology family, vuln distribution |
| Structure shift | held-out topology family | size range, vuln distribution |
| Vulnerability shift | held-out CVE groups / shifted CVSS distribution | size range, topology family |

Each shift changes **one** factor only.

---

## 4. Metrics and statistics

- Nodes expanded (primary), wall-clock time (end-to-end), plan cost / optimal cost, fraction solved within a fixed expansion budget, overestimation stats.
- Report **ratios relative to normal A*** per instance; summarize with geometric mean (ratios) and median; mean ± std across seeds.
- Paired significance: Wilcoxon signed-rank on per-instance values; bootstrap 95% CIs for summary ratios. Report effect sizes, not just p-values.
- One summary table per test split; plots of nodes expanded and suboptimality vs graph size; coverage-vs-budget curves.
- Optimal cost for large test graphs: if the exact solver can't finish, say so and report suboptimality only where h* is known (or vs best-known cost, clearly labelled).

---

## 5. Paper-readiness checklist (what reviewers will ask)

Treat these as open items; tick them in `docs/decisions.md` when addressed.
- [ ] Stronger classical baselines than h_max: **LM-cut** (state-of-the-art admissible for delete-free/optimal planning) and ideally **h_FF**. Optionally export instances to PDDL and run Fast Downward as an external sanity check.
- [ ] Greedy best-first search (GBFS) with h_θ as well as A* — learned heuristics are often reported with both.
- [ ] Ranking-based loss as a comparison to regression (learned heuristics literature argues ranking can beat cost-to-go regression) — Optional.
- [ ] Cost of training + label generation reported honestly (amortization argument).
- [ ] Ablation: GNN depth / hidden size; with vs without CVSS features; MLP vs GNN.
- [ ] Failure analysis: where does h_θ overestimate badly; which shift hurts most and why.
- [ ] Related work checked for prior learned-heuristic work on attack graphs / automated pentesting (incl. RL-based pentesting, e.g. NASim-style environments) — position the novelty precisely.
- [ ] Reproducibility: one command regenerates every table and figure from raw results.
- [ ] Threats to validity: synthetic topologies, uncalibrated cost model, label-size limit, full observability assumed.

Candidate venues (verify current CFPs/deadlines before targeting): ICAPS workshops (e.g. HSDIP, PRL), AISec (CCS workshop), relevant NeurIPS/ICML/ICLR workshops on learning + reasoning/planning, then journals/conferences if results are strong.

---

## 6. Engineering conventions

Follow existing repo conventions where they exist; otherwise default to these.

- **Python 3.11+**, PyTorch + PyTorch Geometric for the GNN. Pin versions (`requirements.txt` or `pyproject.toml` + lock).
- **Layout** (adapt to what exists, don't churn working code just to match):
  ```
  src/          # package: generators/, cve/, attackgraph/, search/, heuristics/, learning/, eval/
  configs/      # YAML configs for datasets, training, experiments
  scripts/      # entry points: generate, label, train, evaluate, make_tables, make_figures
  tests/        # pytest
  data/         # raw/ (gitignored, large), snapshots documented
  results/      # raw/ (append-only run outputs), aggregates/, figures/
  docs/         # decisions.md, experiment_log.md, ai_usage_log.md, paper/
  ```
- **Configs, not hardcoded constants.** Every experiment runs from a config file; the run directory stores a copy of it.
- **Tests that must exist and pass** before trusting results: label correctness vs independent UCS; admissible heuristics never exceed h* on small graphs; A* with admissible h returns optimal cost; identical node counting across heuristics; split disjointness (no topology seed shared across splits).
- Run `pytest` before committing changes to search, heuristics, labels, or splits.
- Type hints and short docstrings on public functions. No giant notebooks as the source of truth — notebooks only for exploration.

---

## 7. Workflow rules for Claude Code

- **Small, frequent, descriptive commits.** The course flags projects with last-minute history; the commit log is graded evidence of steady work. Never squash history or rewrite pushed commits.
- Before large changes: state the plan briefly, then implement. Don't refactor unrelated code.
- After any experiment: append an entry to `docs/experiment_log.md` (date, commit, config, what was run, headline numbers, anything surprising).
- Any decision that changes formulation, cost model, splits, metrics, or hypotheses → `docs/decisions.md` with date and reason.
- **AI-usage disclosure is required by the course.** At the end of each session, append to `docs/ai_usage_log.md`: date, what Claude Code did, which files, how it was verified (tests run, manual checks). Be specific, not generic.
- Devansh must be able to explain every line in the viva. When writing non-trivial logic (search, heuristics, GNN, loss, stats), add a brief comment on *why*, and summarize the key idea in the session's final message.
- If something is ambiguous or a result looks too good, say so and investigate leakage/bugs before celebrating.
- Long runs: print estimated time first; prefer a small pilot before the full run.

---

## 8. Current state

> Keep this section up to date. Replace placeholders after each milestone.

- Proposal submitted (Oct 2026). Timeline: ~10 weeks from the week of 5 Oct 2026; final dates TBA.
- Generator in use: native (`src/ahg/attack_graph.py`); MulVAL not used.
- Implemented: generator, classical heuristics (h0, h_max, h_add, h_sp, h_FF, LM-cut), A*/GBFS, D19 label
  pipeline with cross-checks, models (MLP, WL-linear, GNN) and losses (`src/ahg/learning/`), the D21
  harness (`src/ahg/evaluate.py`), `scripts/train.py`, `scripts/evaluate.py`.
- Experiments run (as of 2026-10-30): C1 characterisation and its replication; labels for every split at
  72e8821 (backup SHA-256 in the experiment log); D21 epoch timing, val hyperparameter search (11/15
  configs in the 3 h budget), seed-0 pilot of every model × {MSE, asym}, val-pilot evaluation, cost projection.
- Known issues: on val, no learned model yet expands fewer nodes than h_max or LM-cut (one seed, pilot).
  WL vocabulary is ~1.9M colours (near graph-specific). 6-layer GNN configs never searched.
- Next milestone: multi-seed training (D17 seed plan, ~32 M4-CPU-hours projected) on the HPC; decide on
  the H1 situation before freezing models. No test split has been evaluated.

## 9. Key references (verified in proposal)
Hart, Nilsson, Raphael 1968 (A*); Sheyner et al. 2002 (attack graphs); Ou et al. 2005 (MulVAL); Hoffmann 2015 (simulated pentesting); Shmaryahu et al. 2018 (pentesting as contingent planning); Agostinelli et al. 2019 (DeepCubeA); Shen, Trevizan, Thiébaux 2020 (STRIPS-HGN); NVD; FIRST CVSS. Add new ones only with a verifiable link.