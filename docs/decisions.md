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

## 2026-10-19 — D9: Exact integer encoding of the frozen cost model

**Status.** Decided; not yet implemented. No code computes costs from CVSS yet.

**What does NOT change.** The attack-effort model in CLAUDE.md §1 rule 5 is
unchanged: `c(a) = 1 + 9·(1 − x_a)`, where `x_a ∈ [0,1]` is the normalised CVSS
exploitability sub-score. It is an effort proxy, not a probability. This entry
does two things:

1. It fixes the normalisation of `x_a`, which rule 5 left open.
2. It chooses an exact numeric encoding of `c(a)`.

Multiplying every cost by the same positive constant changes no optimal plan,
no ratio we report (plan cost / optimal cost), and no A* expansion order,
provided the heuristics are scaled the same way. The classical heuristics are
computed from the same encoded costs, so they scale automatically.

### Normalisation of x_a

- **Source.** The CVSS **v3.x** base-metric exploitability sub-score `E`, as
  stored in the pinned NVD snapshot.
  - Use v3.1 if the record has it, otherwise v3.0. Both use the identical
    formula `8.22 × AV × AC × PR × UI`. The v3.1 revision changed scoring
    guidance and some metric wording, not this computation. (Resolved; was
    `[VERIFY]`.)
  - CVEs with only v2 or only v4 metrics are **excluded** and counted in the
    dataset log. v2's sub-score has a different range, and v4 has no
    exploitability sub-score, so mixing versions would silently change the
    distribution of x_a.
- **Grid.** NVD reports `E` to one decimal place. The integer `k = round(10·E)` is
  therefore exact. It must be computed with `round`, not `int()`, because
  `10·E` is not exact in floating point. Assert `|10·E − k| < 1e-9`.
- **Anchors, fixed from the spec, not from data.**
  - The raw maximum is 8.22·0.85·0.77·0.85·0.85 = 3.887, which reports as 3.9.
  - The raw minimum is 8.22·0.2·0.44·0.27·0.62 = 0.121, which reports as 0.1,
    or 0.2 if NVD rounds up `[VERIFY rounding rule]`. This will be confirmed
    against a real NVD record when `cost.py` is built. Option B is unaffected
    either way, because the anchors come from the spec, not from the data.
  - Either way, every reported `E` lies in [0.1, 3.9]. We fix `E_lo = 0.1` and
    `E_hi = 3.9`, i.e. `k ∈ [1, 39]`.
  - Computing the anchors from the observed CVE set is **rejected**. It would
    make the cost model depend on the data, including test-split CVEs (rule 1),
    and on the snapshot date.
- **Formula.** `x_a = (k − 1) / 38`. This gives `x_a ∈ [0, 1]` exactly:
  `k = 39` (easiest to exploit) gives `x = 1`, and `k = 1` gives `x = 0`.

### Encoding

- **Unit.** One cost unit is 1/38 of an effort unit. The stored cost is
  `C(a) = 38·c(a) = 38 + 9·(39 − k) = 389 − 9k`, which is an integer.
- **Range.** `C ∈ [38, 380]`, which corresponds to `c ∈ [1, 10]` exactly. Each
  step of 0.1 in `E` changes `C` by 9. Under round-to-nearest, 26 distinct `k`
  values are reachable from the v3.x metric combinations.
- **Reporting.** Costs are shown in effort units, `C / 38`, only at reporting
  time. Ratios are unit-free and unaffected.

### Why

- **Exactness.**
  - LM-cut subtracts costs and tests `costs[ai] == 0` and `m > 0`
    (`src/ahg/heuristics.py:170`, `:202`, `:205`).
  - Search compares path costs with `g2 >= g_best[s2]` (`src/ahg/search.py:75`)
    and drops stale entries with `g > g_best[s]` (`src/ahg/search.py:63`).
  - Label checks compare costs with `==` (`tests/test_core.py:35-40`).

  With real-valued costs, floating-point residue can make these comparisons
  wrong: a zero-cost action may look non-zero, two equal paths may be treated
  as different, or a label check may fail. With integers, all of them are
  exact, and they are the setting the current tests already verify.
- **Faithful normalisation.** Min-max on spec anchors uses the whole of
  `[0, 1]` and therefore the whole cost range `[1, 10]`, which is what rule 5
  states.
- **Rejected alternatives.**
  - (a) `x = E/3.9` with unit 1/39 is also exact, but `x` can never reach 0, so
    `c ≤ 9.77`.
  - (b) Floats plus an epsilon in comparisons: the tolerance is arbitrary and
    becomes a source of silent bugs.
  - (c) `fractions.Fraction` costs: exact, but much slower in the search's hot
    loop, and the same exactness is available more cheaply with integers.

### Consequences

- `Action.cost` is already annotated `int` (`src/ahg/task.py:24`), so no type
  change is needed.
- Learned heuristics may return floats. Only the priority `f` mixes int and
  float. `g` and every label stay integers.
- The toy network and the random test tasks already use integer costs, so they
  are unaffected. They are not in the CVSS range, and they don't need to be.

## 2026-10-21 — D10: Topology family definitions and default distribution

