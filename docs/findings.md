# Findings so far

Research record as of 2026-10-22. Every number below comes from a committed run output or a
decision entry in `docs/decisions.md` (D-numbers), and the source is cited
next to it. Anything without a committed source is marked **not yet
measured** or **unverified**.

Run folders cited below:

- **[S]** `results/landscape/landscape_small_n/2026-10-22T114620Z-4f00c1b/`
- **[L]** `results/landscape/landscape_large_n/2026-10-22T122711Z-4f00c1b/`
- **[F15]** `results/landscape/depth_coupling_sweep/full/2026-10-28T131617Z-ab208e3/` (§7)
- **[F16]** `results/landscape/depth_coupling_sweep/full_d16/2026-10-28T142309Z-ab208e3/` (§7)

Each has `report.md`, `raw.json` and `provenance.json` (commit 4f00c1b,
`git_dirty: false`). Both were produced by `scripts/measure_landscape.py`.

**Their provenance has no hardware field or library versions.** Both runs
predate those fields, which were added to `runlog.provenance()` on
2026-10-28. Their `provenance.json` records only `platform`
(macOS-15.6-arm64), `machine` (arm64), `processor` and the Python version.
They are left unedited (rule 11). Later runs record CPU model, core
counts, RAM and every installed library version.
Costs are in D9 integer units: 38 units = 1 effort unit, and actions cost
38–380.

## 1. Research question and original hypotheses

From `CLAUDE.md` §0, verbatim:

> **Research question.** Compared with A* using classical heuristics, can a neural cost-to-go estimator trained on some attack graphs reduce search effort on attack graphs from *unseen* network topologies, and how much solution quality does it cost?
>
> - **H1 (efficiency):** on unseen in-distribution test graphs, A* + learned heuristic expands fewer nodes than A* + hand-crafted baselines.
> - **H2 (trade-off):** the learned heuristic reduces effort at a measurable suboptimality cost relative to admissible baselines (which return optimal plans).
> - **H3 (generalization):** the advantage shrinks under shifts in (a) graph size, (b) topology family, (c) vulnerability-feature distribution — each measured separately.

**Status: under revision.** The finding in §3 bears directly on H1. No
revision has been decided, and no D-entry changes the hypotheses yet.
`CLAUDE.md` requires that any change be recorded in `docs/decisions.md`.

## 2. What was built

**The task model and search (D1–D8).** An attack is a delete-free planning
task: privileges are never lost, so a state is the set of facts held,
stored as an integer bitmask (D1). UCS, A\*, weighted A\* and GBFS all run
through one `best_first_search`, so node counting, tie-breaking and
duplicate detection are identical for every method by construction (D2).
Settings fixed for every heuristic:

- ties broken on (f, h, FIFO counter) (D3);
- closed states reopened when a strictly cheaper g is found (D4);
- the goal tested on expansion (D5);
- the goal node not counted as expanded (D6).

The admissible set is {h0, h_sp, h_max, LM-cut}; h_add and h_FF are treated
as inadmissible (D7). h_sp treats AND-preconditions as OR, and is
admissible for that reason (D8).

**The attack-graph generator and schema (D10, D12).** A native generator
(MulVAL produced no dataset) builds networks from three topology families:
flat, tiered and hub_and_spoke. Their default parameters are the training
distribution (D10). D12 turns a network into a task:

- **Facts:** one `execCode(h)` fact per host, with the attacker starting at
  `attackerLocated(internet)`.
- **Exploits:** one per reach edge, with a single precondition.
- **Logins:** one per trust edge × login-service reach edge, conjunctive
  when the credentials and the network access come from different hosts.
  A login costs 38 units (1 effort unit).
- **Goal:** `execCode(target)`, where the target is drawn among the hosts
  farthest from the internet.
- **MulVAL correspondence:** MulVAL's cost-free intermediate facts are
  folded into the actions that consume them. The rule-name correspondence
  is still marked `[VERIFY]` in D12.

**The CVE and cost pipeline, grounded in NVD (D9, D11, D13).**

- **CVEs (D11).** CVEs come from a pinned NVD snapshot, using NVD Primary
  CVSS v3.x scores only. They are mapped to eight service families (dns,
  ftp, http, mail, rdp, smb, sql, ssh), published 2016–2023, and must
  belong to exactly one family. This gives 1,473 CVEs (D11(c)).
- **Cost (D9).** The frozen cost model `c(a) = 1 + 9·(1 − x_a)` is encoded
  exactly in integers: `x_a = (k − 1)/38` with `k = round(10·E)`, stored
  cost `C = 389 − 9k ∈ [38, 380]`. It is an attack-effort proxy, not a
  probability.
- **Privileges Required (D13).** The derived table gained a
  `privileges_required` column (N/L/H) from the same NVD Primary v3 vector:
  N 693, L 449, H 331.

**The PR-gated variant (a measurement variant, not an adopted schema).**

