# KEV coverage of the scope options (proposal only; nothing adopted)

KEV catalogVersion 2026.11.06: 1769 entries; 1014 have a CVE ID year 2016–2023 (the ID year, not the publication date). One category per entry, first rule wins.

## 1. KEV entries per category

| category | meaning | KEV | KEV, CVE year 2016–2023 |
|---|---|---|---|
| C1 | current FAMILY_PRODUCTS (snapshot match) | 55 | 37 |
| C2 | Windows network services (MSRC tag) | 13 | 13 |
| C3/C5-linux | Linux kernel (network vs LPE unresolved) | 32 | 14 |
| C4 | edge devices (VPN, firewall, gateway, router OS) | 238 | 139 |
| C5-win | Windows local privilege escalation (MSRC) | 172 | 89 |
| C6 | client-side (browser, office, mail client, PDF, archive) | 232 | 123 |
| WEBAPP | enterprise web / server applications not in FAMILY_PRODUCTS | 403 | 211 |
| SOHO | small-office routers and NAS | 71 | 52 |
| MOBILE | mobile OS / chipsets | 89 | 66 |
| CLOUD | cloud / Azure | 8 | 4 |
| MS-OTHER | Microsoft, other component | 78 | 49 |
| OTHER | none of the above | 378 | 217 |

Correction to product_list_v1: its C6 rule (`^Microsoft Office` tag prefix) also matched SharePoint, a server product. **3 KEV entries** were counted as C6 there; here they are WEBAPP.

## 2. Name rules (regex over "vendorProject : product", first match wins)

| category | regex |
|---|---|
| MOBILE | `^(Android|Samsung|Qualcomm|Arm|MediaTek) :|^Google : (Pixel|Android)|^Apple : (iOS|iPadOS|watchOS)` |
| CLOUD | `Azure|Kubernetes|\bAWS\b|Cloud (Services|Platform)` |
| C4 | `^(Fortinet|Palo Alto Networks|SonicWall|WatchGuard|Sophos|Check Point|Juniper|F5|Zyxel|Arista) :|^Cisco : .*(ASA|Adaptive Security|Firepower|IOS|Small Business RV|AnyConnect|Secure Firewall|SD-WAN)|^Ivanti : .*(Connect Secure|Pulse|Policy Secure)|^Pulse Secure :|^Citrix : .*(NetScaler|ADC|Gateway)` |
| SOHO | `^(D-Link|NETGEAR|TP-Link|DrayTek|MikroTik|Ubiquiti|ASUS|Synology|QNAP|Tenda|Linksys|TOTOLINK|Buffalo) :` |
| C6 | `^Google : (Chromium|Chrome)|^Mozilla :|^Adobe : .*(Acrobat|Reader|Flash)|^RARLAB :|^7-Zip :|^Foxit :|^Microsoft : (Office|Word|Excel|Outlook|Internet Explorer|Edge|PowerPoint|Publisher)|^Apple : (Safari|WebKit)` |
| WEBAPP | `^(Oracle|Atlassian|Synacor|SAP|Zoho|SolarWinds|GitLab|Jenkins|JetBrains|Roundcube|WordPress|Drupal|Sitecore|Kentico|Craft CMS|Laravel|PHP Group|Accellion|Fortra|Gladinet|PaperCut|Progress|VMware|Telerik|ConnectWise|BeyondTrust|N-able|SimpleHelp ?|Veeam|Nagios|Langflow|BerriAI|JFrog|Kaseya|IBM|Mitel|Plex|Apache|Adobe|Citrix|Ivanti|Trend Micro|Broadcom|Red Hat|Smartertools|SmarterTools) :|^Microsoft : SharePoint` |
| C5-win | `^Microsoft : (Win32k|Windows)$` |

## 3. Options

