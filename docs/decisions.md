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

## 2026-10-21 — D14: Label-generation design for the cost-to-go estimator

**Status.** Design only, not implemented. It will be implemented once the
task schema is final (D12 is under revision). No states have been sampled
and no labels exist.

### 1. What a label is

- **The label.** A label is the exact optimal cost-to-go h\*(s) of a sampled
  state s of one instance, in D9 integer cost units.
- **The solver.** It is computed by the exact solver, A\* with LM-cut. That
  search is optimal because LM-cut is admissible (D7), the goal is tested on
  expansion (D5) and states are reopened (D4).
- **The cross-check.** Every label is also computed by the independent UCS
  in `src/ahg/oracle.py` (CLAUDE.md §1 rule 6).
  - The two must agree exactly; costs are integers (D9).
  - A mismatch is a hard failure: the batch is aborted and nothing from it
    is used.
- **Infinite labels.** In a delete-free task whose goal is reachable from
  the initial state, every reachable state can still reach the goal. An
  infinite label is therefore a generation failure, logged separately and
  never dropped (rule 10).
- **Goal states** (h\* = 0) are kept, but counted separately in the batch
  log.

### 2. State sampling

- **Order.** Splits are made at the topology level from disjoint seeds
  before any state is sampled (rule 1). Sampling then happens per instance,
  so a state's instance, and therefore its split, is fixed before the state
  exists. States are never pooled or drawn across splits.
- **Enumeration.** If an instance's reachable state space is at or below a
  cap (set in the label config), every reachable state is labelled.
- **Above the cap**, states are drawn, deduplicated per instance, from:
  - **On-optimal:** every state along one optimal plan from the initial
    state.
  - **Off-optimal:** states from random rollouts. Each rollout applies
    uniformly chosen applicable, useful actions from the initial state and
    stops after a uniformly drawn number of steps.

  Both kinds are needed. A\* evaluates h mostly off the optimal path, and a
  learned heuristic trained only on optimal-path states would be fitted to
  states it rarely meets.
- **Sampling rng.** It is seeded on `"labels:family:seed"`, separate from
  the topology, CVE and goal streams (D10, D12). So relabelling an instance
  never changes the instance itself.
- **Labels for every split.** Validation and test instances are labelled
  too, because evaluation needs h\* for overestimation statistics and
  suboptimality. They are written as separate batches tagged with their
  split, and training code reads only `train` batches. A test asserts that
  no topology seed occurs in two splits.

### 3. Exact-solver size ceiling

- **What sets it.** Labels need h\*, so training instance size is capped at
  what the exact solver and the oracle both finish in reasonable time. The
  oracle is uninformed UCS, so it will usually bind first.
- **Measured so far.**
  - Random tasks, not attack graphs (`docs/status_report.md` §3.4 and §6.4):
    - UCS and A\*(h_max) exceeded 30 s at about 60 facts / 90 actions on
      some seeds.
    - A\*(LM-cut) stayed ≤ 0.4 s up to 80 facts / 120 actions.
    - Brute-force enumeration is usable only to about 13–15 actions, so it
      cross-checks small instances in tests only, not labels.
  - D12 (v1) attack graphs: at n = 12, one instance had 13 facts, 89
    actions and 1,894 reachable states, solved in milliseconds. That schema
    is being revised, so this number does not carry over.
- **How the ceiling will be set.** Empirically, on the final schema, before
  any training run:
  1. Time labelling (solver plus oracle) per instance across sizes.
  2. Set the ceiling from a per-instance time budget recorded in the
     config.
  3. Record the measurement in `docs/experiment_log.md`.
- **Larger instances.** Size-shift test instances above the ceiling get h\*
  only where the solver finishes. Elsewhere they are reported per CLAUDE.md
  §4, against the best-known cost and clearly labelled.

### 4. Provenance and storage

**Recommendation: `data/labels/<batch-id>/`, not `results/raw/`.**

- Labels are inputs to training, generated deterministically from a config.
  `results/raw/` holds run outputs that tables and figures are computed
  from. Keeping the two apart means an aggregation script can never pick up
  labels as results.
- `data/*` is already gitignored (D11(e)), so label batches stay local like
  the raw NVD snapshot.
- Batches are **append-only**. A new config or commit means a new
  `<batch-id>`, and an existing batch is never overwritten (rule 11, applied
  to labels).

Each batch directory holds:

- **`manifest.json`:**
  - batch id and UTC timestamp;
  - git commit and dirty flag;
  - a copy of the label config and its SHA-256;
  - split name;
  - the instance list (family, seed, n_hosts, generator parameters, schema
    version);
  - every rng seed and stream name;
  - the SHA-256 of `data/derived/cves.csv` and the NVD snapshot date;
  - solver and oracle identifiers;
  - Python and library versions;
  - hardware (platform, CPU, RAM);
  - counts: states labelled, goal states, enumerated vs sampled, failures;
  - per-instance labelling time.
- **The labels:** one row per (instance, state) with:
  - the instance id;
  - the state bitmask;
  - h\*;
  - the sampling source (`enumeration`, `optimal_path` or `rollout`).
- **A failures file:** unreachable goals and solver timeouts, kept apart
  from the labels (rule 10).

### 5. Train-only normalisation

- **Fit on train only.** Any statistic fitted to data is fitted on the
  train split only and applied unchanged to validation and test (rule 1).
  This covers feature means and stds, label scaling, and any
  outlier/clipping thresholds.
- **Prefer fixed constants.** Where a fixed constant works, it is used
  instead of a fitted statistic, and nothing then needs fitting. One example
  is expressing costs in effort units via the D9 scale of 38.
- **Stored with the checkpoint.** The fitted statistics are saved with the
  model checkpoint and the train batch ids they came from.
- **Separate decisions.** Validation is used for early stopping and tuning
  only. Test batches are read only by the evaluation scripts.

## 2026-10-28 — D15: Depth–coupling sweep design

**Status: ADOPTED (sweep design), 2026-10-28.** It was drafted as
PROPOSED, then amended and adopted the same day. **Every amendment below
was made before any part of the sweep ran:**

- the censoring rule in §6 (censored instances count as R = +∞);
- the report-row requirement in §4;
- the forced level-0 host in §1(a), found while specifying the generator:
  without it cred(1) can be unobtainable;
- the shared sampling stream in §3, needed for the anchor cells to
  reproduce [S].
- an erratum to the meaning of n, found while writing the tests:
  - n is `n_hosts`, the number of internal hosts, as in [S]/[L]; the
    internet is one more host;
  - the draft wrongly read n as including the internet;
  - so "n − 1" became n in the level-count condition and in the
    share-pool size m;
  - the grid values are unchanged.

**The R ≥ 5 threshold in §6 was chosen before any run** and is unchanged by
the amendments.

It replaces the earlier depth-coupling sweep (`findings.md` §5 item 1),
which left no committed script or output and is treated as never run.

**Question.** Is there any structural regime of the generator in which
h_max and LM-cut stop being near-exact, i.e. in which A\*+LM-cut expands
substantially more than plan-length nodes? The explanation under test
(`findings.md` §4): optimal plans are short, and prerequisites are shallow
and do not interact. Each knob below lengthens or couples prerequisites.

### 1. Generator knobs

Two new keyword arguments to `build_task` / `make_instance`, both off by
default. A third axis reuses an existing D10 parameter.

**Byte-identity requirement.** With `cred_levels=0` and `coupling=0`, the
default D12 schema and the `pr_gated=True` variant must produce identical
output: same facts, same actions in the same order, same names, costs and
goal.

- *Test.* Golden SHA-256 hashes of the serialised `Task` for every family ×
  n ∈ {6, 8, 12, 20} × seeds 0–9 × `pr_gated` ∈ {False, True}. They are
  computed at the commit before the change and asserted afterwards.
- *Rng streams.* Each knob draws from its own stream (`"depth:family:seed"`,
  `"coupling:family:seed"`). The topology, CVE and goal streams (D10, D12)
  are never consumed differently.
- *Fact indices.* New facts are appended after every existing fact (hosts,
  then `pr_gated` capabilities), so existing indices never move.

**Base schema for the sweep.** The knobs act on the D12 schema with
`pr_gated=False`, so their effect is not mixed with PR gating. The two
compose (independent extra preconditions), but only the anchor cells (§2)
use `pr_gated=True`.

#### (a) Depth: `cred_levels = D` (0 = off)

*Security grounding.* Tiered administrative credentials, as in
Active-Directory-style tiering. Hosts in a higher tier accept access only
with that tier's credentials. Those credentials are cached on machines one
tier down, where higher-tier admins log in. Breaking such a tier model is
exactly a credential-hopping chain: compromise a host, dump the cached
credentials, use them together with a network position to enter the next
tier.

*Schema.*

