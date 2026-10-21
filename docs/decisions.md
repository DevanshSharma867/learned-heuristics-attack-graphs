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
  - **Resolved 2026-10-21: NVD reports 0.1.**
    - NVD API query `cvssV3Metrics=AV:P/AC:H/PR:H/UI:R`, fetched
      2026-10-21, returned 4 CVEs, all with NVD Primary scores.
      - Scope unchanged (`S:U`) gives exploitability **0.1**:
        CVE-2018-5235 (v3.0), CVE-2019-2872 and CVE-2019-18373 (v3.1).
      - Scope changed (`S:C`) gives **0.2**: CVE-2018-2888 (v3.0).
    - The 0.2 is not a rounding effect. In the CVSS v3 spec the PR weight
      depends on scope: PR:H is 0.27 under `S:U` and 0.50 under `S:C`. That
      gives 8.22·0.2·0.44·0.50·0.62 = 0.224 → 0.2.
    - So the floor reports as 0.1 (round to nearest, not up). It is
      consistent with `E_lo = 0.1`, and no anchor changes.
    - The formula above is shorthand for the spec's scope-dependent PR
      weight. We read NVD's reported `exploitabilityScore`, which already
      includes it, so the encoding is unaffected.
    - Cross-check: recomputing from the spec weights over both scopes gives
      the 26 reachable `k` values stated below. All 22 distinct values seen
      in the D11 measurement fall inside that set.
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

## 2026-10-21 — D11: CVE source, family mapping, window and storage

**Status.** Approved 2026-10-21. The counts below come from a measurement
fetch made on 2026-10-21, not from the pinned snapshot. The pinned snapshot
is built by `scripts/fetch_nvd.py` and `scripts/derive_cves.py`, and its own
counts are recorded in `data/derived/build_log.json`.

### (a) Scorer rule: NVD Primary v3.x only

- **Rule.** A CVE's exploitability `E` is the `exploitabilityScore` of its
  `cvssMetricV31` entry with `source == "nvd@nist.gov"` and
  `type == "Primary"`. If there is no such entry, the `cvssMetricV30` entry
  with the same source and type is used. CNA scores (`type == "Secondary"`)
  are never used.
- **Why.**
  - One CVE can carry several v3 scores from different scorers. For example,
    CVE-2021-44228 has both NVD's and the CNA's.
  - Using only NVD Primary means a single analyst process scored every `E`.
    Mixing scorers would add scorer-dependent noise to `x_a`, and would let
    the vulnerability-shift split partly measure a change of scorer instead
    of a change of vulnerabilities.
- **What it costs.** 966 unique CVEs that have only a CNA v3 score are
  dropped (all years, all families). They are counted as `v3_cna_only`.

### (b) Service family → product mapping

**How products are selected.**

- Each family is a set of `vendor:product` pairs, queried with
  `virtualMatchString=cpe:2.3:*:<vendor>:<product>`.
- A CVE belongs to a product only if one of its `cpeMatch` entries has
  `vulnerable: true` and names that product. Matches where the product is
  only the platform are excluded and counted as `platform_only` (48, all
  years).

