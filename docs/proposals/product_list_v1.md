# Product list v1: coverage audit and a proposed product list (PROPOSAL ONLY)

**Status: proposal, 2026-11-08. Nothing here is adopted.** No exclusion, filter or criterion follows from this
file; it only records where real-world implementations of each service are filed in NVD and how many CVEs a
wider product list would touch. Every number is produced by
`scripts/measure_product_coverage.py` → `results/cve_semantics/product_coverage/2026-11-08T120925Z-a84842d/`
(R below), from stored inputs listed in `docs/sources.md` §3–4. No NVD snapshot was fetched: NVD numbers are
count-only queries (`totalResults`), logged with query string and time in R §1.

**New error candidate (for AUDIT_4): services filed under the OS.** FAMILY_PRODUCTS queries only application CPEs
of standalone server products. The Windows implementations of SMB, RDP, DNS, HTTP (http.sys) and the directory
services are, as far as the test cases show, filed under Windows OS CPEs (`o:microsoft:windows_*`) or a
separate Microsoft application CPE, so the frozen study's families never contain them. CVE-2017-0144 (EternalBlue)
and CVE-2019-0708 (BlueKeep) are both absent from the 2026-10-21 snapshot (R §4).

## 1. Coverage audit: where each service's real-world implementation is filed

Sources: S3 (NVD API docs), S8/S9 (MSRC CVRF), S12/S13 (other vendors), NVD count queries (R §1). "UNVERIFIED"
means no per-CVE NVD check was made for that service.