- **Levels.** Every internal host gets a level in {0, …, D} from the depth
  stream:
  - the target is at level D;
  - for each k in 0…D−1, one non-target host is forced to level k, so that
    every level is occupied. This needs n ≥ D + 1 internal hosts;
    otherwise `make_instance` raises `KnobInfeasible`, which is logged as a
    generation failure.
    - *Amendment, before any run:* the draft forced only levels 1…D−1. With
      no level-0 host, cred(1) has no harvest action, so every gated host,
      and the goal, would be unreachable by construction rather than by
      structure.
  - every other host is drawn uniformly from {0, …, D}.
- **Facts.** `cred(1)` … `cred(D)`.
- **Harvest.** `harvest cred(k)@h`, for each internal host h at level k − 1:
  pre {execCode(h)}, add {cred(k)}, cost `LOGIN_COST`.
- **Gated entry.** Every exploit and login whose effect is execCode(h), for
  h at level k ≥ 1, gains `cred(k)` as an extra conjunctive precondition.
  - Entering a level-k host therefore needs a credential taken from a
    *different* host at level k − 1, AND network access from a controlled
    `src`.
  - So reaching the target is a chain of D conjunctive steps across hosts.
- **Exploit costs** stay CVSS-derived (D9). Only the gate is added.

*Why h_max should degrade.* h_max takes the max over preconditions, while h\*
pays for both branches (the credential and the network position). The gap
should grow with D. LM-cut prices disjoint landmarks additively, so it
should degrade only where the credential branch and the network branch
share actions. That is a falsifiable prediction, recorded before running.

*Reachability.* Repair edges (D10) guarantee a host-graph path, not a path
that respects levels. Instances whose goal becomes unreachable raise
`UnreachableGoal` and are logged per cell (rule 10).

#### (b) Hop depth: tiered `n_tiers` ∈ {3 (D10 default), 5}

*Security grounding.* The depth of network segmentation: the number of
firewalled zones between the internet and the asset.

- This uses the existing D10 parameter, so no new code is needed.
- It applies to tiered only. flat and hub_and_spoke have no zone-depth
  parameter, and adding one would change their family definitions (D10).
- `choose_target` already picks among the deepest hosts.

#### (c) Coupling: `coupling = ρ` ∈ [0, 1], with `share_pool = m`

*Security grounding.* Lateral movement that needs material from a third
host, besides network access to the target. Examples:

- a database password read from an application server's config, then used
  against the DB;
- NTLM relay, which needs a controlled host to coerce or capture
  authentication plus a host that reaches the target service;
- a payload staged on an internal file share.

In each case the second precondition is "control of host k", with
k ∉ {src, h}.

*Schema.*

- **Secret holders.** From the coupling stream, draw a pool P of m distinct
  internal hosts (m = 1: one shared secret holder; m = n: all internal
  hosts).
- **Which exploits.** Each exploit with an *internal* src is selected
  independently with probability ρ. Exploits from the internet are exempt,
  so the first foothold is unconstrained, as before.
- **Extra precondition.** A selected exploit on host h gains execCode(k),
  with k drawn uniformly from P \ {src, h}. If that set is empty, the exploit
  is left unchanged, and the count of such exploits is logged.
- **ρ** sets how many actions carry two non-trivial preconditions from
  different hosts.
- **m** sets how much those preconditions are shared:
  - small m: a few holders feed many actions, i.e. shared landmarks. This is
    predicted easy for LM-cut, like `capability(user)` in [S]/[L].
  - m = n: mostly distinct holders, i.e. many interacting sub-goals.

*Reachability.* Coupling can create cycles (k reachable only through h), so
instances can become unreachable. They are logged as for (a).

### 2. Grid

| axis | values |
|---|---|
| `cred_levels` D | 0, 1, 2, 3 |
| (ρ, m) | (0, –), (0.25, 1), (0.25, n), (0.5, 1), (0.5, n), (1, 1), (1, n) |
| family variant | flat, hub_and_spoke, tiered (`n_tiers`=3), tiered (`n_tiers`=5) |
| n (`n_hosts`: internal hosts; the internet is one more, as in [S]/[L]) | 8, 12, 20 |
| seeds per cell | 0–19, fixed. No "until k reachable" rule, so seed selection is the same in every cell. |

- **Size.** 4 × 7 = 28 knob configurations × 4 family variants × 3 sizes =
  **336 cells, 6,720 instances**. All other generator parameters are at the
  D10 defaults. tiered at n = 8 with 5 tiers has ~1–2 hosts per tier; such
  cells are reported but flagged.
- **Anchor cells.** D = 0, ρ = 0, with `pr_gated=True`, at n ∈ {8, 12}. The
  new script must reproduce the [S] per-instance numbers for those
  (family, n, seed) exactly. This checks that the new tooling measures the
  same thing as `measure_landscape.py`.
- **Budgets.** All caps are expansion counts, never wall-clock timeouts, so
  every result is deterministic and reproducible.
  - Search from the initial state: 200,000 expansions per search (h0,
    h_max, LM-cut), as in [S]/[L]. A capped count is a lower bound and is
    flagged.
  - h\* of a measured state (§3): 20,000 expansions per search.
  - Labelling, per instance: 2,000,000 expansions in total across all
    measured states. Once it is spent, the remaining states are counted as
    `h* unknown`, never dropped.
- **Enumeration.** Full enumeration plus backward induction, capped at
  `ENUM_CAP` = 50,000 reachable states, as in [S].
  - At n = 12, [S] had a median of 3,079 and a max of 9,023 reachable
    states. D credential facts can multiply that by up to 2^D, so some
    n = 12, D = 3 instances will exceed the cap.
  - Instances that are not enumerated are counted per cell.
  - n = 8 is expected to enumerate everywhere; n = 20 will not.

### 3. Which states are measured

1. **Initial state.** Every instance.
2. **Random-walk samples.** The D14 §2 off-optimal rollouts, up to 300
   distinct non-goal states per instance. The procedure is identical to
   `measure_landscape.sample_states`. The rng is
   `"landscape:{family}:{n}:{seed}"`, the [S]/[L] stream, in every knob
   configuration.
   - *Amendment, before any run:* the draft named a per-configuration
     stream, under which the anchor cells could not reproduce [S]'s
     sampled states.
   - The tasks differ between configurations anyway, so sharing the stream
     only gives common random numbers across configurations.
3. **A\*-expanded states (`findings.md` §5 item 3).** Every state expanded
   by A\*+LM-cut from the initial state, and separately every state
   expanded by A\*+h_max.
   - *Lookup.* Where the instance is enumerated, h\* comes from the backward
     induction table for every expanded state.
   - *Otherwise.* Up to 300 expanded states are drawn uniformly (recorded
     rng) and labelled by A\*. A subsampled set is flagged.
   - *Code change needed.* `SearchResult` does not expose the expanded
     states today. This needs an opt-in `trace=` argument on
     `best_first_search` that records each state at the point where
     `expanded` is incremented. A test asserts that expansion counts, plans
     and costs are unchanged with and without tracing, for every heuristic.
4. **Every reachable state** where enumerated, as in [S]. This keeps sampler
   bias visible next to the sampled and expanded-state numbers.

### 4. Metrics (per instance; per cell as medians, plus a bootstrap 95% CI where stated)

- **Effort.** Nodes expanded from the initial state by h0, h_max and LM-cut
  (D6 convention), next to the optimal plan length and h\*. The primary
  ratio is **R = expanded(LM-cut) / plan length**; R_hmax likewise.
  - An instance whose initial A\*+LM-cut search hit the budget is
    *censored*: its R is +∞ (§6).
- **Report rows (amendment, before any run).** In `report.md`, each cell's
  row shows median R, the censored count, the reachable fraction (k/20)
  and the generation-failure count side by side. A hard cell that is
  mostly unreachable is then visible at once.
- **Exactness.** For h_max and LM-cut, separately over the sampled,
  expanded and enumerated state sets: the fraction of states with h < h\*,
  the mean gap, and the max gap (in D9 units and effort units).
- **Instance accounting, every category logged and listed by seed:**
  reachable, `UnreachableGoal`, any other generation failure
  (`KnobInfeasible`: forced levels cannot be placed because
  n < D + 1), init searches at
  budget, `h* unknown` states, and coupled exploits left unchanged.
- **Structure descriptors** (so a hard cell can be explained):
  - #facts, #actions, #reachable states;
  - the number of actions with ≥ 2 non-trivial preconditions from distinct
    hosts;
  - the length of the credential chain on the optimal plan;
  - the target's hop depth.
- **Time.**
  - Per-instance wall-clock, plus per-heuristic search time from the
    initial state, including heuristic computation (rule 7).
  - This is diagnostic: if instances run in parallel workers, absolute
    times are noisier. All methods for one instance run sequentially in the
    same worker, so within-instance comparisons stay paired.
  - Hardware is recorded in provenance; see the note in §7.

### 5. h\* checks

- **Abort on any mismatch, as in `measure_landscape.py`.** Nothing is
  written if any of these fail:
  - A\*+LM-cut = A\*+h_max on every measured state;
  - backward induction = A\* on every measured state of enumerated
    instances;
  - UCS = h\* on the initial state where UCS finished;
  - no admissible heuristic above h\* on any measured state;
  - no reachable state with infinite h\*.
