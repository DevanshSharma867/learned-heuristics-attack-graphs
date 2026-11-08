# KEV and MSRC counts for product_list_v2 (D27 scope; proposal only)

KEV catalogVersion 2026.11.06: 1769 entries; 1014 have a CVE ID year 2016–2023. One category per entry, first rule wins (MSRC tag rules for Microsoft CVEs in the 2016–2023 MSRC data, then the name rules of §3).

## 1. KEV entries per category

| category | meaning | status | KEV | KEV, CVE year 2016–2023 |
|---|---|---|---|---|
| W-SVC | Windows network and domain services (SMB, RDP, RPC, Print Spooler, DNS, LDAP, Kerberos, Netlogon, NTLM, LSA, AD, AD CS, DCOM) | in | 24 | 23 |
| W-LPE | Windows local privilege escalation (MSRC EoP on a Windows component) | in | 172 | 85 |
| L-KERNEL | Linux kernel (LPE if AV:L; network if AV:N/A) | in | 32 | 14 |
| L-LPE | Linux userland privilege boundaries (sudo, polkit, glibc loader, libuser, ABRT) | in | 7 | 4 |
| L-SVC | Linux remote-access and file-sharing services (SSH, Samba, xrdp, VNC) | in | 1 | 1 |
| CLIENT | client software opened by a user (office, mail, browser, PDF, archive) | in | 233 | 123 |
| SRC-APP | internal server applications named in ATT&CK lateral-movement / PE / credential-access examples (JBoss, Jenkins, Jira, Confluence, GitLab, vCenter, Configuration Manager) | conditional | 41 | 29 |
| MS-APP | Microsoft server applications (Exchange, SQL Server, SharePoint) | conditional | 35 | 22 |
| OLD-APP | old FAMILY_PRODUCTS server roles other than SSH/SMB/RDP (dns, ftp, http, mail, sql) | conditional | 27 | 13 |
| VIRT | hypervisors and containers (Hyper-V, ESXi, Docker/runc) | conditional | 11 | 5 |
| MS-OTHER | Microsoft, no rule above | out | 72 | 48 |
| OUT | outside the D27 scope or no rule | out | 1114 | 647 |

- **In** (status in): 469 (250).
- **Conditional** (host roles undecided): 114 (69).
- KEV entries matching an old FAMILY_PRODUCTS product in the snapshot: 55; by v2 category: {'OLD-APP': 27, 'MS-APP': 20, 'MS-OTHER': 2, 'OUT': 3, 'L-SVC': 1, 'CLIENT': 1, 'W-SVC': 1}.

## 2. MSRC 2016–2023 CVEs per Microsoft category (same tag rules), by impact

| category | CVEs | Remote Code Execution | Elevation of Privilege | Information Disclosure | Security Feature Bypass | Spoofing | Denial of Service |
|---|---|---|---|---|---|---|---|
| W-SVC | 482 | 192 | 106 | 63 | 21 | 13 | 81 |
| MS-APP | 418 | 146 | 60 | 51 | 7 | 137 | 7 |
| VIRT | 168 | 49 | 26 | 29 | 6 | 0 | 59 |
| CLIENT | 2346 | 977 | 134 | 190 | 92 | 66 | 6 |
| W-LPE | 1428 | 1 | 1428 | 1 | 1 | 0 | 9 |

## 3. Rules

W_SVC_TAGS (MSRC Note Type 7):

