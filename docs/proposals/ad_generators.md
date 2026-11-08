# AD graph generators and session realism (review for the D27 scope; PROPOSAL ONLY)

**Status: review, 2026-11-08. Nothing here is adopted.**
- **Why this review.** The D27 scope needs Active Directory objects, permission edges and sessions. These are
  configuration, not CVE (`product_list_v2.md` §3), so a generator has to produce them.
- **What it covers.** For each generator: what it produces, how it creates sessions, and whether sessions ever
  end. Then the sources on how real sessions behave and how an attacker loses access.
- **Where the sources are.** All sources are stored under `data/raw/sources/2026-11-08/gen/` and listed in
  `docs/sources.md` (S20–S29 and the fetched-page register).
- **Where the trial runs were done.** Repositories were cloned into a scratch directory, one directory per tool,
  each with its own Python virtual environment. Nothing from them is in this repository.

## 1. What the papers in this line used

| paper (opened) | generator used | graph | sessions | code link in paper |
|---|---|---|---|---|
| Guo, Li, Neumann, Neumann, Nguyen, arXiv:2112.13175 (S17, full PDF now read) | DBCreator | "R2000": 2,000 computers, 5,997 nodes, 18,795 edges; edge types AdminTo, MemberOf, HasSession only ("the only three default edge types in BloodHound") | static HasSession edges from DBCreator | none (BloodHound link only) |
| Goel, Ward-Graham, Neumann, Neumann, Nguyen, Guo, *Defending Active Directory by Combining Neural Network based Dynamic Program and Evolutionary Diversity Optimisation*, arXiv:2204.03397 (S20) | DBCreator | R500 (1,493 nodes, 3,456 edges), R1000 (2,996; 8,814), R2000 (5,997; 18,795); same three edge types | static | none (BloodHound and SharpHound links only) |
| **Goel, Ahmad, Moore, Guo**, *Co-Evolutionary Defence of Active Directory Attack Graphs via GNN-Approximated Dynamic Programming*, arXiv:2505.11710 (S21). This is the D27 baseline; it resolves D27 §4's `[VERIFY]` | DBCreator | r500, r1000, r2000 with the same node and edge counts; "only the default BloodHound edge types: AdminTo, HasSession, and MemberOf". Stackelberg game, defender blocks up to k edges | static. The paper's own limitation: DBCreator graphs "do not fully capture … evolving user behaviours, dynamic access policies, and diverse edge types" | none found in the text |
| Ngo, Guo, Nguyen, *Catch Me if You Can: Effective Honeypot Placement in Dynamic AD Attack Graphs*, arXiv:2312.16820 (S22) | DBCreator (R2000, R4000) and ADSimulator (ADX05, ADX10; ADU10 and ADU100 "tuned to mimic the real AD network of University of Anonymized") | same three edge types; ADU100 has 137,207 nodes and 1,410,679 edges | **dynamic.** (a) Synthetic: each HasSession edge is ON independently with p = 0.5. (b) Real: the "AuthOrg" authentication data (§3) mapped onto ADSimulator graphs | "Code and data will be made publicly available" (no link in the text) |
| Nguyen, Falkner, Nguyen et al., *ADSynth*, DSN 2024 (S23) | ADSynth (their own) | compared with DBCreator, ADSimulator and "a University AD system" | static (§2) | `github.com/adsynthesizer/ADSynth`, now `AUCyberLab/ADSynth` |

## 2. Generators

### 2a. Comparison