- **Independent oracle (`src/ahg/oracle.py`) on the actual run instances.**
  - *n ∈ {8, 12}, every enumerated instance:* `optimal_cost` from the
    initial state, plus from 20 states drawn uniformly (recorded rng) from
    the union of sampled and expanded states.
  - *n = 20:* from the initial state only, and only where `uniform_cost`
    finished within budget. The oracle has no budget, and it explores the
    same space, so this bounds its run time without changing its code.
  - *On mismatch:* abort.
- **Recording.** `raw.json` stores, per instance, a list of
  `(state, oracle h*, A* h*)` for every oracle-checked state. `report.md`
  shows per cell how many instances and states the oracle checked, so the
  claim "checked by the independent oracle" is scoped exactly.

### 6. Pre-registered success criterion

Fixed here, before any run. Changing it after seeing results needs a new
D-entry that says so.

- **Calibration from [S]/[L].** Median R is ≈ 1.0–1.25 in every cell
  measured so far. For example, tiered n = 12 has h_max 6 and LM-cut 5
  against plan length 5.
- **Eligible cell.** n ≥ 12, ≥ 10 reachable instances out of 20, and median
  plan length ≥ 3 among the instances whose initial A\*+LM-cut search
  solved. The plan-length rule excludes trivially short plans, where a
  small absolute excess gives a large R.
- **Censoring (amendment, before any run).** A budget hit must not make a
  cell look easier or drop out.
  - *Censored instances stay in.* An instance whose initial A\*+LM-cut
    search hit the 200k budget counts as censored-hard, with R = +∞. It
    stays in the median and in every bootstrap resample as +∞.
  - *Only two exclusions.* An instance is excluded from R only if it is
    unreachable or a generation failure.
  - *Censoring never makes a cell ineligible.* The censored count is
    reported next to R.
  - *Mostly censored cells.* If more than half of a cell is censored, its
    median R is +∞. It meets condition 1 below, but still needs the
    fresh-seed confirmation in condition 2.
  - *Cross-check.* If LM-cut solved but A\*+h_max hit the budget, R is
    finite, taken from LM-cut's plan. That instance is flagged
    "h\* not cross-checked".
- **A hard regime exists** if at least one eligible cell meets **both**:
  1. median R ≥ 5, with the bootstrap 95% CI lower bound of the median ≥ 3
     (10,000 resamples of instances);
  2. **confirmation on fresh seeds.** The same cell rerun on seeds 100–119
     gives median R ≥ 5 again.

  336 cells are screened. Without fresh seeds, a single cell crossing a
  threshold could be selection noise, which is why condition 2 is required.
- **Why 5.** If A\*+LM-cut expands ≥ 5× plan length, a perfect heuristic
  could save ≥ 80% of expansions. That leaves room for an H1 effect large
  enough to survive the inference-time cost (`findings.md` §5 item 5).
  Below that, any learned-heuristic win would sit inside the noise of
  inference overhead.
- **Secondary, descriptive only (never sufficient alone).** In the cells
  that meet the criterion, LM-cut has h < h\* on ≥ 20% of A\*-expanded
  states. The same statistics are reported for h_max with R_hmax.
- **If no eligible cell meets it.** Within this generator and these knob
  ranges, classical admissible A\* is near-exact, and H1 as stated has no
  room to show an effect on these graphs.
  - That is recorded as a negative result in `findings.md`, using the
    full grid, the predictions in §1 and whether they held.
  - The knob ranges are **not** widened post hoc to search for a hard cell.
    Any further sweep (larger D, other generators, multi-goal tasks) needs
    its own pre-registered D-entry.
  - The paper framing, and any hypothesis revision, is then decided in a
    separate D-entry. This draft does not decide it.

### 7. Runtime estimate (M4 MacBook, 16 GB)

- **Base rates.** These come from the [S]/[L] runs on this machine's
  platform (macOS 15.6 arm64; the provenance has no hardware field, see
  below). Median per-instance time including 300 sampled states is 0.15 s
  at n = 8, 1.1 s at n = 12 and 3.3 s at n = 20.
- **Easy cells** (structure like [S]/[L]). With the expanded-state and
  oracle checks, estimate ≈ 0.2 s, 1.5 s and 4.5 s per instance. At 2,240
  instances per size that is ≈ 14,000 s ≈ **4 h serial**, or ≈ 40–60 min
  with 6 worker processes.
- **Hard cells, which the sweep is looking for, dominate and cannot be
  estimated before the pilot.**
  - *UCS.* In [L], a UCS search that hit the 200k budget took 11–130 s.
  - *LM-cut.* An LM-cut search at budget costs several times more per
    expansion.
  - *Bound.* The labelling budget (§2) bounds a hard instance to roughly
    3 × 200k init expansions plus 2M labelling expansions, i.e. tens of
    minutes worst case.
  - *Example.* If 10% of n = 20 instances were hard, that alone would be on
    the order of 100+ h serial.
- **Plan.**
  1. A pilot of one seed per cell (336 instances, written nowhere) measures
     the real per-cell cost.
  2. n ∈ {8, 12} then runs locally in any case. Memory is not a constraint:
     ≤ 50k enumerated states and ≤ 200k open/closed states per process.
  3. n = 20 runs locally if the pilot projects ≤ 12 h with 6 workers.
     Otherwise it goes to the cluster, unchanged, with the same config and
     a commit recorded in provenance.

**Before the real run: provenance needs a hardware field.** The [S]/[L]
`provenance.json` files have `platform` and `python` but no CPU/RAM. Rule
9 and D14 §4 require hardware, so `runlog.provenance()` must record CPU
model, core count and RAM. Library versions (an open TODO there) should be
added at the same time.

### Implementation footprint (for approval; nothing is built yet)

- `src/ahg/attack_graph.py`: `cred_levels`, `coupling` and `share_pool`
  arguments, plus a docstring section for each.
- `src/ahg/search.py`: opt-in `trace=` for expanded states.
- `src/ahg/runlog.py`: hardware and library versions in provenance.
- `scripts/measure_depth_coupling.py`: reuses the measurement helpers of
  `measure_landscape.py`. Move them into one shared module rather than
  copying them, and keep `measure_landscape.py` behaving identically.
- Output: `results/landscape/depth_coupling_sweep/` via `write_run`.
- Tests:
  - the byte-identity golden hashes;
  - knob semantics (levels occupied, gates present, coupled k ∉ {src, h});
  - oracle vs search on knob instances at n ≤ 8;
  - search counts unchanged with `trace`.

## 2026-10-28 — D16: Pilot-informed amendment: internet-exposed hosts are level 0

**Status: ADOPTED, 2026-10-28, before either full run of the D15 sweep
started.** It amends the depth knob of D15 §1(a) as a *new, separately
flagged variant*. The D15 knob as registered is unchanged and is run as
registered.

### Rule (`exposed_level0=True`, only meaningful with `cred_levels` ≥ 1)

- **Exposed hosts are level 0.** Every internal host with a reach edge from
  the internet is forced to level 0.
- **Remaining hosts.** Levels are assigned only among the other internal
  hosts, the non-exposed ones, exactly as D15 does over all hosts:
  - the target is at level D;
  - one non-exposed, non-target host is forced to each level 1…D−1;
  - every other non-exposed host is drawn uniformly from {0, …, D}, the
    D15 distribution.
  - Level 0 is always occupied, since repair edges guarantee at least one
    exposed host (D10).
- **Generation failures (`KnobInfeasible`).** Each is logged and listed per
  cell, never dropped:
  - *Too few hosts:* there are fewer than D − 1 non-exposed, non-target
    hosts to occupy levels 1…D−1.
  - *Exposed target:* the target itself is internet-exposed, so it would be
    forced to level 0 and the chain could not end at it.
- **Same rng stream.** It uses D15's stream `"depth:family:seed"`. Because
  it is a different variant, its draws are not comparable host by host with
  D15's, and that is not required.

### Security grounding

In AD-style tiering, internet-facing and DMZ hosts sit outside the
credential tiers. They are exposed precisely because they are meant to be
reachable, and no tiered administrator credential is required to attack
their services. The tiers protect the internal estate behind them.

### Honesty note

- **Pilot information was used.** The amendment was made after seeing the
  D15 pilot's reachability counts: 133 of 152 unreachable D ≥ 1 instances
  had every exposed host gated.
- **No result information was used.** The amendment was made before any
  full-run result. Pilot R was 1.0–1.4 in every cell, so no outcome
  information motivated it.

### What does not change

- **The success criterion** of D15 §6 applies to both runs separately:
  R ≥ 5, the censoring rule, eligibility, and fresh-seed confirmation.
- **Coupling** (D15 §1(c)) is unchanged. Its unreachability comes from real
  dependency cycles: host k is reachable only through h, while h's exploit
  needs k. That is a structural property of the networks the knob
  describes, not an artefact of an implausible gate.

### Which run the hard-regime decision rests on

- **The amended run (D15+D16) is primary.**
- **The original D15 run** is reported in full next to it.
- **A hard regime that appears only in the original run** is reported but
  not claimed.

