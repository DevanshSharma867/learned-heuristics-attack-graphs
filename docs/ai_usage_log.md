# AI-usage disclosure log

Course requirement: record which AI tools were used, for what, on which files,
and how the output was verified. One entry per session, appended at the end of
the session.

---

## 2026-10-19 — Claude Code (Claude Opus 5.5)

**Session 1: read-only repository audit.**

- **What it did:**
  - Read every source, test and script file, plus `CLAUDE.md`, the proposal and the course guidelines.
  - Ran the test suite and `scripts/toy_demo.py`.
  - Ran two throwaway probe scripts, kept outside the repo in a temporary scratchpad and not committed:
    - a check that UCS cost-to-go matches brute-force enumeration on every reachable state of the toy task and 60 random tasks (1726/1726 agree);
    - an exact-solver scaling probe on random delete-free tasks (10–80 facts) with UCS, A*(h_max) and A*(LM-cut), 30 s cap per run.
  - Wrote the audit report.
- **Files created:** `docs/status_report.md`. No source, test or config file was changed.
- **How verified:**
  - `pytest -q` gave 125 passed.
  - Demo output matches the hard-coded toy expectations in `tests/test_core.py`.
  - Every claim in the report cites a file:line or a command that was run. Claims that were not checked are marked "not verified" or `[VERIFY]`.

**Session 1 (continued): repository hygiene, no source logic changed.**

- **What it did:**
  - Extended `.gitignore` with `.DS_Store` and `results/` (keeping `results/raw/.gitkeep`).
  - Created `docs/decisions.md`, with entries D1–D8 for the conventions already in the code, each citing file:line.
  - Created `docs/experiment_log.md` (empty table) and this file.
  - Made the repository's first commits as a series split by component (setup, task model, search, heuristics, example, tests, script, docs) and pushed to `origin`.
- **Files touched:** `.gitignore`, `results/raw/.gitkeep`, `docs/decisions.md`, `docs/experiment_log.md`, `docs/ai_usage_log.md`.
- **How verified:**
  - `pytest -q` was run before committing (125 passed).
  - The `.gitignore` patterns were checked with `git check-ignore`.
  - Every file:line reference in `docs/decisions.md` was checked against `grep -n` output on the committed code.

**Note on history.** File modification times show the code in `src/`, `tests/` and `scripts/` was written on
2026-10-17. It was first committed on 2026-10-19, so commit timestamps reflect
commit time, not authoring time.

## 2026-10-21 — Claude Code (Claude Opus 5.5)

**Session 2: handout removal, cost encoding decision (D9), topology generators (D10).**

- **Housekeeping (2026-10-19, logged late).**
  - Removed the course handout from the working tree. It remains in git
    history at commit `28683ef`, because rewriting pushed history is forbidden
    (CLAUDE.md §7).
  - Renamed the proposal to `docs/proposal.md`.
- **D9: integer cost encoding** (`docs/decisions.md`).
  - Compared three encodings and recorded the one chosen: `C = 389 − 9k`
    with `k = round(10·E)`, a 38× scaling of `c ∈ [1, 10]`.
  - The `[VERIFY]` on the formula being identical in CVSS v3.0 and v3.1 was
    resolved on the author's instruction.
  - The NVD rounding `[VERIFY]` is still open.
- **Topology generators.** Claude Code wrote:
  - `src/ahg/network.py`: a typed, JSON-serialisable network description
    with validation and label-free structure statistics;
  - `src/ahg/topology.py`: seeded flat, tiered and hub-and-spoke generators;
  - `tests/test_topology.py`;
  - `scripts/gen_networks.py`: prints and saves one example network per
    family. Its output goes to a temporary directory and is not committed.
- **Bug found and fixed.** The first version seeded on `seed` alone, so the
  same seed gave identical service assignments in every family. The
  generators now seed on `"family:seed"`; the reason is in D10.
- **D10** (`docs/decisions.md`) records the family rules and the default
  probabilities. These defaults define the training distribution.
- **Also committed:** the author's own reframing of `CLAUDE.md` §0. That text
  was written by the author, not Claude Code.
- **Files touched:** `src/ahg/network.py`, `src/ahg/topology.py`,
  `scripts/gen_networks.py`, `tests/test_topology.py`, `docs/decisions.md`,
  `docs/ai_usage_log.md`.
- **How verified.**
  - `.venv/bin/python -m pytest -q` gave **562 passed**: the 125 earlier
    tests plus 437 new ones.
  - The new tests check:
    - same seed gives byte-identical JSON, in-process and across two
      processes with different `PYTHONHASHSEED`;
    - JSON round-trip;
    - the recorded metadata regenerates the identical network;
    - every host is reachable from the internet;
    - each family's rules hold;
    - same seed gives different service draws across families;
    - a classifier with no labels recovers the family for 50/50 seeds at
      n = 30 and n = 60;
    - bad parameters and malformed JSON are rejected.
  - Example networks were inspected by hand from the script output.
  - Every file:line citation in D10 was checked against numbered source
    output.
