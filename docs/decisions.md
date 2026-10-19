# Decision log

Every decision that fixes or changes the formulation, cost model, search
conventions, heuristics, splits, metrics or hypotheses goes here, newest at the
bottom, with a date and the reason. Entries are never edited after the fact; a
later decision that overrides one says so and links back to it.

File:line references point at the code as of the commit that adds the entry.

---

## 2026-10-19 — D1: States are integer bitmasks

**Decision.** A search state is a Python `int` used as a bitmask over fact
indices: bit *i* set means fact *i* is held (`src/ahg/task.py:16`,
`State = int`; masks built by `to_mask`, `src/ahg/task.py:105`).

**Why.** Ints are hashable, so duplicate detection is a dict lookup. They are
immutable and cheap to copy. "Are all preconditions held?" becomes one AND:
`pre_mask & ~state == 0` (`src/ahg/task.py:36-37`). Applying an action is
`state | add_mask`, which is correct only because the task is delete-free
(privileges are never removed).

## 2026-10-19 — D2: One shared best-first search for every algorithm

**Decision.** UCS, A*, weighted A* and GBFS are all the same function,
`best_first_search` (`src/ahg/search.py:41`). They differ only in the weights
of the priority `f = w_g·g + w_h·h`: UCS is h ≡ 0, A* has w_g = w_h = 1,
weighted A* has w_h = w, and GBFS has w_g = 0 (wrappers at
`src/ahg/search.py:100-113`).

**Why.** CLAUDE.md §1 rule 7 requires identical expansion counting,
tie-breaking and duplicate detection across methods. A single code path makes
that hold by construction instead of by convention.

## 2026-10-19 — D3: Tie-breaking key is (f, h, counter, g, state)

**Decision.** Open-list entries are tuples `(f, h, counter, g, state)`
(`src/ahg/search.py:51` for the root, `src/ahg/search.py:86` for successors).
Ties on f go to lower h, i.e. the node believed closer to the goal. Remaining
ties go to the node generated first, using a FIFO insertion counter
(`itertools.count`). g and state are payload and never decide order, because
the counter is unique.

**Why.** On these tasks many nodes share an f value, and tie-breaking changes
node counts a lot. Fixing one documented rule for every heuristic keeps the
comparison fair and reproducible. Lower-h-first is the standard choice for A*.
The counter makes order deterministic and avoids comparing states.

## 2026-10-19 — D4: Reopen closed states on a strictly cheaper g

**Decision.** A successor is pushed only if its new g is strictly lower than
the best known g (`src/ahg/search.py:75`). This applies even if the successor
was already expanded: it is then reopened (`src/ahg/search.py:77-79`). Stale
heap entries, superseded by a cheaper g or already expanded at ≤ g, are
skipped when popped (`src/ahg/search.py:63`).

**Why.** With an admissible but inconsistent heuristic, A* needs reopening to
stay optimal. Learned heuristics and h_add/h_FF are not consistent. The same
policy applies to every heuristic (D2), so node counts stay comparable.

## 2026-10-19 — D5: Goal test on expansion, not generation

**Decision.** A node is tested for the goal when it is popped from the open
list (`src/ahg/search.py:65-67`), not when it is generated.

**Why.** Testing at generation can return a non-optimal path, because a cheaper
path to the goal may still be on the open list. Testing on expansion is what
makes A* with an admissible heuristic (and UCS) return optimal cost.

## 2026-10-19 — D6: The expansion count excludes the goal node

**Decision.** `expanded` is incremented only after the goal test and the
budget check (`src/ahg/search.py:66-71`). When the goal node is popped, the
search returns before counting it. Stale entries skipped at line 63 are not
counted either.

**Why.** It is a convention, and papers differ on it. It applies identically
to every method (D2). It is recorded here so that reported numbers can be
interpreted and compared with other work: add 1 per solved instance to
convert to the "goal counted" convention.

## 2026-10-19 — D7: Admissible set = {h0, hsp, hmax, lmcut}

**Decision.** `ADMISSIBLE = {"h0", "hsp", "hmax", "lmcut"}`
(`src/ahg/heuristics.py:209`). h_add and h_FF are treated as inadmissible.
Only heuristics in this set may carry optimality or bounded-suboptimality
claims (CLAUDE.md §1 rule 8).

**Why.** h0 is trivially admissible. h_max and LM-cut are admissible by their
standard proofs. For h_sp, see D8. Admissibility of every heuristic in the set
is also checked empirically: `hsp ≤ hmax ≤ lmcut ≤ h*` on every reachable
state of 60 random tasks, against brute-force h*
(`tests/test_core.py:48-60`).

Note: on our delete-free tasks h_FF's relaxed plan is a real plan, so h_FF ≥ h*
always. The tests assert `h* ≤ hff ≤ hadd` (`tests/test_core.py:58-60`).
"Inadmissible" therefore means "overestimating" here.

## 2026-10-19 — D8: h_sp = min over preconditions, max over goals

**Decision.** h_sp runs the generalised Dijkstra over facts in `"min"` mode:

- An action fires as soon as its first (cheapest) precondition is reached
  (`src/ahg/heuristics.py:50`, `need = min(1, len(pre))`).
- Its value is that precondition's cost plus the action cost
  (`src/ahg/heuristics.py:83`).
- Goal facts are combined with `max` (`src/ahg/heuristics.py:103-104`).

In effect, conjunctive (AND) preconditions are treated as OR: a plain
cost-weighted shortest path in the fact–action graph.

**Why this keeps it admissible.** For every action, the min over its
preconditions' costs is ≤ the max over them. By induction on the order in
which Dijkstra finalises facts, every fact's h_sp value is ≤ its h_max value.
Taking max over goals, as h_max does, gives h_sp(s) ≤ h_max(s) ≤ h*(s).

Combining goals with sum instead of max would lose this guarantee. Two goals
can share most of their cheapest paths, so summing would count shared actions
twice and could exceed h*.

h_sp is the weakest admissible baseline (always ≤ h_max). It is included
because it is the "attack graph as a plain graph" view that the proposal
compares against.