## 2026-10-29 — D17: Paper plan after the depth–coupling sweeps

**Status: ADOPTED, 2026-10-29, by the author, with the amendments below.**

- The research question and the wording of H1–H3 in CLAUDE.md §0 are
  unchanged. §2 below adds the thresholds and tests they are judged by.
  CLAUDE.md §0 now states the paper framing and points here.
- This version replaces the options draft committed at b57b0c8. The target is
  now a workshop paper or arXiv preprint (CLAUDE.md §0, 2026-10-29), so the
  plan is shaped as one paper with two contributions.

**Amendments made at adoption (2026-10-29, before any training or label run):**

1. **Paper framing.** Working title: *"Learned heuristics for attack-graph
   planning: what they can and cannot buy"*.
   - **Contribution 2 (learning: informedness and generalisation under
     shift) is the headline.**
   - Contribution 1 (characterisation, including h\* = h+ and the sampling
     bias) is the motivating study that sets up C2.
   - The timing result against Fast Downward is a **pre-registered
     negative** (§2, H1). It is reported prominently, in the abstract and
     in its own results subsection, not buried in a limitations paragraph.
2. **Threats to validity / reviewer questions:** §8 is rewritten as that
   subsection.
3. **Fallback order (§6):** the WL-feature (WL-GOOSE-style) baseline moves
   from optional to planned, and is kept until last because reviewers
   expect it.
4. **Replication criteria for C1 (§1, Remaining C1 work (a)):** fixed here,
   before the replication runs.
5. **Sampling scheme:** the D14 update that implements §3 is recorded as
   D19.

### Inputs (run folders)

| tag | run folder |
|---|---|
| **[F15]** | `results/landscape/depth_coupling_sweep/full/2026-10-28T131617Z-ab208e3/` |
| **[F16]** | `results/landscape/depth_coupling_sweep/full_d16/2026-10-28T142309Z-ab208e3/` (primary, D16) |
| **[B]** | `results/feasibility/inference_microbench/2026-10-29T062211Z-1627e16/` |
| **[FD]** | `results/feasibility/fd_crosscheck/2026-10-29T070649Z-41e9d1c/` |
| **[N30]** | `results/feasibility/size_shift_n30/2026-10-29T111143Z-d221bc9/` |
| **[RW]** | `docs/related_work.md` |

Per-instance sampling-bias counts are printed by
`scripts/summarize_depth_coupling.py [F15] [F16]`.

### 1. Contribution 1 (characterisation): already measured

**Claim.** On CVE-grounded attack graphs, A\* with classical admissible
heuristics expands about plan-length nodes:

- in the default schema ([S], [L]);
- under pre-registered deeper and coupled variants (D15, D16): 0 of 190 and
  0 of 192 eligible cells meet D15 §6, and pooled median R = 1.00 in every
  row ([F15], [F16]).

**Framing required by [RW].**

- Monotonic privileges make the task delete-free, so h\* = h+. Helmert &
  Domshlak (ICAPS 2009) show that LM-cut closely approximates h+. The
  near-exactness is therefore *expected*, and the paper says so.
- The contribution is the measurement and its consequences:
  1. it holds on CVE-grounded attack graphs, under deliberate depth and
     coupling, with pre-registered criteria;
  2. A\* expansions stay at about plan length (contrast Helmert & Röger,
     AAAI 2008);
  3. random-walk sampling misses where the heuristics err (below);
  4. the inference-cost bound: on these graphs, no learned heuristic of the
     benchmarked sizes can beat compiled A\* on time ([FD]).
- Exact delete-free solvers exist: hitting sets (Haslum et al. 2012), IP
  (Imai & Fukunaga 2015), incremental-LM-cut branch and bound (Pommerening &
  Helmert 2012). The paper must say why it studies A\*: learned heuristics
  are defined and compared inside A\*/GBFS, and those solvers become a
  stated baseline gap or an optional extra.

**Sampling-bias finding** (per instance, [F16], n = 20, D ≥ 2; exact sign
test):

| heuristic | expanded-state rate higher | equal | lower | sign-test p |
|---|---|---|---|---|
| LM-cut | 292 | 400 (all 0 = 0) | 150 | 1.3e-11 |
| h_max | 735 | 7 | 100 | 3.3e-120 |

- At D ≤ 1 the LM-cut difference is not significant (D = 1: 124 / 1,184 /
  116, p = 0.65). The pooled 6.5% vs 36.9% figure (`findings.md` §7.3)
  therefore comes from a minority of instances, and the paper reports the
  per-instance form.

**Remaining C1 work.**

- (a) The fresh-seed replication pre-registered as (b) H1 in the earlier
  draft: the D16 grid on seeds 100–119, D15 §6 applied unchanged. It takes
  about 70 min locally ([F16] took 66 min).

  **Replication criteria (fixed at adoption, before the run).** C1 has
  *replicated* only if all three hold on the seeds 100–119 run; otherwise
  it has *not replicated*, and `findings.md` says which part failed.
  - **(R1) No hard regime.** No eligible cell meets D15 §6 condition 1
    (median R ≥ 5 with bootstrap CI lower bound ≥ 3), with eligibility and
    censoring exactly as in D15 §6. [F16]: 0 of 192.
  - **(R2) h_max sampling bias.** In the n = 20, D ≥ 2 group, the
    h_max per-instance sign test (expanded-state h < h\* rate against the
    walk-state rate) has more "higher" than "lower" instances, with exact
    two-sided p < 0.01. [F16]: 735 / 100, p = 3.3e-120.
  - **(R3) LM-cut sampling bias.** The same test for LM-cut in the same
    group: more "higher" than "lower", p < 0.01. [F16]: 292 / 150,
    p = 1.3e-11.

  The other per-group rows (all D, D = 0, 1, …) are reported but carry no
  criterion.
- (b) The `findings.md` §7.5 limitation, that levels are independent of
  position, stays a stated limitation. No new generator variant is added
  before the deadline.

### 2. Contribution 2 (learning): the proposal's H1–H3, fixed before any training

**Thresholds and tests are fixed by adopting this entry.** Any change after
the first training run needs a new D-entry that says so.

**Statistics everywhere.**

- Per-instance paired comparisons; geometric means of per-instance ratios.
- Bootstrap 95% CIs over instances, nested over training seeds: each
  resample draws instances, then seeds.
- Wilcoxon signed-rank tests, Holm-corrected within each hypothesis.
- Effect sizes are reported next to every p.

**Baselines.**

- h0, h_max and h_sp: the admissible or classical comparators for H1.
- h_add: the inadmissible reference, reported with no threshold.
- LM-cut: the strongest admissible comparator, reported.
- Fast Downward A\*+h_max and A\*+LM-cut: the C++ timing baselines.

**H1 (efficiency).** On unseen in-distribution test instances, A\*+h_θ (GNN)
expands fewer nodes than each of A\*+h0, A\*+h_max and A\*+h_sp.

- *Threshold, for each baseline:* geometric-mean expansion ratio ≤ 0.90,
  with CI upper bound < 1 and Holm-corrected Wilcoxon p < 0.01. H1 holds
  only if it holds against all three.
- *End-to-end time, inference included (rule 7):*
  - it is measured on one machine (the M4, single process) against Python
    A\*+h_max and A\*+LM-cut and against FD A\*+h_max and A\*+LM-cut;
  - each is reported as a geometric-mean ratio with its CI;
  - a time win is claimed only if the CI upper bound is < 1.
- *Pre-registered prediction from [B] and [FD]:*
  - h_θ loses on time to both FD baselines: E\* < 1 expansion for the GNN
    64×3 against FD A\*+LM-cut;
  - it can beat Python A\*+LM-cut;
  - against Python A\*+h_max it can win only on instances where it expands
    ≤ about 5 nodes, i.e. almost never.
- *If the time result comes out as predicted,* the paper reports it as a
  finding, not a failure.

**H2 (trade-off).** The H1 effect costs a geometric-mean plan-cost ratio
against the optimum of ≤ 1.05 (CI upper bound). A CI lower bound > 1.10
falsifies "small cost".

- *Reported alongside:* the fraction of instances solved optimally, and the
  overestimation rate |{s : h_θ(s) > h\*(s)}| / |states|, with mean and max
  violation. These are reported separately on walk states and on A\* states.
- *Measured suboptimality only;* no bounded-suboptimality claim (rule 8).

**H3 (generalisation).** The H1 advantage shrinks under each shift, measured
separately with one factor changed.

- *Test:* the geometric-mean expansion ratio against h_max is higher under
  the shift than in distribution, and the bootstrap CI of the difference
  excludes 0.
