# CVE semantics in the pinned NVD snapshot (2026-10-21)

**Analysis only. No exclusion, filter or criterion is adopted here; every count is descriptive.**

- Snapshot `data/raw/nvd/2026-10-21/`, manifest SHA-256 `0e5a3b6208a6b9a6f554d2234f1acbf7474f141fa1d16f5d989ea25578cb387e` (matches `data/derived/build_log.json`). Every page's SHA-256 was checked against the manifest.
- **The snapshot was queried per product in FAMILY_PRODUCTS** (37 pages, 35 CPE products, 8 families), **so it is not a sample of all of NVD.**
- Population (a): the 1473 included CVEs of `data/derived/cves.csv`, grouped by their family and products. Population (b): all 4216 distinct records in the snapshot, grouped by every family / product whose query returned them (a record can count under several groups; 'all' counts it once).
- CWE catalogue: `data/raw/cwe/2026-11-08/cwec_v5.0.xml`, SHA-256 `47165a9593def89c69b9ef50c34d99ac68db55df8373613e85e9cc9ceecefb1d`, 984 Weaknesses, 493 Groupings (categories)/Views (docs/sources.md S6, S7).
- D11 score = NVD Primary (`source == nvd@nist.gov`, `type == Primary`) v3.1, else v3.0; re-implemented here and identical to `cves.csv` (version, exploitability, PR) for all included CVEs.
- Product roles: docs/sources.md §2 (P1–P35).

## 1. Which scores exist; NVD Primary vs CNA v3 disagreement
### 1a. Score presence (a CVE can have several)
nvd_primary_v30 counts a v3.0 NVD Primary score whether or not a v3.1 one also exists.

**(a) 1,473 included CVEs**

| group | n | nvd_primary_v31 | nvd_primary_v30 | cna_v3 | v2 | v4 | none |
|---|---|---|---|---|---|---|---|
| all | 1473 | 1056 | 417 | 463 | 1308 | 0 | 0 |
| family dns | 158 | 108 | 50 | 79 | 140 | 0 | 0 |
| family ftp | 62 | 52 | 10 | 16 | 50 | 0 | 0 |
| family http | 189 | 127 | 62 | 39 | 167 | 0 | 0 |
| family mail | 125 | 82 | 43 | 28 | 113 | 0 | 0 |
| family rdp | 106 | 100 | 6 | 81 | 68 | 0 | 0 |
| family smb | 107 | 83 | 24 | 54 | 76 | 0 | 0 |
| family sql | 668 | 471 | 197 | 131 | 647 | 0 | 0 |
| family ssh | 58 | 33 | 25 | 35 | 47 | 0 | 0 |
| product apache:http_server | 87 | 60 | 27 | 11 | 79 | 0 | 0 |
| product apache:tomcat | 83 | 48 | 35 | 18 | 71 | 0 | 0 |
| product cerberusftp:ftp_server | 5 | 4 | 1 | 0 | 5 | 0 | 0 |
| product crushftp:crushftp | 7 | 3 | 4 | 0 | 5 | 0 | 0 |
| product dovecot:dovecot | 28 | 18 | 10 | 13 | 27 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 4 | 8 | 3 | 11 | 0 | 0 |
| product exim:exim | 39 | 33 | 6 | 6 | 34 | 0 | 0 |
| product f5:nginx | 19 | 19 | 0 | 10 | 16 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 85 | 4 | 67 | 63 | 0 | 0 |
| product isc:bind | 72 | 50 | 22 | 56 | 62 | 0 | 0 |
| product libssh:libssh | 11 | 8 | 3 | 5 | 7 | 0 | 0 |
| product mariadb:mariadb | 200 | 175 | 25 | 18 | 197 | 0 | 0 |
| product microsoft:exchange_server | 54 | 28 | 26 | 9 | 50 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| product microsoft:sql_server | 13 | 6 | 7 | 4 | 11 | 0 | 0 |
| product mysql:mysql | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 15 | 2 | 14 | 5 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 21 | 1 | 1 | 19 | 0 | 0 |
| product openbsd:openssh | 35 | 21 | 14 | 27 | 29 | 0 | 0 |
| product oracle:mysql | 516 | 347 | 169 | 96 | 512 | 0 | 0 |
| product postfix:postfix | 3 | 2 | 1 | 0 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 51 | 19 | 21 | 58 | 0 | 0 |
| product powerdns:authoritative | 17 | 7 | 10 | 9 | 17 | 0 | 0 |
| product powerdns:recursor | 24 | 10 | 14 | 13 | 21 | 0 | 0 |
| product proftpd:proftpd | 12 | 10 | 2 | 1 | 10 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 5 | 1 | 0 | 6 | 0 | 0 |
| product samba:samba | 107 | 83 | 24 | 54 | 76 | 0 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 21 | 2 | 10 | 20 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 20 | 8 | 5 | 26 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 8 | 0 | 4 | 4 | 0 | 0 |


**(b) all snapshot records**

| group | n | nvd_primary_v31 | nvd_primary_v30 | cna_v3 | v2 | v4 | none |
|---|---|---|---|---|---|---|---|
| all | 4216 | 1383 | 433 | 1665 | 3136 | 153 | 0 |
| family dns | 364 | 151 | 50 | 167 | 252 | 15 | 0 |
| family ftp | 159 | 78 | 10 | 77 | 87 | 13 | 0 |
| family http | 777 | 157 | 67 | 188 | 615 | 1 | 0 |
| family mail | 453 | 129 | 50 | 194 | 324 | 0 | 0 |
| family rdp | 280 | 203 | 6 | 205 | 70 | 119 | 0 |
| family smb | 216 | 91 | 26 | 66 | 175 | 0 | 0 |
| family sql | 1765 | 499 | 198 | 663 | 1479 | 3 | 0 |
| family ssh | 209 | 78 | 26 | 106 | 140 | 2 | 0 |
| product apache:http_server | 371 | 79 | 28 | 91 | 290 | 0 | 0 |
| product apache:tomcat | 276 | 57 | 38 | 85 | 198 | 0 | 0 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 5 | 1 | 0 | 9 | 1 | 0 |
| product crushftp:crushftp | 17 | 7 | 4 | 10 | 5 | 0 | 0 |
| product dovecot:dovecot | 69 | 30 | 10 | 29 | 52 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 5 | 8 | 4 | 18 | 0 | 0 |
| product exim:exim | 71 | 52 | 6 | 30 | 44 | 0 | 0 |
| product f5:nginx | 41 | 20 | 0 | 12 | 37 | 1 | 0 |
| product filezilla-project:filezilla_server | 7 | 3 | 0 | 2 | 6 | 0 | 0 |
| product freerdp:freerdp | 243 | 178 | 4 | 177 | 65 | 113 | 0 |
| product isc:bind | 184 | 58 | 22 | 81 | 152 | 0 | 0 |
| product libssh:libssh | 45 | 24 | 3 | 31 | 16 | 1 | 0 |
| product mariadb:mariadb | 431 | 185 | 26 | 68 | 396 | 3 | 0 |
| product microsoft:exchange_server | 268 | 41 | 33 | 134 | 186 | 0 | 0 |
| product microsoft:internet_information_services | 93 | 2 | 1 | 2 | 93 | 0 | 0 |
| product microsoft:sql_server | 110 | 8 | 7 | 26 | 91 | 0 | 0 |
| product mysql:mysql | 94 | 0 | 2 | 0 | 94 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 25 | 2 | 28 | 5 | 6 | 0 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 41 | 1 | 38 | 24 | 15 | 0 |
| product openbsd:openssh | 146 | 51 | 15 | 73 | 106 | 1 | 0 |
| product oracle:mysql | 1328 | 352 | 169 | 520 | 1158 | 0 | 0 |
| product postfix:postfix | 12 | 3 | 1 | 1 | 10 | 0 | 0 |
| product postgresql:postgresql | 209 | 63 | 19 | 75 | 145 | 0 | 0 |
| product powerdns:authoritative | 31 | 16 | 10 | 20 | 20 | 0 | 0 |
| product powerdns:recursor | 50 | 19 | 14 | 30 | 30 | 0 | 0 |
| product proftpd:proftpd | 33 | 14 | 2 | 8 | 24 | 5 | 0 |
| product pureftpd:pure-ftpd | 11 | 5 | 1 | 1 | 10 | 0 | 0 |
| product samba:samba | 216 | 91 | 26 | 66 | 175 | 0 | 0 |
| product sendmail:sendmail | 33 | 3 | 0 | 0 | 32 | 0 | 0 |
| product solarwinds:serv-u | 55 | 31 | 2 | 42 | 20 | 0 | 0 |
| product thekelleys:dnsmasq | 39 | 23 | 8 | 9 | 33 | 0 | 0 |
| product wftpserver:wing_ftp_server | 20 | 11 | 0 | 13 | 8 | 5 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 0 | 2 | 3 | 2 | 0 |

### 1b. NVD Primary v3 vs CNA v3 on the same CVE: metrics that differ

**(a) 1,473 included CVEs**

| group | n | both_present | any_differs | AV | PR | UI | C | I | A |
|---|---|---|---|---|---|---|---|---|---|
| all | 1473 | 463 | 136 | 10 | 40 | 34 | 57 | 50 | 65 |
| family dns | 158 | 79 | 18 | 0 | 7 | 6 | 3 | 4 | 8 |
| family ftp | 62 | 16 | 6 | 0 | 2 | 4 | 2 | 1 | 3 |
| family http | 189 | 39 | 6 | 1 | 2 | 1 | 0 | 1 | 4 |
| family mail | 125 | 28 | 7 | 1 | 3 | 1 | 2 | 3 | 3 |
| family rdp | 106 | 81 | 63 | 2 | 12 | 13 | 40 | 30 | 38 |
| family smb | 107 | 54 | 16 | 3 | 5 | 6 | 7 | 7 | 4 |
| family sql | 668 | 131 | 14 | 2 | 6 | 3 | 1 | 4 | 4 |
| family ssh | 58 | 35 | 6 | 1 | 3 | 0 | 2 | 0 | 1 |
| product apache:http_server | 87 | 11 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| product apache:tomcat | 83 | 18 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| product cerberusftp:ftp_server | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 28 | 13 | 4 | 0 | 1 | 1 | 0 | 1 | 1 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| product exim:exim | 39 | 6 | 3 | 1 | 2 | 0 | 2 | 2 | 2 |
| product f5:nginx | 19 | 10 | 4 | 1 | 1 | 1 | 0 | 0 | 2 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 67 | 51 | 1 | 11 | 11 | 30 | 26 | 33 |
| product isc:bind | 72 | 56 | 5 | 0 | 2 | 1 | 1 | 0 | 2 |
| product libssh:libssh | 11 | 5 | 2 | 0 | 1 | 0 | 0 | 0 | 1 |
| product mariadb:mariadb | 200 | 18 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| product microsoft:exchange_server | 54 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| product mysql:mysql | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 14 | 12 | 1 | 1 | 2 | 10 | 4 | 5 |
| product nlnetlabs:unbound | 22 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product openbsd:openssh | 35 | 27 | 3 | 1 | 2 | 0 | 1 | 0 | 0 |
| product oracle:mysql | 516 | 96 | 3 | 1 | 1 | 0 | 0 | 0 | 1 |
| product postfix:postfix | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product postgresql:postgresql | 70 | 21 | 9 | 1 | 4 | 3 | 0 | 3 | 2 |
| product powerdns:authoritative | 17 | 9 | 9 | 0 | 3 | 2 | 0 | 2 | 4 |
| product powerdns:recursor | 24 | 13 | 9 | 0 | 3 | 3 | 2 | 4 | 4 |
| product proftpd:proftpd | 12 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product samba:samba | 107 | 54 | 16 | 3 | 5 | 6 | 7 | 7 | 4 |
| product sendmail:sendmail | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 10 | 2 | 0 | 0 | 2 | 1 | 0 | 1 |
| product thekelleys:dnsmasq | 28 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 4 | 4 | 0 | 2 | 2 | 1 | 1 | 2 |


**(b) all snapshot records**

| group | n | both_present | any_differs | AV | PR | UI | C | I | A |
|---|---|---|---|---|---|---|---|---|---|
| all | 4216 | 699 | 258 | 17 | 70 | 59 | 104 | 100 | 123 |
| family dns | 364 | 108 | 32 | 0 | 8 | 6 | 4 | 8 | 18 |
| family ftp | 159 | 37 | 16 | 1 | 3 | 6 | 7 | 5 | 7 |
| family http | 777 | 60 | 15 | 1 | 4 | 1 | 3 | 5 | 7 |
| family mail | 453 | 70 | 34 | 1 | 10 | 4 | 13 | 17 | 12 |
| family rdp | 280 | 136 | 96 | 3 | 15 | 26 | 58 | 44 | 55 |
| family smb | 216 | 57 | 17 | 3 | 5 | 6 | 7 | 8 | 5 |
| family sql | 1765 | 154 | 21 | 3 | 10 | 5 | 2 | 6 | 6 |
| family ssh | 209 | 78 | 27 | 5 | 15 | 5 | 10 | 7 | 13 |
| product apache:http_server | 371 | 23 | 6 | 0 | 1 | 0 | 1 | 4 | 2 |
| product apache:tomcat | 276 | 27 | 5 | 0 | 2 | 0 | 2 | 1 | 3 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 17 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 69 | 23 | 10 | 0 | 2 | 2 | 1 | 4 | 4 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 4 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| product exim:exim | 71 | 25 | 12 | 1 | 5 | 0 | 6 | 5 | 6 |
| product f5:nginx | 41 | 10 | 4 | 1 | 1 | 1 | 0 | 0 | 2 |
| product filezilla-project:filezilla_server | 7 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 243 | 118 | 80 | 2 | 13 | 24 | 46 | 39 | 48 |
| product isc:bind | 184 | 60 | 7 | 0 | 2 | 1 | 1 | 2 | 3 |
| product libssh:libssh | 45 | 21 | 7 | 0 | 4 | 0 | 1 | 1 | 6 |
| product mariadb:mariadb | 431 | 26 | 4 | 0 | 3 | 0 | 1 | 2 | 2 |
| product microsoft:exchange_server | 268 | 21 | 11 | 0 | 3 | 2 | 6 | 8 | 1 |
| product microsoft:internet_information_services | 93 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 110 | 5 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| product mysql:mysql | 94 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 18 | 16 | 1 | 2 | 2 | 12 | 5 | 7 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 12 | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| product openbsd:openssh | 146 | 55 | 19 | 5 | 11 | 5 | 8 | 6 | 7 |
| product oracle:mysql | 1328 | 99 | 3 | 1 | 1 | 0 | 0 | 0 | 1 |
| product postfix:postfix | 12 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| product postgresql:postgresql | 209 | 32 | 13 | 2 | 5 | 5 | 1 | 4 | 3 |
| product powerdns:authoritative | 31 | 18 | 15 | 0 | 4 | 2 | 1 | 4 | 7 |
| product powerdns:recursor | 50 | 22 | 14 | 0 | 3 | 3 | 2 | 5 | 9 |
| product proftpd:proftpd | 33 | 3 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| product pureftpd:pure-ftpd | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product samba:samba | 216 | 57 | 17 | 3 | 5 | 6 | 7 | 8 | 5 |
| product sendmail:sendmail | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 55 | 20 | 6 | 1 | 0 | 3 | 3 | 2 | 2 |
| product thekelleys:dnsmasq | 39 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 20 | 7 | 7 | 0 | 2 | 3 | 3 | 2 | 4 |
| product xlightftpd:xlight_ftp_server | 5 | 2 | 2 | 0 | 1 | 0 | 0 | 0 | 1 |

## 2. Base vector distribution (D11 score: NVD Primary v3.1, else v3.0)
### 2. AV

**(a) 1,473 included CVEs**

| group | n | N | A | L | P | no_d11_score |
|---|---|---|---|---|---|---|
| all | 1473 | 1300 | 13 | 160 | 0 | 0 |
| family dns | 158 | 156 | 0 | 2 | 0 | 0 |
| family ftp | 62 | 57 | 0 | 5 | 0 | 0 |
| family http | 189 | 172 | 1 | 16 | 0 | 0 |
| family mail | 125 | 96 | 5 | 24 | 0 | 0 |
| family rdp | 106 | 102 | 0 | 4 | 0 | 0 |
| family smb | 107 | 97 | 4 | 6 | 0 | 0 |
| family sql | 668 | 573 | 2 | 93 | 0 | 0 |
| family ssh | 58 | 47 | 1 | 10 | 0 | 0 |
| product apache:http_server | 87 | 84 | 1 | 2 | 0 | 0 |
| product apache:tomcat | 83 | 73 | 0 | 10 | 0 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 28 | 25 | 0 | 3 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 10 | 0 | 2 | 0 | 0 |
| product exim:exim | 39 | 25 | 0 | 14 | 0 | 0 |
| product f5:nginx | 19 | 15 | 0 | 4 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 88 | 0 | 1 | 0 | 0 |
| product isc:bind | 72 | 71 | 0 | 1 | 0 | 0 |
| product libssh:libssh | 11 | 11 | 0 | 0 | 0 | 0 |
| product mariadb:mariadb | 200 | 144 | 1 | 55 | 0 | 0 |
| product microsoft:exchange_server | 54 | 43 | 5 | 6 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 12 | 0 | 1 | 0 | 0 |
| product mysql:mysql | 1 | 0 | 0 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 14 | 0 | 3 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 21 | 0 | 1 | 0 | 0 |
| product openbsd:openssh | 35 | 26 | 1 | 8 | 0 | 0 |
| product oracle:mysql | 516 | 457 | 2 | 57 | 0 | 0 |
| product postfix:postfix | 3 | 2 | 0 | 1 | 0 | 0 |
| product postgresql:postgresql | 70 | 60 | 0 | 10 | 0 | 0 |
| product powerdns:authoritative | 17 | 17 | 0 | 0 | 0 | 0 |
| product powerdns:recursor | 24 | 24 | 0 | 0 | 0 | 0 |
| product proftpd:proftpd | 12 | 11 | 0 | 1 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 | 0 | 0 |
| product samba:samba | 107 | 97 | 4 | 6 | 0 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 22 | 0 | 1 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 0 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 5 | 0 | 3 | 0 | 0 |


**(b) all snapshot records**

| group | n | N | A | L | P | no_d11_score |
|---|---|---|---|---|---|---|
| all | 4216 | 1603 | 17 | 196 | 0 | 2400 |
| family dns | 364 | 197 | 1 | 3 | 0 | 163 |
| family ftp | 159 | 81 | 0 | 7 | 0 | 71 |
| family http | 777 | 204 | 1 | 19 | 0 | 553 |
| family mail | 453 | 134 | 7 | 38 | 0 | 274 |
| family rdp | 280 | 203 | 0 | 6 | 0 | 71 |
| family smb | 216 | 106 | 5 | 6 | 0 | 99 |
| family sql | 1765 | 600 | 2 | 95 | 0 | 1068 |
| family ssh | 209 | 81 | 1 | 22 | 0 | 105 |
| product apache:http_server | 371 | 102 | 1 | 4 | 0 | 264 |
| product apache:tomcat | 276 | 84 | 0 | 11 | 0 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 6 | 0 | 0 | 0 | 4 |
| product crushftp:crushftp | 17 | 11 | 0 | 0 | 0 | 6 |
| product dovecot:dovecot | 69 | 35 | 1 | 4 | 0 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 11 | 0 | 2 | 0 | 7 |
| product exim:exim | 71 | 39 | 1 | 18 | 0 | 13 |
| product f5:nginx | 41 | 16 | 0 | 4 | 0 | 21 |
| product filezilla-project:filezilla_server | 7 | 3 | 0 | 0 | 0 | 4 |
| product freerdp:freerdp | 243 | 180 | 0 | 2 | 0 | 61 |
| product isc:bind | 184 | 78 | 0 | 2 | 0 | 104 |
| product libssh:libssh | 45 | 21 | 0 | 6 | 0 | 18 |
| product mariadb:mariadb | 431 | 154 | 1 | 56 | 0 | 220 |
| product microsoft:exchange_server | 268 | 54 | 5 | 15 | 0 | 194 |
| product microsoft:internet_information_services | 93 | 3 | 0 | 0 | 0 | 90 |
| product microsoft:sql_server | 110 | 14 | 0 | 1 | 0 | 95 |
| product mysql:mysql | 94 | 1 | 0 | 1 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 23 | 0 | 4 | 0 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 40 | 1 | 1 | 0 | 31 |
| product openbsd:openssh | 146 | 51 | 1 | 14 | 0 | 80 |
| product oracle:mysql | 1328 | 461 | 2 | 58 | 0 | 807 |
| product postfix:postfix | 12 | 3 | 0 | 1 | 0 | 8 |
| product postgresql:postgresql | 209 | 72 | 0 | 10 | 0 | 127 |
| product powerdns:authoritative | 31 | 26 | 0 | 0 | 0 | 5 |
| product powerdns:recursor | 50 | 33 | 0 | 0 | 0 | 17 |
| product proftpd:proftpd | 33 | 14 | 0 | 2 | 0 | 17 |
| product pureftpd:pure-ftpd | 11 | 6 | 0 | 0 | 0 | 5 |
| product samba:samba | 216 | 106 | 5 | 6 | 0 | 99 |
| product sendmail:sendmail | 33 | 3 | 0 | 0 | 0 | 30 |
| product solarwinds:serv-u | 55 | 32 | 0 | 1 | 0 | 22 |
| product thekelleys:dnsmasq | 39 | 31 | 0 | 0 | 0 | 8 |
| product wftpserver:wing_ftp_server | 20 | 8 | 0 | 3 | 0 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 2 | 0 | 1 | 0 | 2 |

### 2. AC

**(a) 1,473 included CVEs**

| group | n | L | H | no_d11_score |
|---|---|---|---|---|
| all | 1473 | 1197 | 276 | 0 |
| family dns | 158 | 121 | 37 | 0 |
| family ftp | 62 | 62 | 0 | 0 |
| family http | 189 | 154 | 35 | 0 |
| family mail | 125 | 111 | 14 | 0 |
| family rdp | 106 | 87 | 19 | 0 |
| family smb | 107 | 77 | 30 | 0 |
| family sql | 668 | 544 | 124 | 0 |
| family ssh | 58 | 41 | 17 | 0 |
| product apache:http_server | 87 | 74 | 13 | 0 |
| product apache:tomcat | 83 | 63 | 20 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 0 | 0 |
| product dovecot:dovecot | 28 | 22 | 6 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 10 | 2 | 0 |
| product exim:exim | 39 | 36 | 3 | 0 |
| product f5:nginx | 19 | 17 | 2 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 70 | 19 | 0 |
| product isc:bind | 72 | 55 | 17 | 0 |
| product libssh:libssh | 11 | 9 | 2 | 0 |
| product mariadb:mariadb | 200 | 158 | 42 | 0 |
| product microsoft:exchange_server | 54 | 49 | 5 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 |
| product microsoft:sql_server | 13 | 13 | 0 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 21 | 1 | 0 |
| product openbsd:openssh | 35 | 22 | 13 | 0 |
| product oracle:mysql | 516 | 411 | 105 | 0 |
| product postfix:postfix | 3 | 3 | 0 | 0 |
| product postgresql:postgresql | 70 | 54 | 16 | 0 |
| product powerdns:authoritative | 17 | 14 | 3 | 0 |
| product powerdns:recursor | 24 | 16 | 8 | 0 |
| product proftpd:proftpd | 12 | 12 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 |
| product samba:samba | 107 | 77 | 30 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 18 | 10 | 0 |
| product wftpserver:wing_ftp_server | 8 | 8 | 0 | 0 |