`Active Directory`, `Active Directory Domain Services`, `HTTP.sys`, `Kerberos`, `Local Security Authority Subsystem Service`, `Microsoft Local Security Authority Server (lsasrv)`, `Microsoft RPC`, `Microsoft Windows DNS`, `Role: Active Directory Certificate Services; Active Directory Domain Services`, `Role: DNS Server`, `Role: Windows Active Directory Server`, `SAM and LSAD Remote Protocols`, `Windows Active Directory`, `Windows Active Directory Certificate Services`, `Windows DCOM Server`, `Windows DNS`, `Windows HTTP Protocol Stack`, `Windows HTTP.sys`, `Windows IIS`, `Windows Kerberos`, `Windows LDAP - Lightweight Directory Access Protocol`, `Windows Local Security Authority`, `Windows Local Security Authority (LSA)`, `Windows Local Security Authority Subsystem Service (LSASS)`, `Windows NTLM`, `Windows Netlogon`, `Windows Print Spooler Components`, `Windows RDP`, `Windows RPC API`, `Windows Remote Desktop`, `Windows Remote Procedure Call`, `Windows Remote Procedure Call Runtime`, `Windows SMB`, `Windows SMB Server`, `Windows Server Service`, `Windows TCP/IP`

| category | name regex over "vendorProject : product" |
|---|---|
| W-SVC | `^Microsoft : (Active Directory$|Netlogon|Kerberos|Win32k Print|.*Print Spooler|SMB|Remote Desktop|Server Message Block)` |
| MS-APP | `^Microsoft : (Exchange|SQL Server|SharePoint|\.NET Framework, SharePoint)` |
| SRC-APP | `^Red Hat : JBoss|^Jenkins :|^Atlassian : (Jira|Confluence)|^GitLab :|^(VMware|Broadcom) : .*vCenter|^Microsoft : Configuration Manager` |
| VIRT | `^(VMware|Broadcom) : .*(ESX|Workstation|Tools)|^Microsoft : Hyper-V|^Docker :|runc|containerd` |
| CLIENT | `^Google : (Chromium|Chrome)|^Mozilla :|^Adobe : .*(Acrobat|Reader|Flash)|^RARLAB :|^7-Zip :|^Foxit :|^Microsoft : (Office|Word|Excel|Outlook|Internet Explorer|Edge|PowerPoint|Publisher)` |
| W-LPE | `^Microsoft : (Win32k|Windows)$` |
| L-KERNEL | `^Linux : Kernel$` |
| L-LPE | `^Sudo : Sudo$|^Red Hat : (Polkit|Libuser|Automatic Bug Reporting Tool)$|^GNU : GNU C Library$` |
| L-SVC | `^Samba :|OpenSSH|libssh|[Dd]ropbear|xrdp|VNC` |
| OLD-APP | `^ISC : BIND|PowerDNS|dnsmasq|Unbound|ProFTPD|vsftpd|Serv-U|CrushFTP|Wing FTP|Cerberus|FileZilla|Pure-FTPd|Xlight|^Apache : (HTTP Server|Tomcat)$|nginx|Internet Information Services|^Exim :|Postfix|Dovecot|Sendmail|MySQL|MariaDB|PostgreSQL` |

## 4. Largest vendor : product pairs per category