**The mapping.** Counts are CVEs included in the window (c), per product.
| family | product (CPE `cpe:2.3:*:` + …) | in window |
|---|---|---|
| dns | `isc:bind` | 72 |
| dns | `nlnetlabs:unbound` | 22 |
| dns | `powerdns:authoritative` | 17 |
| dns | `powerdns:recursor` | 24 |
| dns | `thekelleys:dnsmasq` | 28 |
| ftp | `proftpd:proftpd` | 13 |
| ftp | `pureftpd:pure-ftpd` | 6 |
| ftp | `filezilla-project:filezilla_server` | 1 |
| ftp | `solarwinds:serv-u` | 23 |
| ftp | `wftpserver:wing_ftp_server` | 8 |
| ftp | `crushftp:crushftp` | 8 |
| ftp | `cerberusftp:ftp_server` | 5 |
| ftp | `beasts:vsftpd` | 0 |
| ftp | `xlightftpd:xlight_ftp_server` | 0 |
| http | `apache:http_server` | 87 |
| http | `apache:tomcat` | 83 |
| http | `f5:nginx` | 20 |
| http | `nginx:nginx` (pre-F5 vendor name) | 0 |
| http | `microsoft:internet_information_services` | 1 |
| mail | `microsoft:exchange_server` | 54 |
| mail | `exim:exim` | 39 |
| mail | `dovecot:dovecot` | 28 |
| mail | `postfix:postfix` | 3 |
| mail | `sendmail:sendmail` | 2 |
| rdp | `freerdp:freerdp` | 89 |
| rdp | `neutrinolabs:xrdp` | 17 |
| smb | `samba:samba` | 107 |
| sql | `oracle:mysql` | 516 |
| sql | `mariadb:mariadb` | 200 |
| sql | `postgresql:postgresql` | 70 |
| sql | `microsoft:sql_server` | 13 |
| sql | `mysql:mysql` (pre-Oracle vendor name) | 1 |
| ssh | `openbsd:openssh` | 36 |
| ssh | `libssh:libssh` | 12 |
| ssh | `dropbear_ssh_project:dropbear_ssh` | 13 |

**How the mapping was arrived at, for transparency.**

- The FTP list originally had only the first four products and gave 25
  CVEs over all years. Serv-U, Wing FTP, CrushFTP, Xlight and Cerberus were
  added after that first measurement. No split exists yet, so this is not
  test leakage, but the mapping was extended in response to the data.
- `microsoft:remote_desktop_protocol` was tried and does not exist as a
  CPE (0 results), so it was dropped.

**Known weaknesses, kept on purpose and documented.**

- **rdp: known modelling limitation.** rdp is kept, as FreeRDP plus xrdp.
  - **Why it is imperfect.**
    - Windows RDP-server CVEs (e.g. CVE-2019-0708) are filed under Windows
      OS CPEs, so they cannot be isolated by CPE.
    - FreeRDP CVEs are mostly client-side: a malicious server attacks the
      client. That is the opposite direction to "attacker reaches an RDP
      service".
  - **Why that is acceptable.** The cost model consumes only the CVSS
    exploitability sub-score, as an abstract attack-effort proxy (D9). It
    does not model which way an exploit runs. So the rdp family works as a
    labelled distribution of exploitability scores, which is all the
    pipeline needs from it.
  - **What the paper must not say.** It must not claim these are realistic
    RDP-server scenarios. This belongs with the synthetic-topology threat to
    validity.
- **smb.** Samba only. Windows SMB has the same OS-CPE problem. With a
  single product, a held-out-product shift is impossible inside smb.
- **sql.** Dominated by `oracle:mysql` (516 of 668).

**For later split design.**

- A held-out-product vulnerability shift is only feasible within families
  that have real product diversity: dns, ftp, http, mail and sql.
- smb (Samba only) and rdp (FreeRDP plus xrdp, dominated by FreeRDP) cannot
  support an intra-family held-out-product shift.

**CVEs in more than one family.** Seven CVEs match two families over all
years, and 2 of them are inside the window. They are excluded and counted
as `multi_family`, so families stay disjoint for the vulnerability-shift
split.

### (c) Window and inclusion rule

- **Inclusion.** A CVE is included if it is published from 2016-01-01 to
  2023-12-31 inclusive, has an NVD Primary v3.0/v3.1 `exploitabilityScore`,
  and is matched as vulnerable by exactly one family.
- **Per-family counts in this window.**

  | dns | ftp | http | mail | rdp | smb | sql | ssh | total |
  |---|---|---|---|---|---|---|---|---|
  | 158 | 62 | 189 | 125 | 106 | 107 | 668 | 58 | 1473 |

  These counts are unique CVEs after removing the multi-family ones. The
  per-product table in (b) is counted before that, so its rows can overlap.
  Every family has at least 58, so none is under a few dozen.