- *The shifts:*
  - **Size:** train n ∈ {12, 20}; test n = 30. [N30]: reachable
    227/280 (flat 70/70, tiered3 70/70, tiered5 57/70, hub_and_spoke 30/70) instances; LM-cut never hit the budget; labels take a median
    0.111 (p90 0.365) s/state; the oracle cross-check is available only where UCS
    finishes (206/227; UCS hit the 200k budget on 21, 6 of them hub_and_spoke at D = 3). The split is feasible.
  - **Structure:** hold out hub_and_spoke. It is the topology most unlike
    the others; train on flat, tiered3 and tiered5. Its reachable instances
    at D = 3 are a selected subset ([F16] n = 20: 54/140), which is
    reported as a caveat.
  - **Vulnerability:** CVE pools split by a hash of the CVE id into
    disjoint train and test pools, so make_instance is given a pool subset
    and no generator change is needed. A second variant draws test CVEs
    from the top exploitability tercile, shifting the cost distribution.
- *Not claimed new in kind.* GNN size generalisation (GOOSE, AAAI 2024) and
  RL generalisation over unseen networks (Terranova et al., RAID 2024) exist
  [RW]. The novelty is a search heuristic with optimal-cost evaluation, with
  three separately controlled shifts, on attack graphs.

**Ablations** (≥ 3 seeds each):

- MLP on the §2 graph features (secondary tier, the proposal promise);
- walk-only labels against walk + A\* labels at equal label count;
- GNN depth and width (64×3, 128×6);
- with vs without CVSS features.

**A reviewer-proofing baseline from [RW] (planned, amendment 3):** WL
features with linear or GP regression (WL-GOOSE style; Chen, Trevizan &
Thiébaux, ICAPS 2024), on the grounds that it is cheaper than a GNN. It is
trained on the same label batches and reported against the same H1–H3
thresholds as the GNN, with 5 seeds where training is stochastic.

### 3. Training distribution and sampling scheme

**Distribution:** D15+D16 knob settings, D ∈ {2, 3}, all seven (ρ, m),
n ∈ {12, 20}, plus families as per the H3 structure split.

- *Why not the default D12 or pr_gated schemas:* h_max already expands about
  plan-length nodes there ([S], [L]), so H1 has nothing to measure.
- *Why D ≥ 2:* at D = 3, n = 20, h_max expands a median of 15 nodes against
  plan length 8 ([F16]). That is the only room the grid offers.

**Splits** are made at the topology-seed level before any state is sampled
(rule 1):

- *train:* seeds 1000–1599;
- *validation:* 1600–1699;
- *in-distribution test:* 1700–1799;
- *shift tests:* their own seed ranges, 1800 and up.

They are disjoint from the sweep seeds (0–19) and the replication seeds
(100–119).

**Sampling scheme (D14 §2 extended):** every label records its source.

- `optimal_path`;
- `rollout` (random walks);
- the new `astar` source: the states expanded by A\*+LM-cut and A\*+h_max
  from the initial state, plus their generated successors.

*Why:* the per-instance sign tests in §1 show that walk states
under-represent heuristic error. A\* evaluates h on generated successors, so
those are the states h_θ must be accurate on. Test metrics are reported per
source.

### 4. Experimental rigour

- **Seeds.**
  - *Primary GNN and MLP: 5 training seeds* (CLAUDE.md rule 9 requires ≥ 5;
    the 2026-10-29 request said ≥ 3, which would need a rule-9 change).
  - *Ablations: ≥ 3 seeds,* reported as ablations.
- **Model selection** on validation only.
- **The test splits are read exactly once,** after every model is frozen.
  - The evaluation script appends to a committed test-access log the frozen
    model manifest hash and the split.
  - A second access to the same split is refused unless a D-entry records
    why.
- **Timing.** All timing runs in a single process on the M4. HPC runs report
  expansions, costs and labels only, never time.
- **One command** regenerates every table and figure from the raw results
  (CLAUDE.md §5).

### 5. Compute plan

**Local (M4, 16 GB):**

- development and tests;
- pilots;
- the C1 replication (about 70 min);
- every timing measurement (Python and FD);
- final test evaluation of expansions, costs and timing;
- paper figures.

**BITS HPC** (group 18, SLURM, one GPU partition, at most half an RTX Pro
6000 via NVIDIA MPS):

- **Label generation at scale.** CPU-bound Python (A\*+LM-cut per state,
  cross-checked by A\*+h_max and the oracle).
  - Run as a SLURM array over instance shards on the GPU node's CPU cores,
    one instance per task, writing append-only label batches
    (`data/labels/<batch-id>/`, D14 §4).
  - *Estimate:* n = 30 takes a median of 0.111 (p90 0.365) s/state on the M4
    ([N30]). The n = 20 rate has **not been measured** and is expected to be
    lower, so the n = 30 rate is used as an upper estimate.
  - *Budget:* about 600 train instances × 300–600 states ≈ 0.2–0.4 M labels
    ≈ 6–12 CPU-hours at the n = 30 rate. That is about 1 h on 8–16 cores.
- **Multi-seed training.** The GNNs are small (fewer than 500 nodes per
  graph), so several seeds share the half-GPU slice through MPS.
  - One SLURM job per (model, seed), plus the ablation grid of about 30
    runs.
- **Never on HPC:** test-split evaluation and timing. They stay local so that
  one machine produces every timing number, and the test-access log stays
  in one place.

### 6. Week-by-week plan

Working back from a submission-ready draft and arXiv preprint in the week
of 14 December 2026: the course's week 10, and in time for MS applications.
The preprint is then revised for the primary workshop target. Today is
29 October.

| week | dates | deliverable |
|---|---|---|
| 0 | 29 Oct – 1 Nov | Adopt D17; commit §2 thresholds and split seed ranges; request an arXiv endorsement (cs.AI; needed for first submissions); HPC account and environment check |
| 1 | 2 – 6 Nov | D14 label pipeline with the `astar` source; label-check tests (rule 6); split-disjointness test; batched successor evaluation in `search.py`; C1 fresh-seed replication run |
| 2 | 9 – 13 Nov | Label generation on HPC (train, validation, all test splits); GNN, MLP and WL-baseline training code; local pilot training |
| 3 | 16 – 20 Nov | Multi-seed training on HPC (primary 5 seeds, ablations 3); validation-only model selection; freeze models |
| 4 | 23 – 27 Nov | Evaluation harness with the test-access log; in-distribution test run **once**; timing against Python and FD locally |
| 5 | 30 Nov – 4 Dec | Shift tests **once** each (size, structure, vulnerability); statistics, figures, failure analysis |
| 6 | 7 – 11 Dec | Full paper draft (C1 + C2); course report, demo, viva |
| 7 | 14 – 18 Dec | Polish; reproducibility command; **arXiv submission** |

**Fallback if the plan slips** (amendment 3; each step keeps a complete
paper; items are dropped in this order):

1. Drop the vulnerability shift.
2. Drop the structure shift.
3. Drop the extra cheap comparisons: the CVSS-feature ablation, the GNN
   128×6 width ablation and the walk-only-labels ablation. The MLP stays
   (it is the course's secondary tier and the proposal's promise).
4. If training slips past week 4, post C1 alone, with the feasibility and
   break-even results, as the arXiv v1 in week 7. The learning results then
   go to v2 and the workshop version.

The WL baseline is never dropped on its own. Reviewers will ask "why a GNN
and not WL features" ([RW]), so it goes only with step 4. The size shift is
kept to the end too: it needs no new generator code, and [N30] shows it is
feasible.

C1 is already measured, so no slip leaves the paper empty.

### 7. Venue

**Primary target: HSDIP at ICAPS 2027.**

- *Scope:* the 2026 call lists "learning heuristics" explicitly.
- *2026 terms:* long papers 9 pages and short papers 5 (AAAI style, both
  including references); deadline 14 May 2026.
- *2027 call:* not yet published (unverified).
- *ICAPS 2027 itself:* Columbia, SC, with workshops 28–29 June 2027
  (verified).
- *Effect:* the arXiv preprint goes first; the workshop version adds
  whatever lands after December.

**Backup: PRL at ICAPS 2027, or AISec 2027 at CCS.**

- *PRL 2026:* 8-page long papers, non-archival, deadline 20 May 2026.
- *AISec 2026:* 10 pages in ACM format, archival, deadline 24 July 2026.
- *Their 2027 dates* are not yet published.

**Not chosen, despite a verified near deadline: AICS at AAAI-27** (papers due
20 November 2026; 5–9 pages AAAI; non-archival). Planning and attack graphs
are not among its listed topics, and by 20 November only C1 would be ready.

### 8. Threats to validity / reviewer questions (amendment 2)

Each item becomes a paragraph of the paper's threats section, with the
answer given here.

- **"Near-exactness is expected: h\* = h+."** Privileges are monotonic, so
  every task is delete-free and its optimal cost *is* the delete-relaxation
  optimum h+. Helmert & Domshlak (ICAPS 2009) show experimentally that
  LM-cut "gives excellent approximations to h+".
  - *Answer:* C1 does not claim surprise. It claims the measurement on
    CVE-grounded attack graphs under pre-registered depth and coupling
    knobs, and its consequences: A\* expansions at about plan length, the
    per-instance sampling bias, and the inference-cost bound. The paper
    cites Helmert & Domshlak where C1 is introduced, not in related work
    only.