**Decision.** The three topology families are defined by the structural rules
below. Their default parameters, listed with each family, **are the training
distribution**. Every shift split (size, structure, vulnerability; CLAUDE.md
§3) is defined relative to these defaults: a shift changes one factor and
keeps the rest at the values recorded here. Changing a default later is a
change to the training distribution and needs a new entry.

`n_hosts` has no default; the training size range is not fixed yet.

**Rules shared by all families** (`src/ahg/topology.py`):

- **Hosts and services.**
  - Host 0 is the internet: it is the attacker's start and runs no
    services (`src/ahg/network.py:25`).
  - Each internal host runs k services with distinct families from
    `SERVICE_FAMILIES` (`src/ahg/network.py:26`), where
    k ~ U[services[0], services[1]] (`src/ahg/topology.py:50-53`).
  - Default `services = (1, 3)` for every family.
- **Links.** A link from host a to host b allows each of b's services
  independently with the family's link probability.
- **Trust.** Trust edges are drawn per allowed pair with probability
  `p_trust` (`src/ahg/topology.py:66`).
- **Repair edges.**
  - If the internet reaches nothing, one service of an allowed host is
    exposed (`src/ahg/topology.py:83`).
  - Then edges are added until every host is reachable from the internet,
    each from a reached host the family allows (`src/ahg/topology.py:89`).
  - Without this, some hosts would be dead weight no attack can touch.

### flat (`src/ahg/topology.py:135-159`)

- **Rules.**
  - One LAN zone.
  - The internet may reach any host.
  - Any internal host may reach and trust any other (`:149-155`).
  - Repair edges come from any other LAN host (`:156-157`).
- **Tests.** The single-zone rule is checked in `tests/test_topology.py:79`.
- **Defaults.**
  - `p_exposed = 0.2`: per service, internet → host.
  - `p_reach = 0.3`: per service, host → host.
  - `p_trust = 0.05`: per ordered host pair.

### tiered (`src/ahg/topology.py:162-202`)

- **Rules.**
  - Hosts are split as evenly as possible into a DMZ plus `n_tiers − 1`
    deeper tiers (`:178-181`).
  - Only DMZ hosts are exposed to the internet (`:183-184`).
  - Reach and trust edges stay inside a tier or go exactly one tier deeper.
    They never skip a tier and never go upward (`:185-194`).
  - Repair edges come only from the tier directly above (`:197`), so depth
    ≥ `n_tiers`.
- **Tests.** All of the above are checked in `tests/test_topology.py:86`.
- **Defaults.**
  - `n_tiers = 3`.
  - `p_exposed = 0.5`: per service, internet → DMZ.
  - `p_intra = 0.3`: per service, within a tier.
  - `p_down = 0.2`: per service, tier t → t+1.
  - `p_trust = 0.05`: per allowed ordered pair.

### hub_and_spoke (`src/ahg/topology.py:205-244`)

- **Rules.**
  - Hubs come first; spokes are assigned to hubs round-robin (`:225`).
  - Only spokes are exposed to the internet (`:227`).
  - A spoke links only to and from its own hub (`:228-229`).
  - Hubs link to each other (`:231-234`).
  - Trust runs only from a hub to its own spokes, i.e. central
    administration (`:230`).
  - If the internet reaches no spoke, one spoke is exposed (`:235`).
  - Repair edges follow the same rules (`:237-242`).
- **Tests.** All of the above are checked in `tests/test_topology.py:101`.
- **Defaults.**
  - `n_hubs = 1`.
  - `p_exposed = 0.2`: per service, internet → spoke.
  - `p_link = 0.5`: per service, on spoke ↔ hub and hub ↔ hub links.
  - `p_trust = 0.3`: per hub → own-spoke pair.

### Structural distinguishability

At the defaults, a classifier that sees no zone labels and no metadata
recovers the family for 50/50 seeds at n = 30 and n = 60
(`tests/test_topology.py:116-130`). Its rules:

- hub_and_spoke if every internal link touches the top-degree host;
- otherwise tiered if ≥ 20% of hosts are ≥ 3 hops from the internet;
- otherwise flat.

At n ≈ 10, a sparse flat network can look like a chain, so the families are
**not** reliably distinguishable at that size. Structure-shift results on
very small graphs must be read with that in mind.

### Seeding on "family:seed"

**Decision.** Each generator draws all of its randomness from
`random.Random(f"{family}:{seed}")` (`src/ahg/topology.py:121-126`, used at
`:147`, `:176`, `:222`).

**Why.**

- The first version seeded on `seed` alone. Every family draws services
  first, so the same seed gave the same service assignment in every family:
  at seed 0, `lan-1`, `dmz-1` and `hub-1` all ran `[dns, sql]`.
- In the H3b structure-shift test, a held-out-family test graph and a
  training graph with the same seed number would then share their service
  (and later CVE) draws. That is a cross-family correlation that could
  inflate apparent generalisation.
- Seeding on the family string removes it. This is checked in
  `tests/test_topology.py:38`.
- Python hashes string seeds with SHA-512, not `hash()`, so the result does
  not depend on `PYTHONHASHSEED`. This is checked by the cross-process
  determinism test at `tests/test_topology.py:25`.
