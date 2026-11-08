# Scope v1: options for the revised model's scope (PROPOSAL ONLY, for Devansh to decide)

**Status: proposal, 2026-11-08. Nothing here is adopted.** It lays out options per scope dimension and three
coherent packages. The choice, and any D-entry, is Devansh's.

**Sources** are the S-rows of `docs/sources.md`:
- S8 MSRC CVRF;
- S10 CISA KEV;
- S14 MITRE ATT&CK TA0001;
- S15 MulVAL (Ou et al. 2005);
- S16 BloodHound documentation;
- S17 Guo et al., arXiv:2112.13175 (abstract only);
- S18 NASim.

**Counts:**
- KEV coverage comes from `scripts/measure_scope_kev.py` → `results/cve_semantics/scope_kev/2026-11-08T122323Z-74ab443/` (K below).
- MSRC/NVD counts come from `results/cve_semantics/product_coverage/2026-11-08T120925Z-a84842d/` (R below).

**Product categories** are those of `docs/proposals/product_list_v1.md`, plus four more: WEBAPP (enterprise
web/server applications outside FAMILY_PRODUCTS), SOHO (small-office routers and NAS), MOBILE and CLOUD.

**How to read the KEV numbers:**
- **One category per entry.** Each KEV entry gets exactly one category, by the first matching rule. The rules are explicit regexes over KEV's vendor and product names (K §2), because KEV has no CPEs.
- **Format "x (y)".** x is all 1,769 entries of catalogVersion 2026.11.06; y counts only the 1,014 whose CVE ID year is 2016–2023.
- **Option coverage.** An option's coverage is the number of entries in its categories.
- **Unmatched entries.** 378 entries (217 in 2016–2023) match no category ("OTHER"). The largest group is "Apple : Multiple Products" (55); K §5 lists the rest.

**Where the frozen study sits.** It is roughly: servers only, an external attacker, initial access by remote
exploit of a server service, and the goal of code execution on one target host. In option terms that is close
to S1, A1, E1 and G3, and its CVE pool is C1 only. KEV entries: 55 (37).

**Correction to product_list_v1.** Its C6 tag rule (prefix `Microsoft Office`) also matched SharePoint, a
server product: 3 KEV entries (K §1). K counts SharePoint as WEBAPP.

## 1. Network type

| option | sources supporting it as realistic | categories pulled in | KEV | new action types | build and data work |
|---|---|---|---|---|---|
| **N1 Windows/AD enterprise with a DMZ** | S16: BloodHound's edges model AD domains (users, groups, sessions, ACLs). S17: AD attack graphs reach "one destination node" (Domain Admin). S8: 305 MSRC CVEs (2016–23) on Windows network services (SMB, RDP, DNS Server, LDAP, Kerberos, AD, Netlogon, http.sys, IIS, TCP/IP); 129 are RCE. S10: "Microsoft : Windows" is KEV's largest pair (173). | C1, C2, C4, C5-win, C6, WEBAPP | 1,113 (612) | Windows LPE; credential use (hash/ticket reuse, sessions); AD permission edges (GenericAll, DCSync, …); lateral movement over legitimate services (CanRDP, CanPSRemote, ExecuteDCOM) | AD object generator (users, groups, computers, sessions, ACLs). DMZ/internal/tier topology. MSRC tag join for C2/C5. A product list beyond FAMILY_PRODUCTS, plus a fresh NVD snapshot (decision needed). |
| **N2 mixed Linux/Windows enterprise** | N1's sources. S15: MulVAL's rules are OS-agnostic (networkService, clientProgram, local exploit, NFS). The Linux kernel has 32 KEV entries (14 in 2016–23). | N1 + C3/C5-linux | 1,145 (626) | N1's, plus Linux LPE and Linux-specific trust (NFS exports, SSH keys) | N1's, plus Linux hosts. **Linux kernel CVEs have no per-CVE component field** (R §1), so kernel network-vs-LPE classification is unresolved. |
| **N3 small office** | S10: router/NAS vendors (D-Link 26, QNAP 11, NETGEAR 8, TP-Link 6, DrayTek 5, …) have 71 KEV entries. S14: T1190, T1133. No attack-graph source in hand models SOHO networks specifically. | C2, C5-win, C6, SOHO | 488 (277) | Device exploitation (router/NAS gives a network position); phishing; Windows LPE | Small topology (one router, NAS, few workstations). SOHO CPEs (firmware `o:`/`h:` parts). Graphs may be too small to be hard (pilot needed). |