- **Known limitation.** At n ≈ 10, flat and tiered networks are not reliably
  distinguishable by structure. This is recorded in D10.

## 2026-10-21 — Claude Code (Claude Opus 5.5)

**Session 3: CVE data source, measurement, D11, and the build pipeline.**

- **Data-source probe.**
  - Made one NVD API request to test reachability. No API key is available,
    so every later request was paced at one per 6.5 s with at most one
    delayed retry.
- **Measurement pass**, made before any feature code.
  - Fetched full records per candidate product into a scratch directory
    outside the repo. This was needed because "has an NVD Primary v3 score"
    is not an API filter.
  - Measured per-family and per-year counts.
  - Resolved D9's min-rounding `[VERIFY]` from four real CVEs with vector
    `AV:P/AC:H/PR:H/UI:R`: NVD reports 0.1 when scope is unchanged. The 0.2
    seen with scope changed comes from the spec's scope-dependent PR weight,
    not from rounding.
  - D11 was then drafted from these counts and approved by the author, with
    the author's own decisions on rdp, the `published` column and
    product-held-out feasibility folded in.
  - Errors found and corrected during the pass:
    - two total counts were wrong in the first D11 draft;
    - a zsh word-splitting bug briefly made two windows look identical;
    - an analysis merge bug could overwrite an included row.
- **Build pipeline.** Claude Code wrote:
  - `src/ahg/cve.py`: the D11 product mapping and the inclusion and
    exclusion rules as pure functions.
  - `scripts/fetch_nvd.py`: a paced, resumable fetch that writes the
    manifest with per-page SHA-256s and the git commit.
  - `scripts/derive_cves.py`: refuses to run if a page fails its checksum;
    writes `data/derived/cves.csv` and `build_log.json`, with every outcome
    listed, zeros included.
  - `src/ahg/cost.py`: D9's `C = 389 − 9k`, with `k = round(10E)` and an
    explicit grid check.
  - `src/ahg/assign.py`: seeded per-family CVE-to-service assignment. It
    seeds on `"cves:family:seed"`, so it does not replay the topology
    generator's own stream.
  - `NOTICE`: NVD and MITRE attribution, quoted from the archived CVE Terms
    of Use, with a `[VERIFY]` against the live pages before going public.
- **Pinned snapshot.** The 2026-10-21 snapshot has 37 page files and 4,652
  records; 6 requests needed their single retry.
  - The manifest's git-dirty flag is true only because of untracked new
    files. The code that ran matched commit `bcf91c8`. This is recorded as a
    provenance note in the build log; the snapshot was not re-fetched.
- **Files touched:**
  - code: `src/ahg/cve.py`, `src/ahg/cost.py`, `src/ahg/assign.py`;
  - scripts: `scripts/fetch_nvd.py`, `scripts/derive_cves.py`;
  - tests: `tests/test_cve.py`, `tests/test_cost.py`,
    `tests/test_assign.py`;
  - data: `data/derived/cves.csv`, `data/derived/build_log.json`;
  - docs and config: `NOTICE`, `.gitignore`, `docs/decisions.md` (the D9
    resolution and D11), `docs/ai_usage_log.md`.
- **How verified.**
  - `.venv/bin/python -m pytest -q` gave **624 passed**.
  - The tests include:
    - the cost endpoints, and exact rational equality with
      `c = 1 + 9(1 − x)` for every k from 1 to 39;
    - the `round`-vs-`int` pitfall (`4.35 − 1.15`);
    - a hand-checked real CVE: CVE-2016-10012, E = 1.8, k = 18, C = 227;
    - every derived score maps to an integer C in [38, 380];
    - the D11 rules on synthetic records;
    - assignment determinism, pool-order independence and cross-family
      decorrelation.
  - The derive step was run twice with byte-identical outputs. It also
    checks every page's SHA-256 against the manifest.
  - The derived counts (1,473 CVEs) match the independent measurement pass
    exactly.
  - The platform-only zeros were confirmed by recounting from the raw pages.

## 2026-10-21 — Claude Code (Claude Opus 5.5)

**Session: attack-graph generator (D12), PR column (D13), label design (D14).**

- **D12 attack-graph generator.** This part of the session was not yet
  logged. Claude Code wrote:
  - `src/ahg/attack_graph.py`: network plus CVEs → delete-free `Task`.
  - `src/ahg/oracle.py`: an independent UCS on frozenset states that
    shares no code with `search.py`.
  - `tests/test_attack_graph.py`.
  - `scripts/gen_attack_graphs.py`.
  - `hop_distances` extracted in `src/ahg/network.py`.
- **The D12 measurement** found generated tasks are near shortest-path:
  hmax and LM-cut equal h\* on almost every state, and hub_and_spoke has no
  genuine AND structure. This is recorded in D12 as an open issue, not
  worked around.