- **"Why A\* at all, when exact h+ solvers exist?"** Optimal delete-free
  planning has dedicated exact methods:
  - minimal-landmark hitting sets (Haslum, Slaney & Thiébaux, ICAPS 2012);
  - an integer-programming model (Imai & Fukunaga, JAIR 2015);
  - branch and bound with incremental LM-cut (Pommerening & Helmert,
    ICAPS 2012).
  - *Answer:* the question is about learned heuristics, which are defined
    and compared inside A\* and GBFS (STRIPS-HGN, GOOSE, WL-GOOSE [RW]).
    Those solvers are named as a stronger exact baseline that we do not
    run, and the paper states that this weakens any claim that A\* is the
    right tool for these tasks. It does not weaken the H1–H3 comparison,
    which is A\* against A\*.
- **Synthetic topologies.** Networks come from three generator families
  (D10), not from real enterprise networks. Structure shift (H3b) measures
  sensitivity to the family, but not distance from reality. MulVAL
  validation stays optional (CLAUDE.md §0). The topology generator and its
  parameters are published with the code.
- **The cost model is a proxy.** c(a) = 1 + 9·(1 − x_a) is an attack-effort
  proxy from the CVSS exploitability sub-score (rule 5), not a calibrated
  probability or time. "Optimal" always means optimal under this model.
  Plan-cost ratios (H2) inherit this. The vulnerability shift tests
  sensitivity to the CVSS distribution, not the validity of the proxy.
- **The time comparison.** Python heuristics run against compiled Fast
  Downward. Both are reported, and the FD loss is pre-registered (§2, H1).
- **Levels are independent of position** (`findings.md` §7.5). This is a
  stated limitation of the depth knob.
- **Full observability** of the network and its vulnerabilities is assumed,
  as in MulVAL-style attack-graph analysis. The contingent-planning view
  (Shmaryahu et al. 2018) is out of scope.
- **The label-size limit.** Training instances are capped by what the exact
  solver labels in budget (D14 §3). The size shift (n = 30) is the only
  test above it.

### Recommendation (separate from the plan; written before adoption)

**Adopt D17 as written, with 5 seeds for the primary models.**

- Week 0 has two items with lead times: the arXiv endorsement and the HPC
  environment.
- Run the C1 replication in week 1. It is the cheapest piece and makes C1
  final.
- Treat a lost time comparison against FD as a reported result. [B] and [FD]
  already predict it, and pre-registering that prediction makes it
  publishable rather than embarrassing.

## 2026-10-29 — D18: Compressed raw run data (`raw.json.gz`)

**Status: ADOPTED, 2026-10-29.** This is a storage change only. No
measurement, formulation or result changes.

**Why.**

- The D15/D16 full runs' `raw.json` files are 50.4 and 55.7 MB.
- GitHub warns above 50 MB and rejects files above 100 MB. Any larger
  future run would be unpushable.
- Gzip compresses the D15+D16 file from 58.4 MB to 1.9 MB, or 1.2 MB if
  the JSON is also written compactly.

**Rule.**

- *What is written.* `runlog.write_run` writes `raw.json.gz`: compact JSON,
  gzip with mtime = 0, so identical raw data gives identical bytes.
- *How runs are read.* Every reader goes through `runlog.load_raw(run_dir)`.
  - It reads `raw.json.gz` if present, else `raw.json`.
  - A folder holding both is an error.
- *Committed runs are untouched (rule 11).* Every run before this decision
  keeps its `raw.json` and is read unchanged through the fallback.
- *Tests.*
  - a round trip in both formats;
  - deterministic bytes;
  - the both-files error;
  - a committed pre-D18 run still loads.

## 2026-10-29 — D19: Label pipeline: splits, sampling scheme and storage (updates D14)

**Status: ADOPTED, 2026-10-29,** before any label batch exists. D14 stays as
written. Where this entry differs from it, this entry wins (§2 sampling,
§1 cross-check scope, §4 storage format). Implemented in `src/ahg/splits.py`,
`src/ahg/labels.py`, `src/ahg/dataset.py` and `scripts/make_labels.py`.

### 1. Splits (D17 §3, fixed here before any state is sampled)

One topology seed gives exactly one instance. The instance's knob cell
(variant, n, D, ρ, m) is `cells[(seed − first seed) mod |cells|]`, so cells
are balanced and the mapping needs no rng.

| split | seeds | variants | n | D | (ρ, m) | CVE pool |
|---|---|---|---|---|---|---|
| `train` | 1000–1599 | flat, tiered3, tiered5 | 12, 20 | 2, 3 | all 7 of D15 | `train` |
| `val` | 1600–1699 | same | same | same | same | `train` |
| `test_id` | 1700–1799 | same | same | same | same | `train` |
| `test_size` | 1800–1899 | same | **30** | same | same | `train` |
| `test_structure` | 1900–1999 | **hub_and_spoke** | 12, 20 | same | same | `train` |
| `test_vuln` | 2000–2099 | flat, tiered3, tiered5 | 12, 20 | same | same | **`heldout`** |
| `test_vuln_cost` | 2100–2199 | same | same | same | same | **`heldout_costly`** |

All splits use D15+D16 knobs (`exposed_level0=True`). Each test split
changes exactly one factor against `train` (CLAUDE.md §3). The seed ranges
are disjoint from each other, from the sweep seeds (0–19) and from the
replication seeds (100–119). `tests/test_splits.py` asserts this.

**CVE pools.**
- `heldout` = the CVEs with `int(sha256("cvepool:" + cve_id), 16) mod 10 < 3`
  (485 of 1,473 here); `train` = the other 988. They are disjoint by
  construction. Every service family keeps CVEs in both; the smallest are
  ssh (40 / 18) and ftp (45 / 17).
- *Expected:* the GNN sees CVSS attributes, not CVE ids, so `test_vuln`
  shifts *which* CVEs appear but barely shifts the feature distribution. The
  cost-shifted pool is the real feature shift.
- `heldout_costly` = `heldout` restricted to exploitability E ≤ 2.8, i.e.
  every exploit cost ≥ 1 + 9·(1 − 27/38) ≈ 3.6 effort units (344 CVEs;
  smallest families ftp and ssh, 11 each). **This replaces
  D17's "top exploitability tercile":** E = 3.9 is the most common score in
  6 of 8 families, so a tercile split is not defined without arbitrary
  tie-breaking. Its top would also be almost entirely E = 3.9, which makes
  every exploit cost the 1-unit floor. Excluding the mode instead shifts
  costs upwards and keeps every family populated.

**Test-access log.** Every read of a test-split batch through the loader
appends a line (UTC time, batch id, split, git commit, argv, the caller's
stated purpose) to the committed `results/test_access_log.jsonl`.
- A read without a stated purpose is refused.
- A second `evaluation` read of the same split is refused unless the caller
  names the D-entry that permits it (D17 §4).
- Generating a test batch writes it but never reads it back.

### 2. Sampling scheme (replaces D14 §2's two sources)

Per instance, in this order, from separate rng streams seeded on
`"labels:<source>:<variant>:<n>:<seed>"`:

1. **`optimal_path`:** the states along A\*+LM-cut's optimal plan from the
   initial state, the initial state included.
2. **`walk`:** D14's random rollouts (`measure.sample_states`), capped at
   `walk_cap` distinct non-goal states.
3. **`expanded_lmcut`, `expanded_hmax`:** the distinct states expanded by
   A\*+LM-cut and by A\*+h_max from the initial state.
4. **`successor`:** the distinct generated successors of those expanded
   states, subsampled to `successor_cap` if there are more. These are the
   states A\* evaluates h on (D17 §3; the per-instance sign test, D17 §1).

States are deduplicated per instance. A state reached by several sources
gets one label row, listing every source. Goal states (h\* = 0) can occur
only as successors or as the end of the optimal path. They are kept and
counted (D14 §1).

### 3. Labels and their checks (updates D14 §1)

- **Label.** h\*(s) is A\*+LM-cut's cost from s, with a per-state budget.
  States on the optimal path are labelled from the suffix of that one plan
  (a suffix of an optimal plan is optimal). A budget hit is a failure row,
  never dropped (rule 10).
- **Cross-checks** (any mismatch aborts the batch, and nothing is written):
  - the independent oracle (`src/ahg/oracle.py`) on **every** state of
    instances with n ≤ 12, and on `oracle_states` states drawn per instance
    above that. An oracle run that exceeds its pop budget is recorded as
    "not checked", never as agreement;
  - backward-induction enumeration (`measure.enumerate_exact`) on every
    state, wherever the reachable space is ≤ `enum_cap`;
  - no admissible heuristic (h_max, LM-cut) above the label.
- **Changed from D14 §1:** D14 had the oracle check every label. At n = 20,
  D = 3 the uninformed oracle is too slow from early states (UCS hit 200k
  pops on 21 of 227 instances at n = 30, [N30]). A recorded subset, plus
  enumeration where it fits, keeps the rule-6 cross-check without that
  cost.

### 4. Storage (D14 §4, made concrete)

`data/labels/<batch-id>/`, gitignored and append-only. An existing batch
directory is never overwritten.
- `<batch-id>` = `<split>-<config sha256[:8]>-<commit[:7]>[-s<k>of<K>]`.
  The shard suffix is used by the SLURM array: one batch per shard.