| category | real-world implementation | where its CVEs are filed in NVD (CPE, part) | per-CVE component field | source |
|---|---|---|---|---|
| dns | BIND, Unbound, PowerDNS, dnsmasq | `a:isc:bind`, `a:nlnetlabs:unbound`, `a:powerdns:*`, `a:thekelleys:dnsmasq` (current) | none in NVD | snapshot, D11 |
| dns | Windows DNS Server | Windows OS CPEs `o:microsoft:windows_server_*`: UNVERIFIED per CVE | MSRC Tag "Role: DNS Server" (44 CVEs 2016–23), "Microsoft Windows DNS" (29), "Windows DNS" (5) | S8, R §2a |
| ftp | vsftpd, ProFTPD, Pure-FTPd, Serv-U, … | `a:` products in FAMILY_PRODUCTS (current) | none in NVD | snapshot |
| ftp | IIS FTP | UNVERIFIED (no MSRC tag names FTP; "Windows IIS" has 11 CVEs) | MSRC Tag "Windows IIS" | S8 |
| http | Apache httpd, nginx, Tomcat, IIS | `a:apache:http_server`, `a:nginx:nginx`, `a:f5:nginx`, `a:apache:tomcat`, `a:microsoft:internet_information_services` (93 CVEs all-time) | none in NVD | snapshot, R §1 |
| http | Windows http.sys (kernel HTTP stack) | Windows OS CPEs: UNVERIFIED per CVE | MSRC Tag "Windows HTTP.sys" (8), "HTTP.sys" (1), "Windows HTTP Protocol Stack" (2) | S8 |
| mail | Exim, Postfix, Sendmail, Dovecot, Exchange | `a:` products incl. `a:microsoft:exchange_server` (current) | MSRC Tag "Microsoft Exchange Server" (135) for Exchange | snapshot, S8 |
| rdp | FreeRDP (library + clients + servers), xrdp | `a:freerdp:freerdp`, `a:neutrinolabs:xrdp` (current) | none in NVD | snapshot, P25 |
| rdp | **Windows Remote Desktop Services** | **`o:microsoft:windows_7` etc. is the vulnerable CPE** (CVE-2019-0708: `isVulnerable` on `o:microsoft:windows_7:-:sp1` = 1); `a:microsoft:remote_desktop_services` has 0 CVEs | MSRC Tag "Windows RDP" (37), "Windows Remote Desktop" (11) | R §1, §4; S8 |
| smb | Samba | `a:samba:samba` (current) | none in NVD | snapshot |
| smb | **Windows SMB server** | **`a:microsoft:server_message_block`** (5 CVEs all-time; vulnerable for CVE-2017-0144), with Windows OS CPEs as non-vulnerable platform (`isVulnerable` on `o:microsoft:windows_7:-:sp1` = 0). MSRC has 60 SMB-tagged CVEs 2016–23, so most are filed elsewhere, presumably under Windows OS CPEs: UNVERIFIED | MSRC Tag "Windows SMB Server" (42), "Windows SMB" (18) | R §1, §4; S8 |
| sql | MySQL, MariaDB, PostgreSQL, SQL Server | `a:` products incl. `a:microsoft:sql_server` (current) | MSRC Tag "SQL Server" (43) | snapshot, S8 |
| ssh | OpenSSH, Dropbear, libssh | `a:` products (current) | none in NVD | snapshot |
| Windows built-in: WinRM | WinRM | UNVERIFIED | **no MSRC tag** containing "WinRM" or "Remote Management" in 2016–23 | S8 (tag list, R §2) |
| Windows built-in: LDAP / Kerberos / AD DS / Netlogon | AD DS | Windows Server OS CPEs: UNVERIFIED per CVE | MSRC Tags "Windows LDAP - Lightweight Directory Access Protocol" (24), "Windows Kerberos" (17), "Kerberos" (2), "Windows Active Directory" (20), "Active Directory Domain Services" (5), "Active Directory" (3), "Role: Windows Active Directory Server" (1), "Windows Netlogon" (5) | S8 |
| Windows built-in: TCP/IP stack | tcpip.sys | Windows OS CPEs: UNVERIFIED | MSRC Tag "Windows TCP/IP" (20) | S8 |
| Linux in-kernel network services | netfilter, TCP/IP, SCTP, ksmbd, NFS server … | `o:linux:linux_kernel` (19,633 CVEs all-time; 1,873 with v3 AV:N; the AV:N/PR:N/UI:N count query failed twice) | **none in NVD.** CVE Record 5 allows `programFiles`/`modules` (S12); whether the kernel CNA fills them is UNVERIFIED. Red Hat gives only a package (`kernel`) | R §1, S12, S13 |
| Edge devices | FortiOS, PAN-OS, Cisco ASA/IOS/IOS XE, Junos, Ivanti/Pulse Connect Secure, NetScaler ADC, F5 BIG-IP, SonicOS | `o:fortinet:fortios` 279, `o:paloaltonetworks:pan-os` 238, `a:cisco:adaptive_security_appliance_software` 37, `o:cisco:ios_xe` 560, `o:cisco:ios` 620, `o:juniper:junos` 794, `a:ivanti:connect_secure` 133, `a:pulsesecure:pulse_connect_secure` 57, `a:citrix:netscaler_application_delivery_controller` 34, `o:citrix:application_delivery_controller_firmware` 30, `a:f5:big-ip_local_traffic_manager` 541, `o:sonicwall:sonicos` 68 (all-time) | none in NVD; vendor advisories not checked this round | R §1 |
| OS LPE: Windows | Windows kernel, win32k, drivers | Windows OS CPEs (`o:microsoft`: 3,996 CVEs with v3 AV:L, all-time) | MSRC Threat Impact "Elevation of Privilege" with a Windows tag: 1,515 CVEs 2016–23 (C5 rule) | R §1, §2b |
| OS LPE: Linux kernel | Linux kernel | `o:linux:linux_kernel` (12,444 with v3 AV:L, all-time) | none in NVD | R §1 |
| Client-side: browsers | Chrome, Firefox, Edge, IE, Safari | `a:google:chrome` 7,599, `a:mozilla:firefox` 3,487, `a:microsoft:edge_chromium` 328, `a:microsoft:internet_explorer` 1,742, `a:apple:safari` 1,700 | MSRC Tags "Microsoft Edge (Chromium-based)" (971), "Internet Explorer" (125), "Microsoft Scripting Engine" (433), … for Microsoft; Apple component headings (S13) | R §1, §2 |
| Client-side: office / mail clients | Microsoft Office, Outlook, Thunderbird | `a:microsoft:office` 1,033, `a:microsoft:outlook` 126, `a:mozilla:thunderbird` 2,070 | MSRC Tags "Microsoft Office" (480), "Microsoft Office Outlook" (16), … | R §1, §2 |
| Client-side: PDF / plug-ins | Acrobat/Reader, Foxit, Flash | `a:adobe:acrobat_reader_dc` 1,832, `a:adobe:acrobat_dc` 1,832, `a:foxit:pdf_reader` 373, `a:adobe:flash_player` 1,084 | none in NVD | R §1 |

**Other OS vendors' per-CVE component field** (S13): Red Hat: `package_state[].package_name` and
`affected_release[].package` in per-CVE JSON (package level, e.g. `kernel`, `samba`). Apple: a component heading per
CVE on per-release HTML pages (e.g. "ImageIO"). Linux kernel CNA: none named on its process page. Cisco, Fortinet,
Palo Alto Networks, Juniper: not checked this round (UNVERIFIED).

**Caveat on the NVD counts.** `virtualMatchString` matches a CPE anywhere in the applicability statement,
vulnerable or not (S3), so these counts include CVEs where the CPE is only a running-on/with platform. They are
all-time (not 2016–2023) and overlap across CPEs.

## 2. Proposed categories (for discussion; not adopted)