| option | categories pulled in | KEV | KEV 2016–2023 |
|---|---|---|---|
| N1 Windows/AD enterprise with DMZ | C1, C2, C4, C5-win, C6, WEBAPP | 1113 | 612 |
| N2 mixed Linux/Windows enterprise | C1, C2, C3/C5-linux, C4, C5-win, C6, WEBAPP | 1145 | 626 |
| N3 small office | C2, C5-win, C6, SOHO | 488 | 277 |
| A1 external opportunistic | C1, C4, SOHO, WEBAPP | 767 | 439 |
| A2 external targeted | C1, C2, C3/C5-linux, C4, C5-win, C6, WEBAPP | 1145 | 626 |
| A3 phished / malicious insider | C1, C2, C3/C5-linux, C5-win, C6 | 504 | 276 |
| E1 T1190 + T1133 (internet-facing) | C1, C4, SOHO, WEBAPP | 767 | 439 |
| E2 E1 + T1566 + T1189 (phishing, drive-by) | C1, C4, C6, SOHO, WEBAPP | 999 | 562 |
| E3 E2 + T1078 (valid accounts) | C1, C4, C6, SOHO, WEBAPP | 999 | 562 |
| E4 assume breach (no Initial Access) | C1, C2, C3/C5-linux, C5-win | 272 | 153 |
| S1 servers only | C1, C2, C3/C5-linux | 100 | 64 |
| S2 servers + workstations | C1, C2, C3/C5-linux, C5-win, C6 | 504 | 276 |
| S3 S2 + edge devices + enterprise web apps | C1, C2, C3/C5-linux, C4, C5-win, C6, WEBAPP | 1145 | 626 |
| S4 S3 + mobile + cloud | C1, C2, C3/C5-linux, C4, C5-win, C6, CLOUD, MOBILE, WEBAPP | 1242 | 696 |

## 4. Packages

Pool = network option ∩ asset option. Initial access = pool ∩ attacker option ∩ entry-point option (the categories a first step may use). KEV counted per set.

| package | options | pool categories | KEV in pool (2016–2023) | initial-access categories | KEV initial (2016–2023) |
|---|---|---|---|---|---|
| P1 AD enterprise, targeted external | N1 Windows/AD enterprise with DMZ / A2 external targeted / E3 E2 + T1078 (valid accounts) / S3 S2 + edge devices + enterprise web apps | C1, C2, C4, C5-win, C6, WEBAPP | 1113 (612) | C1, C4, C6, WEBAPP | 928 (510) |
| P2 internet-facing perimeter, opportunistic | N2 mixed Linux/Windows enterprise / A1 external opportunistic / E1 T1190 + T1133 (internet-facing) / S3 S2 + edge devices + enterprise web apps | C1, C2, C3/C5-linux, C4, C5-win, C6, WEBAPP | 1145 (626) | C1, C4, WEBAPP | 696 (387) |
| P3 assume breach, insider | N2 mixed Linux/Windows enterprise / A3 phished / malicious insider / E4 assume breach (no Initial Access) / S2 servers + workstations | C1, C2, C3/C5-linux, C5-win, C6 | 504 (276) | C1, C2, C3/C5-linux, C5-win | 272 (153) |

## 5. Largest uncovered (OTHER) vendor : product pairs

| vendorProject : product | KEV |
|---|---|
| Apple : Multiple Products | 55 |
| Apple : macOS | 6 |
| GIGABYTE : Multiple Products | 4 |
| Cisco : Identity Services Engine | 3 |
| Dassault Systèmes : DELMIA Apriso | 3 |
| Meta Platforms : WhatsApp | 3 |
| Rails : Ruby on Rails | 3 |
| TeleMessage : TM SGNL | 3 |
| Qlik : Sense | 3 |
| ImageMagick : ImageMagick | 3 |
| Veritas : Backup Exec Agent | 3 |
| DotNetNuke (DNN) : DotNetNuke (DNN) | 3 |
| SaltStack : Salt | 3 |
| Ahsay : AhsayCBS | 2 |
| Cisco : Secure Email Gateway | 2 |
| Zammad GmbH : Zammad | 2 |
| WSO2 : Multiple Products | 2 |
| TrueConf : Server | 2 |
| Metabase : Metabase | 2 |
| Cisco : Unified Communications Manager | 2 |
| LiteSpeed : cPanel Plugin | 2 |
| Sangoma : FreePBX | 2 |
| OSGeo : GeoServer | 2 |
| OpenPLC : ScadaBR | 2 |
| CWP : Control Web Panel | 2 |

