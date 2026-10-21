"""CVE records per service family: the D11 rules as pure functions.

The pipeline:

- scripts/fetch_nvd.py downloads the pinned NVD snapshot, one query per
  product in FAMILY_PRODUCTS.
- derive() turns it into one CveRecord per included CVE, plus a count of
  every exclusion and its reason.
- scripts/derive_cves.py writes those as data/derived/cves.csv and
  build_log.json.

Inclusion rule (D11):

- NVD marks the CVE vulnerable for a product of exactly one family.
- It has an NVD Primary v3.1 (else v3.0) exploitabilityScore.
- It was published in WINDOW.
"""

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

FAMILY_PRODUCTS: dict[str, tuple[str, ...]] = {
    "dns": ("isc:bind", "nlnetlabs:unbound", "powerdns:authoritative", "powerdns:recursor", "thekelleys:dnsmasq"),
    "ftp": (
        "beasts:vsftpd", "cerberusftp:ftp_server", "crushftp:crushftp", "filezilla-project:filezilla_server",
        "proftpd:proftpd", "pureftpd:pure-ftpd", "solarwinds:serv-u", "wftpserver:wing_ftp_server",
        "xlightftpd:xlight_ftp_server",
    ),
    "http": ("apache:http_server", "apache:tomcat", "f5:nginx", "microsoft:internet_information_services", "nginx:nginx"),
    "mail": ("dovecot:dovecot", "exim:exim", "microsoft:exchange_server", "postfix:postfix", "sendmail:sendmail"),
    "rdp": ("freerdp:freerdp", "neutrinolabs:xrdp"),  # known modelling limitation, see D11
    "smb": ("samba:samba",),
    "sql": ("mariadb:mariadb", "microsoft:sql_server", "mysql:mysql", "oracle:mysql", "postgresql:postgresql"),
    "ssh": ("dropbear_ssh_project:dropbear_ssh", "libssh:libssh", "openbsd:openssh"),
}  # fmt: skip
WINDOW = (date(2016, 1, 1), date(2023, 12, 31))
NVD_SOURCE = "nvd@nist.gov"
CSV_FIELDS = ("cve_id", "family", "products", "cvss_version", "exploitability_score", "published")
# Every outcome derive() can assign to a (CVE, family) pair, in rule order.
OUTCOMES = (
    "included", "platform_only", "multi_family", "v3_cna_only", "v2_only", "v4_only",
    "v2_and_v4_no_v3", "no_score", "outside_window",
)  # fmt: skip


@dataclass(frozen=True, order=True)
class CveRecord:
    cve_id: str
    family: str
    products: str  # vendor:product names matched as vulnerable, ";"-joined and sorted
    cvss_version: str  # "3.0" or "3.1"
    exploitability_score: float
    published: date


def nvd_primary_v3(cve: dict) -> tuple[str, float] | None:
    """(version, exploitabilityScore) of NVD's own v3.1 score, else its v3.0 score, else None.

    CNA scores (type "Secondary") are ignored. One CVE can carry both NVD's
    and the CNA's score, and D11 uses a single scorer, NVD.
    """
    metrics = cve.get("metrics", {})
    for key, version in (("cvssMetricV31", "3.1"), ("cvssMetricV30", "3.0")):
        for m in metrics.get(key, []):
            if m.get("source") == NVD_SOURCE and m.get("type") == "Primary":
                return version, float(m["exploitabilityScore"])
    return None


def score_status(cve: dict) -> str:
    """'ok' if the CVE has an NVD Primary v3 score, else the exclusion reason."""
    if nvd_primary_v3(cve) is not None:
        return "ok"
    m = cve.get("metrics", {})
    has3 = bool(m.get("cvssMetricV31") or m.get("cvssMetricV30"))
    has2, has4 = bool(m.get("cvssMetricV2")), bool(m.get("cvssMetricV40"))
    if has3:
        return "v3_cna_only"
    if has2 and has4:
        return "v2_and_v4_no_v3"
    if has2:
        return "v2_only"
    if has4:
        return "v4_only"
    return "no_score"


def vulnerable_products(cve: dict, products) -> set[str]:
    """Products from `products` named by a cpeMatch entry with vulnerable: true.

    A CPE query also returns CVEs where the product is only the platform
    (e.g. "app X running on product Y"). Those are not vulnerabilities of
    the product, so they are not counted here.
    """
    hit = set()
    for cfg in cve.get("configurations", []):
        for node in cfg.get("nodes", []):
            for m in node.get("cpeMatch", []):
                if m.get("vulnerable"):
                    criteria = m.get("criteria", "")
                    hit.update(p for p in products if f":{p}:" in criteria)
    return hit


def derive(matches) -> tuple[list[CveRecord], Counter]:
    """Apply the D11 rules.

    matches: iterable of (family, product, cve dict), one per CVE returned by
    that product's query. The same CVE may appear under several products.

    Returns the included records, sorted, and a Counter of
    (family, reason) -> number of CVEs. reason is "included" or an exclusion
    reason. Each (CVE, family) pair is counted exactly once. The first rule it
    fails, in this order, is its reason:

    1. platform_only: no product of this family is marked vulnerable.
    2. multi_family: vulnerable products in more than one family. The CVE is
       dropped from every family so that families stay disjoint.
    3. score: v3_cna_only, v2_only, v4_only, v2_and_v4_no_v3 or no_score.
    4. outside_window: published outside WINDOW.
    """
    cves: dict[str, dict] = {}
    seen: dict[str, set[str]] = defaultdict(set)  # cve_id -> families whose query returned it
    vuln: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))  # cve_id -> family -> products
    for family, product, cve in matches:
        cid = cve["id"]
        cves[cid] = cve
        seen[cid].add(family)
        if vulnerable_products(cve, [product]):
            vuln[cid][family].add(product)

    records, counts = [], Counter()
    for cid in sorted(cves):
        cve, vfams = cves[cid], vuln[cid]
        for family in sorted(seen[cid]):
            if family not in vfams:
                counts[family, "platform_only"] += 1
                continue
            if len(vfams) > 1:
                counts[family, "multi_family"] += 1
                continue
            status = score_status(cve)
            if status != "ok":
                counts[family, status] += 1
                continue
            published = date.fromisoformat(cve["published"][:10])
            if not WINDOW[0] <= published <= WINDOW[1]:
                counts[family, "outside_window"] += 1
                continue
            version, score = nvd_primary_v3(cve)
            records.append(CveRecord(cid, family, ";".join(sorted(vfams[family])), version, score, published))
            counts[family, "included"] += 1
    return sorted(records), counts


def write_table(records: list[CveRecord], path: Path) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(CSV_FIELDS)
        for r in records:
            w.writerow([r.cve_id, r.family, r.products, r.cvss_version, f"{r.exploitability_score:.1f}", r.published.isoformat()])


def load_table(path: Path) -> list[CveRecord]:
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and tuple(rows[0]) != CSV_FIELDS:
        raise ValueError(f"unexpected columns in {path}: {tuple(rows[0])}")
    return [
        CveRecord(r["cve_id"], r["family"], r["products"], r["cvss_version"], float(r["exploitability_score"]),
                  date.fromisoformat(r["published"]))
        for r in rows
    ]  # fmt: skip