- **W-SVC:** Microsoft : Windows 12; Microsoft : Active Directory 3; Microsoft : SMBv1 server 2; Microsoft : SMBv1 2; Microsoft : HTTP Protocol Stack 1; Microsoft : Kerberos Key Distribution Center (KDC) 1; Microsoft : SMBv3 1; Microsoft : Remote Desktop Services 1; Microsoft : Netlogon 1
- **W-LPE:** Microsoft : Windows 134; Microsoft : Win32k 25; Microsoft : DirectX Graphics Kernel (DXGKRNL) 2; Microsoft : Enhanced Cryptographic Provider 2; Microsoft : Windows  1; Microsoft : DWM Core Library 1; Microsoft : Windows CNG Key Isolation Service 1; Microsoft : Windows COM+ Event System Service 1; Microsoft : Input Method Editor (IME) Japanese 1; Microsoft : Update Notification Manager 1; Microsoft : Task Scheduler 1; Microsoft : Graphics Device Interface (GDI) 1
- **L-KERNEL:** Linux : Kernel 32
- **L-LPE:** Sudo : Sudo 2; Red Hat : Polkit 2; Red Hat : Libuser 1; Red Hat : Automatic Bug Reporting Tool 1; GNU : GNU C Library 1
- **L-SVC:** Samba : Samba 1
- **CLIENT:** Google : Chromium V8 41; Microsoft : Internet Explorer 36; Adobe : Flash Player 33; Microsoft : Office 29; Adobe : Acrobat and Reader 13; Adobe : Reader and Acrobat 8; Google : Chromium 6; Mozilla : Firefox and Thunderbird 6; Mozilla : Firefox 5; RARLAB : WinRAR 4; Microsoft : Word 4; Microsoft : Excel 3
- **SRC-APP:** VMware : vCenter Server 9; Atlassian : Confluence Data Center and Server 3; GitLab : Community Edition and Enterprise Edition 2; GitLab : Community and Enterprise Editions 2; Atlassian : Jira Server and Data Center 2; Red Hat : JBoss 2; Atlassian : Confluence Server and Data Center 2; Broadcom : VMware vCenter 1; GitLab : GitLab 1; Microsoft : Configuration Manager 1; Broadcom : VMware vCenter Server 1; Jenkins : Jenkins 1
- **MS-APP:** Microsoft : Exchange Server 17; Microsoft : SharePoint 10; Microsoft : SharePoint Server 5; Microsoft : SQL Server 2; Microsoft : Exchange 1
- **OLD-APP:** Apache : Tomcat 6; SolarWinds : Serv-U 4; Apache : HTTP Server 4; CrushFTP : CrushFTP 3; Exim : Exim 3; Wing FTP Server : Wing FTP Server 2; ISC : BIND 1; ProFTPD : ProFTPD 1; Exim : Exim Internet Mailer 1; Exim : Mail Transfer Agent (MTA) 1; Microsoft : Internet Information Services (IIS) 1
- **VIRT:** VMware : ESXi 3; Broadcom : VMware ESX 1; Broadcom : VMware Aria Operations and VMware Tools 1; VMware : ESXi, Workstation, and Fusion 1; VMware : ESXi and Workstation 1; VMware : Tools 1; Docker : Desktop Community Edition 1; Microsoft : Hyper-V RemoteFX 1; VMware : VMware ESXi and Horizon DaaS 1
- **MS-OTHER:** Microsoft : Windows 26; Microsoft : Defender 5; Microsoft : Open Management Infrastructure (OMI) 4; Microsoft : .NET Framework 3; Microsoft : Silverlight 3; Microsoft : XML Core Services 2; Microsoft : Edge and Internet Explorer 2; Microsoft : Internet Key Exchange (IKE) Service Extensions 1; Microsoft : Windows Ancillary Function Driver for WinSock  1; Microsoft : Active Directory Federation Services 1; Microsoft : DirectX 1; Microsoft : Microsoft 1
- **OUT:** Apple : Multiple Products 55; Synacor : Zimbra Collaboration Suite (ZCS) 16; Adobe : ColdFusion 16; Cisco : IOS and IOS XE Software 14; Palo Alto Networks : PAN-OS 13; Samsung : Mobile Devices 13; Oracle : WebLogic Server 12; Apple : iOS, iPadOS, and macOS 11; Qualcomm : Multiple Chipsets 10; SAP : NetWeaver 10; Fortinet : FortiOS 9; Apple : iOS 8

## 5. ATT&CK procedure examples (stored bundle v20.1)

### T1210 (26)