**(b) all snapshot records**

| group | n | L | H | no_d11_score |
|---|---|---|---|---|
| all | 4216 | 1500 | 316 | 2400 |
| family dns | 364 | 159 | 42 | 163 |
| family ftp | 159 | 86 | 2 | 71 |
| family http | 777 | 186 | 38 | 553 |
| family mail | 453 | 159 | 20 | 274 |
| family rdp | 280 | 184 | 25 | 71 |
| family smb | 216 | 84 | 33 | 99 |
| family sql | 1765 | 569 | 128 | 1068 |
| family ssh | 209 | 73 | 31 | 105 |
| product apache:http_server | 371 | 93 | 14 | 264 |
| product apache:tomcat | 276 | 74 | 21 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 6 | 0 | 4 |
| product crushftp:crushftp | 17 | 10 | 1 | 6 |
| product dovecot:dovecot | 69 | 31 | 9 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 10 | 3 | 7 |
| product exim:exim | 71 | 55 | 3 | 13 |
| product f5:nginx | 41 | 17 | 3 | 21 |
| product filezilla-project:filezilla_server | 7 | 2 | 1 | 4 |
| product freerdp:freerdp | 243 | 159 | 23 | 61 |
| product isc:bind | 184 | 61 | 19 | 104 |
| product libssh:libssh | 45 | 21 | 6 | 18 |
| product mariadb:mariadb | 431 | 168 | 43 | 220 |
| product microsoft:exchange_server | 268 | 67 | 7 | 194 |
| product microsoft:internet_information_services | 93 | 3 | 0 | 90 |
| product microsoft:sql_server | 110 | 15 | 0 | 95 |
| product mysql:mysql | 94 | 2 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 25 | 2 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 39 | 3 | 31 |
| product openbsd:openssh | 146 | 42 | 24 | 80 |
| product oracle:mysql | 1328 | 416 | 105 | 807 |
| product postfix:postfix | 12 | 4 | 0 | 8 |
| product postgresql:postgresql | 209 | 63 | 19 | 127 |
| product powerdns:authoritative | 31 | 23 | 3 | 5 |
| product powerdns:recursor | 50 | 24 | 9 | 17 |
| product proftpd:proftpd | 33 | 15 | 1 | 17 |
| product pureftpd:pure-ftpd | 11 | 6 | 0 | 5 |
| product samba:samba | 216 | 84 | 33 | 99 |
| product sendmail:sendmail | 33 | 2 | 1 | 30 |
| product solarwinds:serv-u | 55 | 33 | 0 | 22 |
| product thekelleys:dnsmasq | 39 | 21 | 10 | 8 |
| product wftpserver:wing_ftp_server | 20 | 11 | 0 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 0 | 2 |

### 2. PR

**(a) 1,473 included CVEs**

| group | n | N | L | H | no_d11_score |
|---|---|---|---|---|---|
| all | 1473 | 693 | 449 | 331 | 0 |
| family dns | 158 | 136 | 19 | 3 | 0 |
| family ftp | 62 | 39 | 20 | 3 | 0 |
| family http | 189 | 162 | 26 | 1 | 0 |
| family mail | 125 | 89 | 36 | 0 | 0 |
| family rdp | 106 | 62 | 28 | 16 | 0 |
| family smb | 107 | 45 | 59 | 3 | 0 |
| family sql | 668 | 122 | 241 | 305 | 0 |
| family ssh | 58 | 38 | 20 | 0 | 0 |
| product apache:http_server | 87 | 80 | 6 | 1 | 0 |
| product apache:tomcat | 83 | 67 | 16 | 0 | 0 |
| product cerberusftp:ftp_server | 5 | 3 | 2 | 0 | 0 |
| product crushftp:crushftp | 7 | 6 | 0 | 1 | 0 |
| product dovecot:dovecot | 28 | 20 | 8 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 7 | 5 | 0 | 0 |
| product exim:exim | 39 | 25 | 14 | 0 | 0 |
| product f5:nginx | 19 | 15 | 4 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 49 | 24 | 16 | 0 |
| product isc:bind | 72 | 60 | 9 | 3 | 0 |
| product libssh:libssh | 11 | 8 | 3 | 0 | 0 |
| product mariadb:mariadb | 200 | 54 | 89 | 57 | 0 |
| product microsoft:exchange_server | 54 | 41 | 13 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 5 | 8 | 0 | 0 |
| product mysql:mysql | 1 | 0 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 13 | 4 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 19 | 3 | 0 | 0 |
| product openbsd:openssh | 35 | 23 | 12 | 0 | 0 |
| product oracle:mysql | 516 | 53 | 166 | 297 | 0 |
| product postfix:postfix | 3 | 2 | 1 | 0 | 0 |
| product postgresql:postgresql | 70 | 22 | 42 | 6 | 0 |
| product powerdns:authoritative | 17 | 13 | 4 | 0 | 0 |
| product powerdns:recursor | 24 | 21 | 3 | 0 | 0 |
| product proftpd:proftpd | 12 | 9 | 2 | 1 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 | 0 |
| product samba:samba | 107 | 45 | 59 | 3 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 13 | 9 | 1 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 2 | 6 | 0 | 0 |


**(b) all snapshot records**

| group | n | N | L | H | no_d11_score |
|---|---|---|---|---|---|
| all | 4216 | 960 | 508 | 348 | 2400 |
| family dns | 364 | 173 | 22 | 6 | 163 |
| family ftp | 159 | 50 | 28 | 10 | 71 |
| family http | 777 | 193 | 29 | 2 | 553 |
| family mail | 453 | 128 | 51 | 0 | 274 |
| family rdp | 280 | 161 | 32 | 16 | 71 |
| family smb | 216 | 53 | 61 | 3 | 99 |
| family sql | 1765 | 132 | 254 | 311 | 1068 |
| family ssh | 209 | 73 | 31 | 0 | 105 |
| product apache:http_server | 371 | 97 | 9 | 1 | 264 |
| product apache:tomcat | 276 | 78 | 16 | 1 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 3 | 3 | 0 | 4 |
| product crushftp:crushftp | 17 | 10 | 0 | 1 | 6 |
| product dovecot:dovecot | 69 | 29 | 11 | 0 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 8 | 5 | 0 | 7 |
| product exim:exim | 71 | 40 | 18 | 0 | 13 |
| product f5:nginx | 41 | 16 | 4 | 0 | 21 |
| product filezilla-project:filezilla_server | 7 | 2 | 1 | 0 | 4 |
| product freerdp:freerdp | 243 | 140 | 26 | 16 | 61 |
| product isc:bind | 184 | 67 | 10 | 3 | 104 |
| product libssh:libssh | 45 | 18 | 9 | 0 | 18 |
| product mariadb:mariadb | 431 | 60 | 91 | 60 | 220 |
| product microsoft:exchange_server | 268 | 53 | 21 | 0 | 194 |
| product microsoft:internet_information_services | 93 | 3 | 0 | 0 | 90 |
| product microsoft:sql_server | 110 | 7 | 8 | 0 | 95 |
| product mysql:mysql | 94 | 0 | 1 | 1 | 92 |
| product neutrinolabs:xrdp | 37 | 21 | 6 | 0 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 39 | 3 | 0 | 31 |
| product openbsd:openssh | 146 | 49 | 17 | 0 | 80 |
| product oracle:mysql | 1328 | 53 | 168 | 300 | 807 |
| product postfix:postfix | 12 | 3 | 1 | 0 | 8 |
| product postgresql:postgresql | 209 | 24 | 52 | 6 | 127 |
| product powerdns:authoritative | 31 | 19 | 6 | 1 | 5 |
| product powerdns:recursor | 50 | 28 | 3 | 2 | 17 |
| product proftpd:proftpd | 33 | 11 | 4 | 1 | 17 |
| product pureftpd:pure-ftpd | 11 | 6 | 0 | 0 | 5 |
| product samba:samba | 216 | 53 | 61 | 3 | 99 |
| product sendmail:sendmail | 33 | 3 | 0 | 0 | 30 |
| product solarwinds:serv-u | 55 | 14 | 12 | 7 | 22 |
| product thekelleys:dnsmasq | 39 | 31 | 0 | 0 | 8 |
| product wftpserver:wing_ftp_server | 20 | 3 | 7 | 1 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 2 | 1 | 0 | 2 |

### 2. UI

**(a) 1,473 included CVEs**

| group | n | N | R | no_d11_score |
|---|---|---|---|---|
| all | 1473 | 1353 | 120 | 0 |
| family dns | 158 | 157 | 1 | 0 |
| family ftp | 62 | 46 | 16 | 0 |
| family http | 189 | 175 | 14 | 0 |
| family mail | 125 | 94 | 31 | 0 |
| family rdp | 106 | 93 | 13 | 0 |
| family smb | 107 | 100 | 7 | 0 |
| family sql | 668 | 636 | 32 | 0 |
| family ssh | 58 | 52 | 6 | 0 |
| product apache:http_server | 87 | 83 | 4 | 0 |
| product apache:tomcat | 83 | 74 | 9 | 0 |
| product cerberusftp:ftp_server | 5 | 3 | 2 | 0 |
| product crushftp:crushftp | 7 | 2 | 5 | 0 |
| product dovecot:dovecot | 28 | 28 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 0 | 0 |
| product exim:exim | 39 | 39 | 0 | 0 |
| product f5:nginx | 19 | 18 | 1 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 76 | 13 | 0 |
| product isc:bind | 72 | 72 | 0 | 0 |
| product libssh:libssh | 11 | 10 | 1 | 0 |
| product mariadb:mariadb | 200 | 192 | 8 | 0 |
| product microsoft:exchange_server | 54 | 23 | 31 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 |
| product microsoft:sql_server | 13 | 11 | 2 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 0 | 0 |
| product openbsd:openssh | 35 | 30 | 5 | 0 |
| product oracle:mysql | 516 | 494 | 22 | 0 |
| product postfix:postfix | 3 | 3 | 0 | 0 |
| product postgresql:postgresql | 70 | 64 | 6 | 0 |
| product powerdns:authoritative | 17 | 17 | 0 | 0 |
| product powerdns:recursor | 24 | 23 | 1 | 0 |
| product proftpd:proftpd | 12 | 12 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 |
| product samba:samba | 107 | 100 | 7 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 16 | 7 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 6 | 2 | 0 |


**(b) all snapshot records**

| group | n | N | R | no_d11_score |
|---|---|---|---|---|
| all | 4216 | 1645 | 171 | 2400 |
| family dns | 364 | 200 | 1 | 163 |
| family ftp | 159 | 68 | 20 | 71 |
| family http | 777 | 208 | 16 | 553 |
| family mail | 453 | 137 | 42 | 274 |
| family rdp | 280 | 180 | 29 | 71 |
| family smb | 216 | 110 | 7 | 99 |
| family sql | 1765 | 662 | 35 | 1068 |
| family ssh | 209 | 83 | 21 | 105 |
| product apache:http_server | 371 | 101 | 6 | 264 |
| product apache:tomcat | 276 | 86 | 9 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 4 | 2 | 4 |
| product crushftp:crushftp | 17 | 6 | 5 | 6 |
| product dovecot:dovecot | 69 | 40 | 0 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 13 | 0 | 7 |
| product exim:exim | 71 | 58 | 0 | 13 |
| product f5:nginx | 41 | 19 | 1 | 21 |
| product filezilla-project:filezilla_server | 7 | 3 | 0 | 4 |
| product freerdp:freerdp | 243 | 153 | 29 | 61 |
| product isc:bind | 184 | 80 | 0 | 104 |
| product libssh:libssh | 45 | 20 | 7 | 18 |
| product mariadb:mariadb | 431 | 202 | 9 | 220 |
| product microsoft:exchange_server | 268 | 32 | 42 | 194 |
| product microsoft:internet_information_services | 93 | 3 | 0 | 90 |
| product microsoft:sql_server | 110 | 12 | 3 | 95 |
| product mysql:mysql | 94 | 2 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 27 | 0 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 42 | 0 | 31 |
| product openbsd:openssh | 146 | 52 | 14 | 80 |
| product oracle:mysql | 1328 | 499 | 22 | 807 |
| product postfix:postfix | 12 | 4 | 0 | 8 |
| product postgresql:postgresql | 209 | 75 | 7 | 127 |
| product powerdns:authoritative | 31 | 26 | 0 | 5 |
| product powerdns:recursor | 50 | 32 | 1 | 17 |
| product proftpd:proftpd | 33 | 16 | 0 | 17 |
| product pureftpd:pure-ftpd | 11 | 6 | 0 | 5 |
| product samba:samba | 216 | 110 | 7 | 99 |
| product sendmail:sendmail | 33 | 3 | 0 | 30 |
| product solarwinds:serv-u | 55 | 24 | 9 | 22 |
| product thekelleys:dnsmasq | 39 | 31 | 0 | 8 |
| product wftpserver:wing_ftp_server | 20 | 7 | 4 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 0 | 2 |

### 2. S

**(a) 1,473 included CVEs**

| group | n | U | C | no_d11_score |
|---|---|---|---|---|
| all | 1473 | 1406 | 67 | 0 |
| family dns | 158 | 152 | 6 | 0 |
| family ftp | 62 | 45 | 17 | 0 |
| family http | 189 | 179 | 10 | 0 |
| family mail | 125 | 108 | 17 | 0 |
| family rdp | 106 | 106 | 0 | 0 |
| family smb | 107 | 107 | 0 | 0 |
| family sql | 668 | 653 | 15 | 0 |
| family ssh | 58 | 56 | 2 | 0 |
| product apache:http_server | 87 | 81 | 6 | 0 |
| product apache:tomcat | 83 | 79 | 4 | 0 |
| product cerberusftp:ftp_server | 5 | 3 | 2 | 0 |
| product crushftp:crushftp | 7 | 2 | 5 | 0 |
| product dovecot:dovecot | 28 | 28 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 11 | 1 | 0 |
| product exim:exim | 39 | 39 | 0 | 0 |
| product f5:nginx | 19 | 19 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 89 | 0 | 0 |
| product isc:bind | 72 | 68 | 4 | 0 |
| product libssh:libssh | 11 | 11 | 0 | 0 |
| product mariadb:mariadb | 200 | 193 | 7 | 0 |
| product microsoft:exchange_server | 54 | 37 | 17 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 |
| product microsoft:sql_server | 13 | 12 | 1 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 0 | 0 |
| product openbsd:openssh | 35 | 34 | 1 | 0 |
| product oracle:mysql | 516 | 504 | 12 | 0 |
| product postfix:postfix | 3 | 3 | 0 | 0 |
| product postgresql:postgresql | 70 | 69 | 1 | 0 |
| product powerdns:authoritative | 17 | 17 | 0 | 0 |
| product powerdns:recursor | 24 | 23 | 1 | 0 |
| product proftpd:proftpd | 12 | 12 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 |
| product samba:samba | 107 | 107 | 0 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 15 | 8 | 0 |
| product thekelleys:dnsmasq | 28 | 27 | 1 | 0 |
| product wftpserver:wing_ftp_server | 8 | 6 | 2 | 0 |


**(b) all snapshot records**

| group | n | U | C | no_d11_score |
|---|---|---|---|---|
| all | 4216 | 1729 | 87 | 2400 |
| family dns | 364 | 191 | 10 | 163 |
| family ftp | 159 | 67 | 21 | 71 |
| family http | 777 | 212 | 12 | 553 |
| family mail | 453 | 159 | 20 | 274 |
| family rdp | 280 | 208 | 1 | 71 |
| family smb | 216 | 115 | 2 | 99 |
| family sql | 1765 | 681 | 16 | 1068 |
| family ssh | 209 | 99 | 5 | 105 |
| product apache:http_server | 371 | 99 | 8 | 264 |
| product apache:tomcat | 276 | 91 | 4 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 4 | 2 | 4 |
| product crushftp:crushftp | 17 | 5 | 6 | 6 |
| product dovecot:dovecot | 69 | 40 | 0 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 12 | 1 | 7 |
| product exim:exim | 71 | 58 | 0 | 13 |
| product f5:nginx | 41 | 20 | 0 | 21 |
| product filezilla-project:filezilla_server | 7 | 3 | 0 | 4 |
| product freerdp:freerdp | 243 | 181 | 1 | 61 |
| product isc:bind | 184 | 75 | 5 | 104 |
| product libssh:libssh | 45 | 26 | 1 | 18 |
| product mariadb:mariadb | 431 | 203 | 8 | 220 |
| product microsoft:exchange_server | 268 | 54 | 20 | 194 |
| product microsoft:internet_information_services | 93 | 3 | 0 | 90 |
| product microsoft:sql_server | 110 | 14 | 1 | 95 |
| product mysql:mysql | 94 | 2 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 27 | 0 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 40 | 2 | 31 |
| product openbsd:openssh | 146 | 63 | 3 | 80 |
| product oracle:mysql | 1328 | 509 | 12 | 807 |
| product postfix:postfix | 12 | 4 | 0 | 8 |
| product postgresql:postgresql | 209 | 81 | 1 | 127 |
| product powerdns:authoritative | 31 | 25 | 1 | 5 |
| product powerdns:recursor | 50 | 32 | 1 | 17 |
| product proftpd:proftpd | 33 | 16 | 0 | 17 |
| product pureftpd:pure-ftpd | 11 | 6 | 0 | 5 |
| product samba:samba | 216 | 115 | 2 | 99 |
| product sendmail:sendmail | 33 | 3 | 0 | 30 |
| product solarwinds:serv-u | 55 | 23 | 10 | 22 |
| product thekelleys:dnsmasq | 39 | 30 | 1 | 8 |
| product wftpserver:wing_ftp_server | 20 | 8 | 3 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 0 | 2 |

### 2. C

**(a) 1,473 included CVEs**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 1473 | 438 | 161 | 874 | 0 |
| family dns | 158 | 32 | 7 | 119 | 0 |
| family ftp | 62 | 29 | 19 | 14 | 0 |
| family http | 189 | 76 | 29 | 84 | 0 |
| family mail | 125 | 61 | 25 | 39 | 0 |
| family rdp | 106 | 50 | 21 | 35 | 0 |
| family smb | 107 | 43 | 9 | 55 | 0 |
| family sql | 668 | 117 | 40 | 511 | 0 |
| family ssh | 58 | 30 | 11 | 17 | 0 |
| product apache:http_server | 87 | 28 | 10 | 49 | 0 |
| product apache:tomcat | 83 | 40 | 16 | 27 | 0 |
| product cerberusftp:ftp_server | 5 | 1 | 3 | 1 | 0 |
| product crushftp:crushftp | 7 | 2 | 5 | 0 | 0 |
| product dovecot:dovecot | 28 | 6 | 3 | 19 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 8 | 3 | 1 | 0 |
| product exim:exim | 39 | 30 | 0 | 9 | 0 |
| product f5:nginx | 19 | 7 | 3 | 9 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 35 | 20 | 34 | 0 |
| product isc:bind | 72 | 4 | 4 | 64 | 0 |
| product libssh:libssh | 11 | 3 | 1 | 7 | 0 |
| product mariadb:mariadb | 200 | 31 | 9 | 160 | 0 |
| product microsoft:exchange_server | 54 | 24 | 22 | 8 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 11 | 2 | 0 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 15 | 1 | 1 | 0 |
| product nlnetlabs:unbound | 22 | 9 | 1 | 12 | 0 |
| product openbsd:openssh | 35 | 19 | 7 | 9 | 0 |
| product oracle:mysql | 516 | 43 | 29 | 444 | 0 |
| product postfix:postfix | 3 | 1 | 0 | 2 | 0 |
| product postgresql:postgresql | 70 | 50 | 9 | 11 | 0 |
| product powerdns:authoritative | 17 | 2 | 1 | 14 | 0 |
| product powerdns:recursor | 24 | 4 | 1 | 19 | 0 |
| product proftpd:proftpd | 12 | 5 | 0 | 7 | 0 |
| product pureftpd:pure-ftpd | 6 | 3 | 0 | 3 | 0 |
| product samba:samba | 107 | 43 | 9 | 55 | 0 |
| product sendmail:sendmail | 1 | 0 | 0 | 1 | 0 |
| product solarwinds:serv-u | 23 | 12 | 8 | 3 | 0 |
| product thekelleys:dnsmasq | 28 | 13 | 0 | 15 | 0 |
| product wftpserver:wing_ftp_server | 8 | 6 | 2 | 0 | 0 |


**(b) all snapshot records**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 4216 | 609 | 196 | 1011 | 2400 |
| family dns | 364 | 40 | 7 | 154 | 163 |
| family ftp | 159 | 46 | 21 | 21 | 71 |
| family http | 777 | 91 | 36 | 97 | 553 |
| family mail | 453 | 93 | 34 | 52 | 274 |
| family rdp | 280 | 112 | 25 | 72 | 71 |
| family smb | 216 | 47 | 12 | 58 | 99 |
| family sql | 1765 | 137 | 44 | 516 | 1068 |
| family ssh | 209 | 45 | 17 | 42 | 105 |
| product apache:http_server | 371 | 38 | 13 | 56 | 264 |
| product apache:tomcat | 276 | 43 | 20 | 32 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 2 | 3 | 1 | 4 |
| product crushftp:crushftp | 17 | 5 | 5 | 1 | 6 |
| product dovecot:dovecot | 69 | 12 | 5 | 23 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 8 | 3 | 2 | 7 |
| product exim:exim | 71 | 43 | 3 | 12 | 13 |
| product f5:nginx | 41 | 8 | 3 | 9 | 21 |
| product filezilla-project:filezilla_server | 7 | 2 | 1 | 0 | 4 |
| product freerdp:freerdp | 243 | 88 | 24 | 70 | 61 |
| product isc:bind | 184 | 7 | 4 | 69 | 104 |
| product libssh:libssh | 45 | 6 | 4 | 17 | 18 |
| product mariadb:mariadb | 431 | 40 | 10 | 161 | 220 |
| product microsoft:exchange_server | 268 | 36 | 26 | 12 | 194 |
| product microsoft:internet_information_services | 93 | 2 | 0 | 1 | 90 |
| product microsoft:sql_server | 110 | 13 | 2 | 0 | 95 |
| product mysql:mysql | 94 | 2 | 0 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 24 | 1 | 2 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 12 | 1 | 29 | 31 |
| product openbsd:openssh | 146 | 31 | 10 | 25 | 80 |
| product oracle:mysql | 1328 | 44 | 30 | 447 | 807 |
| product postfix:postfix | 12 | 1 | 0 | 3 | 8 |
| product postgresql:postgresql | 209 | 58 | 12 | 12 | 127 |
| product powerdns:authoritative | 31 | 4 | 1 | 21 | 5 |
| product powerdns:recursor | 50 | 4 | 1 | 28 | 17 |
| product proftpd:proftpd | 33 | 7 | 0 | 9 | 17 |
| product pureftpd:pure-ftpd | 11 | 3 | 0 | 3 | 5 |
| product samba:samba | 216 | 47 | 12 | 58 | 99 |
| product sendmail:sendmail | 33 | 1 | 0 | 2 | 30 |
| product solarwinds:serv-u | 55 | 19 | 9 | 5 | 22 |
| product thekelleys:dnsmasq | 39 | 13 | 0 | 18 | 8 |
| product wftpserver:wing_ftp_server | 20 | 7 | 3 | 1 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 1 | 0 | 2 | 2 |

