# Product list v2 for the D27 scope (PROPOSAL ONLY, for Devansh to decide)

**Status: proposal, 2026-11-08. Nothing here is adopted.**

**Scope (D27).**
- Assume breach and post-compromise movement in a mixed Linux/Windows enterprise network (N2).
- The goal is Domain Admin (G1).
- Everything inside the scope must be modelled completely.

This list replaces the family-based list (`product_list_v1.md`) for that scope. It starts from attack steps, not
from the old service families.

**Sources.**
- **S19: MITRE ATT&CK Enterprise v20.1.**
  - The STIX bundle `enterprise-attack.json`, plus the tactic pages TA0004 Privilege Escalation, TA0006
    Credential Access, TA0008 Lateral Movement and TA0007 Discovery (`docs/sources.md`).
  - Each technique below is cited by its ID. Its page is `https://attack.mitre.org/techniques/<ID with / for .>`.
  - Technique descriptions and procedure examples were read from the stored bundle.
- **S8:** MSRC CVRF.
- **S10:** CISA KEV.
- **P1–P35:** the old product roles.

**Counts.**
- From `scripts/measure_scope2_kev.py`, run `results/cve_semantics/scope2_kev/2026-11-08T151315Z-04ea8c9/` (R2 below).
- KEV figures are "x (y)":
  - x counts all 1,769 entries of catalogVersion 2026.11.06;
  - y counts the 1,014 entries whose CVE ID year is 2016–2023.
- Each KEV entry has exactly one category: the first rule that fires (R2 §3).

## 1. In-scope attack steps, from ATT&CK

These are techniques in TA0004, TA0006, TA0008 and TA0007 whose platforms include Windows or Linux (S19), and
that act on hosts or Active Directory. Only three steps have CVEs as their source: **ST1–ST3**. All others are
**configuration, not CVE** (§3).

| step | ATT&CK techniques (tactic) | what the step does in the model | where its CVEs live |
|---|---|---|---|
| **ST1 exploit a remote service** | T1210 Exploitation of Remote Services (LM) | code execution on a reachable host through a vulnerable network service | Windows network services: MSRC tags (W-SVC). Linux services: CPEs (L-SVC). Linux kernel network stack: CPE plus AV:N/A (L-KERNEL). Server applications, if those host roles exist (SRC-APP, MS-APP, OLD-APP) |
| **ST2 local privilege escalation** | T1068 Exploitation for Privilege Escalation (PE); T1548.001 Setuid and Setgid, T1548.003 Sudo and Sudo Caching (PE, Linux) | user → SYSTEM/root on a host already held | Windows: MSRC Impact "Elevation of Privilege" on a Windows component (W-LPE). Linux: kernel with AV:L (L-KERNEL); setuid/sudo/polkit/loader (L-LPE) |
| **ST3 exploit for credentials or authentication** | T1212 Exploitation for Credential Access (CA); T1558 Steal or Forge Kerberos Tickets and T1649 Steal or Forge Authentication Certificates, where a CVE is the means (e.g. MS14-068, named in T1212) | obtain credentials or forge authentication through a vulnerability in an authentication service | MSRC tags Kerberos, Netlogon, NTLM, LSA, AD, AD CS (in W-SVC) |
| ST4 log on with credentials | T1021 Remote Services: .001 RDP, .002 SMB/Windows Admin Shares, .003 DCOM, .004 SSH, .005 VNC, .006 WinRM (LM); T1078.002 Domain Accounts, T1078.003 Local Accounts (PE) | use held credentials on a host that accepts them | configuration, not CVE |
| ST5 reuse authentication material | T1550.002 Pass the Hash, T1550.003 Pass the Ticket (LM) | as ST4, with a hash or ticket | configuration, not CVE |
| ST6 harvest credentials from a held host | T1003.001 LSASS Memory, .002 SAM, .004 LSA Secrets, .005 Cached Domain Credentials, .008 /etc/passwd and /etc/shadow; T1552.001 Credentials in Files, .004 Private Keys; T1555 Credentials from Password Stores (CA) | admin/root on a host → credentials of users with sessions or stored secrets there | configuration, not CVE (needs sessions and stored secrets) |
| ST7 domain credential attacks | T1003.006 DCSync, T1003.003 NTDS (CA); T1558.003 Kerberoasting, .004 AS-REP Roasting, .001 Golden Ticket, .002 Silver Ticket (CA); T1552.006 Group Policy Preferences (CA); T1110.002 Password Cracking (CA) | domain rights or readable domain data → more credentials | configuration, not CVE (AD rights, SPNs, account flags, password strength) |
| ST8 AD permission abuse | T1098 Account Manipulation incl. .007 Additional Local or Domain Groups (PE); T1484.001 Group Policy Modification (PE); T1649 for AD CS template misconfiguration (CA) | an ACL right over an AD object → control of that object | configuration, not CVE (AD permission edges) |
| ST9 hijack a live session | T1563.001 SSH Hijacking, T1563.002 RDP Hijacking (LM); T1134.001 Token Impersonation/Theft (PE) | take over another user's existing session or token on a held host | configuration, not CVE (sessions) |
| ST10 coerce or relay authentication | T1187 Forced Authentication; T1557.001 Name Resolution Poisoning and SMB Relay (CA) | capture or relay another account's authentication | configuration, not CVE (protocol settings such as SMB signing and LLMNR). Some coercion paths are CVEs: open question Q6 |
| ST11 user-executed content | T1534 Internal Spearphishing, T1080 Taint Shared Content (LM) | a user on another host opens attacker content | the user action is configuration, not CVE. Client exploits are CVEs (CLIENT) |
| ST12 deployment tools | T1072 Software Deployment Tools (LM) | control of a management server → code execution on its managed hosts | configuration, not CVE. The management products' own CVEs fall under ST1 (SRC-APP) |
| ST13 discovery | TA0007: T1087.002 Domain Account, T1069.002 Domain Groups, T1482 Domain Trust Discovery, T1018 Remote System Discovery, T1046 Network Service Discovery, T1135 Network Share Discovery, T1615 Group Policy Discovery, T1033 System Owner/User Discovery | learn the facts the other steps need | configuration, not CVE. Whether discovery is an action or the model assumes full observability is open (Q1) |