## 2. Attacker

| option | sources | categories it can use for the first step | KEV | new action types | build and data work |
|---|---|---|---|---|---|
| **A1 external opportunistic** | S14 T1190 and T1133. S10 criterion "reliable evidence … actively exploited in the wild". KEV's internet-facing categories: C4 238 and WEBAPP 403 entries. | C1, C4, WEBAPP, SOHO | 767 (439) | Exploit of internet-facing service or device only | Smallest change from the frozen study: an internet node plus exposed services. Needs "exposed" flags per service. |
| **A2 external targeted** | S14 T1566 Phishing ("spearphishing … targeted"), T1189. S15: MulVAL's client-program rule needs only a malicious attacker. | A1 + C6 (and later steps from the pool) | 1,145 (626) | Phishing / user execution (UI:R client exploits); credential theft and use | Workstations with client software, users and mailboxes; a "user acts" action with cost or probability (needs a cost-model decision). |
| **A3 phished user or malicious insider** | S17: the entry node "is chosen by nature", i.e. many entry nodes inside. S14 T1078 Valid Accounts. S16: paths start from a compromised user. | starts inside: C1, C2, C3/C5-linux, C5-win, C6 | 504 (276) | Start state = a user's account on a workstation; LPE; credential use; lateral movement | Initial state is a set of facts on a workstation (the frozen study's single-init assumption changes, AUDIT_3 §3). No external entry modelling. |

## 3. Entry points (MITRE ATT&CK TA0001, S14: 11 techniques)

TA0001's 11 techniques are T1659 Content Injection, T1189 Drive-by Compromise, T1190 Exploit Public-Facing
Application, T1133 External Remote Services, T1200 Hardware Additions, T1566 Phishing, T1091 Replication Through
Removable Media, T1195 Supply Chain Compromise, T1199 Trusted Relationship, T1078 Valid Accounts and T1669 Wi-Fi
Networks. T1200, T1091 and T1669 are physical or proximity techniques, and T1195, T1199 and T1659 are not tied
to a CVE in a target's own product. None of the options below covers those six. Keeping them out is a scope
choice, not a sourced fact about how often they are used.

| option | techniques | categories (initial access) | KEV | new action types | build and data work |
|---|---|---|---|---|---|
| **E1 internet-facing** | T1190, T1133 | C1, C4, WEBAPP, SOHO | 767 (439) | Exploit public-facing service; use of a remote service (VPN) with valid credentials | Exposure flags; an edge-device node type |
| **E2 E1 + user-driven** | + T1566, T1189 | + C6 | 999 (562) | + phishing / drive-by (client exploit with user interaction) | Client software per workstation; a user-interaction action |
| **E3 E2 + valid accounts** | + T1078 | same CVE categories as E2 (**T1078 adds no CVEs**) | 999 (562) | + log in with stolen or bought credentials | Credential facts (accounts, password reuse) in the generator; a sourced prior on credential availability (none found yet) |
| **E4 assume breach** | none (start inside) | C1, C2, C3/C5-linux, C5-win | 272 (153) | none for entry; starts on an internal host | Simplest: choose the start host(s); no exposure modelling |

## 4. Assets in scope