### 2. I

**(a) 1,473 included CVEs**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 1473 | 375 | 165 | 933 | 0 |
| family dns | 158 | 37 | 11 | 110 | 0 |
| family ftp | 62 | 20 | 18 | 24 | 0 |
| family http | 189 | 67 | 26 | 96 | 0 |
| family mail | 125 | 55 | 28 | 42 | 0 |
| family rdp | 106 | 33 | 5 | 68 | 0 |
| family smb | 107 | 45 | 9 | 53 | 0 |
| family sql | 668 | 93 | 61 | 514 | 0 |
| family ssh | 58 | 25 | 7 | 26 | 0 |
| product apache:http_server | 87 | 30 | 12 | 45 | 0 |
| product apache:tomcat | 83 | 31 | 13 | 39 | 0 |
| product cerberusftp:ftp_server | 5 | 1 | 3 | 1 | 0 |
| product crushftp:crushftp | 7 | 2 | 5 | 0 | 0 |
| product dovecot:dovecot | 28 | 5 | 1 | 22 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 6 | 1 | 5 | 0 |
| product exim:exim | 39 | 28 | 3 | 8 | 0 |
| product f5:nginx | 19 | 5 | 1 | 13 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 | 1 | 0 |
| product freerdp:freerdp | 89 | 23 | 4 | 62 | 0 |
| product isc:bind | 72 | 7 | 2 | 63 | 0 |
| product libssh:libssh | 11 | 2 | 1 | 8 | 0 |
| product mariadb:mariadb | 200 | 25 | 19 | 156 | 0 |
| product microsoft:exchange_server | 54 | 21 | 21 | 12 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 8 | 2 | 3 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 10 | 1 | 6 | 0 |
| product nlnetlabs:unbound | 22 | 8 | 2 | 12 | 0 |
| product openbsd:openssh | 35 | 17 | 5 | 13 | 0 |
| product oracle:mysql | 516 | 29 | 56 | 431 | 0 |
| product postfix:postfix | 3 | 1 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 45 | 2 | 23 | 0 |
| product powerdns:authoritative | 17 | 4 | 1 | 12 | 0 |
| product powerdns:recursor | 24 | 7 | 2 | 15 | 0 |
| product proftpd:proftpd | 12 | 5 | 0 | 7 | 0 |
| product pureftpd:pure-ftpd | 6 | 1 | 0 | 5 | 0 |
| product samba:samba | 107 | 45 | 9 | 53 | 0 |
| product sendmail:sendmail | 1 | 0 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 6 | 8 | 9 | 0 |
| product thekelleys:dnsmasq | 28 | 13 | 4 | 11 | 0 |
| product wftpserver:wing_ftp_server | 8 | 5 | 2 | 1 | 0 |


**(b) all snapshot records**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 4216 | 526 | 206 | 1084 | 2400 |
| family dns | 364 | 48 | 12 | 141 | 163 |
| family ftp | 159 | 37 | 22 | 29 | 71 |
| family http | 777 | 78 | 30 | 116 | 553 |
| family mail | 453 | 81 | 33 | 65 | 274 |
| family rdp | 280 | 83 | 10 | 116 | 71 |
| family smb | 216 | 49 | 11 | 57 | 99 |
| family sql | 1765 | 109 | 66 | 522 | 1068 |
| family ssh | 209 | 44 | 22 | 38 | 105 |
| product apache:http_server | 371 | 36 | 14 | 57 | 264 |
| product apache:tomcat | 276 | 35 | 15 | 45 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 2 | 3 | 1 | 4 |
| product crushftp:crushftp | 17 | 6 | 5 | 0 | 6 |
| product dovecot:dovecot | 69 | 7 | 1 | 32 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 7 | 1 | 5 | 7 |
| product exim:exim | 71 | 39 | 4 | 15 | 13 |
| product f5:nginx | 41 | 6 | 1 | 13 | 21 |
| product filezilla-project:filezilla_server | 7 | 1 | 0 | 2 | 4 |
| product freerdp:freerdp | 243 | 67 | 8 | 107 | 61 |
| product isc:bind | 184 | 10 | 2 | 68 | 104 |
| product libssh:libssh | 45 | 7 | 4 | 16 | 18 |
| product mariadb:mariadb | 431 | 33 | 21 | 157 | 220 |
| product microsoft:exchange_server | 268 | 33 | 25 | 16 | 194 |
| product microsoft:internet_information_services | 93 | 1 | 0 | 2 | 90 |
| product microsoft:sql_server | 110 | 9 | 2 | 4 | 95 |
| product mysql:mysql | 94 | 1 | 0 | 1 | 92 |
| product neutrinolabs:xrdp | 37 | 16 | 2 | 9 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 14 | 3 | 25 | 31 |
| product openbsd:openssh | 146 | 32 | 17 | 17 | 80 |
| product oracle:mysql | 1328 | 30 | 57 | 434 | 807 |
| product postfix:postfix | 12 | 1 | 2 | 1 | 8 |
| product postgresql:postgresql | 209 | 51 | 5 | 26 | 127 |
| product powerdns:authoritative | 31 | 5 | 1 | 20 | 5 |
| product powerdns:recursor | 50 | 7 | 2 | 24 | 17 |
| product proftpd:proftpd | 33 | 8 | 0 | 8 | 17 |
| product pureftpd:pure-ftpd | 11 | 1 | 0 | 5 | 5 |
| product samba:samba | 216 | 49 | 11 | 57 | 99 |
| product sendmail:sendmail | 33 | 1 | 1 | 1 | 30 |
| product solarwinds:serv-u | 55 | 13 | 10 | 10 | 22 |
| product thekelleys:dnsmasq | 39 | 14 | 4 | 13 | 8 |
| product wftpserver:wing_ftp_server | 20 | 6 | 4 | 1 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 1 | 0 | 2 | 2 |

### 2. A

**(a) 1,473 included CVEs**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 1473 | 1045 | 76 | 352 | 0 |
| family dns | 158 | 124 | 8 | 26 | 0 |
| family ftp | 62 | 23 | 1 | 38 | 0 |
| family http | 189 | 111 | 10 | 68 | 0 |
| family mail | 125 | 71 | 5 | 49 | 0 |
| family rdp | 106 | 64 | 35 | 7 | 0 |
| family smb | 107 | 62 | 4 | 41 | 0 |
| family sql | 668 | 563 | 9 | 96 | 0 |
| family ssh | 58 | 27 | 4 | 27 | 0 |
| product apache:http_server | 87 | 59 | 5 | 23 | 0 |
| product apache:tomcat | 83 | 38 | 3 | 42 | 0 |
| product cerberusftp:ftp_server | 5 | 1 | 0 | 4 | 0 |
| product crushftp:crushftp | 7 | 2 | 0 | 5 | 0 |
| product dovecot:dovecot | 28 | 18 | 5 | 5 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 5 | 0 | 7 | 0 |
| product exim:exim | 39 | 32 | 0 | 7 | 0 |
| product f5:nginx | 19 | 14 | 2 | 3 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 | 1 | 0 |
| product freerdp:freerdp | 89 | 49 | 34 | 6 | 0 |
| product isc:bind | 72 | 61 | 3 | 8 | 0 |
| product libssh:libssh | 11 | 6 | 2 | 3 | 0 |
| product mariadb:mariadb | 200 | 176 | 3 | 21 | 0 |
| product microsoft:exchange_server | 54 | 20 | 0 | 34 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 8 | 1 | 4 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 15 | 1 | 1 | 0 |
| product nlnetlabs:unbound | 22 | 17 | 1 | 4 | 0 |
| product openbsd:openssh | 35 | 16 | 2 | 17 | 0 |
| product oracle:mysql | 516 | 445 | 8 | 63 | 0 |
| product postfix:postfix | 3 | 1 | 0 | 2 | 0 |
| product postgresql:postgresql | 70 | 43 | 0 | 27 | 0 |
| product powerdns:authoritative | 17 | 13 | 1 | 3 | 0 |
| product powerdns:recursor | 24 | 15 | 2 | 7 | 0 |
| product proftpd:proftpd | 12 | 6 | 0 | 6 | 0 |
| product pureftpd:pure-ftpd | 6 | 4 | 0 | 2 | 0 |
| product samba:samba | 107 | 62 | 4 | 41 | 0 |
| product sendmail:sendmail | 1 | 0 | 0 | 1 | 0 |
| product solarwinds:serv-u | 23 | 5 | 1 | 17 | 0 |
| product thekelleys:dnsmasq | 28 | 21 | 1 | 6 | 0 |
| product wftpserver:wing_ftp_server | 8 | 5 | 0 | 3 | 0 |


**(b) all snapshot records**

| group | n | H | L | N | no_d11_score |
|---|---|---|---|---|---|
| all | 4216 | 1276 | 99 | 441 | 2400 |
| family dns | 364 | 156 | 13 | 32 | 163 |
| family ftp | 159 | 40 | 2 | 46 | 71 |
| family http | 777 | 128 | 12 | 84 | 553 |
| family mail | 453 | 101 | 7 | 71 | 274 |
| family rdp | 280 | 157 | 41 | 11 | 71 |
| family smb | 216 | 65 | 5 | 47 | 99 |
| family sql | 1765 | 580 | 9 | 108 | 1068 |
| family ssh | 209 | 49 | 10 | 45 | 105 |
| product apache:http_server | 371 | 71 | 5 | 31 | 264 |
| product apache:tomcat | 276 | 42 | 5 | 48 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 2 | 0 | 4 | 4 |
| product crushftp:crushftp | 17 | 5 | 0 | 6 | 6 |
| product dovecot:dovecot | 69 | 21 | 6 | 13 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 5 | 0 | 8 | 7 |
| product exim:exim | 71 | 45 | 1 | 12 | 13 |
| product f5:nginx | 41 | 14 | 2 | 4 | 21 |
| product filezilla-project:filezilla_server | 7 | 0 | 0 | 3 | 4 |
| product freerdp:freerdp | 243 | 135 | 37 | 10 | 61 |
| product isc:bind | 184 | 67 | 3 | 10 | 104 |
| product libssh:libssh | 45 | 16 | 5 | 6 | 18 |
| product mariadb:mariadb | 431 | 182 | 3 | 26 | 220 |
| product microsoft:exchange_server | 268 | 32 | 0 | 42 | 194 |
| product microsoft:internet_information_services | 93 | 2 | 0 | 1 | 90 |
| product microsoft:sql_server | 110 | 9 | 1 | 5 | 95 |
| product mysql:mysql | 94 | 1 | 0 | 1 | 92 |
| product neutrinolabs:xrdp | 37 | 22 | 4 | 1 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 30 | 6 | 6 | 31 |
| product openbsd:openssh | 146 | 28 | 5 | 33 | 80 |
| product oracle:mysql | 1328 | 449 | 8 | 64 | 807 |
| product postfix:postfix | 12 | 2 | 0 | 2 | 8 |
| product postgresql:postgresql | 209 | 49 | 0 | 33 | 127 |
| product powerdns:authoritative | 31 | 21 | 1 | 4 | 5 |
| product powerdns:recursor | 50 | 24 | 2 | 7 | 17 |
| product proftpd:proftpd | 33 | 9 | 0 | 7 | 17 |
| product pureftpd:pure-ftpd | 11 | 4 | 0 | 2 | 5 |
| product samba:samba | 216 | 65 | 5 | 47 | 99 |
| product sendmail:sendmail | 33 | 1 | 0 | 2 | 30 |
| product solarwinds:serv-u | 55 | 11 | 1 | 21 | 22 |
| product thekelleys:dnsmasq | 39 | 23 | 1 | 7 | 8 |
| product wftpserver:wing_ftp_server | 20 | 6 | 1 | 4 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 0 | 0 | 2 |

### 2. Joint (AV, PR, UI)

**(a) 1,473 included CVEs**

| group | n | A/H/N | A/L/N | A/L/R | A/N/N | L/H/N | L/H/R | L/L/N | L/L/R | L/N/N | L/N/R | N/H/N | N/H/R | N/L/N | N/L/R | N/N/N | N/N/R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1473 | 1 | 6 | 1 | 5 | 14 | 6 | 116 | 5 | 5 | 14 | 307 | 3 | 297 | 24 | 602 | 67 |
| family dns | 158 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 3 | 0 | 17 | 0 | 135 | 1 |
| family ftp | 62 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 2 | 1 | 10 | 5 | 29 | 10 |
| family http | 189 | 0 | 0 | 0 | 1 | 0 | 0 | 15 | 0 | 0 | 1 | 1 | 0 | 11 | 0 | 147 | 13 |
| family mail | 125 | 0 | 5 | 0 | 0 | 0 | 0 | 17 | 0 | 1 | 6 | 0 | 0 | 12 | 2 | 59 | 23 |
| family rdp | 106 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 16 | 0 | 14 | 11 | 59 | 2 |
| family smb | 107 | 0 | 0 | 0 | 4 | 0 | 0 | 5 | 0 | 0 | 1 | 3 | 0 | 54 | 0 | 34 | 6 |
| family sql | 668 | 1 | 1 | 0 | 0 | 14 | 6 | 59 | 5 | 3 | 6 | 282 | 2 | 171 | 5 | 105 | 8 |
| family ssh | 58 | 0 | 0 | 1 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 34 | 4 |
| product apache:http_server | 87 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 4 | 0 | 75 | 4 |
| product apache:tomcat | 83 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 58 | 9 |
| product cerberusftp:ftp_server | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 2 |
| product crushftp:crushftp | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 4 |
| product dovecot:dovecot | 28 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 20 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 7 | 0 |
| product exim:exim | 39 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 24 | 0 |
| product f5:nginx | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 14 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 16 | 0 | 12 | 11 | 47 | 2 |
| product isc:bind | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 8 | 0 | 60 | 0 |
| product libssh:libssh | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 7 | 1 |
| product mariadb:mariadb | 200 | 0 | 1 | 0 | 0 | 7 | 4 | 39 | 1 | 1 | 3 | 46 | 0 | 48 | 0 | 50 | 0 |
| product microsoft:exchange_server | 54 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 6 | 2 | 12 | 23 |
| product microsoft:internet_information_services | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| product microsoft:sql_server | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 8 | 0 | 3 | 1 |
| product mysql:mysql | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | 12 | 0 |
| product nlnetlabs:unbound | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 19 | 0 |
| product openbsd:openssh | 35 | 0 | 0 | 1 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 20 | 3 |
| product oracle:mysql | 516 | 1 | 1 | 0 | 0 | 12 | 6 | 30 | 3 | 3 | 3 | 276 | 2 | 130 | 2 | 41 | 6 |
| product postfix:postfix | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| product postgresql:postgresql | 70 | 0 | 0 | 0 | 0 | 2 | 0 | 6 | 2 | 0 | 0 | 4 | 0 | 31 | 3 | 21 | 1 |
| product powerdns:authoritative | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 13 | 0 |
| product powerdns:recursor | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 20 | 1 |
| product proftpd:proftpd | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 9 | 0 |
| product pureftpd:pure-ftpd | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| product samba:samba | 107 | 0 | 0 | 0 | 4 | 0 | 0 | 5 | 0 | 0 | 1 | 3 | 0 | 54 | 0 | 34 | 6 |
| product sendmail:sendmail | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| product solarwinds:serv-u | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 4 | 4 | 10 | 3 |
| product thekelleys:dnsmasq | 28 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 28 | 0 |
| product wftpserver:wing_ftp_server | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 1 |


**(b) all snapshot records**

| group | n | A/H/N | A/L/N | A/L/R | A/N/N | L/H/N | L/H/R | L/L/N | L/L/R | L/N/N | L/N/R | N/H/N | N/H/R | N/L/N | N/L/R | N/N/N | N/N/R | no_d11_score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4216 | 1 | 6 | 1 | 9 | 15 | 6 | 135 | 9 | 5 | 26 | 323 | 3 | 328 | 29 | 823 | 97 | 2400 |
| family dns | 364 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 6 | 0 | 19 | 0 | 171 | 1 | 163 |
| family ftp | 159 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 9 | 1 | 13 | 8 | 39 | 11 | 71 |
| family http | 777 | 0 | 0 | 0 | 1 | 1 | 0 | 17 | 0 | 0 | 1 | 1 | 0 | 12 | 0 | 176 | 15 | 553 |
| family mail | 453 | 0 | 5 | 0 | 2 | 0 | 0 | 24 | 0 | 1 | 13 | 0 | 0 | 19 | 3 | 86 | 26 | 274 |
| family rdp | 280 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 | 1 | 0 | 16 | 0 | 16 | 11 | 143 | 17 | 71 |
| family smb | 216 | 0 | 0 | 0 | 5 | 0 | 0 | 5 | 0 | 0 | 1 | 3 | 0 | 56 | 0 | 41 | 6 | 99 |
| family sql | 1765 | 1 | 1 | 0 | 0 | 14 | 6 | 60 | 5 | 3 | 7 | 288 | 2 | 182 | 6 | 113 | 9 | 1068 |
| family ssh | 209 | 0 | 0 | 1 | 0 | 0 | 0 | 15 | 3 | 0 | 4 | 0 | 0 | 11 | 1 | 57 | 12 | 105 |
| product apache:http_server | 371 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0 | 1 | 0 | 5 | 0 | 90 | 6 | 264 |
| product apache:tomcat | 276 | 0 | 0 | 0 | 0 | 1 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 69 | 9 | 181 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 1 | 2 | 4 |
| product crushftp:crushftp | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 6 | 4 | 6 |
| product dovecot:dovecot | 69 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 28 | 0 | 29 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 8 | 0 | 7 |
| product exim:exim | 71 | 0 | 0 | 0 | 1 | 0 | 0 | 17 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 38 | 0 | 13 |
| product f5:nginx | 41 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 15 | 0 | 21 |
| product filezilla-project:filezilla_server | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 4 |
| product freerdp:freerdp | 243 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 16 | 0 | 13 | 11 | 123 | 17 | 61 |
| product isc:bind | 184 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 3 | 0 | 8 | 0 | 67 | 0 | 104 |
| product libssh:libssh | 45 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 | 0 | 1 | 0 | 0 | 4 | 0 | 14 | 3 | 18 |
| product mariadb:mariadb | 431 | 0 | 1 | 0 | 0 | 7 | 4 | 39 | 1 | 1 | 4 | 49 | 0 | 50 | 0 | 55 | 0 | 220 |
| product microsoft:exchange_server | 268 | 0 | 5 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 13 | 0 | 0 | 11 | 3 | 14 | 26 | 194 |
| product microsoft:internet_information_services | 93 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 90 |
| product microsoft:sql_server | 110 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 8 | 0 | 4 | 2 | 95 |
| product mysql:mysql | 94 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 92 |
| product neutrinolabs:xrdp | 37 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 20 | 0 | 10 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 38 | 0 | 31 |
| product openbsd:openssh | 146 | 0 | 0 | 1 | 0 | 0 | 0 | 11 | 0 | 0 | 3 | 0 | 0 | 4 | 1 | 37 | 9 | 80 |
| product oracle:mysql | 1328 | 1 | 1 | 0 | 0 | 12 | 6 | 31 | 3 | 3 | 3 | 279 | 2 | 131 | 2 | 41 | 6 | 807 |
| product postfix:postfix | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 8 |
| product postgresql:postgresql | 209 | 0 | 0 | 0 | 0 | 2 | 0 | 6 | 2 | 0 | 0 | 4 | 0 | 40 | 4 | 23 | 1 | 127 |
| product powerdns:authoritative | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 6 | 0 | 19 | 0 | 5 |
| product powerdns:recursor | 50 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 | 0 | 27 | 1 | 17 |
| product proftpd:proftpd | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 11 | 0 | 17 |
| product pureftpd:pure-ftpd | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 5 |
| product samba:samba | 216 | 0 | 0 | 0 | 5 | 0 | 0 | 5 | 0 | 0 | 1 | 3 | 0 | 56 | 0 | 41 | 6 | 99 |
| product sendmail:sendmail | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 30 |
| product solarwinds:serv-u | 55 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 7 | 0 | 5 | 6 | 11 | 3 | 22 |
| product thekelleys:dnsmasq | 39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 0 | 8 |
| product wftpserver:wing_ftp_server | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 2 | 2 | 1 | 2 | 9 |
| product xlightftpd:xlight_ftp_server | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 |

## 3. vulnStatus distribution (and CISA KEV fields present)
### 3. vulnStatus

**(a) 1,473 included CVEs**

| group | n | Analyzed | Modified |
|---|---|---|---|
| all | 1473 | 41 | 1432 |
| family dns | 158 | 1 | 157 |
| family ftp | 62 | 2 | 60 |
| family http | 189 | 23 | 166 |
| family mail | 125 | 8 | 117 |
| family rdp | 106 | 0 | 106 |
| family smb | 107 | 5 | 102 |
| family sql | 668 | 2 | 666 |
| family ssh | 58 | 0 | 58 |
| product apache:http_server | 87 | 16 | 71 |
| product apache:tomcat | 83 | 6 | 77 |
| product cerberusftp:ftp_server | 5 | 0 | 5 |
| product crushftp:crushftp | 7 | 0 | 7 |
| product dovecot:dovecot | 28 | 1 | 27 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 0 | 12 |
| product exim:exim | 39 | 4 | 35 |
| product f5:nginx | 19 | 1 | 18 |
| product filezilla-project:filezilla_server | 1 | 0 | 1 |
| product freerdp:freerdp | 89 | 0 | 89 |
| product isc:bind | 72 | 0 | 72 |
| product libssh:libssh | 11 | 0 | 11 |
| product mariadb:mariadb | 200 | 0 | 200 |
| product microsoft:exchange_server | 54 | 3 | 51 |
| product microsoft:internet_information_services | 1 | 1 | 0 |
| product microsoft:sql_server | 13 | 2 | 11 |
| product mysql:mysql | 1 | 0 | 1 |
| product neutrinolabs:xrdp | 17 | 0 | 17 |
| product nlnetlabs:unbound | 22 | 1 | 21 |
| product openbsd:openssh | 35 | 0 | 35 |
| product oracle:mysql | 516 | 0 | 516 |
| product postfix:postfix | 3 | 0 | 3 |
| product postgresql:postgresql | 70 | 0 | 70 |
| product powerdns:authoritative | 17 | 0 | 17 |
| product powerdns:recursor | 24 | 0 | 24 |
| product proftpd:proftpd | 12 | 0 | 12 |
| product pureftpd:pure-ftpd | 6 | 0 | 6 |
| product samba:samba | 107 | 5 | 102 |
| product sendmail:sendmail | 1 | 0 | 1 |
| product solarwinds:serv-u | 23 | 2 | 21 |
| product thekelleys:dnsmasq | 28 | 0 | 28 |
| product wftpserver:wing_ftp_server | 8 | 0 | 8 |