- **Spread of `E` values.** The number of distinct `E` values per family is
  6–20. Over all families, 22 distinct values occur, and the mass is
  concentrated at 3.9 (472) and 2.8 (310).
- **Why this window.** It comes from the per-year share of matched CVEs
  that carry an NVD Primary v3 score:

  | year | ≤2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | share | ≤0.05 | 0.89 | 0.95 | 1.00 | 1.00 | 0.79 | 0.43 | 0.55 | 0.55 | 0.32 | 0.22 | 0.39 |

  - **Before 2016**, NVD scored almost only in v2 (43 back-filled v3
    exceptions in total, which are dropped).
  - **From 2024**, coverage falls further. The explanation is NVD's
    analysis backlog and its shift toward relying on CNA scores. Those
    records are also still being analysed, so a snapshot of them would be
    unstable. We do not need the exact backlog start date: the window
    boundary is set from the coverage drop and the instability.
  - **What the window costs.** Extending to the snapshot date would add 38
    dns, 22 ftp, 16 http, 39 mail, 103 rdp, 3 smb, 19 sql and 41 ssh. Most
    of the rdp gain is FreeRDP (93 of 103).
- **Coverage is uneven within the window too.** NVD scored fewer of the
  2021–23 CVEs, and unevenly by vendor: `oracle:mysql` drops from 89
  included in 2020 to 3 in 2021, while its CNA-only count rises from 50 to
  121. So a vulnerability-shift split must not be defined by publication
  year, or it would partly measure NVD's scoring coverage.
- **Invisible CVEs.** CVEs that NVD never analysed have no CPE
  configuration, so a CPE query never returns them. They are invisible, not
  excluded. The exclusion counts in (d) are therefore a lower bound on what
  the window misses.

### (d) Exclusions, counted in the dataset log

- **What each build records.** Each dataset build logs per-family counts for
  every exclusion reason:
  - `v2_only`: has a v2 score but no v3 score. 1,405 unique CVEs over all
    years, before the window is applied.
  - `v4_only`: has a v4 score but no v2 or v3 score. 0 among CPE-matched
    records, because NVD-analysed records carry v3.
  - `v3_cna_only`: has a v3 score from the CNA but none from NVD.
  - `platform_only`: the product matched only as a platform, not as the
    vulnerable component.
  - `multi_family`: matched by more than one family.
  - `outside_window`: published outside 2016–2023.
- **Why it matters.** Excluded CVEs are never dropped silently. This mirrors
  CLAUDE.md §1 rule 10 for data.

### (e) Storage split

- **Raw snapshot** goes in `data/raw/nvd/<snapshot-date>/`, outside git.
  - It holds one gzipped API response per product query.
  - `manifest.json` records:
    - the exact query URL and parameters;
    - `totalResults`;
    - the UTC fetch timestamp;
    - the SHA-256 of each file;
    - the script's git commit.
  - The fetch script uses smaller pages and one paced retry, because
    2000-record pages were cut off mid-transfer during measurement.
  - Experiments never touch the network (CLAUDE.md §3).
- **Derived table, committed to git.** `data/derived/cves.csv` with columns:
  - `cve_id`
  - `family`
  - `products`: every vendor:product matched as vulnerable within the
    family, `;`-separated and sorted
  - `cvss_version`: 3.0 or 3.1
  - `exploitability_score`
  - `published`: date only, YYYY-MM-DD

  The `published` column lets the window be re-checked from the table
  alone. It also lets us show that the vulnerability-shift split is not a
  publication-year artefact.

  It holds no descriptions, references, vectors or CNA-authored text. It is
  generated by a script from the raw snapshot plus the manifest, and is
  never hand-edited.
- **Build log, committed to git.** `data/derived/build_log.json` records:
  - the snapshot date;
  - the manifest's SHA-256;
  - the window;
  - per-family included counts;
  - per-family exclusion counts.
