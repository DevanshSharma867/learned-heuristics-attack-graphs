# Findings so far

Research record as of 2026-10-22. Every number below comes from a committed run output or a
decision entry in `docs/decisions.md` (D-numbers), and the source is cited
next to it. Anything without a committed source is marked **not yet
measured** or **unverified**.

Run folders cited below:

- **[S]** `results/landscape/landscape_small_n/2026-10-22T114620Z-4f00c1b/`
- **[L]** `results/landscape/landscape_large_n/2026-10-22T122711Z-4f00c1b/`

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

1. **Depth-coupling sweep.** Running in another session at the time of
   writing. Its result is pending and not cited here. Its output is to be
   brought into `results/landscape/depth_coupling_sweep/` through
   `src/ahg/runlog.py`.
2. **Exposure vs target-control decomposition** of the size effect:
   **not yet measured**.
3. **Exactness over A\*-expanded states vs sampled states**: **not yet
   measured**.
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