**(b) all snapshot records**

| group | n | Analyzed | Modified | Undergoing Analysis |
|---|---|---|---|---|
| all | 4216 | 572 | 3643 | 1 |
| family dns | 364 | 71 | 292 | 1 |
| family ftp | 159 | 59 | 100 | 0 |
| family http | 777 | 114 | 663 | 0 |
| family mail | 453 | 89 | 364 | 0 |
| family rdp | 280 | 133 | 147 | 0 |
| family smb | 216 | 7 | 209 | 0 |
| family sql | 1765 | 69 | 1696 | 0 |
| family ssh | 209 | 30 | 179 | 0 |
| product apache:http_server | 371 | 65 | 306 | 0 |
| product apache:tomcat | 276 | 47 | 229 | 0 |
| product beasts:vsftpd | 2 | 0 | 2 | 0 |
| product cerberusftp:ftp_server | 10 | 1 | 9 | 0 |
| product crushftp:crushftp | 17 | 7 | 10 | 0 |
| product dovecot:dovecot | 69 | 10 | 59 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 20 | 0 |
| product exim:exim | 71 | 21 | 50 | 0 |
| product f5:nginx | 41 | 2 | 39 | 0 |
| product filezilla-project:filezilla_server | 7 | 1 | 6 | 0 |
| product freerdp:freerdp | 243 | 114 | 129 | 0 |
| product isc:bind | 184 | 6 | 178 | 0 |
| product libssh:libssh | 45 | 6 | 39 | 0 |
| product mariadb:mariadb | 431 | 24 | 407 | 0 |
| product microsoft:exchange_server | 268 | 58 | 210 | 0 |
| product microsoft:internet_information_services | 93 | 1 | 92 | 0 |
| product microsoft:sql_server | 110 | 3 | 107 | 0 |
| product mysql:mysql | 94 | 0 | 94 | 0 |
| product neutrinolabs:xrdp | 37 | 19 | 18 | 0 |
| product nginx:nginx | 2 | 0 | 2 | 0 |
| product nlnetlabs:unbound | 73 | 39 | 33 | 1 |
| product openbsd:openssh | 146 | 24 | 122 | 0 |
| product oracle:mysql | 1328 | 34 | 1294 | 0 |
| product postfix:postfix | 12 | 0 | 12 | 0 |
| product postgresql:postgresql | 209 | 9 | 200 | 0 |
| product powerdns:authoritative | 31 | 11 | 20 | 0 |
| product powerdns:recursor | 50 | 16 | 34 | 0 |
| product proftpd:proftpd | 33 | 7 | 26 | 0 |
| product pureftpd:pure-ftpd | 11 | 1 | 10 | 0 |
| product samba:samba | 216 | 7 | 209 | 0 |
| product sendmail:sendmail | 33 | 0 | 33 | 0 |
| product solarwinds:serv-u | 55 | 31 | 24 | 0 |
| product thekelleys:dnsmasq | 39 | 2 | 37 | 0 |
| product wftpserver:wing_ftp_server | 20 | 9 | 11 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 2 | 3 | 0 |

### 3b. Records with a `cisaExploitAdd` field

**(a) 1,473 included CVEs**

| group | n | kev | no_kev |
|---|---|---|---|
| all | 1473 | 21 | 1452 |
| family dns | 158 | 0 | 158 |
| family ftp | 62 | 2 | 60 |
| family http | 189 | 10 | 179 |
| family mail | 125 | 6 | 119 |
| family rdp | 106 | 0 | 106 |
| family smb | 107 | 1 | 106 |
| family sql | 668 | 2 | 666 |
| family ssh | 58 | 0 | 58 |
| product apache:http_server | 87 | 4 | 83 |
| product apache:tomcat | 83 | 5 | 78 |
| product cerberusftp:ftp_server | 5 | 0 | 5 |
| product crushftp:crushftp | 7 | 0 | 7 |
| product dovecot:dovecot | 28 | 0 | 28 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 0 | 12 |
| product exim:exim | 39 | 3 | 36 |
| product f5:nginx | 19 | 1 | 18 |
| product filezilla-project:filezilla_server | 1 | 0 | 1 |
| product freerdp:freerdp | 89 | 0 | 89 |
| product isc:bind | 72 | 0 | 72 |
| product libssh:libssh | 11 | 0 | 11 |
| product mariadb:mariadb | 200 | 0 | 200 |
| product microsoft:exchange_server | 54 | 3 | 51 |
| product microsoft:internet_information_services | 1 | 1 | 0 |
| product microsoft:sql_server | 13 | 2 | 11 |
| product mysql:mysql | 1 | 0 | 1 |
| product neutrinolabs:xrdp | 17 | 0 | 17 |
| product nlnetlabs:unbound | 22 | 0 | 22 |
| product openbsd:openssh | 35 | 0 | 35 |
| product oracle:mysql | 516 | 0 | 516 |
| product postfix:postfix | 3 | 0 | 3 |
| product postgresql:postgresql | 70 | 0 | 70 |
| product powerdns:authoritative | 17 | 0 | 17 |
| product powerdns:recursor | 24 | 0 | 24 |
| product proftpd:proftpd | 12 | 0 | 12 |
| product pureftpd:pure-ftpd | 6 | 0 | 6 |
| product samba:samba | 107 | 1 | 106 |
| product sendmail:sendmail | 1 | 0 | 1 |
| product solarwinds:serv-u | 23 | 2 | 21 |
| product thekelleys:dnsmasq | 28 | 0 | 28 |
| product wftpserver:wing_ftp_server | 8 | 0 | 8 |


**(b) all snapshot records**

| group | n | kev | no_kev |
|---|---|---|---|
| all | 4216 | 55 | 4161 |
| family dns | 364 | 1 | 363 |
| family ftp | 159 | 11 | 148 |
| family http | 777 | 13 | 764 |
| family mail | 453 | 25 | 428 |
| family rdp | 280 | 0 | 280 |
| family smb | 216 | 2 | 214 |
| family sql | 1765 | 3 | 1762 |
| family ssh | 209 | 0 | 209 |
| product apache:http_server | 371 | 5 | 366 |
| product apache:tomcat | 276 | 7 | 269 |
| product beasts:vsftpd | 2 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 0 | 10 |
| product crushftp:crushftp | 17 | 3 | 14 |
| product dovecot:dovecot | 69 | 0 | 69 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 20 |
| product exim:exim | 71 | 5 | 66 |
| product f5:nginx | 41 | 1 | 40 |
| product filezilla-project:filezilla_server | 7 | 1 | 6 |
| product freerdp:freerdp | 243 | 0 | 243 |
| product isc:bind | 184 | 1 | 183 |
| product libssh:libssh | 45 | 0 | 45 |
| product mariadb:mariadb | 431 | 0 | 431 |
| product microsoft:exchange_server | 268 | 20 | 248 |
| product microsoft:internet_information_services | 93 | 1 | 92 |
| product microsoft:sql_server | 110 | 3 | 107 |
| product mysql:mysql | 94 | 0 | 94 |
| product neutrinolabs:xrdp | 37 | 0 | 37 |
| product nginx:nginx | 2 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 0 | 73 |
| product openbsd:openssh | 146 | 0 | 146 |
| product oracle:mysql | 1328 | 0 | 1328 |
| product postfix:postfix | 12 | 0 | 12 |
| product postgresql:postgresql | 209 | 0 | 209 |
| product powerdns:authoritative | 31 | 0 | 31 |
| product powerdns:recursor | 50 | 0 | 50 |
| product proftpd:proftpd | 33 | 1 | 32 |
| product pureftpd:pure-ftpd | 11 | 0 | 11 |
| product samba:samba | 216 | 2 | 214 |
| product sendmail:sendmail | 33 | 0 | 33 |
| product solarwinds:serv-u | 55 | 4 | 51 |
| product thekelleys:dnsmasq | 39 | 0 | 39 |
| product wftpserver:wing_ftp_server | 20 | 2 | 18 |
| product xlightftpd:xlight_ftp_server | 5 | 0 | 5 |

## 4. CWE
### 4a. CWE source and type (per CVE; columns are not exclusive)

**(a) 1,473 included CVEs**

| group | n | no_weakness | has_type_Primary | has_type_Secondary | has_nvd_source | has_cna_source | NVD-CWE-Other | NVD-CWE-noinfo | only_NVD-CWE-* | grouping_or_view | unknown_id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1473 | 0 | 1382 | 436 | 1420 | 436 | 30 | 603 | 572 | 40 | 0 |
| family dns | 158 | 0 | 151 | 46 | 155 | 46 | 3 | 16 | 9 | 3 | 0 |
| family ftp | 62 | 0 | 62 | 16 | 62 | 16 | 2 | 6 | 4 | 1 | 0 |
| family http | 189 | 0 | 163 | 84 | 178 | 84 | 8 | 21 | 22 | 8 | 0 |
| family mail | 125 | 0 | 122 | 18 | 125 | 18 | 6 | 20 | 21 | 4 | 0 |
| family rdp | 106 | 0 | 80 | 81 | 80 | 81 | 1 | 2 | 1 | 1 | 0 |
| family smb | 107 | 0 | 95 | 82 | 103 | 82 | 2 | 10 | 1 | 9 | 0 |
| family sql | 668 | 0 | 651 | 71 | 659 | 71 | 2 | 525 | 509 | 10 | 0 |
| family ssh | 58 | 0 | 58 | 38 | 58 | 38 | 6 | 3 | 5 | 4 | 0 |
| product apache:http_server | 87 | 0 | 77 | 42 | 81 | 42 | 4 | 6 | 8 | 3 | 0 |
| product apache:tomcat | 83 | 0 | 71 | 30 | 78 | 30 | 3 | 15 | 14 | 5 | 0 |
| product cerberusftp:ftp_server | 5 | 0 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 7 | 0 | 7 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 28 | 0 | 28 | 5 | 28 | 5 | 1 | 3 | 3 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 0 | 12 | 2 | 12 | 2 | 1 | 1 | 2 | 0 | 0 |
| product exim:exim | 39 | 0 | 36 | 6 | 39 | 6 | 4 | 1 | 5 | 3 | 0 |
| product f5:nginx | 19 | 0 | 15 | 12 | 19 | 12 | 1 | 1 | 0 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 0 | 72 | 67 | 72 | 67 | 1 | 1 | 1 | 0 | 0 |
| product isc:bind | 72 | 0 | 72 | 9 | 72 | 9 | 0 | 8 | 5 | 1 | 0 |
| product libssh:libssh | 11 | 0 | 11 | 8 | 11 | 8 | 1 | 0 | 1 | 0 | 0 |
| product mariadb:mariadb | 200 | 0 | 196 | 10 | 196 | 10 | 1 | 147 | 146 | 2 | 0 |
| product microsoft:exchange_server | 54 | 0 | 54 | 7 | 54 | 7 | 0 | 15 | 11 | 1 | 0 |
| product microsoft:internet_information_services | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 0 | 13 | 4 | 13 | 4 | 0 | 4 | 1 | 4 | 0 |
| product mysql:mysql | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 0 | 8 | 14 | 8 | 14 | 0 | 1 | 0 | 1 | 0 |
| product nlnetlabs:unbound | 22 | 0 | 22 | 4 | 22 | 4 | 0 | 0 | 0 | 0 | 0 |
| product openbsd:openssh | 35 | 0 | 35 | 28 | 35 | 28 | 4 | 2 | 2 | 4 | 0 |
| product oracle:mysql | 516 | 0 | 516 | 7 | 516 | 7 | 1 | 484 | 484 | 3 | 0 |
| product postfix:postfix | 3 | 0 | 3 | 0 | 3 | 0 | 1 | 1 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 0 | 57 | 50 | 65 | 50 | 0 | 12 | 0 | 3 | 0 |
| product powerdns:authoritative | 17 | 0 | 17 | 10 | 17 | 10 | 1 | 2 | 1 | 2 | 0 |
| product powerdns:recursor | 24 | 0 | 24 | 16 | 24 | 16 | 0 | 5 | 2 | 0 | 0 |
| product proftpd:proftpd | 12 | 0 | 12 | 1 | 12 | 1 | 0 | 0 | 0 | 1 | 0 |
| product pureftpd:pure-ftpd | 6 | 0 | 6 | 0 | 6 | 0 | 0 | 1 | 1 | 0 | 0 |
| product samba:samba | 107 | 0 | 95 | 82 | 103 | 82 | 2 | 10 | 1 | 9 | 0 |
| product sendmail:sendmail | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 0 | 23 | 10 | 23 | 10 | 2 | 5 | 3 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 0 | 21 | 12 | 25 | 12 | 2 | 2 | 1 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 0 | 8 | 4 | 8 | 4 | 0 | 0 | 0 | 0 | 0 |


**(b) all snapshot records**

| group | n | no_weakness | has_type_Primary | has_type_Secondary | has_nvd_source | has_cna_source | NVD-CWE-Other | NVD-CWE-noinfo | only_NVD-CWE-* | grouping_or_view | unknown_id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4216 | 0 | 3493 | 1268 | 3530 | 1277 | 502 | 1477 | 1791 | 263 | 0 |
| family dns | 364 | 0 | 281 | 134 | 285 | 134 | 44 | 32 | 62 | 33 | 0 |
| family ftp | 159 | 0 | 106 | 80 | 107 | 80 | 5 | 9 | 6 | 10 | 0 |
| family http | 777 | 0 | 621 | 233 | 641 | 233 | 188 | 68 | 241 | 61 | 0 |
| family mail | 453 | 0 | 383 | 138 | 387 | 138 | 40 | 109 | 105 | 26 | 0 |
| family rdp | 280 | 0 | 102 | 247 | 96 | 253 | 1 | 2 | 1 | 3 | 0 |
| family smb | 216 | 0 | 197 | 89 | 206 | 89 | 38 | 16 | 42 | 29 | 0 |
| family sql | 1765 | 0 | 1655 | 240 | 1660 | 243 | 141 | 1236 | 1291 | 68 | 0 |
| family ssh | 209 | 0 | 154 | 109 | 155 | 109 | 46 | 7 | 46 | 33 | 0 |
| product apache:http_server | 371 | 0 | 293 | 121 | 298 | 121 | 81 | 37 | 112 | 20 | 0 |
| product apache:tomcat | 276 | 0 | 203 | 97 | 213 | 97 | 45 | 20 | 58 | 36 | 0 |
| product beasts:vsftpd | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 0 | 9 | 1 | 9 | 1 | 0 | 0 | 0 | 2 | 0 |
| product crushftp:crushftp | 17 | 0 | 11 | 10 | 11 | 10 | 1 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 69 | 0 | 57 | 21 | 57 | 21 | 5 | 6 | 6 | 10 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 20 | 3 | 20 | 3 | 5 | 1 | 6 | 3 | 0 |
| product exim:exim | 71 | 0 | 47 | 30 | 50 | 30 | 4 | 2 | 5 | 4 | 0 |
| product f5:nginx | 41 | 0 | 36 | 15 | 41 | 15 | 1 | 5 | 4 | 1 | 0 |
| product filezilla-project:filezilla_server | 7 | 0 | 7 | 2 | 7 | 2 | 0 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 243 | 0 | 92 | 213 | 86 | 219 | 1 | 1 | 1 | 2 | 0 |
| product isc:bind | 184 | 0 | 174 | 28 | 174 | 28 | 39 | 23 | 55 | 19 | 0 |
| product libssh:libssh | 45 | 0 | 21 | 34 | 21 | 34 | 2 | 1 | 3 | 5 | 0 |
| product mariadb:mariadb | 431 | 0 | 401 | 37 | 398 | 40 | 1 | 331 | 329 | 3 | 0 |
| product microsoft:exchange_server | 268 | 0 | 236 | 85 | 236 | 85 | 8 | 100 | 70 | 6 | 0 |
| product microsoft:internet_information_services | 93 | 0 | 93 | 2 | 93 | 2 | 61 | 7 | 67 | 4 | 0 |
| product microsoft:sql_server | 110 | 0 | 110 | 22 | 110 | 22 | 43 | 24 | 47 | 14 | 0 |
| product mysql:mysql | 94 | 0 | 94 | 0 | 94 | 0 | 37 | 22 | 59 | 13 | 0 |
| product neutrinolabs:xrdp | 37 | 0 | 10 | 34 | 10 | 34 | 0 | 1 | 0 | 1 | 0 |
| product nginx:nginx | 2 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 0 | 30 | 50 | 30 | 50 | 0 | 0 | 0 | 5 | 0 |
| product openbsd:openssh | 146 | 0 | 115 | 74 | 116 | 74 | 39 | 5 | 37 | 25 | 0 |
| product oracle:mysql | 1328 | 0 | 1305 | 77 | 1305 | 77 | 62 | 1162 | 1177 | 18 | 0 |
| product postfix:postfix | 12 | 0 | 11 | 1 | 11 | 1 | 1 | 1 | 2 | 2 | 0 |
| product postgresql:postgresql | 209 | 0 | 152 | 104 | 160 | 104 | 31 | 19 | 34 | 35 | 0 |
| product powerdns:authoritative | 31 | 0 | 20 | 21 | 20 | 21 | 1 | 2 | 1 | 4 | 0 |
| product powerdns:recursor | 50 | 0 | 37 | 30 | 37 | 30 | 2 | 6 | 5 | 5 | 0 |
| product proftpd:proftpd | 33 | 0 | 27 | 9 | 27 | 9 | 0 | 0 | 0 | 6 | 0 |
| product pureftpd:pure-ftpd | 11 | 0 | 10 | 1 | 10 | 1 | 0 | 1 | 1 | 2 | 0 |
| product samba:samba | 216 | 0 | 197 | 89 | 206 | 89 | 38 | 16 | 42 | 29 | 0 |
| product sendmail:sendmail | 33 | 0 | 32 | 1 | 33 | 1 | 22 | 0 | 22 | 4 | 0 |
| product solarwinds:serv-u | 55 | 0 | 27 | 42 | 28 | 42 | 2 | 8 | 3 | 0 | 0 |
| product thekelleys:dnsmasq | 39 | 0 | 30 | 16 | 34 | 16 | 2 | 2 | 1 | 2 | 0 |
| product wftpserver:wing_ftp_server | 20 | 0 | 11 | 13 | 11 | 13 | 0 | 0 | 0 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 0 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |

### 4b. Top 5 CWEs per family (all weakness entries, any source; CVEs per CWE)

**(a)**

| group | top 5 |
|---|---|
| all | NVD-CWE-noinfo 603, CWE-125 80, CWE-20 69, CWE-787 65, CWE-476 49 |
| family dns | CWE-617 31, CWE-20 24, NVD-CWE-noinfo 16, CWE-400 14, CWE-787 11 |
| family ftp | CWE-79 12, NVD-CWE-noinfo 6, CWE-20 3, CWE-476 3, CWE-732 3 |
| family http | NVD-CWE-noinfo 21, CWE-444 15, CWE-476 14, CWE-400 14, CWE-20 12 |
| family mail | NVD-CWE-noinfo 20, CWE-79 16, CWE-787 14, CWE-20 8, CWE-119 7 |
| family rdp | CWE-125 48, CWE-787 17, CWE-190 12, CWE-120 7, CWE-119 4 |
| family smb | NVD-CWE-noinfo 10, CWE-476 10, CWE-416 8, CWE-125 8, CWE-20 7 |
| family sql | NVD-CWE-noinfo 525, CWE-89 16, CWE-200 16, CWE-416 14, CWE-264 8 |
| family ssh | NVD-CWE-Other 6, CWE-200 6, CWE-287 6, CWE-476 5, CWE-119 4 |

**(b)**

| group | top 5 |
|---|---|
| all | NVD-CWE-noinfo 1477, NVD-CWE-Other 502, CWE-20 171, CWE-125 140, CWE-400 126 |
| family dns | NVD-CWE-Other 44, CWE-20 43, CWE-617 39, NVD-CWE-noinfo 32, CWE-400 17 |
| family ftp | CWE-79 20, CWE-22 10, CWE-639 9, CWE-284 9, NVD-CWE-noinfo 9 |
| family http | NVD-CWE-Other 188, NVD-CWE-noinfo 68, CWE-20 42, CWE-200 41, CWE-79 36 |
| family mail | NVD-CWE-noinfo 109, CWE-79 42, NVD-CWE-Other 40, CWE-20 32, CWE-502 26 |
| family rdp | CWE-125 87, CWE-122 34, CWE-787 33, CWE-416 28, CWE-190 23 |
| family smb | NVD-CWE-Other 38, CWE-119 17, CWE-20 16, NVD-CWE-noinfo 16, CWE-264 13 |
| family sql | NVD-CWE-noinfo 1236, NVD-CWE-Other 141, CWE-400 55, CWE-264 33, CWE-119 29 |
| family ssh | NVD-CWE-Other 46, CWE-264 13, CWE-200 11, CWE-287 10, CWE-399 9 |

## 5. Code-execution candidates, side by side (no choice made)

- **R-CWE**: some CWE on the CVE (any weakness entry, any source) is a Weakness whose Common_Consequences list the Impact "Execute Unauthorized Code or Commands" (S6, S7). This is a property of the weakness *type*. `undetermined` = no CWE on the CVE is a Weakness (none, only NVD-CWE-*, groupings/views or unknown ids); it counts as False in the agreement cells.
- **R-CIA**: D11 vector has C:H and I:H. **CVSS defines C/I/A as impact severity on the impacted component, not as code execution (S1 §2.3).** No D11 score counts as False.
- **R-TEXT** (diagnostic only, not a rule): the English description matches `\bexecut(?:e|es|ed|ing|ion)\s+(?:of\s+)?(?:(?:arbitrary|remote|malicious|unauthori[sz]ed|os|shell|system)\s+)*(?:code|commands?)\b|\b(?:code|command)\s+execution\b|\bcommand\s+injection\b|\brun\s+arbitrary\s+(?:code|commands?)\b` (case-insensitive).

### 5a. Each candidate
R-CWE=None is `undetermined`.

**(a) 1,473 included CVEs**