- **Required `.gitignore` change.** The file currently ignores all of
  `data/`. It would ignore `data/*` but keep `data/derived/`.

### (f) NOTICE file

A top-level `NOTICE` file will contain three things:

1. The NVD non-endorsement notice, using the Terms of Use wording: *"This
   product uses the NVD API but is not endorsed or certified by the NVD."*
2. MITRE's CVE copyright designation and the licence text from the CVE
   Terms of Use: perpetual, worldwide, non-exclusive, no-charge,
   royalty-free, irrevocable copyright licence, on condition that the
   copyright designation and licence are reproduced.
3. A statement that `exploitability_score` values are NVD-generated (U.S.
   Government work).

- **`[VERIFY]` before the repo goes public.** The live cve.org Terms of Use
  page must be checked, because the text above comes from an archived 2017
  copy. This does **not** block building now: the repo stays private until
  the preprint.

## 2026-10-21 — D12: Attack-graph schema (facts, actions, goal)

**Decision.** `src/ahg/attack_graph.py` turns a network (D10) with one CVE per
service (D11, `assign_cves`) into a delete-free `Task` (D1) as follows. The
generator is native; MulVAL is not used to produce any dataset.

**Facts.** One per host, with fact index = host id, so a state's bitmask is
the set of hosts the attacker controls.

| fact | meaning | MulVAL counterpart |
|---|---|---|
| `attackerLocated(internet)` (fact 0) | the attacker's start; the only initial fact | `attackerLocated(internet)` |
| `execCode(h)`, h internal | the attacker can run code on host h | `execCode(h, Perm)` with a single `Perm` |

**Actions.** All preconditions are conjunctive.

- **exploit**: one per reach edge `Reach(src, s)`, where service s runs on
  host h.
  - pre `{fact(src)}`, add `{execCode(h)}`.
  - cost `C = cost_units(E)` (D9), with E the exploitability of the CVE
    assigned to s.
- **login**: one per pair of a trust edge `Trust(t, h)` and a reach edge
  `Reach(a, s)` to a login service s on h. Login services are `ssh`, `rdp`
  and `smb`.
  - pre `{execCode(t), fact(a)}`, i.e. credentials taken from t AND network
    access to h's login service from a. It has a single precondition when
    a = t.
  - add `{execCode(h)}`.
  - cost `LOGIN_COST = 38`, i.e. c = 1 effort unit.

**Goal.** `execCode(target)`. The target is drawn uniformly among the hosts
with the largest hop distance from the internet, using a separate rng stream
`"goal:family:seed"` (next to D10's `"family:seed"` and the CVE stream
`"cves:family:seed"`).

**Correspondence to MulVAL** (Ou et al. 2005) `[VERIFY rule names against
MulVAL's interaction_rules.P before citing them in the paper]`:

- An exploit action is MulVAL's remote-exploit rule (`execCode` from
  `netAccess` plus static `vulExists`/`networkServiceInfo` leaves), with
  `netAccess` derived by the direct-access rule (src = internet) or the
  multi-hop rule (src internal, static `hacl` leaf).
- A login action is MulVAL's login chain: `execCode(h)` from
  `principalCompromised` (credentials taken on t) AND `canAccessHost(h)`,
  which comes from `logInService` plus `netAccess(h, …)` (from a).
- Static MulVAL facts (`hacl`, `vulExists`, `networkServiceInfo`,
  `hasAccount`, `logInService`) are compiled into which actions exist, the
  usual grounding step in planning. They never change, so they carry no
  state bit.
- MulVAL's cost-free intermediate derived facts (`netAccess`,
  `canAccessHost`, `principalCompromised`) are **folded into the actions
  that consume them**. Each action therefore corresponds to one MulVAL
  derivation path ending in `execCode`.

**Why fold the intermediate facts.**

- They have no CVE and no cost. As zero-cost actions they would create
  zero-cost plateaus: every order of acquiring free facts is a distinct
  state at the same g, which inflates node counts for every method alike
  with search that no heuristic can steer.