**Evidence that ST1 is CVE-driven, from T1210's 26 procedure examples (R2 §5).**
- **SMB:** EternalBlue/EternalRomance (MS17-010, CVE-2017-0144).
- **Netlogon:** ZeroLogon (CVE-2020-1472).

(The full list is in R2 §5. No per-service tally was computed.)
- **Print Spooler:** MS10-061.
- **Windows Server Service RPC:** MS08-067.
- **RDP:** BlueKeep (CVE-2019-0708), and "RDP".
- **Other:** JBoss and Jenkins servers (Empire).

**ST2's 44 examples (R2 §5).**
- Windows kernel and Win32k CVEs.
- Vulnerable third-party drivers ("bring your own vulnerable driver"; Q4).
- Internal JIRA, GitLab and Confluence (LAPSUS$).
- ESXi, Windows containers and runc (Q5).

## 2. Categories

A category is in only if a step in §1 needs it. **"Conditional"** means a step needs it only if the generator
gives hosts that role (Q2). Conditional categories are counted, but not in the "in" total.

| category | status | steps | source of CVEs (CPEs or tags) | rule that assigns a CVE to a service or host role | KEV (R2 §1) | open questions |
|---|---|---|---|---|---|---|
| **W-SVC** Windows network and domain services | in | ST1, ST3 | MSRC Note Type 7 tag in W_SVC_TAGS (R2 §3, 36 tags). These are the v1 C2 set (SMB, RDP, DNS, HTTP.sys/IIS, LDAP, Kerberos, AD, Netlogon, TCP/IP), plus Print Spooler and Server Service/RPC (T1210 examples), NTLM, LSA/LSASS, SAM/LSAD, AD CS (T1212, T1558, T1649, T1557.001) and DCOM (T1021.003). Windows OS CPEs (`o:microsoft:windows*`) give only the platform | Service = the tag. Host role: any Windows host runs SMB/RPC. DC-only tags (Kerberos KDC, Netlogon, AD DS, LDAP, AD CS, DNS Server role) apply only to DCs or CA servers. Impact "Remote Code Execution" → ST1. Credential/authentication impacts on the auth tags → ST3. MSRC 2016–2023: 482 CVEs (192 RCE, 106 EoP; R2 §2) | **24 (23)** | Q3: which impacts on which tags count as ST3; whether DoS/Info Disclosure CVEs are actions at all; Windows Message Queuing (40 MSRC CVEs) and NFS tags are not in the set (not named by a sourced technique) |
| **W-LPE** Windows local privilege escalation | in | ST2 | MSRC Threat Type 0 Impact "Elevation of Privilege" with a tag matching `^(Windows\|Microsoft Windows\|Win32k\|Role: \|Microsoft Graphics Component$)`, not W-SVC/VIRT/CLIENT. Outside MSRC 2016–2023: KEV name `Microsoft : (Win32k\|Windows)` or KEV vulnerabilityName "Privilege Escalation" | Applies to every Windows host whose OS version the CVE lists (NVD Windows CPEs). MSRC 2016–2023: 1,428 CVEs | **172 (85)** | Q3: whether EoP always means user → SYSTEM (some are sandbox or AppContainer escapes); Q4: third-party drivers (BYOVD) have no MSRC tag |
| **L-KERNEL** Linux kernel | in | ST2 (AV:L), ST1 (AV:N/A) | `o:linux:linux_kernel` | NVD CVSS v3 AV:L → ST2 on any Linux host with an affected kernel. AV:N or AV:A → ST1 (kernel network stack). AV:P → out | **32 (14)** | **The AV split of these 32 KEV entries is not in stored data** (KEV has no CVSS; they are outside the old snapshot). It needs NVD records (Q7). No per-CVE component field (S12, S13), so "network stack vs other" rests on AV alone. AV:L does not by itself mean privilege gain (D26 E2): an impact rule is needed |
| **L-LPE** Linux userland privilege boundaries | in | ST2 (T1068, T1548.001, T1548.003) | CPEs for sudo, polkit, glibc (the `ld.so` loader), libuser, ABRT (exact CPE names `[VERIFY]` against the NVD CPE dictionary) | AV:L and the binary is setuid or root-run on the host (sudo and polkit by distribution default) | **7 (4)** | Q7 as for L-KERNEL. Which setuid binaries are on a generated Linux host (distribution defaults need a source) |
| **L-SVC** Linux remote-access and file-sharing services | in | ST1 (T1210), ST4 (T1021.002, .004, .005 via these services) | old products P27 `samba:samba`, P33 `dropbear_ssh_project:dropbear_ssh`, P34 `libssh:libssh`, P35 `openbsd:openssh`, P26 `neutrinolabs:xrdp`; P25 `freerdp:freerdp` only for its server components; VNC servers (CPEs `[VERIFY]`) | D11 positive vulnerable match, plus AV:N/A, on a host running the service. Samba also as AD DC (T1003.006 cites Samba DRSUAPI) | **1 (1)** (Samba) | P25: client vs server components need a per-CVE rule (D26 Amendment 2: 13 client-only, 7 server-only, 21 both, 48 neither). P34 libssh is client and server (multi). OpenSSH has no KEV entry: KEV is a weak signal here |
| **CLIENT** client software opened by a user | in | ST11 (T1534, T1080) | MSRC client tags (v1 C6 rule, SharePoint excluded); `a:microsoft:office`, `a:microsoft:outlook`, browsers, PDF readers, archivers (v1 §1 CPEs) | On workstations (and servers where users log on) with the product installed. Applies only after a user action (ST11) | **233 (123)** | Q8: all 21 T1534/T1080 procedure examples use macros, executables, LNK files or infected files that the user runs, with no client CVE. So the CVE is an optional variant of ST11, and the user action is configuration. MSRC 2016–2023: 2,346 CVEs, 870 with no impact |
| **SRC-APP** internal server applications named in ATT&CK examples | conditional | ST1 (T1210: JBoss, Jenkins), ST2 (T1068: JIRA, GitLab, Confluence), ST3 (T1212: vCenter), ST12 (T1072: SCCM) | KEV names (R2 §3); CPEs per product `[VERIFY]` | On hosts given that role | **41 (29)** | Q2: does the generator have these server roles? |
| **MS-APP** Exchange, SQL Server, SharePoint | conditional | ST1 | MSRC tags `Microsoft Exchange Server`, `SQL Server`, `Microsoft Office SharePoint`; P22 `microsoft:exchange_server`, P29 `microsoft:sql_server` | On hosts given that role | **35 (22)** | Q2. No sourced ATT&CK lateral-movement example names Exchange. Its AD privileges (a configuration edge) need a source before they are modelled |
| **OLD-APP** old roles dns, ftp, http, mail, sql (other than above) | conditional | ST1 only if the role exists | P1–P24, P28, P30–P32 CPEs (D11 matching) | As in the frozen study, per role | **27 (13)** | Q2. T1210 names none of these products. They are in only if the author gives internal servers these roles |
| **VIRT** hypervisors and containers | conditional | ST2 (T1068: ESXi, Windows containers, runc); T1611 Escape to Host | MSRC tags Hyper-V and Windows Container; KEV names ESXi, VMware Tools, Docker | Only if hosts are modelled as VMs or containers | **11 (5)** | Q5: whether the host model includes virtualisation. T1611's 5 examples are configuration (privileged containers, hostPath mounts) except BOtB/runc |