| group | n | R-CWE=True | R-CWE=False | R-CWE=None | R-CIA=True | R-CIA=False | R-TEXT=True | R-TEXT=False |
|---|---|---|---|---|---|---|---|---|
| all | 1473 | 469 | 398 | 606 | 310 | 1163 | 103 | 1370 |
| family dns | 158 | 65 | 81 | 12 | 27 | 131 | 11 | 147 |
| family ftp | 62 | 29 | 28 | 5 | 16 | 46 | 4 | 58 |
| family http | 189 | 76 | 84 | 29 | 52 | 137 | 9 | 180 |
| family mail | 125 | 65 | 35 | 25 | 51 | 74 | 24 | 101 |
| family rdp | 106 | 56 | 48 | 2 | 32 | 74 | 9 | 97 |
| family smb | 107 | 55 | 43 | 9 | 32 | 75 | 7 | 100 |
| family sql | 668 | 89 | 60 | 519 | 79 | 589 | 30 | 638 |
| family ssh | 58 | 34 | 19 | 5 | 21 | 37 | 9 | 49 |
| product apache:http_server | 87 | 43 | 34 | 10 | 22 | 65 | 3 | 84 |
| product apache:tomcat | 83 | 22 | 42 | 19 | 24 | 59 | 5 | 78 |
| product cerberusftp:ftp_server | 5 | 3 | 2 | 0 | 1 | 4 | 0 | 5 |
| product crushftp:crushftp | 7 | 3 | 4 | 0 | 2 | 5 | 0 | 7 |
| product dovecot:dovecot | 28 | 14 | 11 | 3 | 5 | 23 | 2 | 26 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 5 | 5 | 2 | 5 | 7 | 4 | 8 |
| product exim:exim | 39 | 21 | 10 | 8 | 26 | 13 | 12 | 27 |
| product f5:nginx | 19 | 10 | 9 | 0 | 5 | 14 | 0 | 19 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| product freerdp:freerdp | 89 | 46 | 42 | 1 | 22 | 67 | 7 | 82 |
| product isc:bind | 72 | 20 | 46 | 6 | 3 | 69 | 2 | 70 |
| product libssh:libssh | 11 | 8 | 2 | 1 | 2 | 9 | 0 | 11 |
| product mariadb:mariadb | 200 | 36 | 16 | 148 | 21 | 179 | 7 | 193 |
| product microsoft:exchange_server | 54 | 30 | 12 | 12 | 19 | 35 | 10 | 44 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| product microsoft:sql_server | 13 | 5 | 3 | 5 | 8 | 5 | 5 | 8 |
| product mysql:mysql | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| product neutrinolabs:xrdp | 17 | 10 | 6 | 1 | 10 | 7 | 2 | 15 |
| product nlnetlabs:unbound | 22 | 10 | 12 | 0 | 7 | 15 | 1 | 21 |
| product openbsd:openssh | 35 | 21 | 12 | 2 | 14 | 21 | 5 | 30 |
| product oracle:mysql | 516 | 16 | 13 | 487 | 23 | 493 | 1 | 515 |
| product postfix:postfix | 3 | 0 | 1 | 2 | 1 | 2 | 0 | 3 |
| product postgresql:postgresql | 70 | 37 | 30 | 3 | 37 | 33 | 18 | 52 |
| product powerdns:authoritative | 17 | 9 | 5 | 3 | 2 | 15 | 2 | 15 |
| product powerdns:recursor | 24 | 11 | 11 | 2 | 3 | 21 | 1 | 23 |
| product proftpd:proftpd | 12 | 4 | 7 | 1 | 2 | 10 | 2 | 10 |
| product pureftpd:pure-ftpd | 6 | 2 | 3 | 1 | 1 | 5 | 0 | 6 |
| product samba:samba | 107 | 55 | 43 | 9 | 32 | 75 | 7 | 100 |
| product sendmail:sendmail | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| product solarwinds:serv-u | 23 | 13 | 7 | 3 | 5 | 18 | 2 | 21 |
| product thekelleys:dnsmasq | 28 | 18 | 9 | 1 | 12 | 16 | 5 | 23 |
| product wftpserver:wing_ftp_server | 8 | 3 | 5 | 0 | 5 | 3 | 0 | 8 |


**(b) all snapshot records**

| group | n | R-CWE=True | R-CWE=False | R-CWE=None | R-CIA=True | R-CIA=False | R-TEXT=True | R-TEXT=False |
|---|---|---|---|---|---|---|---|---|
| all | 4216 | 1207 | 971 | 2038 | 440 | 3776 | 473 | 3743 |
| family dns | 364 | 121 | 149 | 94 | 33 | 331 | 23 | 341 |
| family ftp | 159 | 72 | 71 | 16 | 31 | 128 | 32 | 127 |
| family http | 777 | 256 | 222 | 299 | 62 | 715 | 60 | 717 |
| family mail | 453 | 203 | 120 | 130 | 74 | 379 | 110 | 343 |
| family rdp | 280 | 163 | 113 | 4 | 78 | 202 | 31 | 249 |
| family smb | 216 | 86 | 60 | 70 | 35 | 181 | 35 | 181 |
| family sql | 1765 | 232 | 175 | 1358 | 95 | 1670 | 157 | 1608 |
| family ssh | 209 | 75 | 64 | 70 | 34 | 175 | 25 | 184 |
| product apache:http_server | 371 | 141 | 100 | 130 | 28 | 343 | 28 | 343 |
| product apache:tomcat | 276 | 83 | 100 | 93 | 27 | 249 | 8 | 268 |
| product beasts:vsftpd | 2 | 0 | 0 | 2 | 0 | 2 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 4 | 4 | 2 | 2 | 8 | 0 | 10 |
| product crushftp:crushftp | 17 | 9 | 8 | 0 | 5 | 12 | 2 | 15 |
| product dovecot:dovecot | 69 | 32 | 22 | 15 | 6 | 63 | 3 | 66 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 5 | 6 | 9 | 5 | 15 | 6 | 14 |
| product exim:exim | 71 | 44 | 18 | 9 | 37 | 34 | 24 | 47 |
| product f5:nginx | 41 | 23 | 13 | 5 | 6 | 35 | 7 | 34 |
| product filezilla-project:filezilla_server | 7 | 4 | 3 | 0 | 1 | 6 | 0 | 7 |
| product freerdp:freerdp | 243 | 143 | 97 | 3 | 62 | 181 | 22 | 221 |
| product isc:bind | 184 | 44 | 67 | 73 | 5 | 179 | 8 | 176 |
| product libssh:libssh | 45 | 23 | 14 | 8 | 5 | 40 | 5 | 40 |
| product mariadb:mariadb | 431 | 69 | 30 | 332 | 29 | 402 | 26 | 405 |
| product microsoft:exchange_server | 268 | 117 | 75 | 76 | 29 | 239 | 75 | 193 |
| product microsoft:internet_information_services | 93 | 11 | 11 | 71 | 1 | 92 | 17 | 76 |
| product microsoft:sql_server | 110 | 36 | 13 | 61 | 9 | 101 | 64 | 46 |
| product mysql:mysql | 94 | 21 | 2 | 71 | 1 | 93 | 8 | 86 |
| product neutrinolabs:xrdp | 37 | 20 | 16 | 1 | 16 | 21 | 9 | 28 |
| product nginx:nginx | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 2 |
| product nlnetlabs:unbound | 73 | 24 | 44 | 5 | 10 | 63 | 4 | 69 |
| product openbsd:openssh | 146 | 47 | 46 | 53 | 24 | 122 | 14 | 132 |
| product oracle:mysql | 1328 | 54 | 80 | 1194 | 24 | 1304 | 20 | 1308 |
| product postfix:postfix | 12 | 6 | 2 | 4 | 1 | 11 | 2 | 10 |
| product postgresql:postgresql | 209 | 84 | 56 | 69 | 43 | 166 | 51 | 158 |
| product powerdns:authoritative | 31 | 16 | 10 | 5 | 3 | 28 | 2 | 29 |
| product powerdns:recursor | 50 | 16 | 24 | 10 | 3 | 47 | 3 | 47 |
| product proftpd:proftpd | 33 | 15 | 12 | 6 | 4 | 29 | 8 | 25 |
| product pureftpd:pure-ftpd | 11 | 4 | 4 | 3 | 1 | 10 | 1 | 10 |
| product samba:samba | 216 | 86 | 60 | 70 | 35 | 181 | 35 | 181 |
| product sendmail:sendmail | 33 | 4 | 3 | 26 | 1 | 32 | 6 | 27 |
| product solarwinds:serv-u | 55 | 23 | 29 | 3 | 11 | 44 | 14 | 41 |
| product thekelleys:dnsmasq | 39 | 24 | 12 | 3 | 12 | 27 | 6 | 33 |
| product wftpserver:wing_ftp_server | 20 | 9 | 11 | 0 | 6 | 14 | 6 | 14 |
| product xlightftpd:xlight_ftp_server | 5 | 4 | 1 | 0 | 1 | 4 | 1 | 4 |

### 5b. Three-way agreement (cell = CWE/CIA/TEXT, 1 = True)

**(a) 1,473 included CVEs**

| group | n | CWE1/CIA1/TEXT1 | CWE1/CIA1/TEXT0 | CWE1/CIA0/TEXT1 | CWE1/CIA0/TEXT0 | CWE0/CIA1/TEXT1 | CWE0/CIA1/TEXT0 | CWE0/CIA0/TEXT1 | CWE0/CIA0/TEXT0 |
|---|---|---|---|---|---|---|---|---|---|
| all | 1473 | 72 | 120 | 7 | 270 | 22 | 96 | 2 | 884 |
| family dns | 158 | 8 | 15 | 1 | 41 | 2 | 2 | 0 | 89 |
| family ftp | 62 | 3 | 2 | 0 | 24 | 1 | 10 | 0 | 22 |
| family http | 189 | 5 | 22 | 0 | 49 | 4 | 21 | 0 | 88 |
| family mail | 125 | 14 | 15 | 1 | 35 | 8 | 14 | 1 | 37 |
| family rdp | 106 | 8 | 23 | 1 | 24 | 0 | 1 | 0 | 49 |
| family smb | 107 | 6 | 14 | 0 | 35 | 0 | 12 | 1 | 39 |
| family sql | 668 | 22 | 21 | 2 | 44 | 6 | 30 | 0 | 543 |
| family ssh | 58 | 6 | 8 | 2 | 18 | 1 | 6 | 0 | 17 |
| product apache:http_server | 87 | 3 | 13 | 0 | 27 | 0 | 6 | 0 | 38 |
| product apache:tomcat | 83 | 1 | 4 | 0 | 17 | 4 | 15 | 0 | 42 |
| product cerberusftp:ftp_server | 5 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 1 |
| product crushftp:crushftp | 7 | 0 | 1 | 0 | 2 | 0 | 1 | 0 | 3 |
| product dovecot:dovecot | 28 | 1 | 2 | 1 | 10 | 0 | 2 | 0 | 12 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 3 | 0 | 0 | 2 | 1 | 1 | 0 | 5 |
| product exim:exim | 39 | 6 | 12 | 0 | 3 | 5 | 3 | 1 | 9 |
| product f5:nginx | 19 | 0 | 5 | 0 | 5 | 0 | 0 | 0 | 9 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 6 | 16 | 1 | 23 | 0 | 0 | 0 | 43 |
| product isc:bind | 72 | 1 | 1 | 0 | 18 | 1 | 0 | 0 | 51 |
| product libssh:libssh | 11 | 0 | 2 | 0 | 6 | 0 | 0 | 0 | 3 |
| product mariadb:mariadb | 200 | 6 | 4 | 0 | 26 | 1 | 10 | 0 | 153 |
| product microsoft:exchange_server | 54 | 7 | 1 | 0 | 22 | 3 | 8 | 0 | 13 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 3 | 0 | 1 | 1 | 1 | 4 | 0 | 3 |
| product mysql:mysql | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 2 | 7 | 0 | 1 | 0 | 1 | 0 | 6 |
| product nlnetlabs:unbound | 22 | 0 | 7 | 1 | 2 | 0 | 0 | 0 | 12 |
| product openbsd:openssh | 35 | 3 | 6 | 2 | 10 | 0 | 5 | 0 | 9 |
| product oracle:mysql | 516 | 0 | 4 | 0 | 12 | 1 | 18 | 0 | 481 |
| product postfix:postfix | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 |
| product postgresql:postgresql | 70 | 13 | 15 | 1 | 8 | 4 | 5 | 0 | 24 |
| product powerdns:authoritative | 17 | 2 | 0 | 0 | 7 | 0 | 0 | 0 | 8 |
| product powerdns:recursor | 24 | 0 | 0 | 0 | 11 | 1 | 2 | 0 | 10 |
| product proftpd:proftpd | 12 | 1 | 0 | 0 | 3 | 1 | 0 | 0 | 7 |
| product pureftpd:pure-ftpd | 6 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 3 |
| product samba:samba | 107 | 6 | 14 | 0 | 35 | 0 | 12 | 1 | 39 |
| product sendmail:sendmail | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| product solarwinds:serv-u | 23 | 2 | 0 | 0 | 11 | 0 | 3 | 0 | 7 |
| product thekelleys:dnsmasq | 28 | 5 | 7 | 0 | 6 | 0 | 0 | 0 | 10 |
| product wftpserver:wing_ftp_server | 8 | 0 | 1 | 0 | 2 | 0 | 4 | 0 | 1 |


**(b) all snapshot records**

| group | n | CWE1/CIA1/TEXT1 | CWE1/CIA1/TEXT0 | CWE1/CIA0/TEXT1 | CWE1/CIA0/TEXT0 | CWE0/CIA1/TEXT1 | CWE0/CIA1/TEXT0 | CWE0/CIA0/TEXT1 | CWE0/CIA0/TEXT0 |
|---|---|---|---|---|---|---|---|---|---|
| all | 4216 | 109 | 176 | 159 | 763 | 28 | 127 | 177 | 2677 |
| family dns | 364 | 11 | 17 | 3 | 90 | 2 | 3 | 7 | 231 |
| family ftp | 159 | 6 | 4 | 11 | 51 | 3 | 18 | 12 | 54 |
| family http | 777 | 7 | 27 | 20 | 202 | 5 | 23 | 28 | 465 |
| family mail | 453 | 23 | 25 | 32 | 123 | 8 | 18 | 47 | 177 |
| family rdp | 280 | 17 | 51 | 12 | 83 | 0 | 10 | 2 | 105 |
| family smb | 216 | 7 | 14 | 13 | 52 | 0 | 14 | 15 | 101 |
| family sql | 1765 | 29 | 25 | 65 | 113 | 8 | 33 | 55 | 1437 |
| family ssh | 209 | 9 | 13 | 3 | 50 | 2 | 10 | 11 | 111 |
| product apache:http_server | 371 | 5 | 16 | 9 | 111 | 0 | 7 | 14 | 209 |
| product apache:tomcat | 276 | 1 | 6 | 2 | 74 | 5 | 15 | 0 | 173 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| product cerberusftp:ftp_server | 10 | 0 | 0 | 0 | 4 | 0 | 2 | 0 | 4 |
| product crushftp:crushftp | 17 | 1 | 1 | 1 | 6 | 0 | 3 | 0 | 5 |
| product dovecot:dovecot | 69 | 1 | 3 | 2 | 26 | 0 | 2 | 0 | 35 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 3 | 0 | 0 | 2 | 1 | 1 | 2 | 11 |
| product exim:exim | 71 | 10 | 18 | 6 | 10 | 5 | 4 | 3 | 15 |
| product f5:nginx | 41 | 0 | 5 | 6 | 12 | 0 | 1 | 1 | 16 |
| product filezilla-project:filezilla_server | 7 | 0 | 0 | 0 | 4 | 0 | 1 | 0 | 2 |
| product freerdp:freerdp | 243 | 12 | 43 | 9 | 79 | 0 | 7 | 1 | 92 |
| product isc:bind | 184 | 1 | 2 | 0 | 41 | 1 | 1 | 6 | 132 |
| product libssh:libssh | 45 | 1 | 4 | 1 | 17 | 0 | 0 | 3 | 19 |
| product mariadb:mariadb | 431 | 11 | 6 | 12 | 40 | 1 | 11 | 2 | 348 |
| product microsoft:exchange_server | 268 | 12 | 4 | 21 | 80 | 3 | 10 | 39 | 99 |
| product microsoft:internet_information_services | 93 | 1 | 0 | 3 | 7 | 0 | 0 | 13 | 69 |
| product microsoft:sql_server | 110 | 3 | 0 | 26 | 7 | 2 | 4 | 33 | 35 |
| product mysql:mysql | 94 | 0 | 0 | 4 | 17 | 0 | 1 | 4 | 68 |
| product neutrinolabs:xrdp | 37 | 5 | 8 | 3 | 4 | 0 | 3 | 1 | 13 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 3 | 7 | 1 | 13 | 0 | 0 | 0 | 49 |
| product openbsd:openssh | 146 | 5 | 9 | 2 | 31 | 1 | 9 | 6 | 83 |
| product oracle:mysql | 1328 | 1 | 4 | 9 | 40 | 1 | 18 | 9 | 1246 |
| product postfix:postfix | 12 | 0 | 0 | 1 | 5 | 0 | 1 | 1 | 4 |
| product postgresql:postgresql | 209 | 14 | 17 | 22 | 31 | 5 | 7 | 10 | 103 |
| product powerdns:authoritative | 31 | 2 | 1 | 0 | 13 | 0 | 0 | 0 | 15 |
| product powerdns:recursor | 50 | 0 | 0 | 1 | 15 | 1 | 2 | 1 | 30 |
| product proftpd:proftpd | 33 | 1 | 1 | 4 | 9 | 2 | 0 | 1 | 15 |
| product pureftpd:pure-ftpd | 11 | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 5 |
| product samba:samba | 216 | 7 | 14 | 13 | 52 | 0 | 14 | 15 | 101 |
| product sendmail:sendmail | 33 | 0 | 0 | 2 | 2 | 0 | 1 | 4 | 24 |
| product solarwinds:serv-u | 55 | 3 | 1 | 3 | 16 | 1 | 6 | 7 | 18 |
| product thekelleys:dnsmasq | 39 | 5 | 7 | 1 | 11 | 0 | 0 | 0 | 15 |
| product wftpserver:wing_ftp_server | 20 | 0 | 1 | 3 | 5 | 0 | 5 | 3 | 3 |
| product xlightftpd:xlight_ftp_server | 5 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 1 |

### 5c. Disagreement cells: up to 20 random CVE IDs each (seed 20261108), for manual check

**(a)**

- `CWE1/CIA1/TEXT0` (n = 120): CVE-2015-0244, CVE-2015-2325, CVE-2016-2123, CVE-2016-6664, CVE-2018-1057, CVE-2019-10208, CVE-2019-25033, CVE-2019-6109, CVE-2019-7524, CVE-2020-11523, CVE-2020-11984, CVE-2020-14350, CVE-2020-25717, CVE-2020-28018, CVE-2021-40438, CVE-2021-45951, CVE-2022-2031, CVE-2022-23478, CVE-2022-41741, CVE-2023-40186
- `CWE1/CIA0/TEXT1` (n = 7): CVE-2016-5423, CVE-2017-2834, CVE-2019-18934, CVE-2021-33515, CVE-2023-23384, CVE-2023-25136, CVE-2023-51385
- `CWE1/CIA0/TEXT0` (n = 270): CVE-2015-5174, CVE-2016-2120, CVE-2016-6797, CVE-2016-7072, CVE-2016-7073, CVE-2016-8740, CVE-2017-9788, CVE-2018-1302, CVE-2019-6471, CVE-2020-4031, CVE-2021-32604, CVE-2021-35250, CVE-2021-36369, CVE-2022-27377, CVE-2022-27387, CVE-2022-27457, CVE-2022-41742, CVE-2023-1667, CVE-2023-2283, CVE-2023-39351
- `CWE0/CIA1/TEXT1` (n = 22): CVE-2016-0714, CVE-2016-6662, CVE-2016-7048, CVE-2016-7408, CVE-2016-8735, CVE-2019-10127, CVE-2019-10128, CVE-2019-1373, CVE-2019-13917, CVE-2019-15846, CVE-2020-10030, CVE-2020-1938, CVE-2020-25696, CVE-2020-28008, CVE-2020-28021, CVE-2020-28026, CVE-2020-9484, CVE-2021-25216, CVE-2022-21969, CVE-2023-36439
- `CWE0/CIA1/TEXT0` (n = 96): CVE-2013-1430, CVE-2016-1531, CVE-2016-2118, CVE-2016-5018, CVE-2016-5388, CVE-2016-9775, CVE-2016-9842, CVE-2017-12150, CVE-2017-5648, CVE-2017-7547, CVE-2018-8014, CVE-2018-8581, CVE-2019-0215, CVE-2019-3807, CVE-2019-3814, CVE-2020-14663, CVE-2020-28012, CVE-2020-28912, CVE-2020-8634, CVE-2022-32744
- `CWE0/CIA0/TEXT1` (n = 2): CVE-2015-5370, CVE-2017-1000369

**(b)**

- `CWE1/CIA1/TEXT0` (n = 176): CVE-2015-0244, CVE-2015-2325, CVE-2016-0746, CVE-2016-9774, CVE-2017-12615, CVE-2019-6110, CVE-2020-11656, CVE-2020-11984, CVE-2020-13398, CVE-2020-28018, CVE-2021-28041, CVE-2021-45956, CVE-2022-23477, CVE-2022-23943, CVE-2023-39355, CVE-2025-64666, CVE-2026-23532, CVE-2026-44422, CVE-2026-55626, CVE-2026-55827
- `CWE1/CIA0/TEXT1` (n = 159): CVE-2002-1337, CVE-2003-0542, CVE-2004-0836, CVE-2005-0709, CVE-2007-6015, CVE-2008-1446, CVE-2010-4221, CVE-2010-4652, CVE-2012-5611, CVE-2012-5612, CVE-2014-0088, CVE-2020-17084, CVE-2021-26855, CVE-2021-34473, CVE-2023-21704, CVE-2023-38169, CVE-2025-55752, CVE-2026-69355, CVE-2026-85746, CVE-2026-91957
- `CWE1/CIA0/TEXT0` (n = 763): CVE-2003-1581, CVE-2005-0563, CVE-2006-3918, CVE-2008-1947, CVE-2008-4456, CVE-2009-2939, CVE-2012-0553, CVE-2016-0030, CVE-2016-7073, CVE-2018-15473, CVE-2018-16793, CVE-2019-19269, CVE-2020-11058, CVE-2022-27380, CVE-2022-41040, CVE-2023-49441, CVE-2024-24549, CVE-2024-36387, CVE-2025-25005, CVE-2026-44631
- `CWE0/CIA1/TEXT1` (n = 28): CVE-2012-1856, CVE-2016-0714, CVE-2016-6662, CVE-2016-7048, CVE-2016-7408, CVE-2019-10127, CVE-2019-12815, CVE-2019-15846, CVE-2020-0618, CVE-2020-10030, CVE-2020-25696, CVE-2020-28021, CVE-2020-28026, CVE-2020-9484, CVE-2022-21969, CVE-2023-36439, CVE-2024-10979, CVE-2025-24813, CVE-2025-40538, CVE-2026-35386
- `CWE0/CIA1/TEXT0` (n = 127): CVE-2001-0497, CVE-2015-8325, CVE-2016-2111, CVE-2016-7254, CVE-2016-9842, CVE-2017-5648, CVE-2017-5651, CVE-2017-7547, CVE-2019-10210, CVE-2019-1136, CVE-2020-35481, CVE-2021-25329, CVE-2021-35242, CVE-2022-0336, CVE-2022-22720, CVE-2022-31813, CVE-2022-32744, CVE-2023-36039, CVE-2024-32662, CVE-2026-106583
- `CWE0/CIA0/TEXT1` (n = 177): CVE-2000-1087, CVE-2002-0056, CVE-2002-0147, CVE-2002-0150, CVE-2002-0364, CVE-2002-0644, CVE-2002-0972, CVE-2002-1376, CVE-2003-0694, CVE-2008-0107, CVE-2009-0098, CVE-2010-0425, CVE-2014-2972, CVE-2015-1762, CVE-2021-26412, CVE-2023-21529, CVE-2023-21705, CVE-2025-47811, CVE-2026-2004, CVE-2026-28321

