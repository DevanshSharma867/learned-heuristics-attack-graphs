# Product coverage counts for product_list_v1 (proposal only; nothing adopted)

Inputs are stored files only (no network in this run); SHA-256s are in raw.json.gz.

## 1. NVD CVE API 2.0 count-only queries

`totalResults` only; no record was stored. `virtualMatchString` matches a CPE anywhere in a CVE's applicability statement, vulnerable or not (the API documentation says `isVulnerable` cannot be combined with it), so these counts include 'running on/with' platform matches. Counts are all-time with `noRejected` (not limited to 2016–2023: date ranges are capped at 120 days per query). Counts for different CPEs overlap and must not be added.

| label | totalResults | time (UTC) | query |
|---|---|---|---|
| T1 CVE-2017-0144 exists | 1 | 2026-11-08T11:47:46+00:00 | `cveId=CVE-2017-0144&resultsPerPage=1` |
| T1 CVE-2017-0144 x o:microsoft (any MS OS) | 1 | 2026-11-08T11:47:56+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:o:microsoft&resultsPerPage=1` |
| T1 CVE-2017-0144 x o:microsoft:windows_7 | 1 | 2026-11-08T11:48:04+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:o:microsoft:windows_7&resultsPerPage=1` |
| T1 CVE-2017-0144 x o:microsoft:windows_server_2016 | 1 | 2026-11-08T11:48:12+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:o:microsoft:windows_server_2016&resultsPerPage=1` |
| T1 CVE-2017-0144 x a:microsoft (any MS app) | 1 | 2026-11-08T11:48:21+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:a:microsoft&resultsPerPage=1` |
| T1 CVE-2017-0144 x a:samba:samba | 0 | 2026-11-08T11:48:29+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:a:samba:samba&resultsPerPage=1` |
| T2 CVE-2019-0708 exists | 1 | 2026-11-08T11:48:37+00:00 | `cveId=CVE-2019-0708&resultsPerPage=1` |
| T2 CVE-2019-0708 x o:microsoft (any MS OS) | 1 | 2026-11-08T11:48:46+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:o:microsoft&resultsPerPage=1` |
| T2 CVE-2019-0708 x o:microsoft:windows_7 | 1 | 2026-11-08T11:48:54+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:o:microsoft:windows_7&resultsPerPage=1` |
| T2 CVE-2019-0708 x o:microsoft:windows_server_2008 | 1 | 2026-11-08T11:49:03+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:o:microsoft:windows_server_2008&resultsPerPage=1` |
| T2 CVE-2019-0708 x a:microsoft (any MS app) | 0 | 2026-11-08T11:49:11+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:a:microsoft&resultsPerPage=1` |
| T2 CVE-2019-0708 x a:freerdp:freerdp | 0 | 2026-11-08T11:49:19+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:a:freerdp:freerdp&resultsPerPage=1` |
| T2 CVE-2019-0708 x a:neutrinolabs:xrdp | 0 | 2026-11-08T11:49:27+00:00 | `cveId=CVE-2019-0708&virtualMatchString=cpe:2.3:a:neutrinolabs:xrdp&resultsPerPage=1` |
| T1 CVE-2017-0144 x a:microsoft:server_message_block | 1 | 2026-11-08T11:49:39+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:a:microsoft:server_message_block&resultsPerPage=1` |
| T1 CVE-2017-0144 x a:microsoft:server_message_block:1.0 | 1 | 2026-11-08T11:49:47+00:00 | `cveId=CVE-2017-0144&virtualMatchString=cpe:2.3:a:microsoft:server_message_block:1.0&resultsPerPage=1` |
| T1 isVulnerable a:microsoft:server_message_block:1.0 | 1 | 2026-11-08T11:50:11+00:00 | `cveId=CVE-2017-0144&cpeName=cpe:2.3:a:microsoft:server_message_block:1.0:*:*:*:*:*:*:*&isVulnerable&resultsPerPage=1` |
| T1 isVulnerable o:microsoft:windows_7:-:sp1 | 0 | 2026-11-08T11:50:39+00:00 | `cveId=CVE-2017-0144&cpeName=cpe:2.3:o:microsoft:windows_7:-:sp1:*:*:*:*:*:*&isVulnerable&resultsPerPage=1` |
| T2 isVulnerable o:microsoft:windows_7:-:sp1 | 1 | 2026-11-08T11:50:47+00:00 | `cveId=CVE-2019-0708&cpeName=cpe:2.3:o:microsoft:windows_7:-:sp1:*:*:*:*:*:*&isVulnerable&resultsPerPage=1` |
| ALL noRejected | 401957 | 2026-11-08T11:50:56+00:00 | `noRejected&resultsPerPage=1` |
| WIN-OS o:microsoft | 21874 | 2026-11-08T11:51:07+00:00 | `virtualMatchString=cpe:2.3:o:microsoft&noRejected&resultsPerPage=1` |
| WIN-OS o:microsoft AV:N/PR:N/UI:N | 1785 | 2026-11-08T11:51:19+00:00 | `virtualMatchString=cpe:2.3:o:microsoft&cvssV3Metrics=AV:N/PR:N/UI:N&noRejected&resultsPerPage=1` |
| WIN-OS o:microsoft AV:L | 3996 | 2026-11-08T11:51:32+00:00 | `virtualMatchString=cpe:2.3:o:microsoft&cvssV3Metrics=AV:L&noRejected&resultsPerPage=1` |
| WIN-SMB a:microsoft:server_message_block | 5 | 2026-11-08T11:51:40+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:server_message_block&noRejected&resultsPerPage=1` |
| WIN-RDS a:microsoft:remote_desktop_services | 0 | 2026-11-08T11:51:48+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:remote_desktop_services&noRejected&resultsPerPage=1` |
| WIN-IIS a:microsoft:internet_information_services | 93 | 2026-11-08T11:51:55+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:internet_information_services&noRejected&resultsPerPage=1` |
| APP a:microsoft | 8400 | 2026-11-08T11:52:05+00:00 | `virtualMatchString=cpe:2.3:a:microsoft&noRejected&resultsPerPage=1` |
| LINUX o:linux:linux_kernel | 19633 | 2026-11-08T11:52:20+00:00 | `virtualMatchString=cpe:2.3:o:linux:linux_kernel&noRejected&resultsPerPage=1` |
| LINUX o:linux:linux_kernel AV:N | 1873 | 2026-11-08T11:52:59+00:00 | `virtualMatchString=cpe:2.3:o:linux:linux_kernel&cvssV3Metrics=AV:N&noRejected&resultsPerPage=1` |
| LINUX o:linux:linux_kernel AV:N/PR:N/UI:N | FAILED (HTTP 000) | 2026-11-08T11:54:06+00:00 | `virtualMatchString=cpe:2.3:o:linux:linux_kernel&cvssV3Metrics=AV:N/PR:N/UI:N&noRejected&resultsPerPage=1` |
| LINUX o:linux:linux_kernel AV:L | 12444 | 2026-11-08T11:54:24+00:00 | `virtualMatchString=cpe:2.3:o:linux:linux_kernel&cvssV3Metrics=AV:L&noRejected&resultsPerPage=1` |
| EDGE o:fortinet:fortios | 279 | 2026-11-08T11:54:32+00:00 | `virtualMatchString=cpe:2.3:o:fortinet:fortios&noRejected&resultsPerPage=1` |
| EDGE o:paloaltonetworks:pan-os | 238 | 2026-11-08T11:54:40+00:00 | `virtualMatchString=cpe:2.3:o:paloaltonetworks:pan-os&noRejected&resultsPerPage=1` |
| EDGE a:cisco:adaptive_security_appliance_software | 37 | 2026-11-08T11:54:47+00:00 | `virtualMatchString=cpe:2.3:a:cisco:adaptive_security_appliance_software&noRejected&resultsPerPage=1` |
| EDGE o:cisco:ios_xe | 560 | 2026-11-08T11:54:56+00:00 | `virtualMatchString=cpe:2.3:o:cisco:ios_xe&noRejected&resultsPerPage=1` |
| EDGE o:cisco:ios | 620 | 2026-11-08T11:55:07+00:00 | `virtualMatchString=cpe:2.3:o:cisco:ios&noRejected&resultsPerPage=1` |
| EDGE o:juniper:junos | 794 | 2026-11-08T11:55:18+00:00 | `virtualMatchString=cpe:2.3:o:juniper:junos&noRejected&resultsPerPage=1` |
| EDGE a:ivanti:connect_secure | 133 | 2026-11-08T11:55:26+00:00 | `virtualMatchString=cpe:2.3:a:ivanti:connect_secure&noRejected&resultsPerPage=1` |
| EDGE a:pulsesecure:pulse_connect_secure | 57 | 2026-11-08T11:55:33+00:00 | `virtualMatchString=cpe:2.3:a:pulsesecure:pulse_connect_secure&noRejected&resultsPerPage=1` |
| EDGE a:citrix:netscaler_application_delivery_controller | 34 | 2026-11-08T11:55:41+00:00 | `virtualMatchString=cpe:2.3:a:citrix:netscaler_application_delivery_controller&noRejected&resultsPerPage=1` |
| EDGE o:citrix:application_delivery_controller_firmware | 30 | 2026-11-08T11:55:49+00:00 | `virtualMatchString=cpe:2.3:o:citrix:application_delivery_controller_firmware&noRejected&resultsPerPage=1` |
| EDGE a:f5:big-ip_local_traffic_manager | 541 | 2026-11-08T11:55:57+00:00 | `virtualMatchString=cpe:2.3:a:f5:big-ip_local_traffic_manager&noRejected&resultsPerPage=1` |
| EDGE o:sonicwall:sonicos | 68 | 2026-11-08T11:56:05+00:00 | `virtualMatchString=cpe:2.3:o:sonicwall:sonicos&noRejected&resultsPerPage=1` |
| CLIENT a:google:chrome | 7599 | 2026-11-08T11:56:14+00:00 | `virtualMatchString=cpe:2.3:a:google:chrome&noRejected&resultsPerPage=1` |
| CLIENT a:mozilla:firefox | 3487 | 2026-11-08T11:56:23+00:00 | `virtualMatchString=cpe:2.3:a:mozilla:firefox&noRejected&resultsPerPage=1` |
| CLIENT a:mozilla:thunderbird | 2070 | 2026-11-08T11:56:32+00:00 | `virtualMatchString=cpe:2.3:a:mozilla:thunderbird&noRejected&resultsPerPage=1` |
| CLIENT a:microsoft:edge_chromium | 328 | 2026-11-08T11:56:39+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:edge_chromium&noRejected&resultsPerPage=1` |
| CLIENT a:microsoft:internet_explorer | 1742 | 2026-11-08T11:56:47+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:internet_explorer&noRejected&resultsPerPage=1` |
| CLIENT a:apple:safari | 1700 | 2026-11-08T11:56:56+00:00 | `virtualMatchString=cpe:2.3:a:apple:safari&noRejected&resultsPerPage=1` |
| CLIENT a:microsoft:office | 1033 | 2026-11-08T11:57:23+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:office&noRejected&resultsPerPage=1` |
| CLIENT a:microsoft:outlook | 126 | 2026-11-08T11:57:31+00:00 | `virtualMatchString=cpe:2.3:a:microsoft:outlook&noRejected&resultsPerPage=1` |
| CLIENT a:adobe:acrobat_reader_dc | 1832 | 2026-11-08T11:57:39+00:00 | `virtualMatchString=cpe:2.3:a:adobe:acrobat_reader_dc&noRejected&resultsPerPage=1` |
| CLIENT a:adobe:acrobat_dc | 1832 | 2026-11-08T11:57:47+00:00 | `virtualMatchString=cpe:2.3:a:adobe:acrobat_dc&noRejected&resultsPerPage=1` |
| CLIENT a:foxit:pdf_reader | 373 | 2026-11-08T11:57:55+00:00 | `virtualMatchString=cpe:2.3:a:foxit:pdf_reader&noRejected&resultsPerPage=1` |
| CLIENT a:adobe:flash_player | 1084 | 2026-11-08T11:58:03+00:00 | `virtualMatchString=cpe:2.3:a:adobe:flash_player&noRejected&resultsPerPage=1` |
| LINUX o:linux:linux_kernel AV:N/PR:N/UI:N (retry) | FAILED (HTTP 000) | 2026-11-08T11:59:21+00:00 | `virtualMatchString=cpe:2.3:o:linux:linux_kernel&cvssV3Metrics=AV:N/PR:N/UI:N&noRejected&resultsPerPage=1` |
| T1 isVulnerable o:microsoft:windows_server_2016:- | 0 | 2026-11-08T11:59:29+00:00 | `cveId=CVE-2017-0144&cpeName=cpe:2.3:o:microsoft:windows_server_2016:-:*:*:*:*:*:*:*&isVulnerable&resultsPerPage=1` |

## 2. MSRC Security Update Guide (CVRF), 2016–2023: CVEs per component tag × impact

11228 distinct CVEs across 95 monthly documents (MSRC has no document for 2016-Feb or 2016-Mar; February 2018 is `2018-FEB`, plus `2017-May-B`). A CVE counts once per tag and once per impact it carries.

### 2a. Proposed C2 service tags

| tag | CVEs | Remote Code Execution | Elevation of Privilege | Information Disclosure | Denial of Service | Spoofing | Security Feature Bypass | (no impact) |
|---|---|---|---|---|---|---|---|---|
| Role: DNS Server | 44 | 37 | 0 | 1 | 5 | 1 | 0 | 0 |
| Windows SMB Server | 42 | 16 | 4 | 15 | 8 | 0 | 0 | 0 |
| Windows RDP | 37 | 18 | 1 | 9 | 9 | 0 | 0 | 0 |
| Microsoft Windows DNS | 29 | 12 | 2 | 6 | 6 | 2 | 1 | 0 |
| Windows LDAP - Lightweight Directory Access Protocol | 24 | 22 | 0 | 0 | 2 | 0 | 0 | 0 |
| Windows Active Directory | 20 | 2 | 7 | 3 | 3 | 3 | 1 | 0 |
| Windows TCP/IP | 20 | 4 | 1 | 3 | 11 | 0 | 1 | 0 |
| Windows SMB | 18 | 6 | 2 | 5 | 3 | 0 | 2 | 0 |
| Windows Kerberos | 17 | 1 | 12 | 0 | 2 | 0 | 2 | 0 |
| Windows IIS | 11 | 1 | 4 | 0 | 4 | 0 | 0 | 0 |
| Windows Remote Desktop | 11 | 2 | 0 | 3 | 1 | 0 | 5 | 0 |
| Windows HTTP.sys | 8 | 1 | 3 | 1 | 3 | 0 | 0 | 0 |
| Windows DNS | 5 | 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| Windows Netlogon | 5 | 1 | 3 | 1 | 0 | 0 | 0 | 0 |
| Active Directory Domain Services | 5 | 2 | 2 | 1 | 0 | 0 | 0 | 0 |
| Active Directory | 3 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |
| Windows HTTP Protocol Stack | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Kerberos | 2 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| HTTP.sys | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Role: Windows Active Directory Server | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

### 2b. MSRC CVEs per proposed category (distinct CVEs)

| category | CVEs | of which Remote Code Execution |
|---|---|---|
| C2 Windows network services (tag in 2a) | 305 | 129 |
| C5 Windows LPE (impact EoP, a Windows tag, not C2/C6) | 1515 | — |
| C6 Microsoft client-side (IE, Edge, Office, Scripting Engine, RDP client) | 2346 | 977 |

Top 40 tags overall (CVEs): Mariner 3524, Microsoft Edge (Chromium-based) 971, Microsoft Windows 696, Microsoft Office 480, Microsoft Scripting Engine 433, Microsoft Graphics Component 413, Windows Kernel 337, Microsoft Office SharePoint 240, Microsoft Exchange Server 135, Microsoft Edge 134, Internet Explorer 125, Microsoft Windows Codecs Library 110, Windows Hyper-V 109, Microsoft JET Database Engine 92, Visual Studio 91, Microsoft Browsers 88, Microsoft Dynamics 80, Azure Site Recovery 80, Windows Kernel-Mode Drivers 77, Windows Print Spooler Components 62, Microsoft Office Excel 57, Microsoft Edge (HTML-based) 54, .NET Framework 50, Windows Remote Procedure Call Runtime 49, Windows Installer 48, Role: Windows Hyper-V 47, Windows Media 44, Role: DNS Server 44, SQL Server 43, Adobe Flash Player 42, Windows SMB Server 42, Windows Message Queuing 40, Windows Win32K 39, Visual Studio Code 38, Windows RDP 37, Windows Common Log File System Driver 36, Windows Shell 34, Windows Update Stack 31, Microsoft Windows DNS 29, Azure 29

## 3. KEV coverage

CISA KEV catalog version 2026.11.06 (released 2026-11-06T19:44:45.1797Z), 1769 entries.

| KEV entries | n |
|---|---|
| in current FAMILY_PRODUCTS (snapshot CVE with a positive vulnerable family-product match, any year) | 55 |
| in the 1,473 included CVEs | 21 |
| in the proposed list (C1–C6, rules in product_list_v1.md §3) | 463 |

### 3a. KEV entries by assigned category

| category | n |
|---|---|
| OUT | 1120 |
| C6 client | 192 |
| UNRESOLVED microsoft (not in 2016–2023 MSRC data) | 129 |
| C5 windows LPE | 87 |
| C4 edge | 84 |
| OUT microsoft (other MSRC tag) | 57 |
| C1 current FAMILY_PRODUCTS | 55 |
| C3/C5 linux_kernel (network vs LPE unresolved) | 32 |
| C2 windows network service | 13 |

### 3b. The 20 KEV vendor:product pairs with the most entries

| KEV vendorProject : product | entries | in proposed list? | categories |
|---|---|---|---|
| Microsoft : Windows | 173 | partial (62 of 173 in) | UNRESOLVED microsoft (not in 2016–2023 MSRC data) 80; C5 windows LPE 58; OUT microsoft (other MSRC tag) 31; C2 windows network service 3; C6 client 1 |
| Apple : Multiple Products | 55 | out | OUT 55 |
| Google : Chromium V8 | 41 | in | C6 client 41 |
| Microsoft : Internet Explorer | 36 | in | C6 client 36 |
| Adobe : Flash Player | 33 | in | C6 client 33 |
| Linux : Kernel | 32 | in | C3/C5 linux_kernel (network vs LPE unresolved) 32 |
| Microsoft : Office | 29 | in | C6 client 28; C1 current FAMILY_PRODUCTS 1 |
| Microsoft : Win32k | 25 | partial (20 of 25 in) | C5 windows LPE 20; UNRESOLVED microsoft (not in 2016–2023 MSRC data) 5 |
| Microsoft : Exchange Server | 17 | in | C1 current FAMILY_PRODUCTS 17 |
| Synacor : Zimbra Collaboration Suite (ZCS) | 16 | out | OUT 16 |
| Adobe : ColdFusion | 16 | out | OUT 16 |
| Cisco : IOS and IOS XE Software | 14 | in | C4 edge 14 |
| Palo Alto Networks : PAN-OS | 13 | in | C4 edge 13 |
| Adobe : Acrobat and Reader | 13 | in | C6 client 13 |
| Samsung : Mobile Devices | 13 | out | OUT 13 |
| Oracle : WebLogic Server | 12 | out | OUT 12 |
| Apple : iOS, iPadOS, and macOS | 11 | out | OUT 11 |
| Microsoft : SharePoint | 10 | out | UNRESOLVED microsoft (not in 2016–2023 MSRC data) 9; OUT microsoft (other MSRC tag) 1 |
| Qualcomm : Multiple Chipsets | 10 | out | OUT 10 |
| SAP : NetWeaver | 10 | out | OUT 10 |

## 4. Test cases

### CVE-2017-0144

- MSRC tags: ['Windows SMB Server']; impacts: ['Remote Code Execution']; document(s): ['cvrf_2017-Mar.json']
- KEV: yes, added 2022-02-10, Microsoft : SMBv1
- In the 2026-10-21 snapshot (current FAMILY_PRODUCTS): no

| NVD count query | totalResults |
|---|---|
| T1 CVE-2017-0144 exists | 1 |
| T1 CVE-2017-0144 x o:microsoft (any MS OS) | 1 |
| T1 CVE-2017-0144 x o:microsoft:windows_7 | 1 |
| T1 CVE-2017-0144 x o:microsoft:windows_server_2016 | 1 |
| T1 CVE-2017-0144 x a:microsoft (any MS app) | 1 |
| T1 CVE-2017-0144 x a:samba:samba | 0 |
| T1 CVE-2017-0144 x a:microsoft:server_message_block | 1 |
| T1 CVE-2017-0144 x a:microsoft:server_message_block:1.0 | 1 |
| T1 isVulnerable a:microsoft:server_message_block:1.0 | 1 |
| T1 isVulnerable o:microsoft:windows_7:-:sp1 | 0 |
| T1 isVulnerable o:microsoft:windows_server_2016:- | 0 |

### CVE-2019-0708

- MSRC tags: ['Windows RDP']; impacts: ['Remote Code Execution']; document(s): ['cvrf_2019-May.json']
- KEV: yes, added 2021-11-03, Microsoft : Remote Desktop Services
- In the 2026-10-21 snapshot (current FAMILY_PRODUCTS): no

| NVD count query | totalResults |
|---|---|
| T2 CVE-2019-0708 exists | 1 |
| T2 CVE-2019-0708 x o:microsoft (any MS OS) | 1 |
| T2 CVE-2019-0708 x o:microsoft:windows_7 | 1 |
| T2 CVE-2019-0708 x o:microsoft:windows_server_2008 | 1 |
| T2 CVE-2019-0708 x a:microsoft (any MS app) | 0 |
| T2 CVE-2019-0708 x a:freerdp:freerdp | 0 |
| T2 CVE-2019-0708 x a:neutrinolabs:xrdp | 0 |
| T2 isVulnerable o:microsoft:windows_7:-:sp1 | 1 |