| option | sources | categories | KEV | new action types | build and data work |
|---|---|---|---|---|---|
| **S1 servers only** (the frozen study's class) | S15: networkService rule; NASim (S18): hosts with services | C1, C2, C3/C5-linux | 100 (64) | (as now, plus Windows services from C2) | MSRC join for Windows services; Linux kernel component unresolved |
| **S2 servers + workstations** | S15: clientProgram rule; S16: sessions on workstations (HasSession) | + C5-win, C6 | 504 (276) | LPE; client exploits; credential harvesting from sessions | Workstation hosts, users, sessions, client software |
| **S3 S2 + edge devices + enterprise web apps** | S10: C4 238, WEBAPP 403 KEV entries (the two largest categories); S14 T1133 names VPNs and Citrix | + C4, WEBAPP | 1,145 (626) | Device foothold (network position); web-app exploit on a server | Edge node type in topology; large product list (WEBAPP alone spans ~50 vendors in K §2); fresh NVD queries |
| **S4 S3 + mobile + cloud** | S10: MOBILE 89, CLOUD 8 KEV entries; S16 has Azure (AZ*) edges | + MOBILE, CLOUD | 1,242 (696) | Mobile device compromise; cloud identity edges | Cloud identity model (Entra/Azure) is a different graph (S16 AZ* edges); mobile has few network-reachable services. Largest build cost for the fewest KEV entries (+97). |

## 5. Attacker goal

Goals do not change the CVE pool; the KEV column is therefore "—". They change the facts and actions needed.

| option | sources | categories it makes central | KEV | new action types | build and data work |
|---|---|---|---|---|---|
| **G1 Domain Admin** | S16 (paths to high-value AD groups); S17 ("one destination node", DA) | C2 (AD/Kerberos/LDAP/Netlogon tags), C5-win | — | Credential use; AD permission edges; DCSync-style privilege acquisition | AD object generator; goal fact = DA principal compromised. Most AD-path steps are configuration edges, not CVEs (S16). The CVE share of paths may be small; that needs measuring. |
| **G2 a named data asset** | S15: `dataBind(data, host, path)` and the policy check over reachable data accesses | none specific; needs C/I impact semantics (D26 E2) | — | Data access (read/write) separate from code execution; file-access actions | Data facts and placement; CVE impact semantics (code-exec vs data-read) must be decided (the CVE-semantics measurement shows the rules disagree, K's sibling run e7d95aa §5). |
| **G3 a host class** (e.g. any internal database server; any host with value) | S18 NASim: "compromise every host with a non-zero value"; the frozen study's single target is a special case | none specific | — | as for the chosen assets | Smallest change; a goal set instead of one target (AUDIT_3 §2, single-goal assumption) |

## 6. Packages (one option per dimension)

**Pool** = network option ∩ asset option. **Initial access** = pool ∩ attacker ∩ entry points: the categories a
first step may use. Both are counted from KEV (K §4).

| | **P1 AD enterprise, targeted external** | **P2 internet-facing perimeter, opportunistic** | **P3 assume breach, insider** |
|---|---|---|---|
| options | N1 / A2 / E3 / S3 / G1 | N2 / A1 / E1 / S3 / G3 | N2 / A3 / E4 / S2 / G1 or G2 |
| CVE pool categories | C1, C2, C4, C5-win, C6, WEBAPP | C1, C2, C3/C5-linux, C4, C5-win, C6, WEBAPP | C1, C2, C3/C5-linux, C5-win, C6 |
| KEV in pool | 1,113 (612) | 1,145 (626) | 504 (276) |
| initial-access categories | C1, C4, C6, WEBAPP | C1, C4, WEBAPP | C1, C2, C3/C5-linux, C5-win (starts inside) |
| KEV usable for initial access | 928 (510) | 696 (387) | 272 (153) |
| new action types | phishing/user execution, valid-account login, LPE, credential use, AD permission edges | exploit of edge device / web app, then internal exploits and LPE | LPE, credential use, lateral movement; AD edges if G1, data access if G2 |
| main sources | S16, S17, S14 (T1566, T1078), S8 | S14 (T1190, T1133), S10 (C4 and WEBAPP are KEV's largest categories), S18 | S17 (entry chosen by nature), S16, S15 |
| build and data work | **largest:** AD generator, workstations, users, sessions, client software, edge devices, web apps, MSRC join, wider NVD product list | **large:** edge-device and web-app product lists, exposure flags, Linux and Windows hosts; no AD objects needed for G3 | **medium:** workstations and users, LPE and credential actions, start state; no external entry or edge devices |
| what is still unresolved | credential-availability priors; whether CVEs or config edges dominate DA paths | WEBAPP/C4 naming rules are name matches (K §2); Linux kernel component | Linux kernel component; G2 needs data-impact semantics |
| distance from the frozen study | far | moderate (same attacker shape, wider products and hosts) | moderate (inside start, new action types) |