## 6. Product role (docs/sources.md §2)

Role per CVE: the role shared by all its vulnerable family products; `mixed` if they differ; `platform_only` if no family product is a positive vulnerable match. (a) uses the cves.csv products; (b) the vulnerable FAMILY_PRODUCTS products of the families whose query returned the record.

**6a (a) role**

| group | n | server | multi | unstated | UNAVAILABLE | mixed | platform_only |
|---|---|---|---|---|---|---|---|
| all | 1473 | 533 | 532 | 274 | 1 | 133 | 0 |
| family dns | 158 | 158 | 0 | 0 | 0 | 0 | 0 |
| family ftp | 62 | 61 | 0 | 0 | 1 | 0 | 0 |
| family http | 189 | 106 | 0 | 82 | 0 | 1 | 0 |
| family mail | 125 | 71 | 0 | 54 | 0 | 0 | 0 |
| family rdp | 106 | 17 | 89 | 0 | 0 | 0 | 0 |
| family smb | 107 | 107 | 0 | 0 | 0 | 0 | 0 |
| family sql | 668 | 13 | 385 | 138 | 0 | 132 | 0 |
| family ssh | 58 | 0 | 58 | 0 | 0 | 0 | 0 |
| product apache:http_server | 87 | 87 | 0 | 0 | 0 | 0 | 0 |
| product apache:tomcat | 83 | 0 | 0 | 82 | 0 | 1 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| product dovecot:dovecot | 28 | 28 | 0 | 0 | 0 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 0 | 12 | 0 | 0 | 0 | 0 |
| product exim:exim | 39 | 39 | 0 | 0 | 0 | 0 | 0 |
| product f5:nginx | 19 | 18 | 0 | 0 | 0 | 1 | 0 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 0 | 89 | 0 | 0 | 0 | 0 |
| product isc:bind | 72 | 72 | 0 | 0 | 0 | 0 | 0 |
| product libssh:libssh | 11 | 0 | 11 | 0 | 0 | 0 | 0 |
| product mariadb:mariadb | 200 | 0 | 0 | 68 | 0 | 132 | 0 |
| product microsoft:exchange_server | 54 | 0 | 0 | 54 | 0 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 13 | 0 | 0 | 0 | 0 | 0 |
| product mysql:mysql | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 0 | 0 | 0 | 0 | 0 |
| product openbsd:openssh | 35 | 0 | 35 | 0 | 0 | 0 | 0 |
| product oracle:mysql | 516 | 0 | 385 | 0 | 0 | 131 | 0 |
| product postfix:postfix | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| product postgresql:postgresql | 70 | 0 | 0 | 70 | 0 | 0 | 0 |
| product powerdns:authoritative | 17 | 17 | 0 | 0 | 0 | 0 | 0 |
| product powerdns:recursor | 24 | 24 | 0 | 0 | 0 | 0 | 0 |
| product proftpd:proftpd | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| product samba:samba | 107 | 107 | 0 | 0 | 0 | 0 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 0 | 0 | 0 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 0 | 0 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 8 | 0 | 0 | 0 | 0 | 0 |

**6a (b) role**

| group | n | server | multi | unstated | UNAVAILABLE | mixed | platform_only |
|---|---|---|---|---|---|---|---|
| all | 4216 | 1533 | 1465 | 833 | 6 | 331 | 48 |
| family dns | 364 | 364 | 0 | 0 | 0 | 0 | 0 |
| family ftp | 159 | 151 | 0 | 0 | 6 | 2 | 0 |
| family http | 777 | 476 | 0 | 271 | 0 | 5 | 25 |
| family mail | 453 | 184 | 0 | 253 | 0 | 3 | 13 |
| family rdp | 280 | 37 | 243 | 0 | 0 | 0 | 0 |
| family smb | 216 | 216 | 0 | 0 | 0 | 0 | 0 |
| family sql | 1765 | 107 | 1014 | 309 | 0 | 325 | 10 |
| family ssh | 209 | 0 | 208 | 0 | 0 | 1 | 0 |
| product apache:http_server | 371 | 348 | 0 | 0 | 0 | 2 | 21 |
| product apache:tomcat | 276 | 0 | 0 | 271 | 0 | 3 | 2 |
| product beasts:vsftpd | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| product crushftp:crushftp | 17 | 16 | 0 | 0 | 0 | 1 | 0 |
| product dovecot:dovecot | 69 | 69 | 0 | 0 | 0 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 19 | 0 | 0 | 1 | 0 |
| product exim:exim | 71 | 70 | 0 | 0 | 0 | 0 | 1 |
| product f5:nginx | 41 | 40 | 0 | 0 | 0 | 1 | 0 |
| product filezilla-project:filezilla_server | 7 | 0 | 0 | 0 | 6 | 1 | 0 |
| product freerdp:freerdp | 243 | 0 | 243 | 0 | 0 | 0 | 0 |
| product isc:bind | 184 | 184 | 0 | 0 | 0 | 0 | 0 |
| product libssh:libssh | 45 | 0 | 44 | 0 | 0 | 1 | 0 |
| product mariadb:mariadb | 431 | 0 | 0 | 106 | 0 | 324 | 1 |
| product microsoft:exchange_server | 268 | 0 | 0 | 253 | 0 | 3 | 12 |
| product microsoft:internet_information_services | 93 | 89 | 0 | 0 | 0 | 2 | 2 |
| product microsoft:sql_server | 110 | 107 | 0 | 0 | 0 | 1 | 2 |
| product mysql:mysql | 94 | 0 | 91 | 0 | 0 | 1 | 2 |
| product neutrinolabs:xrdp | 37 | 37 | 0 | 0 | 0 | 0 | 0 |
| product nginx:nginx | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 73 | 0 | 0 | 0 | 0 | 0 |
| product openbsd:openssh | 146 | 0 | 145 | 0 | 0 | 1 | 0 |
| product oracle:mysql | 1328 | 0 | 1006 | 0 | 0 | 322 | 0 |
| product postfix:postfix | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| product postgresql:postgresql | 209 | 0 | 0 | 203 | 0 | 0 | 6 |
| product powerdns:authoritative | 31 | 31 | 0 | 0 | 0 | 0 | 0 |
| product powerdns:recursor | 50 | 50 | 0 | 0 | 0 | 0 | 0 |
| product proftpd:proftpd | 33 | 32 | 0 | 0 | 0 | 1 | 0 |
| product pureftpd:pure-ftpd | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| product samba:samba | 216 | 216 | 0 | 0 | 0 | 0 | 0 |
| product sendmail:sendmail | 33 | 33 | 0 | 0 | 0 | 0 | 0 |
| product solarwinds:serv-u | 55 | 55 | 0 | 0 | 0 | 0 | 0 |
| product thekelleys:dnsmasq | 39 | 39 | 0 | 0 | 0 | 0 | 0 |
| product wftpserver:wing_ftp_server | 20 | 20 | 0 | 0 | 0 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 5 | 0 | 0 | 0 | 0 | 0 |

### 6b. Multi-role products: which component the description / CPEs name

Client terms `\bclients?\b|\bdbclient\b|\bxfreerdp\b|\bwfreerdp\b|\bscp\b`; server terms `\bservers?\b|\bsshd\b|\bmysqld\b|\bshadow\b|\bproxy\b` (case-insensitive), searched in the English description and the positive vulnerable CPE strings with the vendor:product token removed. `both` and `neither` cannot be resolved this way and are listed in full.

**(a)**

| product | CVEs | client | server | both | neither |
|---|---|---|---|---|---|
| freerdp:freerdp | 89 | 13 | 7 | 21 | 48 |
| mysql:mysql | 1 | 0 | 1 | 0 | 0 |
| oracle:mysql | 516 | 8 | 439 | 15 | 54 |
| dropbear_ssh_project:dropbear_ssh | 12 | 2 | 1 | 2 | 7 |
| libssh:libssh | 11 | 2 | 0 | 4 | 5 |
| openbsd:openssh | 35 | 1 | 12 | 11 | 11 |

Unresolved:

- freerdp:freerdp, `both` (21): CVE-2018-1000852, CVE-2020-11017, CVE-2020-11038, CVE-2020-11044, CVE-2020-11047, CVE-2020-11058, CVE-2020-11085, CVE-2020-15103, CVE-2021-41160, CVE-2022-24882, CVE-2022-24883, CVE-2022-39282, CVE-2022-39283, CVE-2022-39316, CVE-2022-39317, CVE-2022-39318, CVE-2022-39319, CVE-2022-39320, CVE-2022-39347, CVE-2022-41877, CVE-2023-40186
- freerdp:freerdp, `neither` (48): CVE-2013-4118, CVE-2013-4119, CVE-2018-8784, CVE-2018-8785, CVE-2018-8786, CVE-2018-8787, CVE-2018-8788, CVE-2018-8789, CVE-2019-17177, CVE-2019-17178, CVE-2020-11019, CVE-2020-11040, CVE-2020-11043, CVE-2020-11046, CVE-2020-11048, CVE-2020-11086, CVE-2020-11087, CVE-2020-11088, CVE-2020-11089, CVE-2020-11095, CVE-2020-11096, CVE-2020-11097, CVE-2020-11099, CVE-2020-11521, CVE-2020-11522, CVE-2020-11523, CVE-2020-11524, CVE-2020-11525, CVE-2020-11526, CVE-2020-13396, CVE-2020-13397, CVE-2020-13398, CVE-2020-4030, CVE-2023-39351, CVE-2023-39352, CVE-2023-39353, CVE-2023-39354, CVE-2023-39355, CVE-2023-39356, CVE-2023-40181, CVE-2023-40187, CVE-2023-40188, CVE-2023-40567, CVE-2023-40569, CVE-2023-40574, CVE-2023-40575, CVE-2023-40576, CVE-2023-40589
- mysql:mysql, `both` (0): none
- mysql:mysql, `neither` (0): none
- oracle:mysql, `both` (15): CVE-2016-2047, CVE-2017-10379, CVE-2017-3305, CVE-2017-3600, CVE-2017-3636, CVE-2017-3651, CVE-2018-2761, CVE-2018-2773, CVE-2018-3070, CVE-2018-3084, CVE-2018-3174, CVE-2019-2797, CVE-2019-2969, CVE-2020-1967, CVE-2020-1971
- oracle:mysql, `neither` (54): CVE-2016-0502, CVE-2016-0639, CVE-2016-0640, CVE-2016-0641, CVE-2016-0642, CVE-2016-0643, CVE-2016-0644, CVE-2016-0646, CVE-2016-0647, CVE-2016-0648, CVE-2016-0649, CVE-2016-0650, CVE-2016-0651, CVE-2016-0652, CVE-2016-0653, CVE-2016-0654, CVE-2016-0655, CVE-2016-0656, CVE-2016-0657, CVE-2016-0658, CVE-2016-0659, CVE-2016-0661, CVE-2016-0662, CVE-2016-0663, CVE-2016-0665, CVE-2016-0666, CVE-2016-0667, CVE-2016-0668, CVE-2016-0705, CVE-2016-2105, CVE-2016-5609, CVE-2016-5612, CVE-2016-5624, CVE-2016-5626, CVE-2016-5634, CVE-2016-7440, CVE-2016-9840, CVE-2016-9841, CVE-2016-9842, CVE-2016-9843, CVE-2017-3302, CVE-2017-3635, CVE-2018-0735, CVE-2019-14540, CVE-2019-1559, CVE-2019-16168, CVE-2019-2920, CVE-2019-7317, CVE-2020-11655, CVE-2020-11656, CVE-2020-15358, CVE-2020-2768, CVE-2020-5398, CVE-2021-22570
- dropbear_ssh_project:dropbear_ssh, `both` (2): CVE-2016-7409, CVE-2021-36369
- dropbear_ssh_project:dropbear_ssh, `neither` (7): CVE-2016-3116, CVE-2016-7406, CVE-2016-7407, CVE-2017-2659, CVE-2017-9079, CVE-2018-15599, CVE-2019-12953
- libssh:libssh, `both` (4): CVE-2018-10933, CVE-2019-14889, CVE-2020-1730, CVE-2023-3603
- libssh:libssh, `neither` (5): CVE-2015-3146, CVE-2016-0739, CVE-2020-16135, CVE-2021-3634, CVE-2023-6918
- openbsd:openssh, `both` (11): CVE-2016-0777, CVE-2016-0778, CVE-2016-1908, CVE-2018-20685, CVE-2019-16905, CVE-2019-6109, CVE-2019-6110, CVE-2019-6111, CVE-2020-12062, CVE-2020-14145, CVE-2021-36368
- openbsd:openssh, `neither` (11): CVE-2016-10009, CVE-2016-1907, CVE-2016-8858, CVE-2018-15473, CVE-2018-15919, CVE-2021-28041, CVE-2023-28531, CVE-2023-38408, CVE-2023-51384, CVE-2023-51385, CVE-2023-51767

**(b)**

| product | CVEs | client | server | both | neither |
|---|---|---|---|---|---|
| freerdp:freerdp | 243 | 33 | 24 | 96 | 90 |
| mysql:mysql | 92 | 1 | 42 | 0 | 49 |
| oracle:mysql | 1328 | 25 | 1056 | 30 | 217 |
| dropbear_ssh_project:dropbear_ssh | 20 | 3 | 7 | 3 | 7 |
| libssh:libssh | 45 | 5 | 3 | 13 | 24 |
| openbsd:openssh | 146 | 8 | 51 | 26 | 61 |

Unresolved:

- freerdp:freerdp, `both` (96): CVE-2018-1000852, CVE-2020-11017, CVE-2020-11038, CVE-2020-11044, CVE-2020-11047, CVE-2020-11058, CVE-2020-11085, CVE-2020-15103, CVE-2021-41160, CVE-2022-24882, CVE-2022-24883, CVE-2022-39282, CVE-2022-39283, CVE-2022-39316, CVE-2022-39317, CVE-2022-39318, CVE-2022-39319, CVE-2022-39320, CVE-2022-39347, CVE-2022-41877, CVE-2023-40186, CVE-2024-22211, CVE-2024-32040, CVE-2024-32458, CVE-2024-32459, CVE-2024-32460, CVE-2024-32660, CVE-2024-32662, CVE-2025-68118, CVE-2026-109678, CVE-2026-111374, CVE-2026-111375, CVE-2026-111376, CVE-2026-111377, CVE-2026-111380, CVE-2026-111382, CVE-2026-22852, CVE-2026-22859, CVE-2026-23530, CVE-2026-23531, CVE-2026-23532, CVE-2026-23533, CVE-2026-23534, CVE-2026-23732, CVE-2026-23883, CVE-2026-23884, CVE-2026-24679, CVE-2026-25941, CVE-2026-26271, CVE-2026-26955, CVE-2026-26965, CVE-2026-27015, CVE-2026-27951, CVE-2026-29774, CVE-2026-29775, CVE-2026-33977, CVE-2026-40033, CVE-2026-40254, CVE-2026-44420, CVE-2026-44421, CVE-2026-44422, CVE-2026-55191, CVE-2026-55192, CVE-2026-55193, CVE-2026-55194, CVE-2026-55564, CVE-2026-55648, CVE-2026-55827, CVE-2026-56297, CVE-2026-57157, CVE-2026-57158, CVE-2026-63117, CVE-2026-63633, CVE-2026-63652, CVE-2026-64620, CVE-2026-67289, CVE-2026-67291, CVE-2026-67294, CVE-2026-67296, CVE-2026-67299, CVE-2026-67301, CVE-2026-67302, CVE-2026-67303, CVE-2026-67305, CVE-2026-67306, CVE-2026-68579, CVE-2026-73241, CVE-2026-85089, CVE-2026-91950, CVE-2026-91951, CVE-2026-91952, CVE-2026-91954, CVE-2026-91955, CVE-2026-91956, CVE-2026-91961, CVE-2026-91963
- freerdp:freerdp, `neither` (90): CVE-2013-4118, CVE-2013-4119, CVE-2018-8784, CVE-2018-8785, CVE-2018-8786, CVE-2018-8787, CVE-2018-8788, CVE-2018-8789, CVE-2019-17177, CVE-2019-17178, CVE-2020-11019, CVE-2020-11040, CVE-2020-11043, CVE-2020-11046, CVE-2020-11048, CVE-2020-11086, CVE-2020-11087, CVE-2020-11088, CVE-2020-11089, CVE-2020-11095, CVE-2020-11096, CVE-2020-11097, CVE-2020-11099, CVE-2020-11521, CVE-2020-11522, CVE-2020-11523, CVE-2020-11524, CVE-2020-11525, CVE-2020-11526, CVE-2020-13396, CVE-2020-13397, CVE-2020-13398, CVE-2020-4030, CVE-2023-39351, CVE-2023-39352, CVE-2023-39353, CVE-2023-39354, CVE-2023-39355, CVE-2023-39356, CVE-2023-40181, CVE-2023-40187, CVE-2023-40188, CVE-2023-40567, CVE-2023-40569, CVE-2023-40574, CVE-2023-40575, CVE-2023-40576, CVE-2023-40589, CVE-2025-4478, CVE-2026-111379, CVE-2026-111381, CVE-2026-22851, CVE-2026-22853, CVE-2026-22855, CVE-2026-22856, CVE-2026-22857, CVE-2026-22858, CVE-2026-24675, CVE-2026-24676, CVE-2026-24678, CVE-2026-24680, CVE-2026-24681, CVE-2026-24682, CVE-2026-24683, CVE-2026-24684, CVE-2026-25952, CVE-2026-25953, CVE-2026-25954, CVE-2026-25955, CVE-2026-25959, CVE-2026-25997, CVE-2026-26986, CVE-2026-27950, CVE-2026-29776, CVE-2026-31885, CVE-2026-31897, CVE-2026-33982, CVE-2026-33983, CVE-2026-33984, CVE-2026-33985, CVE-2026-33986, CVE-2026-33987, CVE-2026-45700, CVE-2026-64624, CVE-2026-66401, CVE-2026-67304, CVE-2026-73242, CVE-2026-91957, CVE-2026-91959, CVE-2026-91962
- mysql:mysql, `both` (0): none
- mysql:mysql, `neither` (49): CVE-2003-0780, CVE-2003-1480, CVE-2004-0381, CVE-2004-0627, CVE-2004-0628, CVE-2004-0835, CVE-2004-0837, CVE-2005-0709, CVE-2005-0710, CVE-2005-0711, CVE-2005-1636, CVE-2005-2558, CVE-2005-2573, CVE-2006-0903, CVE-2006-1516, CVE-2006-1517, CVE-2006-1518, CVE-2006-2753, CVE-2006-3486, CVE-2006-4031, CVE-2006-4226, CVE-2006-4227, CVE-2006-4380, CVE-2006-7232, CVE-2007-1420, CVE-2007-2691, CVE-2007-2692, CVE-2007-2693, CVE-2007-5925, CVE-2007-6303, CVE-2008-0226, CVE-2008-2079, CVE-2008-3963, CVE-2008-4098, CVE-2008-7247, CVE-2009-0819, CVE-2009-4030, CVE-2009-5026, CVE-2010-1621, CVE-2010-1626, CVE-2010-1848, CVE-2010-1849, CVE-2010-1850, CVE-2010-3678, CVE-2010-3839, CVE-2012-0553, CVE-2012-0882, CVE-2013-1492, CVE-2015-2575
- oracle:mysql, `both` (30): CVE-2004-0457, CVE-2009-4484, CVE-2012-3147, CVE-2012-3149, CVE-2014-0001, CVE-2014-6494, CVE-2014-6496, CVE-2014-6530, CVE-2014-6551, CVE-2015-2661, CVE-2015-4819, CVE-2016-0546, CVE-2016-2047, CVE-2017-10379, CVE-2017-3305, CVE-2017-3600, CVE-2017-3636, CVE-2017-3651, CVE-2018-2761, CVE-2018-2773, CVE-2018-3070, CVE-2018-3084, CVE-2018-3174, CVE-2019-2797, CVE-2019-2969, CVE-2020-1967, CVE-2020-1971, CVE-2023-21980, CVE-2024-21096, CVE-2024-21231
- oracle:mysql, `neither` (217): CVE-2000-0045, CVE-2000-0148, CVE-2000-0981, CVE-2001-0407, CVE-2001-1255, CVE-2001-1274, CVE-2001-1275, CVE-2001-1453, CVE-2001-1454, CVE-2002-1374, CVE-2002-1375, CVE-2002-1809, CVE-2002-1921, CVE-2002-1923, CVE-2003-0150, CVE-2003-0780, CVE-2003-1480, CVE-2004-0381, CVE-2004-0388, CVE-2004-0835, CVE-2004-0837, CVE-2004-0956, CVE-2004-0957, CVE-2004-2149, CVE-2005-0004, CVE-2005-0709, CVE-2005-0710, CVE-2005-0711, CVE-2005-0799, CVE-2005-1636, CVE-2005-2558, CVE-2005-2573, CVE-2006-0369, CVE-2006-0903, CVE-2006-1516, CVE-2006-1517, CVE-2006-1518, CVE-2006-2753, CVE-2006-3486, CVE-2006-4031, CVE-2006-4226, CVE-2006-4227, CVE-2007-1420, CVE-2007-2583, CVE-2007-2692, CVE-2007-2693, CVE-2007-5970, CVE-2007-6303, CVE-2008-0226, CVE-2008-2079, CVE-2008-3963, CVE-2008-4097, CVE-2008-4098, CVE-2008-7247, CVE-2009-0819, CVE-2009-4030, CVE-2009-5026, CVE-2010-1626, CVE-2010-1848, CVE-2010-1849, CVE-2010-1850, CVE-2010-3678, CVE-2010-3839, CVE-2012-0553, CVE-2012-0882, CVE-2012-2122, CVE-2012-2750, CVE-2012-4414, CVE-2012-4452, CVE-2012-5611, CVE-2012-5612, CVE-2012-5613, CVE-2012-5615, CVE-2012-5627, CVE-2013-1492, CVE-2013-1511, CVE-2013-1512, CVE-2013-1532, CVE-2013-1544, CVE-2013-1552, CVE-2013-1566, CVE-2013-1567, CVE-2013-1570, CVE-2013-1861, CVE-2013-2375, CVE-2013-2376, CVE-2013-2378, CVE-2013-2389, CVE-2013-2395, CVE-2015-2576, CVE-2015-4730, CVE-2016-0502, CVE-2016-0503, CVE-2016-0504, CVE-2016-0505, CVE-2016-0594, CVE-2016-0595, CVE-2016-0596, CVE-2016-0597, CVE-2016-0598, CVE-2016-0599, CVE-2016-0600, CVE-2016-0601, CVE-2016-0605, CVE-2016-0606, CVE-2016-0607, CVE-2016-0608, CVE-2016-0609, CVE-2016-0610, CVE-2016-0611, CVE-2016-0616, CVE-2016-0639, CVE-2016-0640, CVE-2016-0641, CVE-2016-0642, CVE-2016-0643, CVE-2016-0644, CVE-2016-0646, CVE-2016-0647, CVE-2016-0648, CVE-2016-0649, CVE-2016-0650, CVE-2016-0651, CVE-2016-0652, CVE-2016-0653, CVE-2016-0654, CVE-2016-0655, CVE-2016-0656, CVE-2016-0657, CVE-2016-0658, CVE-2016-0659, CVE-2016-0661, CVE-2016-0662, CVE-2016-0663, CVE-2016-0665, CVE-2016-0666, CVE-2016-0667, CVE-2016-0668, CVE-2016-0705, CVE-2016-2105, CVE-2016-5609, CVE-2016-5612, CVE-2016-5624, CVE-2016-5626, CVE-2016-5634, CVE-2016-7440, CVE-2016-9840, CVE-2016-9841, CVE-2016-9842, CVE-2016-9843, CVE-2017-3302, CVE-2017-3635, CVE-2018-0735, CVE-2019-14540, CVE-2019-1559, CVE-2019-16168, CVE-2019-2920, CVE-2019-7317, CVE-2020-11655, CVE-2020-11656, CVE-2020-15358, CVE-2020-2768, CVE-2020-5258, CVE-2020-5398, CVE-2021-22570, CVE-2022-21279, CVE-2022-21280, CVE-2022-21284, CVE-2022-21285, CVE-2022-21286, CVE-2022-21287, CVE-2022-21288, CVE-2022-21289, CVE-2022-21290, CVE-2022-21307, CVE-2022-21308, CVE-2022-21309, CVE-2022-21310, CVE-2022-21311, CVE-2022-21312, CVE-2022-21313, CVE-2022-21314, CVE-2022-21315, CVE-2022-21316, CVE-2022-21317, CVE-2022-21318, CVE-2022-21319, CVE-2022-21320, CVE-2022-21321, CVE-2022-21322, CVE-2022-21323, CVE-2022-21324, CVE-2022-21325, CVE-2022-21326, CVE-2022-21327, CVE-2022-21328, CVE-2022-21329, CVE-2022-21330, CVE-2022-21331, CVE-2022-21332, CVE-2022-21333, CVE-2022-21334, CVE-2022-21335, CVE-2022-21336, CVE-2022-21337, CVE-2022-21355, CVE-2022-21356, CVE-2022-21357, CVE-2022-21482, CVE-2022-21483, CVE-2022-21484, CVE-2022-21485, CVE-2022-21486, CVE-2022-21489, CVE-2022-39404, CVE-2024-21101, CVE-2024-21272
- dropbear_ssh_project:dropbear_ssh, `both` (3): CVE-2016-7409, CVE-2021-36369, CVE-2023-48795
- dropbear_ssh_project:dropbear_ssh, `neither` (7): CVE-2016-3116, CVE-2016-7406, CVE-2016-7407, CVE-2017-2659, CVE-2017-9079, CVE-2018-15599, CVE-2019-12953
- libssh:libssh, `both` (13): CVE-2018-10933, CVE-2019-14889, CVE-2020-1730, CVE-2023-3603, CVE-2023-48795, CVE-2025-8114, CVE-2026-0964, CVE-2026-15370, CVE-2026-59842, CVE-2026-59844, CVE-2026-59848, CVE-2026-59849, CVE-2026-59851
- libssh:libssh, `neither` (24): CVE-2012-4559, CVE-2012-4560, CVE-2012-4561, CVE-2012-4562, CVE-2012-6063, CVE-2014-0017, CVE-2014-8132, CVE-2015-3146, CVE-2016-0739, CVE-2020-16135, CVE-2021-3634, CVE-2023-6918, CVE-2025-14821, CVE-2025-5318, CVE-2025-5351, CVE-2025-5372, CVE-2025-5987, CVE-2026-0965, CVE-2026-3731, CVE-2026-59843, CVE-2026-59845, CVE-2026-59846, CVE-2026-59847, CVE-2026-59850
- openbsd:openssh, `both` (26): CVE-1999-1010, CVE-2000-0992, CVE-2000-1169, CVE-2001-0144, CVE-2004-0175, CVE-2005-2798, CVE-2006-0883, CVE-2008-5161, CVE-2014-2653, CVE-2015-5600, CVE-2016-0777, CVE-2016-0778, CVE-2016-1908, CVE-2018-20685, CVE-2019-16905, CVE-2019-6109, CVE-2019-6110, CVE-2019-6111, CVE-2020-12062, CVE-2020-14145, CVE-2021-36368, CVE-2023-48795, CVE-2025-26465, CVE-2025-26466, CVE-2026-55653, CVE-2026-60002
- openbsd:openssh, `neither` (61): CVE-2000-0525, CVE-2000-0999, CVE-2001-0361, CVE-2001-0529, CVE-2001-0572, CVE-2001-0872, CVE-2001-1029, CVE-2001-1380, CVE-2001-1382, CVE-2001-1459, CVE-2001-1507, CVE-2002-0575, CVE-2003-0190, CVE-2003-0386, CVE-2003-0682, CVE-2003-0693, CVE-2003-0695, CVE-2003-0786, CVE-2003-0787, CVE-2004-1653, CVE-2005-2666, CVE-2005-2797, CVE-2006-4925, CVE-2006-5051, CVE-2006-5052, CVE-2007-2243, CVE-2007-2768, CVE-2007-3102, CVE-2007-4654, CVE-2008-1483, CVE-2008-1657, CVE-2008-3259, CVE-2008-3844, CVE-2008-4109, CVE-2010-4478, CVE-2010-4755, CVE-2010-5107, CVE-2011-0539, CVE-2011-4327, CVE-2011-5000, CVE-2014-1692, CVE-2015-5352, CVE-2016-10009, CVE-2016-1907, CVE-2016-8858, CVE-2018-15473, CVE-2018-15919, CVE-2021-28041, CVE-2023-28531, CVE-2023-38408, CVE-2023-51384, CVE-2023-51385, CVE-2023-51767, CVE-2026-106583, CVE-2026-106584, CVE-2026-35386, CVE-2026-35387, CVE-2026-35414, CVE-2026-55654, CVE-2026-73281, CVE-2026-73282