| generator | objects / edges | sessions | session removal | realism evidence | runs? (one small graph tried) |
|---|---|---|---|---|---|
| **BloodHound DBCreator** (`BloodHoundAD/BloodHound-Tools`, commit 05c4d52, 2020-04-28; LGPL-3.0; repository not archived, last push 2024-06-28) | Users, Computers, Groups, OUs, GPOs, Domain. MemberOf, Contains, AdminTo, HasSession, GenericAll, WriteDacl, WriteOwner, Owns, GetChanges/GetChangesAll (DCSync), GpLink, ExecuteDCOM, CanRDP, AllowedToDelegate, ReadLAPSPassword. Parameters: node count (`setnodes`, default 500) and domain name | Each user gets `randrange(0, ceil(log10(num_nodes)))` sessions on uniformly random computers. Domain Admins get at least 1 (`DBCreator.py`, "Adding sessions") | **none:** a static snapshot | none stated. ADSynth's authors: such tools "do not follow how ADs are built in real organizations" (S23) | **No.** It installed (pinned neo4j 1.7.6 driver), but `clear_and_generate` printed "Database Connection Failed": it writes only into a running Neo4j server, and there is no Neo4j or Java on this machine |
| **ADSimulator** (`nicolas-carolo/adsimulator` v1.1.1, commit 6e15ac8, 2022-06-29; BSD-3-Clause) | DBCreator's types, plus domain trusts (TrustedBy), AddMember, CanPSRemote, AllowedToAct and ACL rights. Parameters (README): nUsers, nComputers, nGroups, nOUs, nGPOs, trusts, ACL probabilities, CanRDP/CanPSRemote/ExecuteDCOM/AllowedToDelegate percentages, enabled, unconstrained delegation, dontreqpreauth (AS-REP), hassp (SPN), passwordnotreqd, pwdneverexpires, sidhistory, OS and functional-level probabilities | Same rule as DBCreator: `generate_sessions` in `generators/computers.py`, log10 maximum, random computers, DAs ≥ 1 | **none:** static | Ngo et al. tuned its parameters to a real university AD (S22). ADSynth: it "struggles to generate networks of 100000 nodes" (S23) | **No.** Its installer writes to `~/.adsimulator`, so it was run with `HOME` set to its own scratch directory. `generate` failed with `neo4j.exceptions.ServiceUnavailable: Couldn't connect to localhost:7687`, for the same reason as DBCreator |
| **ADSynth** (`AUCyberLab/ADSynth`, commit d7019d0, 2026-09-29; BSD-3-Clause; maintained) | Classic AD: Domain, OUs (tier model), Groups, Users, Computers (PAWs, servers, workstations), GPOs, Container; MemberOf, Contains, HasSession, GenericAll, WriteOwner, WriteDacl, GenericWrite, Owns, GpLink, AdminTo, AllExtendedRights, AddMember, ExecuteDCOM, AddSelf, CanRDP, ForceChangePassword, AllowedToDelegate, ReadLAPSPassword, GetChanges/GetChangesAll, AllowedToAct, CanPSRemote, SQLAdmin; Kerberoastable users. Optional Entra ID / hybrid objects. Parameters: tiers, departments, locations, security level, `sessionsPercentages`, `priority_session_weight`, `perc_misconfig_sessions`, misconfiguration percentages | Per tier, each user gets `randint(0, ps × \|computers at its tier and above\|)` sessions (`synthesizer/sessions.py`). There are separate sets for admin users on PAWs, users on workstations and special-role users on servers. Misconfigured cross-tier sessions are a percentage of users (paper Alg. 3). Print and Server Operators get sessions on DCs with p = 0.5 | **none:** HasSession edges carry no properties (no time, no duration) in the generated output | The paper compares it with a university AD (S23). Its session parameters are best-practice proportions, not fitted to logs | **Yes, after two local fixes:** (1) `openai` is imported but missing from `requirements.txt`; (2) the output folder `generated_datasets/` must exist. With `secure_1k.json` and `generate` it produced 1,047 nodes and 5,073 edges in Neo4j-JSONL. These include 259 HasSession, 3,111 MemberOf, 34 AdminTo, 6 CanRDP, 2 CanPSRemote, 9 ExecuteDCOM and 2 GetChangesAll |
| **BadBlood** (`davidprowe/BadBlood`, commit b3c6325, 2023-06-07; GPL-3.0) | Populates a **real** AD domain with PowerShell: OU structure, users, groups, computers, OU ACL delegations, random permissions, SPNs, AS-REP (no pre-auth), SIDHistory, weak passwords, LAPS schema | **none.** No logon-session module; the only "session" in the code is a PowerShell runspace | n/a | It creates real AD objects, so a SharpHound collection over the result is real data. Sessions would come from whatever activity the lab has | **Not run:** it needs a Windows domain controller with the ActiveDirectory module |
| **GOAD**, Game of Active Directory (`Orange-Cyberdefense/GOAD`, commit 74af01e, 2026-10-24; GPL-3.0; maintained) | A fixed, hand-built vulnerable lab. GOAD: 5 VMs, 2 forests, 3 domains (also GOAD-Light, MINILAB, SCCM, NHA, DRACARYS). Real AD, so every BloodHound edge type the configuration implies | **Scripted bots:** for example `rdp_scheduler.ps1` registers a task that runs `bot_rdp.ps1` as `north\robb.stark` every minute. The `vulns/schedule` role repeats tasks at an interval and at boot | Real Windows behaviour (sessions end when the bots' logons end), but the activity is a fixed script, not a model of users | It is a real AD, but the user behaviour is scripted for pentest exercises, not measured | **Not run:** it needs a VM provider (VirtualBox, VMware, Proxmox, cloud) and Windows evaluation images |

### 2b. Other generators

ADSynthMisconfig is listed in ADSynth's README as built on ADSynth; it was not reviewed. No other maintained AD
graph generator was found in this search.

## 3. Real authentication data

| dataset | opened? | what it contains | session start and end? | access |
|---|---|---|---|---|
| **AuthOrg** (Ngo et al., S22) | paper only | Authentication events from an anonymous organisation over 102 days (24-06-2022 to 04-10-2022): 270 users, 338 computers, 14,249 sessions, 1,015 unique (user, computer) sessions, as tuples ⟨t_start, t_end, user, computer⟩ | yes | **not public** ("will be made publicly available"; no link) |
| **LANL Comprehensive, Multi-Source Cyber-Security Events** (Kent 2015, doi:10.17021/1179829; S24) | description page read; data **not downloaded** (auth.txt.gz is 7.2 GB) | 58 days; 12,425 users, 17,684 computers. `auth.txt.gz` fields: time, source user@domain, destination user@domain, source computer, destination computer, authentication type, logon type, authentication orientation, success/failure. Includes red-team events | the page defines an "authentication orientation" field, and its sample lines show `LogOn`. That it also contains LogOff is **not verified** | download link on the page |
| **LANL Unified Host and Network Data Set** (Turcotte, Kent, Hash 2018; S25) | description page read; data **not downloaded** | about 90 days of Windows host event logs from most enterprise computers, plus netflow. Events include 4624 ("An account was successfully logged on"), 4634 ("An account was logged off"), 4647 (listed on the page as "User initiated logon"), 4648 and 4672, with LogonID, LogonType and AuthenticationPackage. The page says events in a logon session "should report the same Logon ID through to the logoff event". AD servers are combined into one host, `ActiveDirectory` | **yes:** pairing 4624 with 4634 by LogonID gives session durations. LogonType is recorded; the page's sample lines show type 3, "Network". Its Table 2 of logon types was not captured in the stored text | download behind a form that asks for an email address and the intended use. Not filled in here |
| **LANL User-Computer Authentication Associations in Time** (Hagberg, Kent, Lemons, Neil 2014; S26) | description page read | 9 months, 708,304,516 successful authentications as (time, user, computer). AD servers removed | **no:** start events only | download behind the same form |

**Which generator's session model is backed by real data?** None of the five.
- DBCreator and ADSimulator draw a random count (at most log10 of the node count) of uniformly random computers.
- ADSynth draws per-tier proportions from best-practice parameters.
- All three produce a static snapshot.
- GOAD's sessions are real Windows sessions, but they come from a fixed bot script.
- The only real-data session dynamics in this line of work are Ngo et al.'s: they map private AuthOrg sessions
  onto ADSimulator graphs.
- From AuthOrg they report:
  - sessions concentrate in working hours;
  - "some normal employee's session lasts approximately 8 hours";
  - more than 63.8% of HasSession edges correlate (Pearson > 0.5) with at least one other edge;
  - new (user, computer) pairs keep appearing throughout the 102 days.

  Their own synthetic baseline (independent edges, p = 0.5) "significantly diverges from realistic session
  patterns".

**What a session-dynamics generator calibrated on real logs would need:**
1. **Session intervals from logon/logoff pairs.** For example, LANL 2017 events 4624 and 4634 joined on LogonID,
   per user and computer, separated by LogonType.
   - Which logon types leave reusable credential material on the host must be sourced. Not done here: open
     question.
2. **Fitted distributions,** not independent coin flips:
   - start times (time of day, weekday);
   - durations;
   - correlation between a user's sessions on different hosts;
   - the arrival rate of new (user, computer) pairs.
3. **A mapping from de-identified log identities to generated AD roles.** LANL gives no group memberships or
   admin roles, so which logged users are admins, and on which tier, must come from the generator. Calibrating
   admin sessions separately needs a source that labels admin accounts.
4. **The access-loss events of §4 as explicit processes:**
   - reboots (host-level);
   - ticket expiry;
   - password changes and LAPS rotation;
   - account disabling.
5. **A held-out period for validation,** as Ngo et al. did (train on sampled snapshots, test on future states).

## 4. Sourced mechanisms by which access is lost

| mechanism | source (stored, `gen/…`) | what the source says |
|---|---|---|
| **Logoff** | S27, Microsoft, *Cached and Stored Credentials Technical Overview* | Stored credentials "are directly associated with the LSASS logon sessions that have been started since the last restart and have not been closed". So credential material for a session is tied to that logon session being open |
| **Reboot** | S27 (same sentence) | Only sessions started "since the last restart" hold stored credentials. LSA secrets "that must persist after reboot" are stored encrypted on disk and survive (same page) |
| **Session timeouts** | S28a, Microsoft, *Configure Timeout and Reconnection Settings for Remote Desktop Services Sessions* (cc754272); S28b, *Interactive logon: Machine inactivity limit* | RDS "End a disconnected session": "If you specify 'Never,' the user's disconnected session is maintained for an unlimited time". There are separate active-session and idle limits. The machine inactivity limit only **locks** the session ("the user's session locks by invoking the screen saver"), which is not a logoff |
| **Kerberos ticket lifetime** | S29a, Microsoft, *Maximum lifetime for user ticket*; S29b, *… user ticket renewal* | Default 10 hours (Default Domain Policy and DC effective default); renewal 7 days; 0 means TGTs never expire. The same page warns that a disabled account "might be able to continue to access network services by using valid service tickets that were issued before their account was disabled" |
| **Account disabling, expiry, lockout** | S29c, Microsoft, [MS-KILE] §3.3.5.7.1 | When the KDC's validate-client policy is set and "the TGT is older than an implementation-specific time", the account KDC "MUST verify that the account is still in good standing (not expired, locked out, disabled …)", else KDC_ERR_CLIENT_REVOKED. The concrete Windows time is in footnote <72>, **not read**. A 20-minute figure appears in an older MS-KILE §5.1.3 seen only in search results: `[VERIFY]` |
| **Password change** | S27 | "An NT hash is valid for authentication until a user's password is changed" (pass-the-hash material stops working) |
| **Credential rotation: LAPS** | S29d, Microsoft, *Configure policy settings for Windows LAPS*; S29e, *Windows LAPS overview* | PasswordAgeDays: default 30, from 1 to 365. PostAuthenticationActions after PostAuthenticationResetDelay (default 24 h): 1 reset; 3 reset and sign out ("interactive sign-in sessions … are terminated, and SMB sessions … deleted"); 5 reset and reboot; 11 reset, sign out and terminate remaining processes. Overview: LAPS rotates "each device's local administrator password", giving "protection against pass-the-hash and lateral-traversal attacks" |
| **krbtgt reset** (forged-ticket material) | S29f, Microsoft, *AD Forest Recovery: Reset the krbtgt password* | "perform this operation twice"; "wait 10 hours between password resets", because the krbtgt password history holds 2 passwords |
| **Linux sudo credential cache** (T1548.003) | S29g, sudo project, *sudoers* manual | Time stamp: "use sudo without a password for a short period of time (5 minutes unless overridden by the timestamp_timeout option)". A separate record per terminal by default |

**Not sourced here:**
- removal on account deletion;
- Linux Kerberos ccache lifetime (krb5.conf);
- SSH session idle timeouts;
- whether network logons (type 3) leave reusable credentials.

These remain open.

## 5. What this means for the D27 model (for Devansh to decide)

- **Q-G1. Which generator.** ADSynth is the only one of the five that installs and runs here without a database
  server, and it is maintained. The DBCreator graphs (r500, r1000, r2000) are what the Goel et al. baseline used.
  - Using DBCreator would need a local Neo4j 3.5/4.x and Java.
  - So would ADSimulator.
- **Q-G2. Static or dynamic sessions.** Every generator is static.
  - If the model keeps sessions static, that is a scope assumption ("a snapshot at attack time") and must go into
    `docs/assumptions.md`.
  - If sessions are dynamic, §3 lists what calibration needs, and the only usable public data with logoffs is LANL
    2017 (behind a form).
- **Q-G3. Access loss in the planning model.** §4's mechanisms make credentials and sessions expire. They
  conflict with a monotonic (delete-free) model; whether they are in is a formulation decision (D25 §3).