- Folding preserves reachability and optimal cost. The task is delete-free
  and the folded steps are free, so every plan in one representation maps to
  a plan of equal cost in the other.
- Consequence for later MulVAL validation: compare, per instance, the set of
  reachable `execCode` facts and the optimal cost, not graph isomorphism.

**Why one privilege level.** `data/derived/cves.csv` holds only the
exploitability sub-score (D11(e)), with no impact metrics, so there is no
data to decide whether an exploit yields user or root. Two levels would add
an unvalidated assumption.

**Why login costs c = 1.** A login with valid credentials has no CVE, so the
cost model (CLAUDE.md §1 rule 5) has no x_a for it. We take x = 1: the
easiest possible action, the floor of the model's [1, 10] range. Zero was
rejected because it would bring back zero-cost plateaus. This is the one
cost not derived from CVSS, and it applies identically to every instance.

**Reachability (CLAUDE.md §1 rule 10).**

- Every internal host is reachable from the internet over reach edges (D10
  repair edges). Every reach edge yields an exploit action. So by induction
  along a BFS path, every `execCode(h)` is reachable, and every goal is
  reachable by construction.
- `build_task` still checks it: h_max is finite exactly when the goal is
  reachable in a delete-free task. If the check fails, it raises
  `UnreachableGoal`. Callers log that as a generation failure, separately,
  and never drop it or count it as solved.

**Consequence, measured 2026-10-21 at the D10 defaults (20 seeds per
cell).** These tasks are close to shortest-path problems.

- **Why.** An exploit has one precondition, so the only genuine
  conjunctions are logins whose network access comes from a third host
  (a ∉ {t, internet}).
- **hub_and_spoke.** None can exist, by construction. Trust runs hub → own
  spoke, and a spoke's services are reachable only from its hub or the
  internet.
- **Where the heuristics fell below h\*.** Counted over every non-goal
  reachable state; at n = 5–6 hmax(init) < h\* in 1 instance in total, and
  at n = 8 in 3 tiered instances out of 20:

  | n | flat | tiered | hub_and_spoke |
  |---|---|---|---|
  | 5 | hmax: 2 of 205 states; lmcut: 0 | 0 of 190 | 0 of 167 |
  | 6 | 0 of 378 | hmax: 1 of 268 | 0 of 263 |
  | 8 | 0 of 1,602 | hmax: 16 of 871; lmcut: 8 | 0 of 926 |

- **Implication.** On such tasks h_max and LM-cut are nearly perfect, so
  H1 would be close to vacuous. This needs a decision before any dataset is
  generated. It is recorded here, not worked around.

## 2026-10-21 — D13: `privileges_required` column in the derived CVE table

**Decision.** `data/derived/cves.csv` gains a seventh column,
`privileges_required` (`N`, `L` or `H`). This amends the column list in
D11(e); every other part of D11 stands.

**Why.** It is the data needed to give exploits PR-gated conjunctive
preconditions in the attack-graph schema: network reachability AND a prior
privilege for PR:L/H exploits (follow-up to the D12 finding that generated
tasks are near shortest-path). The schema itself is not decided here.

**How.**

- **Source.** The CVSS Privileges Required (PR) metric, read by
  `scripts/derive_cves.py` from the existing 2026-10-21 snapshot, with no
  re-fetch.
- **Same scoring as the score.** PR comes from the same NVD Primary v3.x
  metric as `exploitability_score`, i.e. the same `vectorString` under the
  D11(a) scorer rule. Score and PR therefore always come from one scoring.
- **Cross-check.** The vector's PR is checked against that metric's
  `cvssData.privilegesRequired` field, and a mismatch is an error. None
  occurred.
- **Determinism.** The column is appended last. Regenerating leaves the
  first six columns and `build_log.json` byte-identical.
- **Distribution.** Over the 1,473 rows: N 693 (47.0%), L 449 (30.5%),
  H 331 (22.5%). sql supplies 305 of the 331 PR:H.