## 7. Configurations
### 7a. CPE part of positive vulnerable matches (S5: a application, o OS, h hardware; per CVE, not exclusive)

**(a) 1,473 included CVEs**

| group | n | a | o | h | no_positive_vulnerable_cpe |
|---|---|---|---|---|---|
| all | 1473 | 1472 | 949 | 6 | 0 |
| family dns | 158 | 158 | 96 | 0 | 0 |
| family ftp | 62 | 62 | 10 | 0 | 0 |
| family http | 189 | 189 | 135 | 0 | 0 |
| family mail | 125 | 125 | 41 | 0 | 0 |
| family rdp | 106 | 106 | 96 | 0 | 0 |
| family smb | 107 | 107 | 80 | 0 | 0 |
| family sql | 668 | 667 | 451 | 4 | 0 |
| family ssh | 58 | 58 | 40 | 2 | 0 |
| product apache:http_server | 87 | 87 | 64 | 0 | 0 |
| product apache:tomcat | 83 | 83 | 54 | 0 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 0 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 0 | 0 | 0 |
| product dovecot:dovecot | 28 | 28 | 24 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 4 | 0 | 0 |
| product exim:exim | 39 | 39 | 15 | 0 | 0 |
| product f5:nginx | 19 | 19 | 18 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 89 | 82 | 0 | 0 |
| product isc:bind | 72 | 72 | 42 | 0 | 0 |
| product libssh:libssh | 11 | 11 | 10 | 0 | 0 |
| product mariadb:mariadb | 200 | 200 | 171 | 1 | 0 |
| product microsoft:exchange_server | 54 | 54 | 0 | 0 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 | 0 | 0 |
| product microsoft:sql_server | 13 | 12 | 1 | 0 | 0 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 14 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 21 | 0 | 0 |
| product openbsd:openssh | 35 | 35 | 26 | 2 | 0 |
| product oracle:mysql | 516 | 516 | 358 | 3 | 0 |
| product postfix:postfix | 3 | 3 | 1 | 0 | 0 |
| product postgresql:postgresql | 70 | 70 | 44 | 0 | 0 |
| product powerdns:authoritative | 17 | 17 | 8 | 0 | 0 |
| product powerdns:recursor | 24 | 24 | 9 | 0 | 0 |
| product proftpd:proftpd | 12 | 12 | 6 | 0 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 4 | 0 | 0 |
| product samba:samba | 107 | 107 | 80 | 0 | 0 |
| product sendmail:sendmail | 1 | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 0 | 0 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 19 | 0 | 0 |
| product wftpserver:wing_ftp_server | 8 | 8 | 0 | 0 | 0 |


**(b) all snapshot records**

| group | n | a | o | h | no_positive_vulnerable_cpe |
|---|---|---|---|---|---|
| all | 4216 | 4215 | 1551 | 13 | 0 |
| family dns | 364 | 364 | 137 | 1 | 0 |
| family ftp | 159 | 159 | 17 | 0 | 0 |
| family http | 777 | 777 | 238 | 1 | 0 |
| family mail | 453 | 453 | 67 | 2 | 0 |
| family rdp | 280 | 280 | 110 | 0 | 0 |
| family smb | 216 | 216 | 126 | 2 | 0 |
| family sql | 1765 | 1764 | 780 | 4 | 0 |
| family ssh | 209 | 209 | 81 | 3 | 0 |
| product apache:http_server | 371 | 371 | 141 | 1 | 0 |
| product apache:tomcat | 276 | 276 | 66 | 0 | 0 |
| product beasts:vsftpd | 2 | 2 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 10 | 0 | 0 | 0 |
| product crushftp:crushftp | 17 | 17 | 1 | 0 | 0 |
| product dovecot:dovecot | 69 | 69 | 25 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 20 | 7 | 0 | 0 |
| product exim:exim | 71 | 71 | 17 | 0 | 0 |
| product f5:nginx | 41 | 41 | 31 | 0 | 0 |
| product filezilla-project:filezilla_server | 7 | 7 | 2 | 0 | 0 |
| product freerdp:freerdp | 243 | 243 | 95 | 0 | 0 |
| product isc:bind | 184 | 184 | 74 | 1 | 0 |
| product libssh:libssh | 45 | 45 | 32 | 0 | 0 |
| product mariadb:mariadb | 431 | 431 | 354 | 1 | 0 |
| product microsoft:exchange_server | 268 | 268 | 13 | 1 | 0 |
| product microsoft:internet_information_services | 93 | 93 | 2 | 0 | 0 |
| product microsoft:sql_server | 110 | 109 | 17 | 0 | 0 |
| product mysql:mysql | 94 | 94 | 9 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 37 | 15 | 0 | 0 |
| product nginx:nginx | 2 | 2 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 73 | 25 | 0 | 0 |
| product openbsd:openssh | 146 | 146 | 44 | 3 | 0 |
| product oracle:mysql | 1328 | 1328 | 641 | 3 | 0 |
| product postfix:postfix | 12 | 12 | 1 | 0 | 0 |
| product postgresql:postgresql | 209 | 209 | 61 | 0 | 0 |
| product powerdns:authoritative | 31 | 31 | 9 | 0 | 0 |
| product powerdns:recursor | 50 | 50 | 13 | 0 | 0 |
| product proftpd:proftpd | 33 | 33 | 9 | 0 | 0 |
| product pureftpd:pure-ftpd | 11 | 11 | 6 | 0 | 0 |
| product samba:samba | 216 | 216 | 126 | 2 | 0 |
| product sendmail:sendmail | 33 | 33 | 11 | 1 | 0 |
| product solarwinds:serv-u | 55 | 55 | 0 | 0 | 0 |
| product thekelleys:dnsmasq | 39 | 39 | 24 | 0 | 0 |
| product wftpserver:wing_ftp_server | 20 | 20 | 0 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 5 | 0 | 0 | 0 |

### 7b. Platform CPEs ('running on/with')
NVD's prose definition of 'running on/with' was UNAVAILABLE (docs/sources.md S3). Operational stand-in: a cpeMatch with `vulnerable: false`, and, stricter, one inside an AND configuration or node.

**(a) 1,473 included CVEs**

| group | n | has_vulnerable_false_cpe | AND_config_with_vulnerable_false |
|---|---|---|---|
| all | 1473 | 114 | 112 |
| family dns | 158 | 17 | 15 |
| family ftp | 62 | 4 | 4 |
| family http | 189 | 29 | 29 |
| family mail | 125 | 6 | 6 |
| family rdp | 106 | 2 | 2 |
| family smb | 107 | 3 | 3 |
| family sql | 668 | 37 | 37 |
| family ssh | 58 | 16 | 16 |
| product apache:http_server | 87 | 14 | 14 |
| product apache:tomcat | 83 | 10 | 10 |
| product cerberusftp:ftp_server | 5 | 0 | 0 |
| product crushftp:crushftp | 7 | 0 | 0 |
| product dovecot:dovecot | 28 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 1 | 1 |
| product exim:exim | 39 | 1 | 1 |
| product f5:nginx | 19 | 5 | 5 |
| product filezilla-project:filezilla_server | 1 | 0 | 0 |
| product freerdp:freerdp | 89 | 2 | 2 |
| product isc:bind | 72 | 13 | 13 |
| product libssh:libssh | 11 | 0 | 0 |
| product mariadb:mariadb | 200 | 8 | 8 |
| product microsoft:exchange_server | 54 | 5 | 5 |
| product microsoft:internet_information_services | 1 | 1 | 1 |
| product microsoft:sql_server | 13 | 0 | 0 |
| product mysql:mysql | 1 | 1 | 1 |
| product neutrinolabs:xrdp | 17 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 1 | 1 |
| product openbsd:openssh | 35 | 15 | 15 |
| product oracle:mysql | 516 | 26 | 26 |
| product postfix:postfix | 3 | 0 | 0 |
| product postgresql:postgresql | 70 | 7 | 7 |
| product powerdns:authoritative | 17 | 0 | 0 |
| product powerdns:recursor | 24 | 0 | 0 |
| product proftpd:proftpd | 12 | 3 | 3 |
| product pureftpd:pure-ftpd | 6 | 0 | 0 |
| product samba:samba | 107 | 3 | 3 |
| product sendmail:sendmail | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 1 | 1 |
| product thekelleys:dnsmasq | 28 | 3 | 1 |
| product wftpserver:wing_ftp_server | 8 | 0 | 0 |


**(b) all snapshot records**

| group | n | has_vulnerable_false_cpe | AND_config_with_vulnerable_false |
|---|---|---|---|
| all | 4216 | 249 | 243 |
| family dns | 364 | 27 | 24 |
| family ftp | 159 | 9 | 9 |
| family http | 777 | 91 | 90 |
| family mail | 453 | 27 | 27 |
| family rdp | 280 | 2 | 2 |
| family smb | 216 | 4 | 4 |
| family sql | 1765 | 64 | 62 |
| family ssh | 209 | 27 | 27 |
| product apache:http_server | 371 | 58 | 57 |
| product apache:tomcat | 276 | 19 | 19 |
| product beasts:vsftpd | 2 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 0 | 0 |
| product crushftp:crushftp | 17 | 1 | 1 |
| product dovecot:dovecot | 69 | 1 | 1 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 2 | 2 |
| product exim:exim | 71 | 2 | 2 |
| product f5:nginx | 41 | 7 | 7 |
| product filezilla-project:filezilla_server | 7 | 2 | 2 |
| product freerdp:freerdp | 243 | 2 | 2 |
| product isc:bind | 184 | 23 | 22 |
| product libssh:libssh | 45 | 1 | 1 |
| product mariadb:mariadb | 431 | 12 | 12 |
| product microsoft:exchange_server | 268 | 18 | 18 |
| product microsoft:internet_information_services | 93 | 8 | 8 |
| product microsoft:sql_server | 110 | 13 | 13 |
| product mysql:mysql | 94 | 3 | 3 |
| product neutrinolabs:xrdp | 37 | 0 | 0 |
| product nginx:nginx | 2 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 1 | 1 |
| product openbsd:openssh | 146 | 26 | 26 |
| product oracle:mysql | 1328 | 29 | 29 |
| product postfix:postfix | 12 | 2 | 2 |
| product postgresql:postgresql | 209 | 15 | 13 |
| product powerdns:authoritative | 31 | 0 | 0 |
| product powerdns:recursor | 50 | 1 | 1 |
| product proftpd:proftpd | 33 | 4 | 4 |
| product pureftpd:pure-ftpd | 11 | 1 | 1 |
| product samba:samba | 216 | 4 | 4 |
| product sendmail:sendmail | 33 | 4 | 4 |
| product solarwinds:serv-u | 55 | 1 | 1 |
| product thekelleys:dnsmasq | 39 | 3 | 1 |
| product wftpserver:wing_ftp_server | 20 | 1 | 1 |
| product xlightftpd:xlight_ftp_server | 5 | 0 | 0 |

### 7c. Vulnerable family products per CVE within its family
(a): products in cves.csv; (b): vulnerable FAMILY_PRODUCTS products over the families that returned it.

**(a) 1,473 included CVEs**

| group | n | 1_products | 2_products |
|---|---|---|---|
| all | 1473 | 1335 | 138 |
| family dns | 158 | 153 | 5 |
| family ftp | 62 | 62 | 0 |
| family http | 189 | 188 | 1 |
| family mail | 125 | 125 | 0 |
| family rdp | 106 | 106 | 0 |
| family smb | 107 | 107 | 0 |
| family sql | 668 | 536 | 132 |
| family ssh | 58 | 58 | 0 |
| product apache:http_server | 87 | 87 | 0 |
| product apache:tomcat | 83 | 82 | 1 |
| product cerberusftp:ftp_server | 5 | 5 | 0 |
| product crushftp:crushftp | 7 | 7 | 0 |
| product dovecot:dovecot | 28 | 28 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 0 |
| product exim:exim | 39 | 39 | 0 |
| product f5:nginx | 19 | 18 | 1 |
| product filezilla-project:filezilla_server | 1 | 1 | 0 |
| product freerdp:freerdp | 89 | 89 | 0 |
| product isc:bind | 72 | 72 | 0 |
| product libssh:libssh | 11 | 11 | 0 |
| product mariadb:mariadb | 200 | 68 | 132 |
| product microsoft:exchange_server | 54 | 54 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 0 |
| product microsoft:sql_server | 13 | 13 | 0 |
| product mysql:mysql | 1 | 0 | 1 |
| product neutrinolabs:xrdp | 17 | 17 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 0 |
| product openbsd:openssh | 35 | 35 | 0 |
| product oracle:mysql | 516 | 385 | 131 |
| product postfix:postfix | 3 | 3 | 0 |
| product postgresql:postgresql | 70 | 70 | 0 |
| product powerdns:authoritative | 17 | 12 | 5 |
| product powerdns:recursor | 24 | 19 | 5 |
| product proftpd:proftpd | 12 | 12 | 0 |
| product pureftpd:pure-ftpd | 6 | 6 | 0 |
| product samba:samba | 107 | 107 | 0 |
| product sendmail:sendmail | 1 | 1 | 0 |
| product solarwinds:serv-u | 23 | 23 | 0 |
| product thekelleys:dnsmasq | 28 | 28 | 0 |
| product wftpserver:wing_ftp_server | 8 | 8 | 0 |


**(b) all snapshot records**

| group | n | 0_products | 1_products | 2_products | 4_products | 5_products |
|---|---|---|---|---|---|---|
| all | 4216 | 48 | 3738 | 428 | 1 | 1 |
| family dns | 364 | 0 | 353 | 10 | 1 | 0 |
| family ftp | 159 | 0 | 157 | 1 | 0 | 1 |
| family http | 777 | 25 | 742 | 10 | 0 | 0 |
| family mail | 453 | 13 | 436 | 4 | 0 | 0 |
| family rdp | 280 | 0 | 280 | 0 | 0 | 0 |
| family smb | 216 | 0 | 216 | 0 | 0 | 0 |
| family sql | 1765 | 10 | 1346 | 409 | 0 | 0 |
| family ssh | 209 | 0 | 208 | 0 | 0 | 1 |
| product apache:http_server | 371 | 21 | 347 | 3 | 0 | 0 |
| product apache:tomcat | 276 | 2 | 271 | 3 | 0 | 0 |
| product beasts:vsftpd | 2 | 0 | 2 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 0 | 10 | 0 | 0 | 0 |
| product crushftp:crushftp | 17 | 0 | 16 | 0 | 0 | 1 |
| product dovecot:dovecot | 69 | 0 | 69 | 0 | 0 | 0 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 0 | 19 | 0 | 0 | 1 |
| product exim:exim | 71 | 1 | 70 | 0 | 0 | 0 |
| product f5:nginx | 41 | 0 | 36 | 5 | 0 | 0 |
| product filezilla-project:filezilla_server | 7 | 0 | 6 | 1 | 0 | 0 |
| product freerdp:freerdp | 243 | 0 | 243 | 0 | 0 | 0 |
| product isc:bind | 184 | 0 | 182 | 1 | 1 | 0 |
| product libssh:libssh | 45 | 0 | 44 | 0 | 0 | 1 |
| product mariadb:mariadb | 431 | 1 | 106 | 324 | 0 | 0 |
| product microsoft:exchange_server | 268 | 12 | 253 | 3 | 0 | 0 |
| product microsoft:internet_information_services | 93 | 2 | 88 | 3 | 0 | 0 |
| product microsoft:sql_server | 110 | 2 | 106 | 2 | 0 | 0 |
| product mysql:mysql | 94 | 2 | 8 | 84 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 0 | 37 | 0 | 0 | 0 |
| product nginx:nginx | 2 | 0 | 0 | 2 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 0 | 72 | 0 | 1 | 0 |
| product openbsd:openssh | 146 | 0 | 145 | 0 | 0 | 1 |
| product oracle:mysql | 1328 | 0 | 923 | 405 | 0 | 0 |
| product postfix:postfix | 12 | 0 | 12 | 0 | 0 | 0 |
| product postgresql:postgresql | 209 | 6 | 203 | 0 | 0 | 0 |
| product powerdns:authoritative | 31 | 0 | 22 | 9 | 0 | 0 |
| product powerdns:recursor | 50 | 0 | 39 | 10 | 1 | 0 |
| product proftpd:proftpd | 33 | 0 | 32 | 0 | 0 | 1 |
| product pureftpd:pure-ftpd | 11 | 0 | 11 | 0 | 0 | 0 |
| product samba:samba | 216 | 0 | 216 | 0 | 0 | 0 |
| product sendmail:sendmail | 33 | 0 | 32 | 1 | 0 | 0 |
| product solarwinds:serv-u | 55 | 0 | 55 | 0 | 0 | 0 |
| product thekelleys:dnsmasq | 39 | 0 | 38 | 0 | 1 | 0 |
| product wftpserver:wing_ftp_server | 20 | 0 | 20 | 0 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 0 | 5 | 0 | 0 | 0 |