- AI-Assisted Breach of Mexico's Government Infrastructure: During the [AI-Assisted Breach of Mexico's Government Infrastructure](https://attack.mitre.org/campaigns/C0064), the adversary tasked Claude Code with attempting to exploit the EternalBlue vulnerability.
- APT28: [APT28](https://attack.mitre.org/groups/G0007) exploited a Windows SMB Remote Code Execution Vulnerability to conduct lateral movement.
- Bad Rabbit: [Bad Rabbit](https://attack.mitre.org/software/S0606) used the EternalRomance SMB exploit to spread through victim networks.
- Conficker: [Conficker](https://attack.mitre.org/software/S0608) exploited the MS08-067 Windows vulnerability for remote code execution through a crafted RPC request.
- Dragonfly: [Dragonfly](https://attack.mitre.org/groups/G0035) has exploited a Windows Netlogon vulnerability (CVE-2020-1472) to obtain access to Windows Active Directory servers.
- Earth Lusca: [Earth Lusca](https://attack.mitre.org/groups/G1006) has used [Mimikatz](https://attack.mitre.org/software/S0002) to exploit a domain controller via the ZeroLogon exploit (CVE-2020-1472).
- Ember Bear: [Ember Bear](https://attack.mitre.org/groups/G1003) has used exploits for vulnerabilities such as MS17-010, also known as `Eternal Blue`, during operations.
- Emotet: [Emotet](https://attack.mitre.org/software/S0367) has been seen exploiting SMB via a vulnerability exploit like EternalBlue (MS17-010) to achieve lateral movement and propagation.
- Empire: [Empire](https://attack.mitre.org/software/S0363) has a limited number of built-in modules for exploiting remote SMB, JBoss, and Jenkins servers.
- FIN7: [FIN7](https://attack.mitre.org/groups/G0046) has exploited ZeroLogon (CVE-2020-1472) against vulnerable domain controllers.
- Flame: [Flame](https://attack.mitre.org/software/S0143) can use MS10-061 to exploit a print spooler vulnerability in a remote system with a shared printer in order to move laterally.
- Fox Kitten: [Fox Kitten](https://attack.mitre.org/groups/G0117) has exploited known vulnerabilities in remote services including RDP.
- InvisiMole: [InvisiMole](https://attack.mitre.org/software/S0260) can spread within a network via the BlueKeep (CVE-2019-0708) and EternalBlue (CVE-2017-0144) vulnerabilities in RDP and SMB respectively.
- Lucifer: [Lucifer](https://attack.mitre.org/software/S0532) can exploit multiple vulnerabilities including EternalBlue (CVE-2017-0144) and EternalRomance (CVE-2017-0144).
- MuddyWater: [MuddyWater](https://attack.mitre.org/groups/G0069) has exploited the Microsoft Netlogon vulnerability (CVE-2020-1472).
- NotPetya: [NotPetya](https://attack.mitre.org/software/S0368) can use two exploits in SMBv1, EternalBlue and EternalRomance, to spread itself to other remote systems on the network.
- PoshC2: [PoshC2](https://attack.mitre.org/software/S0378) contains a module for exploiting SMB via EternalBlue.
- QakBot: [QakBot](https://attack.mitre.org/software/S0650) can move laterally using worm-like functionality through exploitation of SMB.
- ShinyHunters: [ShinyHunters](https://attack.mitre.org/groups/G1057) has exploited vulnerabilities in remote services for lateral movement.
- Stuxnet: [Stuxnet](https://attack.mitre.org/software/S0603) propagates using the MS10-061 Print Spooler and MS08-067 Windows Server Service vulnerabilities.
- Threat Group-3390: [Threat Group-3390](https://attack.mitre.org/groups/G0027) has exploited MS17-010 to move laterally to other systems on the network.
- Tonto Team: [Tonto Team](https://attack.mitre.org/groups/G0131) has used EternalBlue exploits for lateral movement.
- TrickBot: [TrickBot](https://attack.mitre.org/software/S0266) utilizes EternalBlue and EternalRomance exploits for lateral movement in the modules wormwinDll, wormDll, mwormDll, nwormDll, tabDll.
- WannaCry: [WannaCry](https://attack.mitre.org/software/S0366) uses an exploit in SMBv1 to spread itself to other remote systems on a network.
- Wizard Spider: [Wizard Spider](https://attack.mitre.org/groups/G0102) has exploited or attempted to exploit Zerologon (CVE-2020-1472) and EternalBlue (MS17-010) vulnerabilities.
- menuPass: [menuPass](https://attack.mitre.org/groups/G0045) has used tools to exploit the ZeroLogon vulnerability (CVE-2020-1472).

### T1212 (2)

- Leviathan Australian Intrusions: [Leviathan](https://attack.mitre.org/groups/G0065) exploited vulnerable network appliances during [Leviathan Australian Intrusions](https://attack.mitre.org/campaigns/C0049), leading to the collection and exfiltration of valid credentials.
- UNC3886: [UNC3886](https://attack.mitre.org/groups/G1048) exploited CVE-2022-22948 in VMware vCenter to obtain encrypted credentials from the vCenter postgresDB.

### T1068 (44)

- APT28: [APT28](https://attack.mitre.org/groups/G0007) has exploited CVE-2014-4076, CVE-2015-2387, CVE-2015-1701, CVE-2017-0263, and CVE-2022-38028 to escalate privileges.
- APT29: [APT29](https://attack.mitre.org/groups/G0016) has exploited CVE-2021-36934 to escalate privileges on a compromised host.
- APT32: [APT32](https://attack.mitre.org/groups/G0050) has used CVE-2016-7255 to escalate privileges.
- APT33: [APT33](https://attack.mitre.org/groups/G0064) has used a publicly available exploit for CVE-2017-0213 to escalate privileges on a local system.
- BITTER: [BITTER](https://attack.mitre.org/groups/G1002) has exploited CVE-2021-1732 for privilege escalation.
- BlackByte: [BlackByte](https://attack.mitre.org/groups/G1043) has exploited CVE-2024-37085 in VMWare ESXi software for authentication bypass and subsequent privilege escalation.
- BlackByte 2.0 Ransomware: [BlackByte 2.0 Ransomware](https://attack.mitre.org/software/S1181) exploits a vulnerability in the RTCore64.sys driver (CVE-2019-16098) to enable privilege escalation and defense evasion when run as a service.
- Carberp: [Carberp](https://attack.mitre.org/software/S0484) has exploited multiple Windows vulnerabilities (CVE-2010-2743, CVE-2010-3338, CVE-2010-4398, CVE-2008-1084) and a .NET Runtime Optimization vulnerability for privilege escalation.
- Cobalt Group: [Cobalt Group](https://attack.mitre.org/groups/G0080) has used exploits to increase their levels of rights and privileges.
- Cobalt Strike: [Cobalt Strike](https://attack.mitre.org/software/S0154) can exploit vulnerabilities such as MS14-058.
- CosmicDuke: [CosmicDuke](https://attack.mitre.org/software/S0050) attempts to exploit privilege escalation vulnerabilities CVE-2010-0232 or CVE-2010-4398.
- Embargo: [Embargo](https://attack.mitre.org/software/S1247) has leveraged MS4Killer to deliver a vulnerable driver to the victim device, sometimes referred to as Bring Your Own Vulnerable Driver (BYOVD). [Embargo](https://attack.mitre.org/software/S1247) has utilized the vulnerable driver probmon.sys version
- Empire: [Empire](https://attack.mitre.org/software/S0363) can exploit vulnerabilities such as MS16-032 and MS16-135.
- FIN6: [FIN6](https://attack.mitre.org/groups/G0037) has used tools to exploit Windows vulnerabilities in order to escalate privileges. The tools targeted CVE-2013-3660, CVE-2011-2005, and CVE-2010-4398, all of which could allow local users to access kernel-level privileges.
- FIN8: [FIN8](https://attack.mitre.org/groups/G0061) has exploited the CVE-2016-0167 local vulnerability.
- HAFNIUM: [HAFNIUM](https://attack.mitre.org/groups/G0125) has targeted unpatched applications to elevate access in targeted organizations.
- Hildegard: [Hildegard](https://attack.mitre.org/software/S0601) has used the BOtB tool which exploits CVE-2019-5736.
- InvisiMole: [InvisiMole](https://attack.mitre.org/software/S0260) has exploited CVE-2007-5633 vulnerability in the speedfan.sys driver to obtain kernel mode privileges.
- JHUHUGIT: [JHUHUGIT](https://attack.mitre.org/software/S0044) has exploited CVE-2015-1701 and CVE-2015-2387 to escalate privileges.
- LAPSUS$: [LAPSUS$](https://attack.mitre.org/groups/G1004) has exploited unpatched vulnerabilities on internally accessible servers including JIRA, GitLab, and Confluence for privilege escalation.
- Leviathan Australian Intrusions: [Leviathan](https://attack.mitre.org/groups/G0065) exploited software vulnerabilities in victim environments to escalate privileges during [Leviathan Australian Intrusions](https://attack.mitre.org/campaigns/C0049).
- MoustachedBouncer: [MoustachedBouncer](https://attack.mitre.org/groups/G1019) has exploited CVE-2021-1732 to execute malware components with elevated rights.
- OilRig: [OilRig](https://attack.mitre.org/groups/G0049) has exploited the Windows Kernel Elevation of Privilege vulnerability, CVE-2024-30088.
- PLATINUM: [PLATINUM](https://attack.mitre.org/groups/G0068) has leveraged a zero-day vulnerability to escalate privileges.
- Pandora: [Pandora](https://attack.mitre.org/software/S0664) can use CVE-2017-15303 to bypass Windows Driver Signature Enforcement (DSE) protection and load its driver.
- PoshC2: [PoshC2](https://attack.mitre.org/software/S0378) contains modules for local privilege escalation exploits such as CVE-2016-9192 and CVE-2016-0099.
- ProLock: [ProLock](https://attack.mitre.org/software/S0654) can use CVE-2019-0859 to escalate privileges on a compromised host.
- Remsec: [Remsec](https://attack.mitre.org/software/S0125) has a plugin to drop and execute vulnerable Outpost Sandbox or avast! Virtualization drivers in order to gain kernel mode privileges.
- Scattered Spider: [Scattered Spider](https://attack.mitre.org/groups/G1015) has deployed a malicious kernel driver through exploitation of CVE-2015-2291 in the Intel Ethernet diagnostics driver for Windows (iqvw64.sys).
- ShadowRay: During [ShadowRay](https://attack.mitre.org/campaigns/C0045), threat actors downloaded a privilege escalation payload to gain root access.
- Siloscape: [Siloscape](https://attack.mitre.org/software/S0623) has leveraged a vulnerability in Windows containers to perform an [Escape to Host](https://attack.mitre.org/techniques/T1611).
- Stuxnet: [Stuxnet](https://attack.mitre.org/software/S0603) used MS10-073 and an undisclosed Task Scheduler vulnerability to escalate privileges on local Windows machines.
- The Gentlemen: [The Gentlemen](https://attack.mitre.org/groups/G1058) has assisted affiliates with gaining privilege escalation through the use of BYOVD.
- Threat Group-3390: [Threat Group-3390](https://attack.mitre.org/groups/G0027) has used CVE-2014-6324 and CVE-2017-0213 to escalate privileges.
- Tonto Team: [Tonto Team](https://attack.mitre.org/groups/G0131) has exploited CVE-2019-0803 and MS16-032 to escalate privileges.
- Turla: [Turla](https://attack.mitre.org/groups/G0010) has exploited vulnerabilities in the VBoxDrv.sys driver to obtain kernel mode privileges.
- UNC3886: [UNC3886](https://attack.mitre.org/groups/G1048) has exploited zero-day vulnerability CVE-2023-20867 to enable execution of privileged commands across Windows, Linux, and PhotonOS (vCenter) guest VMs.
- Volt Typhoon: [Volt Typhoon](https://attack.mitre.org/groups/G1017) has gained initial access by exploiting privilege escalation vulnerabilities in the operating system or network services.
- Whitefly: [Whitefly](https://attack.mitre.org/groups/G0107) has used an open-source tool to exploit a known Windows privilege escalation vulnerability (CVE-2016-0051) on unpatched computers.
- Wingbird: [Wingbird](https://attack.mitre.org/software/S0176) exploits CVE-2016-4117 to allow an executable to gain escalated privileges.
- XCSSET: [XCSSET](https://attack.mitre.org/software/S0658) has used a zero-day exploit in the ssh launchdaemon to elevate privileges and bypass SIP.
- ZIRCONIUM: [ZIRCONIUM](https://attack.mitre.org/groups/G0128) has exploited CVE-2017-0005 for local privilege escalation.
- ZeroCleare: [ZeroCleare](https://attack.mitre.org/software/S1151) has used a vulnerable signed VBoxDrv driver to bypass Microsoft Driver Signature Enforcement (DSE) protections and subsequently load the unsigned [RawDisk](https://attack.mitre.org/software/S0364) driver.
- Zox: [Zox](https://attack.mitre.org/software/S0672) has the ability to leverage local and remote exploits to escalate privileges.

### T1072 (12)

- APT32: [APT32](https://attack.mitre.org/groups/G0050) compromised McAfee ePO to move laterally by distributing malware as a software deployment task.
- C0018: During [C0018](https://attack.mitre.org/campaigns/C0018), the threat actors used PDQ Deploy to move [AvosLocker](https://attack.mitre.org/software/S1053) and tools across the network.
- Medusa Group: [Medusa Group](https://attack.mitre.org/groups/G1051) has utilized software deployment and management solutions to deploy their encryption payload to include BigFix and PDQ Deploy.
- Mustang Panda: [Mustang Panda](https://attack.mitre.org/groups/G0129) has leveraged legitimate software tools such as AntiVirus Agents, Security Services, and App Development tools to execute scripts and to side-load dlls.
- NIMBUS MANTICORE: [NIMBUS MANTICORE](https://attack.mitre.org/groups/G1059) has utilized commercial remote access tools such as Atelier Web Remote Commander (AWRC) and Microsoft System Center Configuration Manager (SCCM) within victim environments.
- Salt Typhoon: [Salt Typhoon](https://attack.mitre.org/groups/G1045) has abused network management tools to include RANCID to facilitate actions in victims’ environments.
- Sandworm Team: [Sandworm Team](https://attack.mitre.org/groups/G0034) has used the commercially available tool RemoteExec for agentless remote code execution.
- ShinyHunters: [ShinyHunters](https://attack.mitre.org/groups/G1057) has abused software deployment tools for lateral movement.
- Silence: [Silence](https://attack.mitre.org/groups/G0091) has used RAdmin, a remote software tool used to remotely control workstations and ATMs.
- Threat Group-1314: [Threat Group-1314](https://attack.mitre.org/groups/G0028) actors used a victim's endpoint management platform, Altiris, for lateral movement.
- VOID MANTICORE: [VOID MANTICORE](https://attack.mitre.org/groups/G1055) has leveraged legitimate built-in features of cloud-based management platforms to include mobile device management (MDM) and Remote Monitoring and Management (RMM) solutions. [VOID MANTICORE](https://attack.mitre.org/groups/G1055) has also init
- Wiper: It is believed that a patch management system for an anti-virus product commonly installed among targeted companies was used to distribute the [Wiper](https://attack.mitre.org/software/S0041) malware.

### T1611 (5)

- Doki: [Doki](https://attack.mitre.org/software/S0600)’s container was configured to bind the host root directory.
- Hildegard: [Hildegard](https://attack.mitre.org/software/S0601) has used the BOtB tool that can break out of containers.
- Peirates: [Peirates](https://attack.mitre.org/software/S0683) can gain a reverse shell on a host node by mounting the Kubernetes hostPath.
- Siloscape: [Siloscape](https://attack.mitre.org/software/S0623) maps the host’s C drive to the container by creating a global symbolic link to the host through the calling of <code>NtSetInformationSymbolicLink</code>.
- TeamTNT: [TeamTNT](https://attack.mitre.org/groups/G0139) has deployed privileged containers that mount the filesystem of victim machine.

### T1534 (9)

- APT-C-36: [APT-C-36](https://attack.mitre.org/groups/G0099) has used a compromised account to send a phishing email to an address likely used and monitored by the IT team within the same targeted organization.
- Gamaredon Group: [Gamaredon Group](https://attack.mitre.org/groups/G0047) has used an Outlook VBA module on infected systems to send phishing emails with malicious attachments to other employees within the organization.
- HEXANE: [HEXANE](https://attack.mitre.org/groups/G1001) has conducted internal spearphishing attacks against executives, HR, and IT personnel to gain information and access.
- Kimsuky: [Kimsuky](https://attack.mitre.org/groups/G0094) has sent internal spearphishing emails for lateral movement after stealing victim information.
- Leviathan: [Leviathan](https://attack.mitre.org/groups/G0065) has conducted internal spearphishing within the victim's environment for lateral movement.
- MuddyWater: [MuddyWater](https://attack.mitre.org/groups/G0069) has used compromised mailboxes within target organizations to send spearphishing emails.
- NIMBUS MANTICORE: [NIMBUS MANTICORE](https://attack.mitre.org/groups/G1059) has conducted internal spearphishing attacks against IT staff and administrators.
- Operation Dream Job: During [Operation Dream Job](https://attack.mitre.org/campaigns/C0022), [Lazarus Group](https://attack.mitre.org/groups/G0032) conducted internal spearphishing from within a compromised organization.
- SameCoin: [SameCoin](https://attack.mitre.org/software/S9030) can send its Setup.exe file as an attachment to other addresses in the same compromised organization.

### T1080 (12)

- BRONZE BUTLER: [BRONZE BUTLER](https://attack.mitre.org/groups/G0060) has placed malware on file shares and given it the same name as legitimate documents on the share.
- Cinnamon Tempest: [Cinnamon Tempest](https://attack.mitre.org/groups/G1021) has deployed ransomware from a batch file in a network share.
- Conti: [Conti](https://attack.mitre.org/software/S0575) can spread itself by infecting other remote machines via network shared drives.
- Darkhotel: [Darkhotel](https://attack.mitre.org/groups/G0012) used a virus that propagates by infecting executables stored on shared drives.
- Gamaredon Group: [Gamaredon Group](https://attack.mitre.org/groups/G0047) has injected malicious macros into all Word and Excel documents on mapped network drives.
- H1N1: [H1N1](https://attack.mitre.org/software/S0132) has functionality to copy itself to network shares.
- InvisiMole: [InvisiMole](https://attack.mitre.org/software/S0260) can replace legitimate software or documents in the compromised network with their trojanized versions, in an attempt to propagate itself within the network.
- Miner-C: [Miner-C](https://attack.mitre.org/software/S0133) copies itself into the public folder of Network Attached Storage (NAS) devices and infects new victims who open the file.
- Ramsay: [Ramsay](https://attack.mitre.org/software/S0458) can spread itself by infecting other portable executable files on networks shared drives.
- RedCurl: [RedCurl](https://attack.mitre.org/groups/G1039) has placed modified LNK files on network drives for lateral movement.
- Stuxnet: [Stuxnet](https://attack.mitre.org/software/S0603) infects remote servers via network shares and by infecting WinCC database views with malicious code.
- Ursnif: [Ursnif](https://attack.mitre.org/software/S0386) has copied itself to and infected files in network drives for propagation.