**Totals (R2 §1):**
- **in: 469 (250)**;
- conditional: 114 (69);
- Microsoft with no rule: 72 (48);
- out: 1,114 (647).

The largest out groups are Apple "Multiple Products" (55), Zimbra (16), ColdFusion (16), Cisco IOS/IOS XE (14),
PAN-OS (13) and Samsung mobile (13). They are perimeter, mobile or non-enterprise-host products and so lie
outside D27.

## 3. In scope, configuration, not CVE (generated, not fetched)

The generator has to produce these. No CVE source applies to any of them:
- **AD objects and permission edges:** users, groups, computers, OUs, GPOs, CA templates; MemberOf, AdminTo,
  GenericAll/GenericWrite/WriteDacl/WriteOwner, ForceChangePassword, AddMember, DCSync rights (GetChanges/
  GetChangesAll), delegation, AD CS enrolment rights (ST7, ST8; BloodHound edge vocabulary, S16).
- **Credentials:**
  - passwords, hashes and tickets per account;
  - password reuse;
  - service-principal names (Kerberoastable accounts) and accounts without pre-authentication (AS-REP);
  - GPP passwords;
  - stored secrets and SSH private keys (ST5–ST7).
- **Sessions:** which accounts are logged on where, and with which credential material in memory (ST6, ST9).
  Whether sessions are static or change over time is the subject of `docs/proposals/ad_generators.md`.