- `labels.jsonl.gz`: one row per (instance, state): instance index, state
  (hex), h\*, sources.
- `failures.jsonl.gz`: unreachable goals, generation failures and
  label-budget hits.
- Both files use gzip with mtime = 0 and are written in instance order, so
  the same config at the same commit gives byte-identical files.
- `manifest.json`: the D14 §4 fields. It adds a content hash (SHA-256 over
  both files) and a per-instance `task_digest`. The loader rebuilds each
  task with `make_instance` and refuses a batch whose digest or
  `cves.csv` SHA-256 does not match.
- Configs are JSON, under `configs/labels/` (stdlib only; there were no
  configs to follow).

## 2026-10-29 — D20: Larger training split (train seeds extended; val and test unchanged)

**Status: ADOPTED, 2026-10-29, before any model exists.** No model has been
trained, and no validation or test label has been read by any training
code. The only labels so far are the D19 pilot batches; they were used for
sizing.

**Why.**
- The D19 train range (seeds 1000–1599) gives about 439 labelled instances.
  27% of seeds are unreachable at D ∈ {2, 3}
  (`results/feasibility/label_pilot/2026-10-29T122326Z-8755cd5/`).
- H3 and the in-distribution claim are about *unseen topologies*. A
  heuristic trained on ~440 graphs may fit topologies, not the domain, so
  generalisation claims need more topology diversity, not more states per
  topology.
- Labels are cheap: 1.24 s per seed in one process in the pilot (unreachable
  seeds included). So a much larger train split fits well inside a ~2 h
  local budget.

**Rule.**
- `train` = seeds **1000–1599 and 10000–12399**, 3,000 seeds: 5× the D19
  range, about 2,200 labelled instances expected at the pilot's 73%.
  - The new range sits far from every other split and from the reserved
    sweep seeds. `tests/test_splits.py` checks disjointness.
  - The D19 range comes first in the seed list, so every D19 seed keeps
    its knob cell. The pilot batch still rebuilds with matching task
    digests.
  - Expected labelling time: about 3,000 × 1.24 s / 6 workers ≈ 10 min.
- *Why 5×, not 3× or more:* labelling would allow far more, but training on
  the M4 then becomes the cost. 5× is the most that keeps the D17 seed plan
  (5 seeds × primary models plus ablations) plausible locally. That is
  measured in the training pilot.
- `val`, `test_id`, `test_size`, `test_structure`, `test_vuln` and
  `test_vuln_cost` are **exactly as in D19**.
- Test-split label generation is now itself logged in the test-access log,
  with purpose `label generation`. It reads no model.

## 2026-10-29 — D21: Models, training protocol, validation harness and the search budget (fixed before training)

**Status: ADOPTED, 2026-10-29,** before any model is trained. Everything
here is used on `train` and `val` only. No test split is evaluated in this
phase.

### 1. Models (`src/ahg/learning/models.py`); every h_θ(s) ≥ 0

Every model predicts h\*(s) in effort units (D9 units / 38) through a
softplus output (or a clamp at 0 for the WL model). Search uses it × 38.

- **MLP:** the CLAUDE.md §2 graph-level features (`dataset.mlp_features`),
  standardised with train-only mean/std (D14 §5); 2 hidden layers with ReLU.
- **WL:** a WL-GOOSE-style linear model.
  - *Features:* the WL colour histogram over the fact–action graph with
    the state marked on the fact nodes (`dataset.wl_colours`, 2 rounds).
    The colour vocabulary is fitted on train only; colours unseen in train
    are dropped.
  - *Fit:* ridge regression by conjugate gradients on the sparse
    histogram. The asymmetric loss is fitted by iteratively reweighted
    least squares (expectile-style weights), 10 rounds.
  - CPU only; deterministic, so it needs no training seed.
- **GNN:** message passing over the fact–action graph.
  - *Per layer:* fact → action over preconditions, then action → fact over
    add effects, both by mean aggregation.
  - *Readout:* mean fact, mean action and mean goal fact.
  - *Inputs:* facts carry (held, is_goal); actions carry normalised cost,
    a kind one-hot and the CVSS PR one-hot (`dataset.static_graph`).
  - *Default:* 64 hidden × 3 layers.

### 2. Losses

- **MSE** on effort units.
- **Asymmetric:** the squared error multiplied by **w = 4** when
  h_θ(s) > h\*(s), so overestimating costs 4× as much as underestimating by
  the same amount. w is fixed here and is **not tuned**.

### 3. Training

- Train batches only. Early stopping on the validation value of the
  training loss, with patience 5 and at most 30 epochs. The best-val
  checkpoint is kept.
- Adam, with batch size 256 for the MLP. The GNN takes one instance's
  states per step (at most 256), so every state of a step shares one graph.
- *Seeded:* `torch.manual_seed(seed)` and instance order from
  `random.Random(f"train:{seed}")`.
- Every run goes through `runlog.write_run` to `results/training/` (tracked):
  config, commit, hardware, per-epoch train and val loss, wall time per
  epoch, and the checkpoint.

### 4. Validation harness (`src/ahg/evaluate.py`, `scripts/evaluate.py`)

The same code will later run each test split once, with
`purpose="evaluation"` through the test-access log. It has no per-split
branches.

- **Per labelled instance:** A\* from the initial state with h0, h_max,
  h_sp, h_add and LM-cut (Python) and each learned h_θ.
  - All runs share `best_first_search`, the same tie-breaking and the same
    200k expansion budget. Budget hits are counted, and the ratio uses the
    budget value.
  - Every admissible baseline's plan cost must equal the label h\*(init),
    or the run aborts.
  - The learned heuristic is called once per state, with feature
    construction and the forward pass inside the timed search (rule 7).
- **Reported, per learned model against each baseline:**
  - the geometric mean of per-instance expansion ratios, with a bootstrap
    95% CI (10,000 resamples of instances);
  - the plan-cost ratio against optimal (geometric mean and CI, plus the
    fraction solved optimally);
  - the end-to-end time ratio (geometric mean and CI);
  - overestimation on the labelled `walk` states and, separately, on the
    A\*-expanded states (`expanded_lmcut` ∪ `expanded_hmax`), plus
    successors as a third row: the rate h_θ > h\*, and the mean and max
    violation in effort units.

### 5. Hyperparameter search on validation (budget fixed here)

One seed (0), MSE loss, selection by validation MSE. Every config tried is
recorded, failures included.

| model | grid | configs |
|---|---|---|
| GNN | lr ∈ {1e-3, 3e-3} × hidden ∈ {64, 128} × layers ∈ {3, 6} | 8 |
| MLP | lr ∈ {1e-3, 3e-3} × hidden ∈ {64, 128} | 4 |
| WL | ridge λ ∈ {0.1, 1, 10} | 3 |

- **Wall-clock budget:** 3 h in total on the M4. If it runs out, the search
  stops and the configs not run are listed as not run.
- **Then the pilot:** for each model, the selected config × {MSE,
  asymmetric}, seed 0, evaluated on `val` with the harness. GNN 64×3 is
  also always reported, as the default and the D17 primary, whatever is
  selected.
- **Epoch time:** measured on CPU and on MPS for the GNN and MLP.

### D21 amendment 1 (2026-10-30, before the search was started)

The epoch timing run (`results/training/epoch_timing/2026-10-30T063831Z-c35e7cd/`)
gives about 100 s per GNN 64×3 epoch on the M4 CPU (MLP 0.3 s). At up to 30
epochs, and more for the 128- and 6-layer GNNs, the 8 GNN configs need about
6 h, twice the 3 h budget. Nothing has been trained on the full train split
yet, so two procedural details are fixed now:

- **Order.** WL, then MLP, then the GNN. Within a model, the cheapest size
  first, and both learning rates at each size before the next size: 64×3,
  128×3, 64×6, 128×6. In the original grid order, the budget would have
  cut every lr = 3e-3 GNN config, so the lr would never have been searched.
- **Hard budget.** The 3 h is checked at every epoch boundary, not only
  between configs. A config that the budget stops mid-training is recorded
  with its partial history as `stopped (budget)`, and is **not eligible for
  selection**, because it did not finish the §3 protocol. The overrun is at
  most one epoch.
- **Device: CPU.** MPS is at most 1.4× faster per GNN epoch, and its
  scatter-add is not deterministic, so seeded runs would not be exactly
  reproducible.

### D21 amendment 2 (2026-10-30): WL checkpoints are not tracked

D21 §3 tracks every checkpoint. A WL checkpoint is about 70 MB, because the
2-round WL vocabulary fitted on train has 1,884,617 colours. Four of them
would put about 280 MB into git history, and each is near GitHub's 100 MB
file limit. WL fitting is deterministic (no seed) and takes about 6 min.
So WL `model.pt` files stay local (`.gitignore`) and are identified by their
SHA-256. Rebuilding one from its tracked config must reproduce the hash.
GNN and MLP checkpoints (3.8 MB in all so far) stay tracked.

