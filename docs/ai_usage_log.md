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