- **Local administrator rights and remote-logon rights:** RDP, WinRM, DCOM, SSH authorized_keys and sudoers
  (ST4, ST2 via T1548.003).
- **Protocol settings:** SMB signing, LLMNR/NBT-NS, NTLM allowed (ST10).
- **Network reachability:** which hosts reach which services. In TA0008 every lateral step needs it.
- **User behaviour:** who opens shared or mailed content (ST11).
- **Management relationships:** which hosts a deployment server manages (ST12).

## 4. ATT&CK techniques in these tactics that are left out, with the reason

- **Identity-provider and cloud only:** T1556.007 Hybrid Identity, T1606.002 SAML Tokens, T1098.005 Device
  Registration, T1621 MFA Request Generation. N2 is on-premises, and scope_v1 S4 (cloud) was not chosen.
- **Physical or proximity:** T1091 Replication Through Removable Media, T1016.002 Wi-Fi Discovery.
- **Persistence-type privilege escalation that needs the privilege it grants, or that only changes integrity
  level:** most of T1547, T1546, T1543 and T1053 on a host already held as admin, plus T1548.002 Bypass UAC.
  - These are left out only where the attacker already has the privilege.
  - Where they are a misconfiguration (for example, a service binary writable by users), they are ST2
    configuration and must be generated: open question Q9.
- **Defence-evasion checks listed under Discovery** (T1497 Virtualization/Sandbox Evasion, T1622 Debugger
  Evasion): no effect on the attacker's privileges.
- **Network-level interception other than ST10** (T1557.002 ARP Cache Poisoning, T1557.003 DHCP Spoofing, T1040
  Network Sniffing): these need an on-link position. They stay in scope as configuration only if the network
  model has link-level segments (Q1).

## 5. The old 35 products (P1–P35)

- **Kept (needed by a step):**
  - P27 samba;
  - P33 dropbear;
  - P34 libssh;
  - P35 openssh;
  - P26 xrdp;
  - P25 freerdp (server components only, if a per-CVE rule can be sourced).
- **Conditional (only if the host role exists):**
  - P22 exchange_server and P29 sql_server (MS-APP);
  - P18 IIS (in W-SVC through the HTTP.sys/IIS tags when on Windows);
  - all of dns P1–P5, ftp P6–P14, http P15–P17 and P19, mail P20, P21, P23 and P24, sql P28 and P30–P32 (OLD-APP).
- **Dropped:** none outright. No product is in unless a role puts it in.

KEV entries matching an old product in the snapshot number 55: OLD-APP 27, MS-APP 20, other categories 8 (R2 §1).

## 6. Open questions (for Devansh)

- **Q1.** Is discovery (ST13) an action with a cost, or does the model assume full observability? Are link-level
  segments modelled (T1557.002, T1040)? Both go to `docs/assumptions.md`.
- **Q2.** Which server roles does the generator place inside? This decides SRC-APP, MS-APP and OLD-APP.
- **Q3.** An impact rule for each category:
  - which MSRC impacts and CWE/CVSS impact fields make a CVE an ST1, ST2 or ST3 action;
  - whether DoS and information-disclosure CVEs are actions at all (D26 E2).
- **Q4.** Third-party vulnerable drivers (T1068 examples): they have no MSRC tag. Is there a sourced driver list?
- **Q5.** Are hosts VMs or containers (VIRT, T1611)?
- **Q6.** Coercion and relay (ST10): which CVEs, if any, sit behind it (for example, MSRC NTLM or LSA tags)?
- **Q7.** CVSS vectors for the Linux KEV entries and for any new Linux product. There are three options:
  - NVD count-only queries per CVE;
  - Red Hat or kernel CNA data;
  - a new NVD snapshot (an author decision).
- **Q8.** ST11: is the user action modelled as a probability or a cost? Is CLIENT kept, given that every sourced
  procedure example is user execution without a CVE?
- **Q9.** Local misconfiguration privilege escalation (writable service binaries, unquoted paths, scheduled tasks,
  sudoers entries): which ones does the generator produce, and from what source?