| run | model.pt SHA-256 |
|---|---|
| `results/training/search/wl-lam0.1-mse-s0/2026-10-30T064612Z-eea7a44` | `3aff6fff7541131cf9cdfec653360215e3c58442194e69899283fcdc438193a7` |
| `results/training/search/wl-lam1.0-mse-s0/2026-10-30T064803Z-eea7a44` | `42c1379373c748090915de3476b374fd75933e009115a6322eac3462fc05ee10` |
| `results/training/search/wl-lam10.0-mse-s0/2026-10-30T064947Z-eea7a44` | `3eeb81971b112a4f909b481a1f42e04eb2c740737bd7206c8c4bac6f5b2b2925` |
| `results/training/wl-lam0.1-asym-s0/2026-10-30T094750Z-eea7a44` | `edc61df5b494d9f79476758827640019da80dbeb46cace4602614cba11ee9b65` |

## 2026-10-30 — D22: One pre-registered improvement round on validation; selection on expansions; stopping rule

**Status: ADOPTED, 2026-10-30,** after the D21 pilot
(`results/evaluation/val-pilot/2026-10-30T115154Z-c4d03e4/`) and before any
D22 diagnostic or training is run. Validation only. **No test split is read
in this round.**

### 1. Why

In the pilot, every learned model expanded more nodes than h_max on
validation. The best was GNN 64×3 MSE: geometric-mean expansion ratio vs
h_max 1.14, 95% CI [0.99, 1.32]. H1 is unsupported at the pilot stage. The
pilot also shows that **validation loss does not predict search**: GNN 128×3
had the lower validation MSE (2.82 vs 3.15) and won the D21 §5 search, but it
expanded more nodes (1.19× vs 1.14× h_max). A model is used for search, so it
is selected by search effort.

### 2. Selection change (replaces D21 §5 selection)

- Models and variants are selected by the **geometric-mean validation
  expansion ratio vs h_max** (D21 §4 harness, 200k budget, budget hits
  counted at the budget).
- Training still early-stops on its own validation loss (D21 §3). Only the
  choice between trained models changes.
- Applied to the pilot, this selects GNN 64×3 MSE as the D22 base (1.14,
  the lowest ratio of the 8 pilot models).

### 3. Diagnostics (run first; cheap, local, validation)

1. **Headroom.** Per val instance, the expansions of A\* with h\* itself, against
   A\* with h_max and with LM-cut.
   - h\*(s) comes from the val labels where labelled. Otherwise it is A\*+LM-cut
     from s, the same solver the labels came from.
   - D3 tie-breaking applies.
   - Reported: the medians, the share of instances where h_max expands no
     more than h\* ("h_max already optimal-effort"), and the geometric mean of
     exp(h\*) / exp(h_max). The last is the ratio a heuristic as good as h\*
     itself would reach under D3, a practical floor for the §5 criterion.
2. **Sibling ordering.** For every labelled A\*-expanded val state, take its
   labelled successors. A\* orders siblings by c(a) + h(s′), because g(s) is
   shared, so that is the key.
   - Over sibling pairs whose c(a) + h\*(s′) differ: concordant 1, tied 0.5,
     discordant 0. The tie rate is reported separately.
   - Heuristics: h_max, LM-cut, h_add, h_sp and every learned model. It is
     compared with each model's validation MSE.
   - It becomes part of the harness, so every later evaluation reports it.
3. **Ties.** Learned h is continuous, so f-ties, and with them D3's
   lower-h rule, almost never engage. Integer-cost baselines tie often.
   - The pilot GNN and MLP models are re-run in A\* with h_θ rounded to the
     nearest integer D9 unit (a control that should change nothing), and to
     the nearest effort unit (38 D9 units), which creates ties.
   - Diagnostic only: a rounded model is a variant only if pre-registered
     here, and it is not.

The base is GNN 64×3 unless the diagnostics show that a different
*already-trained* pilot model has both a lower expansion ratio and higher
sibling-ordering accuracy. None has a lower ratio, so in practice the base
is fixed.

### 4. Variants (one seed, 0; GNN 64×3 base; lr 1e-3; D21 §3 protocol otherwise)

- **a. Residual target.** The GNN predicts r ≈ h\* − h_max in effort units.
  - h_max is an input twice: per fact, a reachable flag and the h_max cost of
    the fact, from one relaxed pass with every fact final; and as a global,
    concatenated to the readout.
  - Search uses h = h_max + max(0, r). Training is MSE on the raw r against
    h\* − h_max ≥ 0. The clamp is applied at search time only, so negative raw
    outputs still get a gradient.
  - h_max computation is inside the timed search (rule 7).
- **b. Max-combination,** at search time only, with no training:
  h = max(h_max, h_θ).
  - Applied to all 8 pilot models.
  - For the residual model it is the identity (h ≥ h_max by construction),
    so it is not run separately for that model, and the identity is
    stated in the report.
- **c. Ranking loss,** Chrestien, Edelkamp, Komenda & Pevný, NeurIPS 2023
  (arXiv:2310.19463), the A\* loss L\* (their Eq. 2 and 4, α = β = 1). It is
  implemented as written:
  - One optimal plan per train instance: A\*+LM-cut from the initial state,
    under D3 tie-breaking.
  - For each plan state s_i (i ≥ 1), the off-path set is the open list O_i
    of a search that expands exactly s_0 … s_{i−1}: every successor generated
    so far that is not on the plan. Its g is the cheapest generating path
    through expanded plan states. This includes the distance-one states
    their experiments add.
  - The loss is Σ_i Σ_{s_j ∈ O_i} log(1 + exp((g_i − g_j) + (h_i − h_j))),
    summed over pairs as in their Eq. 4, with one problem instance per
    minibatch as in their §6. Effort units; same Adam and GNN; early
    stopping on the same loss over val plans.
  - No h\* label is used: the model's scale is free.
  - Deviations, recorded as such: the GNN (not STRIPS-HGN); Adam instead
    of AdaBelief; plans from A\*+LM-cut (optimal) rather than SymBA\*/LAMA;
    the D21 early-stopping protocol.
- **d. Combination of a–c:** the residual architecture trained with the
  ranking loss, h = h_max + softplus(r) in training (a strictly positive
  residual keeps the gradient) and h_max + max(0, r) at search time. This
  already includes b, because h ≥ h_max.
- **6-layer GNN:** skipped unless budget remains (§5).

### 5. Compute budget

- **Training:** 5 h wall-clock in total on the M4 CPU, as a hard budget per
  epoch (D21 amendment 1 rule). Order: a, c, d. A run the budget stops is
  recorded and is not eligible.
- **6-layer:** after a, c and d are evaluated, if at least 2 h of the training
  budget remain, the best of {base, a, c, d} by the §2 rule is retrained at
  64×6. Otherwise it is recorded as not run.
- **Diagnostics and evaluations** are not budgeted by wall-clock. Each is one
  run of a script and is logged.

### 6. Stopping rule (fixed now)

After this round:

- If **no** variant (a, b on any pilot model, c, d, or the 6-layer if run)
  reaches a validation expansion ratio vs h_max with a **bootstrap 95% CI
  upper bound < 1**, then:
  - the best variant by §2 is frozen;
  - the D17 multi-seed plan is run with it anyway;
  - **H1 is reported as unsupported.**
- Otherwise, the best variant by §2 among those meeting the criterion is
  frozen and taken to the multi-seed plan.
- **Either way there is no further round of variants.**

A variant that meets the criterion on val has been selected on val, so its
val ratio is optimistic. The H1 claim rests only on the test splits.

### 7. Reporting

Every variant in this round is reported in the paper, including failures
and anything not run, with the same columns:
- expansion ratio vs h_max, LM-cut and h_sp (geometric mean and CI);
- plan-cost ratio;
- overestimation on walk vs A\* states;
- time vs Python LM-cut;
- sibling-ordering accuracy.

The diagnostics are reported too.

### 8. Outcome (2026-10-30, appended after the round; §1–§7 unchanged)

- Run: diagnostics; a, c, d (1.29 h); the 64×6 retrain of d (§5; 3.71 h remained), with one aborted
  ~11 min attempt, counted against the budget. Total ≈ 1.78 h of 5 h. Rows in `docs/experiment_log.md`.
- b was run on all 8 pilot models; not run on a or d, where it is the identity (§4).
- **Stopping rule (§6): met.** CI upper bounds vs h_max: a 0.892, c 0.675, d 0.665, d 64×6 0.667;
  every b ≥ 1.140.
- **Frozen by §2:** d at 64×6 (0.5946 vs 0.5951 for d at 64×3).
- No further round of variants. The multi-seed plan is not started; the choice is the author's.
- Open points, recorded and not acted on:
  1. §2 breaks a tie far inside the CIs in favour of the slower, less optimal 64×6 model.
  2. §2 selects on expansions alone. It therefore prefers the inadmissible ranking models (plan cost
     1.04–1.09, overestimation everywhere) over a (0.837, every val plan optimal).
  Any change to the frozen choice is a new decision entry, made before any test split is read.