- **D13: `privileges_required` column.**
  - `src/ahg/cve.py` now reads the CVSS PR metric from the same NVD Primary
    v3 vector as the exploitability score and cross-checks it against
    `cvssData.privilegesRequired`. The column was appended to
    `data/derived/cves.csv`.
  - The table was regenerated from the existing 2026-10-21 snapshot. There
    was no re-fetch.
  - The test fixtures in `tests/test_cve.py`, `tests/test_cost.py`,
    `tests/test_assign.py` and `tests/test_attack_graph.py` were updated.
  - D13 was added to `docs/decisions.md` as a new entry, so D11(e) is not
    edited.
- **D14: label-generation design**, documented in `docs/decisions.md`. It
  covers the label definition with a mandatory oracle cross-check, per-split
  state sampling, the exact-solver size ceiling, provenance in
  append-only `data/labels/<batch-id>/`, and train-only normalisation.
  - **No implementation and no sampling were done.** No labels or datasets
    exist.
- **Not done.** Three attempts at a PR-gated generator variant were cut off
  mid-response, and none reached the repo. No PR-gated schema exists, and
  the D12 open issue stands.
- **Files touched:**
  - code: `src/ahg/attack_graph.py`, `src/ahg/oracle.py`,
    `src/ahg/network.py`, `src/ahg/cve.py`;
  - script: `scripts/gen_attack_graphs.py`;
  - tests: `tests/test_attack_graph.py`, `tests/test_cve.py`,
    `tests/test_cost.py`, `tests/test_assign.py`;
  - data: `data/derived/cves.csv`;
  - docs: `docs/decisions.md` (D12, D13, D14), `docs/ai_usage_log.md`.
- **How verified.**
  - `.venv/bin/python -m pytest -q` gave **805 passed** after D13. D14 is
    docs only.
  - **The D12 tests** run on generated graphs (3 families, 44 instances) and
    check:
    - h0 ≤ hsp ≤ hmax ≤ lmcut ≤ h\* and h\* ≤ hff ≤ hadd on every reachable
      state;
    - A\* with each admissible heuristic returns the optimal cost;
    - the oracle agrees with `uniform_cost` on every state, and with brute
      force on 30 small graphs;
    - a hand-checked conjunctive login: h\* = 456 with the trust edge, 760
      without it;
    - every search method goes through the shared `best_first_search`.
  - **The D13 tests and checks:**
    - all 1,473 rows have PR ∈ {N, L, H};
    - a vector/field mismatch is rejected;
    - the first six CSV columns and `build_log.json` stayed byte-identical
      after regeneration;
    - a second derive run was byte-identical.

## 2026-10-22 — Claude Code (Claude Opus 5.5)

- **Lost reports.** The two earlier landscape reports (`pr_landscape`,
  `pr_landscape_large`) lived in a session scratchpad that had been cleared,
  and their measurement scripts were gone too. Nothing was reconstructed
  from memory; both measurements were re-run fresh (below).
- **Run output in the repo.** Added `src/ahg/runlog.py`: `write_run()` puts
  each measurement run in `results/landscape/<name>/<UTC timestamp>-<commit>/`
  as `raw.json`, `report.md` and `provenance.json` (git commit, dirty flag,
  argv, seeds, config, date, Python, platform, hardware). An existing run
  directory is never overwritten (rule 11). `.gitignore` now tracks
  `results/landscape/`. TODO in `provenance()`: library versions must be
  added before any PyTorch run.
- **`scripts/measure_landscape.py`.** One script, two runs
  (`landscape_small_n`, `landscape_large_n`) on the PR-gated variant. Per
  family × size cell: reachable vs UnreachableGoal seeds, median plan length
  and h\*, median nodes expanded from init by h0 / h_max / LM-cut (budget
  hits flagged as lower bounds), and the fraction and gap of h_max and LM-cut
  below h\* over up to 300 random-walk states per instance. At small n it
  also enumerates every reachable state and reports sampled vs exact side
  by side. `report.md` is rendered from `raw.json` alone.
- **Runs.** Both at commit 4f00c1b with a clean tree; numbers are in
  `docs/experiment_log.md`. Headline: LM-cut below h\* on 0–2% of states and
  A\* expands about plan-length nodes at every size.
- **Did not touch** the depth-coupling sweep (`dc_sweep.py`) running in
  another session; its output will be brought in separately.
- **Files touched:** `src/ahg/runlog.py`, `scripts/measure_landscape.py`,
  `.gitignore`, `results/landscape/**`, `docs/experiment_log.md`,
  `docs/ai_usage_log.md`.
- **How verified.**
  - `.venv/bin/python -m pytest -q`: **975 passed, 3 skipped**.
  - `write_run()` smoke test into the scratchpad: all three files written,
    and a second write to the same directory was refused.
    `git check-ignore` confirmed `results/landscape/` is tracked and
    `results/raw/` is still ignored.
  - The script aborts before writing on any h\* mismatch or admissible
    heuristic above h\*. h\* was checked three ways: A\*+LM-cut, A\*+h_max,
    and (small n) backward induction over the enumerated state space.
  - The near-perfect h_max was checked by hand against the independent
    oracle (`src/ahg/oracle.py`) on one instance per family at n = 12. h_sp
    and h_add differ from h\* on the same states, so the heuristics are not
    degenerate.
  - A one-seed-per-cell pilot ran before both full runs.