- **Status.** It is committed code: `make_instance(..., pr_gated=True)`,
  commit 186e05a, documented in the `src/ahg/attack_graph.py` module
  docstring and tested in `tests/test_attack_graph.py`. The default schema
  is unchanged. **There is no D-entry adopting it.** D13 states that "the
  schema itself is not decided here", and D14 records D12 as under
  revision.
- **What it adds.** Two capability facts:
  - `capability(user)`, harvested from any controlled internal host for
    38 units;
  - `capability(admin)`, harvested from a trust source, which also grants
    user.

  PR:L and PR:H exploits gain the matching capability as a conjunctive
  precondition.
- **Why it was built.** To test whether real CVSS privilege requirements
  create enough AND-structure to make the tasks harder than D12's.

## 3. Central finding: classical admissible heuristics are near-optimal

On these CVSS-grounded attack graphs, h_max and LM-cut are almost exactly
h\*. A\* with either heuristic expands about as many nodes as the optimal
plan has steps, which leaves little search effort for a learned heuristic
to save.

### 3.1 Baseline, without PR gating (D12)

D12 ("Consequence, measured 2026-10-21 at the D10 defaults, 20 seeds per
cell") counted the states where the heuristics fall below h\*, over every
non-goal reachable state:

| n | flat | tiered | hub_and_spoke |
|---|---|---|---|
| 5 | hmax: 2 of 205 states; lmcut: 0 | 0 of 190 | 0 of 167 |
| 6 | 0 of 378 | hmax: 1 of 268 | 0 of 263 |
| 8 | 0 of 1,602 | hmax: 16 of 871; lmcut: 8 | 0 of 926 |

D12's own conclusion: the tasks "are close to shortest-path problems", and
"on such tasks h_max and LM-cut are nearly perfect, so H1 would be close to
vacuous". The stated reason is that an exploit has a single precondition,
so the only genuine conjunctions are logins whose network access comes from
a third host. In hub_and_spoke, none can exist by construction.

### 3.2 With PR gating, small n = 6, 8, 12 [S]

Source: `[S]/report.md`, seeds 0–19 per cell. Every reachable instance was
fully enumerated (the "enumerated" column there reads k/k in every cell).

| family | n | reachable / 20 | median plan len | median h\* | median expanded, h0 / h_max / LM-cut | LM-cut h<h\*, sampled / all states | h_max h<h\*, sampled / all states |
|---|---|---|---|---|---|---|---|
| flat | 6 | 18 | 3 | 267 | 10 / 3 / 3 | 0.000 / 0.000 | 0.035 / 0.037 |
| tiered | 6 | 12 | 4 | 325.5 | 9.5 / 4 / 4 | 0.000 / 0.000 | 0.071 / 0.078 |
| hub_and_spoke | 6 | 13 | 4 | 267 | 6 / 4 / 4 | 0.000 / 0.000 | 0.032 / 0.037 |
| flat | 8 | 19 | 3 | 213 | 23 / 3 / 3 | 0.000 / 0.000 | 0.011 / 0.009 |
| tiered | 8 | 15 | 4 | 442 | 14 / 5 / 4 | 0.019 / 0.017 | 0.070 / 0.072 |
| hub_and_spoke | 8 | 15 | 4 | 404 | 20 / 4 / 4 | 0.000 / 0.000 | 0.001 / 0.002 |
| flat | 12 | 18 | 3 | 182.5 | 20.5 / 3 / 3 | 0.000 / 0.000 | 0.032 / 0.020 |
| tiered | 12 | 19 | 5 | 478 | 57 / 6 / 5 | 0.000 / 0.000 | 0.042 / 0.032 |
| hub_and_spoke | 12 | 17 | 4 | 251 | 55 / 4 / 4 | 0.000 / 0.000 | 0.005 / 0.001 |

Notes:

- **Tiered n = 12, LM-cut.** The fraction rounds to 0.000, but the sampled
  max gap is 27 units, so a few states are below h\*. Every other cell with
  0.000 also has max gap 0.
- **Largest sampled gaps.** h_max up to 191 units (tiered n = 8). LM-cut up
  to 85 units (tiered n = 8).
- **The uninformed baseline (h0) never hit the 200,000-expansion budget at
  small n.**

### 3.3 With PR gating, large n = 20, 30, 40 [L]

Source: `[L]/report.md`. Seeds were taken from 0 upward until there were
15 reachable per cell, with 300 sampled states per instance; every
instance reached the cap.

| family | n | median plan len | median h\* | median expanded h0 (at budget) / h_max / LM-cut | LM-cut h<h\* (max gap) | h_max h<h\* (max gap) |
|---|---|---|---|---|---|---|
| flat | 20 | 3 | 152 | 566 (0/15) / 3 / 3 | 0.006 (38) | 0.050 (38) |
| tiered | 20 | 4 | 240 | 492 (0/15) / 4 / 4 | 0.009 (38) | 0.070 (76) |
| hub_and_spoke | 20 | 3 | 251 | 37 (0/15) / 3 / 3 | 0.000 (0) | 0.001 (38) |
| flat | 30 | 2 | 114 | 65 (1/15) / 2 / 2 | 0.010 (38) | 0.024 (38) |
| tiered | 30 | 4 | 190 | 686 (0/15) / 5 / 4 | 0.006 (38) | 0.064 (76) |
| hub_and_spoke | 30 | 4 | 251 | 226 (2/15) / 4 / 4 | 0.000 (0) | 0.026 (38) |
| flat | 40 | 2 | 76 | 47 (2/15) / 2 / 2 | 0.008 (76) | 0.020 (76) |
| tiered | 40 | 4 | 152 | 421 (1/15) / 4 / 4 | 0.019 (38) | 0.033 (38) |
| hub_and_spoke | 40 | 4 | 251 | 236 (2/15) / 4 / 4 | 0.000 (0) | 0.011 (38) |

Notes:

- **Generation failures.** Two, both listed in `[L]/report.md`:
  hub_and_spoke n = 20 seed 1 and n = 30 seed 12.
- **h\* known for every sampled state:** the `h* unknown` column is 0 in
  every cell.

### 3.4 Summary across [S] and [L]

- **LM-cut below h\*:** on 0.000–0.019 of sampled states in every cell.
  Max gap ≤ 85 units at small n and ≤ 76 units (2 effort units) at large n.
- **h_max below h\*:** on 0.001–0.071 of sampled states.
- **Median plan length:** 3–5 steps at small n, 2–4 at large n.
- **Median nodes expanded by A\* from the initial state:** 2–6 with h_max
  or LM-cut, against 6–686 for uniform-cost search.
- **The comparison is the same at every size measured, n = 6 to 40.**

### 3.5 How h\* was checked

The runs abort before writing anything if any check fails
(`scripts/measure_landscape.py`, `HardFailure`). Both runs wrote their
output, so every check below passed. The reports say so explicitly for
checks 1 and 2: "No mismatch and no admissible heuristic above h\*
occurred".

1. **A\*+LM-cut = A\*+h_max** on the initial state and on every sampled
   state, in both runs. These are two different admissible heuristics, but
   the same search code (D2).
2. **Backward induction over the fully enumerated state space** ([S] only,
   every instance). h\*(s) is the minimum over successors of c(a) + h\*(s′),
   processed from the largest states to the smallest. This shares no code
   with A\*, and it must equal A\* on every sampled state and on the
   initial state.
3. **Uniform-cost search (h ≡ 0) = h\* on the initial state**, wherever UCS
   finished within the budget (both runs). This goes through the shared
   `best_first_search`, so it is **not** independent of the A\* code.
4. **The independent oracle** (`src/ahg/oracle.py`, frozenset-based UCS
   sharing no code with `search.py`). This is checked in the test suite,
   not in the runs:
   - `tests/test_attack_graph.py` runs it against search on every reachable
     state of PR-gated instances: the first 8 reachable seeds per family at
     n = 6, and the first 20 at tiered n = 8;
   - and against brute force on PR-gated n = 3 graphs.

   The suite passed (975 passed, 3 skipped; `docs/ai_usage_log.md`,
   2026-10-22). The oracle has **not** been run on the [S]/[L] instances
   themselves. A by-hand oracle check at n = 12 this session left no
   committed output, so it is **unverified** as evidence.

In every check, no admissible heuristic exceeded h\*. In the runs this was
checked on every sampled state ([S], [L]) and every enumerated state ([S]).
In the tests it was checked on every reachable state of the test cases
(`test_admissibility_and_dominance_on_every_state`).

### 3.6 PR gating did not change the conclusion

- **D12** (ungated) found h_max and LM-cut nearly perfect.
- **[S] and [L]** (PR-gated) find the same at every size from 6 to 40.
- **Committed evidence:** one ungated measurement (D12) and two PR-gated
  runs, both at commit 4f00c1b.
- **Earlier PR-gated passes.** They were run in scratch sessions, and their
  outputs and scripts were lost (`docs/ai_usage_log.md`, 2026-10-22). Any
  claim about them is **unverified**, and the claim of "three passes"
  cannot be supported from committed files.

## 4. Why: current working explanation (not yet tested)

This is a **working explanation**. It is consistent with the numbers above,
but no diagnostic has isolated it.

- **Short optimal plans.** Median optimal plans are 2–5 steps ([S], [L]).
  With so few steps there is little room for a heuristic's errors to add up
  to extra search.
- **Some plans shrink as networks grow, but not all.** Median h\* falls
  with n for flat (152 → 114 → 76 at n = 20/30/40) and tiered
  (240 → 190 → 152) [L]. hub_and_spoke stays at 251. At small n the trend
  is not monotone (tiered 325.5 → 442 → 478) [S]. A plausible cause is
  denser internet exposure in larger networks; that is **not yet
  measured**.
- **Shallow, non-interacting prerequisites.** In the PR-gated variant, the
  only added conjunction is a capability fact.
  - `capability(user)` is one global fact, obtainable from any controlled
    internal host for 38 units (`src/ahg/attack_graph.py`). Once any
    foothold exists, it is a single cheap step shared by every PR:L
    exploit.
  - The hypothesis is that LM-cut prices this landmark exactly, and h_max
    nearly so. That would leave gaps of about one action cost (38 or 76
    units), which matches the max gaps in [L].
  - This hypothesis is **unverified**.
- **No real conjunctions elsewhere.** The D12 argument, that exploits have
  one precondition and that hub_and_spoke allows no third-host logins,
  still holds for the non-capability part of the task.

Diagnostics that would test this, both **NOT YET RUN**:

- **Size decomposition.** Split the size effect into internet exposure
  (more exposed hosts) and target control (the goal's hop depth and number
  of entry points).
- **Exactness over expanded states.** Measure whether h_max and LM-cut are
  exact on the states A\* actually expands, rather than on random-walk
  samples. At n = 12 the walks are already known to over-sample states
  where h_max is below h\* (flat 0.032 sampled vs 0.020 exact [S]).

## 5. Open questions: remaining experiments

1. **Depth-coupling sweep.** Done (D15, D16): no hard regime found in
   either run. See §7.
2. **Exposure vs target-control decomposition** of the size effect:
   **not yet measured**.
3. **Exactness over A\*-expanded states vs sampled states**: measured on
   the D15 sweep grid only (§7.3). It is **not yet measured** on the [S]/[L]
   PR-gated instances.
4. **Sensitivity to the CVSS cost model**, e.g. whether the near-exactness
   survives other monotone maps from E to cost, or uniform costs. This is
   **not yet measured**. Rule 5 freezes the cost model for the main
   experiments, so this would be a sensitivity analysis only.
5. **Wall-clock time including inference.** A learned heuristic must beat
   A\*+LM-cut in end-to-end time, and A\*+LM-cut already expands about
   plan-length nodes. No learned heuristic exists yet, and no timing
   comparison has been made: **not yet measured**.

## 6. Implications for the paper (direction under consideration)

**Not decided; no D-entry.**

- **What the evidence suggests.** On attack graphs generated as specified
  in D10–D13, a "learned heuristic beats classical A\*" result (H1) has
  little room to appear. The classical admissible baselines already expand
  about plan-length nodes.
- **An alternative under consideration.** A characterisation, or
  phase-diagram, paper: under which structural conditions do attack-graph
  search problems become hard enough for a learned heuristic to help? The
  candidate conditions are depth, coupling of prerequisites, exposure, and
  cost structure. Items 1–4 of §5 would be the axes of that diagram.
- **What would change it.** The hypotheses (§1) would be revised in
  `docs/decisions.md` before any such change of framing. Whether the
  depth-coupling sweep finds a hard regime is the main open input.

## 7. Depth–coupling sweep (D15, D16): no hard regime found

Added 2026-10-29. Sources:

- **[F15]**: the D15 depth knob as registered.
- **[F16]**: the D16 variant, with internet-exposed hosts at level 0. This
  is the primary run (D16).

Both runs:

- were made at commit ab208e3 with `git_dirty: false`, on an Apple M4 with
  6 workers;
- took 36 min ([F15]) and 66 min ([F16]);
- have 6,720 instances each: 28 knob configs × 4 family variants × n ∈
  {8, 12, 20} × seeds 0–19.

Every table below is printed by `scripts/summarize_depth_coupling.py [F15] [F16]`
from `raw.json`. The criterion uses the same `summarise` function as the
runs' own `report.md`.

### 7.1 Criterion (D15 §6): not met in either run

| run | cells | eligible | meet part 1 (median R ≥ 5, CI low ≥ 3) | highest eligible median R | reachable / unreachable / gen. fail | censored |
|---|---|---|---|---|---|---|
| [F15] | 336 | 190 | **0** | 1.00 | 4,641 / 2,079 / 0 | 0 |
| [F16] | 336 | 192 | **0** | 1.94 (flat n = 20, D = 3, ρ = 1, m = n) | 5,160 / 1,539 / 21 | 0 |

- **Ineligible cells.**
  - 112 in each run fail the size rule: every n = 8 cell.
  - 34 ([F15]) and 32 ([F16]) have fewer than 10 of 20 instances
    reachable.
  - None fails the plan-length rule.
- **Generation failures.** All 21 in [F16] are flat n = 8 instances whose
  target is internet-exposed: 7 at each D ≥ 1 (D16 rule).
- **No fresh-seed confirmation.** No cell meets part 1, so none was run;
  seeds 100–119 are unused.
- **Consequence under D15 §6.** Within this generator and these knob
  ranges, classical admissible A\* is near-exact, and H1 as stated has no
  room to show an effect on these graphs.
  - The knob ranges are not widened post hoc.
  - Framing and any revision of the hypotheses are left to a separate
    D-entry (D15 §6). This section decides neither.
- **No budget hits.** No instance hit the 200k budget, for any of h0, h_max
  or LM-cut, in either run. So censoring played no role.

### 7.2 Search effort: R and R_hmax

R = A\*+LM-cut expansions from the initial state / optimal plan length.
Each entry reads: median R / 90th-percentile R / max R · median R_hmax ·
reachable/instances · censored. Entries pool every other grid factor. The
n = 12 rows of the (ρ, m) and family tables are in the script output.

**By D** (n = 12 and 20):

| D | n | D15 | D15+D16 |
|---|---|---|---|
| 0 | 12 | 1.00 / 1.00 / 1.62 · 1.00 · 475/560 · 0 | 1.00 / 1.00 / 1.62 · 1.00 · 475/560 · 0 |
| 0 | 20 | 1.00 / 1.00 / 2.57 · 1.00 · 508/560 · 0 | 1.00 / 1.00 / 2.57 · 1.00 · 508/560 · 0 |
| 1 | 12 | 1.00 / 1.00 / 1.38 · 1.00 · 447/560 · 0 | 1.00 / 1.00 / 2.22 · 1.17 · 475/560 · 0 |
| 1 | 20 | 1.00 / 1.00 / 3.44 · 1.14 · 486/560 · 0 | 1.00 / 1.00 / 3.40 · 1.50 · 508/560 · 0 |
| 2 | 12 | 1.00 / 1.00 / 1.40 · 1.11 · 354/560 · 0 | 1.00 / 1.00 / 2.40 · 1.29 · 420/560 · 0 |
| 2 | 20 | 1.00 / 1.17 / 2.67 · 1.31 · 458/560 · 0 | 1.00 / 1.50 / 6.29 · 1.67 · 451/560 · 0 |
| 3 | 12 | 1.00 / 1.00 / 1.50 · 1.00 · 257/560 · 0 | 1.00 / 1.25 / 4.36 · 1.33 · 357/560 · 0 |
| 3 | 20 | 1.00 / 1.25 / 2.77 · 1.29 · 389/560 · 0 | 1.00 / 1.78 / 47.31 · 1.75 · 391/560 · 0 |

**By (ρ, m)**, n = 20 (m = all means m = n):

| (ρ, m) | n | D15 | D15+D16 |
|---|---|---|---|
| (0.0, all) | 20 | 1.00 / 1.00 / 2.67 · 1.00 · 291/320 · 0 | 1.00 / 1.00 / 4.43 · 1.12 · 296/320 · 0 |
| (0.25, 1) | 20 | 1.00 / 1.00 / 2.40 · 1.00 · 287/320 · 0 | 1.00 / 1.14 / 6.29 · 1.24 · 290/320 · 0 |
| (0.25, all) | 20 | 1.00 / 1.00 / 2.12 · 1.00 · 291/320 · 0 | 1.00 / 1.12 / 3.89 · 1.25 · 294/320 · 0 |
| (0.5, 1) | 20 | 1.00 / 1.00 / 1.88 · 1.00 · 286/320 · 0 | 1.00 / 1.12 / 3.09 · 1.33 · 285/320 · 0 |
| (0.5, all) | 20 | 1.00 / 1.17 / 3.44 · 1.14 · 281/320 · 0 | 1.00 / 1.38 / 4.29 · 1.42 · 286/320 · 0 |
| (1.0, 1) | 20 | 1.00 / 1.00 / 3.00 · 1.10 · 187/320 · 0 | 1.00 / 1.25 / 3.71 · 1.30 · 183/320 · 0 |
| (1.0, all) | 20 | 1.00 / 1.33 / 2.77 · 1.71 · 218/320 · 0 | 1.00 / 2.45 / 47.31 · 3.00 · 224/320 · 0 |

**By family variant**, n = 20:

| variant | n | D15 | D15+D16 |
|---|---|---|---|
| flat | 20 | 1.00 / 1.25 / 2.71 · 1.25 · 538/560 · 0 | 1.00 / 1.62 / 47.31 · 1.61 · 550/560 · 0 |
| hub_and_spoke | 20 | 1.00 / 1.00 / 2.00 · 1.00 · 466/560 · 0 | 1.00 / 1.00 / 1.33 · 1.00 · 397/560 · 0 |
| tiered3 | 20 | 1.00 / 1.14 / 3.00 · 1.20 · 500/560 · 0 | 1.00 / 1.57 / 4.60 · 1.50 · 535/560 · 0 |
| tiered5 | 20 | 1.00 / 1.00 / 3.44 · 1.09 · 337/560 · 0 | 1.00 / 1.00 / 3.18 · 1.27 · 376/560 · 0 |

**Reading.**

- **Medians.** Pooled median R is 1.00 in every row of both runs. The
  knobs move only the tail.
- **The tail.** The [F16] 90th percentile at n = 20 rises with D, 1.00 →
  1.78, and is largest at (ρ = 1, m = n), 2.45. Few instances get far:
  - R ≥ 2: 21 of 4,641 reachable instances in [F15] and 79 of 5,160 in
    [F16];
  - R ≥ 5: 0 in [F15] and 3 in [F16].
- **The one outlier** is [F16] flat n = 20, D = 3, ρ = 1, m = n, seed 5:
  - LM-cut expands 615 states against plan length 13 (R = 47.3);
  - h_max expands 3,992 (R_hmax = 307);
  - h0 expands 25,011.
- **R_hmax responds more than R.** Its median at n = 20 rises with D: 1.00
  → 1.29 in [F15] and 1.00 → 1.75 in [F16]. At (ρ = 1, m = n) it reaches
  3.00 in [F16].
- **Family.** hub_and_spoke stays at median R_hmax 1.00 in both runs.
  flat and tiered3 respond most.
- **D = 0 sanity check.** The D = 0 rows are identical in the two runs.
  D16 changes nothing at D = 0, so this is a consistency check.

### 7.3 Exactness: sampled, A\*-expanded and enumerated states

Each entry is the fraction of states with h < h\*, then (max gap in D9
units; number of states).

- **Sampled:** the [S]-style random-walk states.
- **Expanded:** the distinct states expanded by A\* with that same
  heuristic. Above 300 states (no instance here) they would be subsampled
  to 300.
- **All:** every reachable non-goal state of the instances that were
  enumerated (≤ 50k states). At n = 20 this covers only the smaller
  instances, so the populations differ by column.

At n = 20 (n = 8 and 12 are in the script output):

[F15]:

| D | n | LM-cut sampled | LM-cut expanded | LM-cut all | h_max sampled | h_max expanded | h_max all |
|---|---|---|---|---|---|---|---|
| 0 | 20 | 0.007 (115; 150847) | 0.069 (115; 2417) | 0.001 (115; 1064339) | 0.067 (364; 150847) | 0.553 (366; 4173) | 0.054 (364; 1064339) |
| 1 | 20 | 0.009 (115; 144038) | 0.078 (115; 2931) | 0.001 (115; 1163344) | 0.096 (402; 144038) | 0.639 (404; 5110) | 0.051 (399; 1163344) |
| 2 | 20 | 0.022 (182; 135872) | 0.116 (182; 3423) | 0.001 (182; 914185) | 0.154 (379; 135872) | 0.713 (437; 6033) | 0.048 (437; 914185) |
| 3 | 20 | 0.020 (229; 115132) | 0.156 (158; 3597) | 0.001 (152; 948156) | 0.165 (413; 115132) | 0.735 (458; 6645) | 0.043 (458; 948156) |

[F16]:

| D | n | LM-cut sampled | LM-cut expanded | LM-cut all | h_max sampled | h_max expanded | h_max all |
|---|---|---|---|---|---|---|---|
| 0 | 20 | 0.007 (115; 150847) | 0.069 (115; 2417) | 0.001 (115; 1064339) | 0.067 (364; 150847) | 0.553 (366; 4173) | 0.054 (364; 1064339) |
| 1 | 20 | 0.014 (153; 150969) | 0.126 (153; 3057) | 0.002 (153; 1030989) | 0.157 (402; 150969) | 0.768 (404; 7160) | 0.064 (402; 1030989) |
| 2 | 20 | 0.031 (191; 134373) | 0.239 (191; 3701) | 0.003 (191; 872873) | 0.237 (415; 134373) | 0.824 (453; 9092) | 0.063 (453; 872873) |
| 3 | 20 | 0.065 (200; 115923) | 0.369 (200; 4675) | 0.004 (175; 1203223) | 0.258 (478; 115923) | 0.842 (480; 11056) | 0.068 (440; 1203223) |

LM-cut on LM-cut-expanded states, against h_max on h_max-expanded states,
by (ρ, m) and D (pooled over variants and n ≥ 12; number of states):

[F15]:

| (ρ, m) | D=0 LM-cut | D=0 h_max | D=1 LM-cut | D=1 h_max | D=2 LM-cut | D=2 h_max | D=3 LM-cut | D=3 h_max |
|---|---|---|---|---|---|---|---|---|
| (0.0, all) | 0.006 (662) | 0.104 (703) | 0.014 (793) | 0.330 (924) | 0.053 (900) | 0.517 (1146) | 0.080 (900) | 0.602 (1328) |
| (0.25, 1) | 0.030 (703) | 0.406 (1022) | 0.042 (841) | 0.535 (1289) | 0.054 (896) | 0.605 (1319) | 0.069 (913) | 0.625 (1364) |
| (0.25, all) | 0.018 (650) | 0.346 (830) | 0.026 (781) | 0.476 (1003) | 0.068 (883) | 0.621 (1277) | 0.102 (925) | 0.648 (1391) |
| (0.5, 1) | 0.010 (697) | 0.378 (961) | 0.020 (840) | 0.506 (1209) | 0.045 (889) | 0.592 (1244) | 0.075 (889) | 0.579 (1165) |
| (0.5, all) | 0.066 (702) | 0.616 (1353) | 0.080 (858) | 0.678 (1629) | 0.094 (894) | 0.748 (1807) | 0.135 (882) | 0.774 (1838) |
| (1.0, 1) | 0.028 (501) | 0.225 (552) | 0.050 (619) | 0.411 (756) | 0.102 (657) | 0.609 (898) | 0.105 (608) | 0.676 (941) |
| (1.0, all) | 0.149 (652) | 0.725 (1240) | 0.130 (748) | 0.727 (1418) | 0.168 (785) | 0.806 (1560) | 0.212 (706) | 0.800 (1434) |

[F16]:

| (ρ, m) | D=0 LM-cut | D=0 h_max | D=1 LM-cut | D=1 h_max | D=2 LM-cut | D=2 h_max | D=3 LM-cut | D=3 h_max |
|---|---|---|---|---|---|---|---|---|
| (0.0, all) | 0.006 (662) | 0.104 (703) | 0.019 (828) | 0.504 (1136) | 0.073 (977) | 0.622 (1586) | 0.126 (1134) | 0.633 (1735) |
| (0.25, 1) | 0.030 (703) | 0.406 (1022) | 0.057 (875) | 0.663 (1643) | 0.108 (1022) | 0.722 (1943) | 0.151 (1145) | 0.683 (1911) |
| (0.25, all) | 0.018 (650) | 0.346 (830) | 0.040 (809) | 0.644 (1368) | 0.112 (978) | 0.743 (2022) | 0.214 (1137) | 0.747 (2075) |
| (0.5, 1) | 0.010 (697) | 0.378 (961) | 0.030 (858) | 0.639 (1502) | 0.084 (928) | 0.698 (1670) | 0.171 (1109) | 0.759 (2176) |
| (0.5, all) | 0.066 (702) | 0.616 (1353) | 0.093 (871) | 0.764 (2009) | 0.195 (1058) | 0.815 (2642) | 0.201 (1125) | 0.847 (3122) |
| (1.0, 1) | 0.028 (501) | 0.225 (552) | 0.068 (622) | 0.606 (942) | 0.146 (628) | 0.738 (1184) | 0.186 (704) | 0.702 (1166) |
| (1.0, all) | 0.149 (652) | 0.725 (1240) | 0.256 (836) | 0.875 (2368) | 0.387 (1024) | 0.902 (2935) | 0.651 (1637) | 0.944 (4615) |

**Reading.**

- **Random walks under-represent where the heuristics fail.**
  - Gaps concentrate on the states A\* actually expands. At D = 3, n = 20
    in [F16], LM-cut is below h\* on 6.5% of sampled states, 36.9% of
    expanded states and 0.4% of all enumerated states.
  - This answers §5 item 3 for this grid: walk-sampled exactness is far
    too optimistic about expanded states.
  - It matters for label sampling (D14). Training states drawn by walks
    would rarely be the states where a learned heuristic could help.
- **Exactness does not equal effort.**
  - LM-cut is below h\* on up to 65.1% of the states it expands ([F16], ρ =
    1, m = n, D = 3).
  - Yet median R stays 1.00. Most gaps do not create extra expansions.
  - Why not is **not yet measured**. A gap only costs expansions if some
    off-plan state then has f below h\*(init).

### 7.4 Predictions in D15 §1

1. **"h_max should degrade, with the gap growing with D." Held**, in
   exactness and modestly in effort.
   - h_max-expanded states below h\* at n = 20, D = 0 → 3: 0.553 → 0.735
     [F15] and 0.553 → 0.842 [F16].
   - Median R_hmax at n = 20: 1.00 → 1.29 [F15] and 1.00 → 1.75 [F16].
2. **"LM-cut should degrade only where the credential branch and the
   network branch share actions." Not tested.**
   - The runs do not record branch sharing, so the "only where" part
     cannot be checked.
   - What was observed: LM-cut also degrades with D on expanded states, at
     n = 20 0.069 → 0.156 [F15] and 0.069 → 0.369 [F16]. Its median R does
     not move.
3. **"Small m (shared landmarks) is easy for LM-cut; m = n is harder."
   Held for ρ ≥ 0.5, reversed at ρ = 0.25 for low D.**
   - *Where it held.* At ρ = 0.5 and ρ = 1, m = n gives a higher LM-cut
     gap fraction than m = 1 at every D in both runs (§7.3 tables).
     - The largest difference is ρ = 1, D = 3 in [F16]: 0.651 against
       0.186.
     - The R tail agrees. The [F16] n = 20 90th-percentile R is 2.45 for
       (1, n) against 1.25 for (1, 1).
   - *Where it reversed.* At ρ = 0.25, m = 1 is the worse setting at D = 0
     in both runs (0.030 vs 0.018) and at D = 1 (0.042 vs 0.026 [F15];
     0.057 vs 0.040 [F16]).

### 7.5 Limitation: credential levels are drawn independently of network position

- **How levels are drawn.** In both variants, every host not forced to a
  level draws one uniformly from {0, …, D}, whatever its place in the
  topology (D15 §1(a), D16).
- **Why that cuts off goals.** A bottleneck host can draw a high level and
  cut the credential chain. The bottleneck is the hub in hub_and_spoke and
  the next tier in tiered. The D16 pilot's inspection of unreachable
  instances found this cause (experiment log, D16 pilot row). The full
  runs' unreachable instances are **not** broken down by cause.
- **Effect on reachability.** It falls with D. Reachable instances at
  n ≥ 12, for D = 0..3, out of 1,120:
  - [F15]: 983 / 933 / 812 / 646;
  - [F16]: 983 / 983 / 871 / 748.

  The steepest drops at n = 20, out of 140:
  - tiered5 in [F15]: 109 / 98 / 78 / 52;
  - hub_and_spoke in [F16]: 124 / 124 / 95 / 54.
- **What this does to the result.**
  1. *The reachable instances at high D are a selected subset:* those whose
     random levels happen to fit the topology. Whether that selection
     favours easy instances is **not yet measured**.
  2. *Real AD-style tiering correlates tier with network position.* This
     generator does not. The negative result covers levels drawn
     independently of position only.
- **Not in scope here.** A position-correlated variant would need its own
  pre-registered D-entry (D15 §6). None is proposed here.

### 7.6 Search time: LM-cut vs h_max

These are wall-clock times in one of 6 parallel workers, so they are
diagnostic only (D15 §4). Each is the median per instance at n = 20 of the
A\* search time from the initial state, heuristic computation included.

| run | D | median s LM-cut | median s h_max | median s h0 | ms/expansion LM-cut | ms/expansion h_max | median exp. LM-cut / h_max |
|---|---|---|---|---|---|---|---|
| D15 | 0 | 0.0222 | 0.0021 | 0.0033 | 4.258 | 0.383 | 4 / 4 |
| D15 | 1 | 0.0301 | 0.0029 | 0.0036 | 4.714 | 0.380 | 5 / 6 |
| D15 | 2 | 0.0358 | 0.0039 | 0.0039 | 4.464 | 0.361 | 7 / 9 |
| D15 | 3 | 0.0501 | 0.0053 | 0.0066 | 5.525 | 0.425 | 8 / 11 |
| D15+D16 | 0 | 0.0243 | 0.0023 | 0.0033 | 4.444 | 0.400 | 4 / 4 |
| D15+D16 | 1 | 0.0376 | 0.0041 | 0.0056 | 5.648 | 0.433 | 5 / 8 |
| D15+D16 | 2 | 0.0588 | 0.0066 | 0.0100 | 7.367 | 0.489 | 7 / 11 |
| D15+D16 | 3 | 0.1044 | 0.0113 | 0.0185 | 9.880 | 0.609 | 9 / 15 |

- **LM-cut costs 11–16× more per expansion than h_max** (median
  ms/expansion, n = 20). In the deepest cells (D = 3, n = 20) its median
  search time is about 9–10× h_max's: 0.050 vs 0.0053 s [F15] and 0.104 vs
  0.0113 s [F16].
- **h_max's extra expansions do not make up the difference.** The medians
  are 9 against 15 expansions in [F16] at D = 3.
- **On the outlier, uninformed search was fastest.**
  - LM-cut took 17.8 s and h_max 2.2 s.
  - Uniform-cost search took 1.1 s despite 25,011 expansions [F16].

### 7.7 The §4 working explanation: partly supported

§4 explains near-exactness by short optimal plans plus shallow,
non-interacting prerequisites.

- **Not supported as a cause of near-plan-length search.**
  - The sweep doubled the median optimal plan length: at n ≥ 12 it goes
    from 4 at D = 0 to 8 at D = 3, in both runs.
  - It added credential chains: median chain length 3 on the optimal plan
    at D = 3.
  - It coupled up to every internal exploit.
  - Pooled median R still stayed at 1.00 (§7.2). So short plans and
    shallow prerequisites are not necessary for A\*+LM-cut to expand about
    plan-length nodes in these ranges.
- **Supported as a description of what makes the heuristics inexact.**
  - Depth and coupling with distinct holders (m = n) do raise the h < h\*
    fraction on expanded states (§7.3).
  - They also lengthen the R tail (§7.2), in the directions §4 and D15 §1
    predict.
- **The link is weak.** Inexactness rarely becomes extra expansions, so
  something §4 does not name keeps search near plan length. What that is,
  is **not yet measured**.

The plan-length and chain-length medians, reachability counts, R ≥ 2 and
R ≥ 5 counts, budget hits and outlier details cited in §7 are printed in the
script's last section, "Instance-level facts cited in findings.md".
