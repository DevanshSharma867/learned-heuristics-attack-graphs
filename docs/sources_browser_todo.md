# Browser to-do: pages an automated fetch could not read (2026-11-08, round 2)

Each of these failed for curl with its default user agent (blocked, client-rendered, redirected, or no usable
content). None was retried with a changed user agent. Please open each in a browser and **save it as PDF** under
`data/raw/sources/2026-11-08/` with exactly the filename given. Part 2 Step 8 reads them, hashes them and
completes the rows that cite them.

| # | URL | save as (`data/raw/sources/2026-11-08/…`) | what failed | needed for |
|---|---|---|---|---|
| 1 | https://filezilla-project.org/download.php?type=server | `filezilla_server_download.pdf` | HTTP 200, but the served page is navigation plus a download block, with no description; the wiki page https://wiki.filezilla-project.org/FileZilla_Server is 404 | `docs/sources.md` P9 (role of `filezilla-project:filezilla_server`, still UNAVAILABLE) |
| 2 | https://filezilla-project.org/ (rendered home page, including any "FileZilla Server" description) | `filezilla_home.pdf` | as #1 | P9, if #1 has no role statement |
| 3 | https://docs.redhat.com/en/documentation/red_hat_security_data_api/1.0/html/red_hat_security_data_api/cve | `redhat_security_data_api_cve.pdf` | HTTP 403 | S13: definition of Red Hat's per-CVE `package_state` / `affected_release` fields (currently only an example record was read) |
| 4 | https://msrc.microsoft.com/update-guide/vulnerability/CVE-2016-7249 | `msrc_CVE-2016-7249.pdf` | client-rendered shell (2,717 bytes, no CVE text) | protocol pilot (Step 10): vendor advisory for CVE-2016-7249 (SQL Server) |
| 5 | https://msrc.microsoft.com/update-guide/vulnerability/CVE-2018-8302 | `msrc_CVE-2018-8302.pdf` | as #4 (NVD link https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2018-8302 redirects there) | pilot: CVE-2018-8302 (Exchange) |
| 6 | https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-0618 | `msrc_CVE-2020-0618.pdf` | as #5 | pilot: CVE-2020-0618 (SQL Server Reporting Services) |
| 7 | https://mariadb.com/kb/en/security/ | `mariadb_kb_security.pdf` | redirected to a documentation landing page (same 682,133 bytes as the "about" page) without the security list | pilot: CVE-2022-24051 and CVE-2022-32081 (MariaDB) |

## Not browser items (for the record)

- **CVE-2017-2834 (FreeRDP):** NVD lists no vendor reference (only Talos TALOS-2017-0336, Debian DSA-3923 and
  a broken SecurityFocus link), and the FreeRDP GitHub advisory list's latest 100 entries all date from 2026.
  The pilot will label it from a vendor source only if Devansh names one; otherwise CANNOT_TELL.
- **CVE-2013-4119 (FreeRDP):** no advisory. The project's own fix commit 0773bb93 was fetched through the GitHub
  API (`advisories/CVE-2013-4119__0.json`).
- **Pages that do not print the CVE ID** (fetched fine; the pilot must match by content): CVE-2016-8652 (Dovecot
  announcement, 2016-12) and CVE-2021-28041 (openssh.com security page and release-8.5 notes).
- **NVD count query that failed twice** (network-level, not a page): `virtualMatchString=cpe:2.3:o:linux:linux_kernel
  &cvssV3Metrics=AV:N/PR:N/UI:N&noRejected`. It will be retried in Part 2 with the same query string.
- https://www.first.org/epss/model and /epss/api returned 404 (the EPSS home and FAQ pages supplied the
  definition), and https://www.postfix.org/ failed over TLS (the same page was read over http). Neither is needed.