## 8. Funnel: 'usable as a remote foothold' = AV:N ∧ PR:N ∧ UI:N ∧ code-exec ∧ server role

**This is a count, not an adopted criterion.** Each column counts CVEs that pass every condition to its left. Server role = the CVE's role (§6) is `server`. One funnel per code-exec candidate; R-TEXT is diagnostic only. R-CWE `undetermined` fails the code-exec step.

**8 (a) code-exec = R-CWE**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 1473 | 1473 | 1300 | 669 | 602 | 261 | 157 |
| family dns | 158 | 158 | 156 | 136 | 135 | 56 | 56 |
| family ftp | 62 | 62 | 57 | 39 | 29 | 9 | 9 |
| family http | 189 | 189 | 172 | 160 | 147 | 62 | 46 |
| family mail | 125 | 125 | 96 | 82 | 59 | 28 | 24 |
| family rdp | 106 | 106 | 102 | 61 | 59 | 35 | 7 |
| family smb | 107 | 107 | 97 | 40 | 34 | 13 | 13 |
| family sql | 668 | 668 | 573 | 113 | 105 | 37 | 2 |
| family ssh | 58 | 58 | 47 | 38 | 34 | 21 | 0 |
| product apache:http_server | 87 | 87 | 84 | 79 | 75 | 38 | 38 |
| product apache:tomcat | 83 | 83 | 73 | 67 | 58 | 16 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 5 | 3 | 1 | 1 | 1 |
| product crushftp:crushftp | 7 | 7 | 7 | 6 | 2 | 1 | 1 |
| product dovecot:dovecot | 28 | 28 | 25 | 20 | 20 | 11 | 11 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 10 | 7 | 7 | 4 | 0 |
| product exim:exim | 39 | 39 | 25 | 24 | 24 | 13 | 13 |
| product f5:nginx | 19 | 19 | 15 | 14 | 14 | 7 | 7 |
| product filezilla-project:filezilla_server | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 89 | 88 | 49 | 47 | 28 | 0 |
| product isc:bind | 72 | 72 | 71 | 60 | 60 | 16 | 16 |
| product libssh:libssh | 11 | 11 | 11 | 8 | 7 | 4 | 0 |
| product mariadb:mariadb | 200 | 200 | 144 | 50 | 50 | 22 | 0 |
| product microsoft:exchange_server | 54 | 54 | 43 | 35 | 12 | 4 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| product microsoft:sql_server | 13 | 13 | 12 | 4 | 3 | 2 | 2 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 14 | 12 | 12 | 7 | 7 |
| product nlnetlabs:unbound | 22 | 22 | 21 | 19 | 19 | 9 | 9 |
| product openbsd:openssh | 35 | 35 | 26 | 23 | 20 | 13 | 0 |
| product oracle:mysql | 516 | 516 | 457 | 47 | 41 | 6 | 0 |
| product postfix:postfix | 3 | 3 | 2 | 2 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 70 | 60 | 22 | 21 | 8 | 0 |
| product powerdns:authoritative | 17 | 17 | 17 | 13 | 13 | 7 | 7 |
| product powerdns:recursor | 24 | 24 | 24 | 21 | 20 | 9 | 9 |
| product proftpd:proftpd | 12 | 12 | 11 | 9 | 9 | 1 | 1 |
| product pureftpd:pure-ftpd | 6 | 6 | 6 | 6 | 6 | 2 | 2 |
| product samba:samba | 107 | 107 | 97 | 40 | 34 | 13 | 13 |
| product sendmail:sendmail | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 22 | 13 | 10 | 4 | 4 |
| product thekelleys:dnsmasq | 28 | 28 | 28 | 28 | 28 | 18 | 18 |
| product wftpserver:wing_ftp_server | 8 | 8 | 5 | 2 | 1 | 0 | 0 |

Families with 0 CVEs at the end: ssh.

**8 (b) code-exec = R-CWE**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 4216 | 1816 | 1603 | 920 | 823 | 381 | 201 |
| family dns | 364 | 201 | 197 | 172 | 171 | 68 | 68 |
| family ftp | 159 | 88 | 81 | 50 | 39 | 12 | 12 |
| family http | 777 | 224 | 204 | 191 | 176 | 74 | 53 |
| family mail | 453 | 179 | 134 | 112 | 86 | 46 | 40 |
| family rdp | 280 | 209 | 203 | 160 | 143 | 95 | 11 |
| family smb | 216 | 117 | 106 | 47 | 41 | 15 | 15 |
| family sql | 1765 | 697 | 600 | 122 | 113 | 41 | 2 |
| family ssh | 209 | 104 | 81 | 69 | 57 | 30 | 0 |
| product apache:http_server | 371 | 107 | 102 | 96 | 90 | 44 | 43 |
| product apache:tomcat | 276 | 95 | 84 | 78 | 69 | 20 | 0 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 6 | 6 | 3 | 1 | 1 | 1 |
| product crushftp:crushftp | 17 | 11 | 11 | 10 | 6 | 2 | 2 |
| product dovecot:dovecot | 69 | 40 | 35 | 28 | 28 | 17 | 17 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 13 | 11 | 8 | 8 | 4 | 0 |
| product exim:exim | 71 | 58 | 39 | 38 | 38 | 21 | 21 |
| product f5:nginx | 41 | 20 | 16 | 15 | 15 | 7 | 7 |
| product filezilla-project:filezilla_server | 7 | 3 | 3 | 2 | 2 | 0 | 0 |
| product freerdp:freerdp | 243 | 182 | 180 | 140 | 123 | 84 | 0 |
| product isc:bind | 184 | 80 | 78 | 67 | 67 | 18 | 18 |
| product libssh:libssh | 45 | 27 | 21 | 17 | 14 | 7 | 0 |
| product mariadb:mariadb | 431 | 211 | 154 | 55 | 55 | 26 | 0 |
| product microsoft:exchange_server | 268 | 74 | 54 | 40 | 14 | 6 | 0 |
| product microsoft:internet_information_services | 93 | 3 | 3 | 3 | 3 | 3 | 3 |
| product microsoft:sql_server | 110 | 15 | 14 | 6 | 4 | 2 | 2 |
| product mysql:mysql | 94 | 2 | 1 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 27 | 23 | 20 | 20 | 11 | 11 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 42 | 40 | 38 | 38 | 14 | 14 |
| product openbsd:openssh | 146 | 66 | 51 | 46 | 37 | 19 | 0 |
| product oracle:mysql | 1328 | 521 | 461 | 47 | 41 | 6 | 0 |
| product postfix:postfix | 12 | 4 | 3 | 3 | 3 | 1 | 1 |
| product postgresql:postgresql | 209 | 82 | 72 | 24 | 23 | 8 | 0 |
| product powerdns:authoritative | 31 | 26 | 26 | 19 | 19 | 10 | 10 |
| product powerdns:recursor | 50 | 33 | 33 | 28 | 27 | 10 | 10 |
| product proftpd:proftpd | 33 | 16 | 14 | 11 | 11 | 1 | 1 |
| product pureftpd:pure-ftpd | 11 | 6 | 6 | 6 | 6 | 2 | 2 |
| product samba:samba | 216 | 117 | 106 | 47 | 41 | 15 | 15 |
| product sendmail:sendmail | 33 | 3 | 3 | 3 | 3 | 1 | 1 |
| product solarwinds:serv-u | 55 | 33 | 32 | 14 | 11 | 5 | 5 |
| product thekelleys:dnsmasq | 39 | 31 | 31 | 31 | 31 | 19 | 19 |
| product wftpserver:wing_ftp_server | 20 | 11 | 8 | 3 | 1 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 2 | 2 | 2 | 1 | 1 |

Families with 0 CVEs at the end: ssh.

**8 (a) code-exec = R-CIA**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 1473 | 1473 | 1300 | 669 | 602 | 147 | 87 |
| family dns | 158 | 158 | 156 | 136 | 135 | 25 | 25 |
| family ftp | 62 | 62 | 57 | 39 | 29 | 6 | 6 |
| family http | 189 | 189 | 172 | 160 | 147 | 33 | 22 |
| family mail | 125 | 125 | 96 | 82 | 59 | 24 | 15 |
| family rdp | 106 | 106 | 102 | 61 | 59 | 23 | 7 |
| family smb | 107 | 107 | 97 | 40 | 34 | 11 | 11 |
| family sql | 668 | 668 | 573 | 113 | 105 | 17 | 1 |
| family ssh | 58 | 58 | 47 | 38 | 34 | 8 | 0 |
| product apache:http_server | 87 | 87 | 84 | 79 | 75 | 18 | 18 |
| product apache:tomcat | 83 | 83 | 73 | 67 | 58 | 11 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 5 | 3 | 1 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 7 | 6 | 2 | 2 | 2 |
| product dovecot:dovecot | 28 | 28 | 25 | 20 | 20 | 1 | 1 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 10 | 7 | 7 | 3 | 0 |
| product exim:exim | 39 | 39 | 25 | 24 | 24 | 14 | 14 |
| product f5:nginx | 19 | 19 | 15 | 14 | 14 | 3 | 3 |
| product filezilla-project:filezilla_server | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 89 | 88 | 49 | 47 | 16 | 0 |
| product isc:bind | 72 | 72 | 71 | 60 | 60 | 2 | 2 |
| product libssh:libssh | 11 | 11 | 11 | 8 | 7 | 1 | 0 |
| product mariadb:mariadb | 200 | 200 | 144 | 50 | 50 | 3 | 0 |
| product microsoft:exchange_server | 54 | 54 | 43 | 35 | 12 | 9 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| product microsoft:sql_server | 13 | 13 | 12 | 4 | 3 | 1 | 1 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 14 | 12 | 12 | 7 | 7 |
| product nlnetlabs:unbound | 22 | 22 | 21 | 19 | 19 | 7 | 7 |
| product openbsd:openssh | 35 | 35 | 26 | 23 | 20 | 4 | 0 |
| product oracle:mysql | 516 | 516 | 457 | 47 | 41 | 7 | 0 |
| product postfix:postfix | 3 | 3 | 2 | 2 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 70 | 60 | 22 | 21 | 8 | 0 |
| product powerdns:authoritative | 17 | 17 | 17 | 13 | 13 | 2 | 2 |
| product powerdns:recursor | 24 | 24 | 24 | 21 | 20 | 2 | 2 |
| product proftpd:proftpd | 12 | 12 | 11 | 9 | 9 | 1 | 1 |
| product pureftpd:pure-ftpd | 6 | 6 | 6 | 6 | 6 | 1 | 1 |
| product samba:samba | 107 | 107 | 97 | 40 | 34 | 11 | 11 |
| product sendmail:sendmail | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 22 | 13 | 10 | 2 | 2 |
| product thekelleys:dnsmasq | 28 | 28 | 28 | 28 | 28 | 12 | 12 |
| product wftpserver:wing_ftp_server | 8 | 8 | 5 | 2 | 1 | 0 | 0 |

Families with 0 CVEs at the end: ssh.

**8 (b) code-exec = R-CIA**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 4216 | 1816 | 1603 | 920 | 823 | 225 | 113 |
| family dns | 364 | 201 | 197 | 172 | 171 | 30 | 30 |
| family ftp | 159 | 88 | 81 | 50 | 39 | 11 | 10 |
| family http | 777 | 224 | 204 | 191 | 176 | 41 | 27 |
| family mail | 453 | 179 | 134 | 112 | 86 | 33 | 23 |
| family rdp | 280 | 209 | 203 | 160 | 143 | 63 | 11 |
| family smb | 216 | 117 | 106 | 47 | 41 | 12 | 12 |
| family sql | 1765 | 697 | 600 | 122 | 113 | 21 | 1 |
| family ssh | 209 | 104 | 81 | 69 | 57 | 16 | 0 |
| product apache:http_server | 371 | 107 | 102 | 96 | 90 | 22 | 22 |
| product apache:tomcat | 276 | 95 | 84 | 78 | 69 | 14 | 0 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 6 | 6 | 3 | 1 | 0 | 0 |
| product crushftp:crushftp | 17 | 11 | 11 | 10 | 6 | 5 | 5 |
| product dovecot:dovecot | 69 | 40 | 35 | 28 | 28 | 2 | 2 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 13 | 11 | 8 | 8 | 3 | 0 |
| product exim:exim | 71 | 58 | 39 | 38 | 38 | 20 | 20 |
| product f5:nginx | 41 | 20 | 16 | 15 | 15 | 4 | 4 |
| product filezilla-project:filezilla_server | 7 | 3 | 3 | 2 | 2 | 1 | 0 |
| product freerdp:freerdp | 243 | 182 | 180 | 140 | 123 | 52 | 0 |
| product isc:bind | 184 | 80 | 78 | 67 | 67 | 3 | 3 |
| product libssh:libssh | 45 | 27 | 21 | 17 | 14 | 1 | 0 |
| product mariadb:mariadb | 431 | 211 | 154 | 55 | 55 | 7 | 0 |
| product microsoft:exchange_server | 268 | 74 | 54 | 40 | 14 | 10 | 0 |
| product microsoft:internet_information_services | 93 | 3 | 3 | 3 | 3 | 1 | 1 |
| product microsoft:sql_server | 110 | 15 | 14 | 6 | 4 | 1 | 1 |
| product mysql:mysql | 94 | 2 | 1 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 27 | 23 | 20 | 20 | 11 | 11 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 42 | 40 | 38 | 38 | 10 | 10 |
| product openbsd:openssh | 146 | 66 | 51 | 46 | 37 | 12 | 0 |
| product oracle:mysql | 1328 | 521 | 461 | 47 | 41 | 7 | 0 |
| product postfix:postfix | 12 | 4 | 3 | 3 | 3 | 0 | 0 |
| product postgresql:postgresql | 209 | 82 | 72 | 24 | 23 | 8 | 0 |
| product powerdns:authoritative | 31 | 26 | 26 | 19 | 19 | 3 | 3 |
| product powerdns:recursor | 50 | 33 | 33 | 28 | 27 | 2 | 2 |
| product proftpd:proftpd | 33 | 16 | 14 | 11 | 11 | 2 | 2 |
| product pureftpd:pure-ftpd | 11 | 6 | 6 | 6 | 6 | 1 | 1 |
| product samba:samba | 216 | 117 | 106 | 47 | 41 | 12 | 12 |
| product sendmail:sendmail | 33 | 3 | 3 | 3 | 3 | 1 | 1 |
| product solarwinds:serv-u | 55 | 33 | 32 | 14 | 11 | 2 | 2 |
| product thekelleys:dnsmasq | 39 | 31 | 31 | 31 | 31 | 12 | 12 |
| product wftpserver:wing_ftp_server | 20 | 11 | 8 | 3 | 1 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 2 | 2 | 2 | 0 | 0 |

Families with 0 CVEs at the end: ssh.

**8 (a) code-exec = R-TEXT**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 1473 | 1473 | 1300 | 669 | 602 | 55 | 32 |
| family dns | 158 | 158 | 156 | 136 | 135 | 10 | 10 |
| family ftp | 62 | 62 | 57 | 39 | 29 | 2 | 2 |
| family http | 189 | 189 | 172 | 160 | 147 | 6 | 3 |
| family mail | 125 | 125 | 96 | 82 | 59 | 15 | 11 |
| family rdp | 106 | 106 | 102 | 61 | 59 | 7 | 0 |
| family smb | 107 | 107 | 97 | 40 | 34 | 4 | 4 |
| family sql | 668 | 668 | 573 | 113 | 105 | 6 | 2 |
| family ssh | 58 | 58 | 47 | 38 | 34 | 5 | 0 |
| product apache:http_server | 87 | 87 | 84 | 79 | 75 | 2 | 2 |
| product apache:tomcat | 83 | 83 | 73 | 67 | 58 | 3 | 0 |
| product cerberusftp:ftp_server | 5 | 5 | 5 | 3 | 1 | 0 | 0 |
| product crushftp:crushftp | 7 | 7 | 7 | 6 | 2 | 0 | 0 |
| product dovecot:dovecot | 28 | 28 | 25 | 20 | 20 | 2 | 2 |
| product dropbear_ssh_project:dropbear_ssh | 12 | 12 | 10 | 7 | 7 | 2 | 0 |
| product exim:exim | 39 | 39 | 25 | 24 | 24 | 9 | 9 |
| product f5:nginx | 19 | 19 | 15 | 14 | 14 | 0 | 0 |
| product filezilla-project:filezilla_server | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| product freerdp:freerdp | 89 | 89 | 88 | 49 | 47 | 7 | 0 |
| product isc:bind | 72 | 72 | 71 | 60 | 60 | 2 | 2 |
| product libssh:libssh | 11 | 11 | 11 | 8 | 7 | 0 | 0 |
| product mariadb:mariadb | 200 | 200 | 144 | 50 | 50 | 2 | 0 |
| product microsoft:exchange_server | 54 | 54 | 43 | 35 | 12 | 4 | 0 |
| product microsoft:internet_information_services | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| product microsoft:sql_server | 13 | 13 | 12 | 4 | 3 | 2 | 2 |
| product mysql:mysql | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 17 | 17 | 14 | 12 | 12 | 0 | 0 |
| product nlnetlabs:unbound | 22 | 22 | 21 | 19 | 19 | 1 | 1 |
| product openbsd:openssh | 35 | 35 | 26 | 23 | 20 | 3 | 0 |
| product oracle:mysql | 516 | 516 | 457 | 47 | 41 | 1 | 0 |
| product postfix:postfix | 3 | 3 | 2 | 2 | 2 | 0 | 0 |
| product postgresql:postgresql | 70 | 70 | 60 | 22 | 21 | 2 | 0 |
| product powerdns:authoritative | 17 | 17 | 17 | 13 | 13 | 2 | 2 |
| product powerdns:recursor | 24 | 24 | 24 | 21 | 20 | 0 | 0 |
| product proftpd:proftpd | 12 | 12 | 11 | 9 | 9 | 1 | 1 |
| product pureftpd:pure-ftpd | 6 | 6 | 6 | 6 | 6 | 0 | 0 |
| product samba:samba | 107 | 107 | 97 | 40 | 34 | 4 | 4 |
| product sendmail:sendmail | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| product solarwinds:serv-u | 23 | 23 | 22 | 13 | 10 | 1 | 1 |
| product thekelleys:dnsmasq | 28 | 28 | 28 | 28 | 28 | 5 | 5 |
| product wftpserver:wing_ftp_server | 8 | 8 | 5 | 2 | 1 | 0 | 0 |

Families with 0 CVEs at the end: rdp, ssh.

**8 (b) code-exec = R-TEXT**

| group | n | d11_score | AV:N | PR:N | UI:N | code_exec | server_role |
|---|---|---|---|---|---|---|---|
| all | 4216 | 1816 | 1603 | 920 | 823 | 79 | 44 |
| family dns | 364 | 201 | 197 | 172 | 171 | 13 | 13 |
| family ftp | 159 | 88 | 81 | 50 | 39 | 4 | 4 |
| family http | 777 | 224 | 204 | 191 | 176 | 9 | 4 |
| family mail | 453 | 179 | 134 | 112 | 86 | 19 | 14 |
| family rdp | 280 | 209 | 203 | 160 | 143 | 13 | 2 |
| family smb | 216 | 117 | 106 | 47 | 41 | 5 | 5 |
| family sql | 1765 | 697 | 600 | 122 | 113 | 8 | 2 |
| family ssh | 209 | 104 | 81 | 69 | 57 | 8 | 0 |
| product apache:http_server | 371 | 107 | 102 | 96 | 90 | 4 | 3 |
| product apache:tomcat | 276 | 95 | 84 | 78 | 69 | 4 | 0 |
| product beasts:vsftpd | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product cerberusftp:ftp_server | 10 | 6 | 6 | 3 | 1 | 0 | 0 |
| product crushftp:crushftp | 17 | 11 | 11 | 10 | 6 | 1 | 1 |
| product dovecot:dovecot | 69 | 40 | 35 | 28 | 28 | 2 | 2 |
| product dropbear_ssh_project:dropbear_ssh | 20 | 13 | 11 | 8 | 8 | 2 | 0 |
| product exim:exim | 71 | 58 | 39 | 38 | 38 | 12 | 12 |
| product f5:nginx | 41 | 20 | 16 | 15 | 15 | 0 | 0 |
| product filezilla-project:filezilla_server | 7 | 3 | 3 | 2 | 2 | 0 | 0 |
| product freerdp:freerdp | 243 | 182 | 180 | 140 | 123 | 11 | 0 |
| product isc:bind | 184 | 80 | 78 | 67 | 67 | 2 | 2 |
| product libssh:libssh | 45 | 27 | 21 | 17 | 14 | 0 | 0 |
| product mariadb:mariadb | 431 | 211 | 154 | 55 | 55 | 4 | 0 |
| product microsoft:exchange_server | 268 | 74 | 54 | 40 | 14 | 5 | 0 |
| product microsoft:internet_information_services | 93 | 3 | 3 | 3 | 3 | 1 | 1 |
| product microsoft:sql_server | 110 | 15 | 14 | 6 | 4 | 2 | 2 |
| product mysql:mysql | 94 | 2 | 1 | 0 | 0 | 0 | 0 |
| product neutrinolabs:xrdp | 37 | 27 | 23 | 20 | 20 | 2 | 2 |
| product nginx:nginx | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| product nlnetlabs:unbound | 73 | 42 | 40 | 38 | 38 | 4 | 4 |
| product openbsd:openssh | 146 | 66 | 51 | 46 | 37 | 6 | 0 |
| product oracle:mysql | 1328 | 521 | 461 | 47 | 41 | 1 | 0 |
| product postfix:postfix | 12 | 4 | 3 | 3 | 3 | 0 | 0 |
| product postgresql:postgresql | 209 | 82 | 72 | 24 | 23 | 2 | 0 |
| product powerdns:authoritative | 31 | 26 | 26 | 19 | 19 | 2 | 2 |
| product powerdns:recursor | 50 | 33 | 33 | 28 | 27 | 0 | 0 |
| product proftpd:proftpd | 33 | 16 | 14 | 11 | 11 | 2 | 2 |
| product pureftpd:pure-ftpd | 11 | 6 | 6 | 6 | 6 | 0 | 0 |
| product samba:samba | 216 | 117 | 106 | 47 | 41 | 5 | 5 |
| product sendmail:sendmail | 33 | 3 | 3 | 3 | 3 | 0 | 0 |
| product solarwinds:serv-u | 55 | 33 | 32 | 14 | 11 | 1 | 1 |
| product thekelleys:dnsmasq | 39 | 31 | 31 | 31 | 31 | 5 | 5 |
| product wftpserver:wing_ftp_server | 20 | 11 | 8 | 3 | 1 | 0 | 0 |
| product xlightftpd:xlight_ftp_server | 5 | 3 | 2 | 2 | 2 | 0 | 0 |

Families with 0 CVEs at the end: ssh.

## D26 re-verification from the raw snapshot

- E1: AV among the 1473 included CVEs (D11 vector): A 13, L 160, N 1300. D26 states 160 AV:L and 13 AV:A: **match**.
- E5: 89 of 106 included rdp CVEs list freerdp:freerdp. D26 states 89 of 106: **match**.