| id | category | CPEs to query (NVD) | component rule assigning a CVE to a service | source of the rule |
|---|---|---|---|---|
| C1 | current service families | FAMILY_PRODUCTS (35 products) | as D11 (positive vulnerable match) | D11 |
| C2 | Windows built-in network services | `o:microsoft:windows_*`, `a:microsoft:server_message_block`, `a:microsoft:internet_information_services` | MSRC Note Type 7 (Tag) ∈ {Windows SMB Server, Windows SMB, Windows RDP, Windows Remote Desktop, Role: DNS Server, Microsoft Windows DNS, Windows DNS, Windows HTTP.sys, HTTP.sys, Windows HTTP Protocol Stack, Windows IIS, Windows LDAP - Lightweight Directory Access Protocol, Windows Kerberos, Kerberos, Windows Active Directory, Active Directory Domain Services, Active Directory, Role: Windows Active Directory Server, Windows Netlogon, Windows TCP/IP} | S8, S9 |
| C3 | Linux in-kernel network services | `o:linux:linux_kernel` | **no sourced per-CVE rule** (no component field in NVD; kernel CNA use of `programFiles` UNVERIFIED). Undecided between C3 and C5 | S3, S12, S13 |
| C4 | edge devices | the 12 CPEs in §1 | the whole product is a network-facing device; no component rule | R §1 |
| C5 | OS local privilege escalation | Windows OS CPEs; `o:linux:linux_kernel` | Windows: MSRC Threat Type 0 (Impact) = "Elevation of Privilege" and a Tag matching `^(Windows|Microsoft Windows|Win32k|Role: |Microsoft Graphics Component$)`, not C2/C6. Linux: none (see C3) | S8, S9 |
| C6 | client-side software reachable by phishing | the browser, office, mail-client and PDF CPEs in §1 | Microsoft: MSRC Tag matching `^(Internet Explorer|Microsoft Edge|Microsoft Office|Microsoft Scripting Engine|Microsoft Outlook|Microsoft Word|Microsoft Excel|Remote Desktop Client|Windows RDP Client)`; others: the product | S8 |

## 3. KEV mapping rule (used for the coverage counts)

In order: (1) the CVE is in the snapshot with a positive vulnerable FAMILY_PRODUCTS match → C1; (2) KEV vendor is
Microsoft and the CVE is in the 2016–2023 MSRC data → C2/C6/C5 by the tag rules above, else "OUT microsoft (other
tag)"; (3) the KEV (vendorProject, product) pair is in the explicit table in `scripts/measure_product_coverage.py`
(`KEV_PRODUCT_CATEGORY`) → that category; (4) other Microsoft entries → "UNRESOLVED (not in 2016–2023 MSRC data)";
(5) otherwise OUT. KEV carries vendor/product names, not CPEs (S10), so step (3) is a name match.

## 4. Counts (R; proposal only)

- **MSRC 2016–2023:** 11,228 distinct CVEs. C2 305 (129 with impact Remote Code Execution); C5 (Windows) 1,515;
  C6 (Microsoft client-side) 2,586 (1,045 RCE).
- **NVD (all-time, overlapping):** see §1 and R §1.
- **KEV (catalogVersion 2026.11.06, 1,769 entries):**
  - in current FAMILY_PRODUCTS (snapshot, positive vulnerable match, any year) 55; in the 1,473 included CVEs 21;
  - in the proposed list C1–C6: **466**, by category: C6 195, C5 87, C4 84, C1 55, C3/C5 Linux kernel 32, C2 13;
  - OUT 1,120; OUT Microsoft (other tag) 54; UNRESOLVED Microsoft (outside 2016–2023 MSRC data) 129.
- **Top 20 KEV vendor:product pairs:** R §3b (also in the session report).

## 5. Test cases (R §4)

- **CVE-2017-0144** (EternalBlue): MSRC 2017-Mar, Tag "Windows SMB Server", Impact "Remote Code Execution". NVD:
  vulnerable CPE `a:microsoft:server_message_block:1.0`; Windows 7 SP1 / Server 2016 present but **not**
  vulnerable (platform). Not under `a:samba:samba`. KEV: yes (2022-02-10, "Microsoft : SMBv1"). Not in the snapshot.
- **CVE-2019-0708** (BlueKeep): MSRC 2019-May, Tag "Windows RDP", Impact "Remote Code Execution". NVD: vulnerable
  CPE `o:microsoft:windows_7:-:sp1` (also matches `o:microsoft:windows_server_2008`); no `a:microsoft` CPE; not under
  `a:freerdp:freerdp` or `a:neutrinolabs:xrdp`. KEV: yes (2021-11-03, "Microsoft : Remote Desktop Services"). Not in
  the snapshot.
