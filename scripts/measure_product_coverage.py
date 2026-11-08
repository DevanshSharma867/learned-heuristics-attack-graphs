"""Counts for the proposed product list (docs/proposals/product_list_v1.md). Analysis only; nothing adopted.

Usage: python scripts/measure_product_coverage.py

Reads only stored inputs (no network):
- data/raw/sources/2026-11-08/nvd_count_queries.jsonl: NVD CVE API count-only queries made by
  scripts/nvd_count_only.py (totalResults only; no records were stored);
- data/raw/sources/2026-11-08/msrc/cvrf_<YYYY-Mon>.json: MSRC Security Update Guide CVRF documents, 2016–2023;
- data/raw/sources/2026-11-08/kev/known_exploited_vulnerabilities.json: the CISA KEV catalog;
- data/raw/nvd/2026-10-21/ and data/derived/cves.csv: the pinned snapshot, for current FAMILY_PRODUCTS coverage.

Writes results/cve_semantics/product_coverage/<stamp>-<commit>/ through ahg.runlog. Every input's SHA-256 is
recorded in raw.json.gz.

MSRC CVRF JSON uses numeric types. Their names come from MSRC's own XML rendering of the same document
(cvrf_2017-Mar.xml): Note Type 7 = "Tag", Threat Type 0 = "Impact" (docs/sources.md S9).
"""

import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ahg import runlog  # noqa: E402

SRC = ROOT / "data" / "raw" / "sources" / "2026-11-08"
SNAP = ROOT / "data" / "raw" / "nvd" / "2026-10-21"
NOTE_TAG, THREAT_IMPACT = 7, 0  # MSRC CVRF JSON codes, named "Tag" and "Impact" in the XML rendering

# Proposed categories (docs/proposals/product_list_v1.md §2). C1 is the current FAMILY_PRODUCTS.
WIN_SERVICE_TAGS = {
    "Windows SMB Server", "Windows SMB", "Windows RDP", "Windows Remote Desktop", "Role: DNS Server",
    "Microsoft Windows DNS", "Windows DNS", "Windows HTTP.sys", "HTTP.sys", "Windows HTTP Protocol Stack",
    "Windows IIS", "Windows LDAP - Lightweight Directory Access Protocol", "Windows Kerberos", "Kerberos",
    "Windows Active Directory", "Active Directory Domain Services", "Active Directory",
    "Role: Windows Active Directory Server", "Windows Netlogon", "Windows TCP/IP",
}  # fmt: skip
# "Microsoft Office SharePoint*" tags are a server product, not client-side (D27 step 2).
WIN_CLIENT_TAGS_RE = re.compile(r"^(Internet Explorer|Microsoft Edge|Microsoft Office(?! SharePoint)|Microsoft Scripting Engine|"
                                r"Microsoft Outlook|Microsoft Word|Microsoft Excel|Remote Desktop Client|Windows RDP Client)")
WIN_OS_TAG_RE = re.compile(r"^(Windows|Microsoft Windows|Win32k|Role: |Microsoft Graphics Component$)")  # C5: Windows components only
# KEV (vendorProject, product) -> category, for entries outside MSRC data. Exact strings from the KEV catalog.
KEV_PRODUCT_CATEGORY = {
    ("Linux", "Kernel"): "C3/C5 linux_kernel (network vs LPE unresolved)",
    ("Fortinet", "FortiOS"): "C4 edge", ("Palo Alto Networks", "PAN-OS"): "C4 edge",
    ("Cisco", "Adaptive Security Appliance (ASA) and Firepower Threat Defense (FTD)"): "C4 edge",
    ("Cisco", "IOS and IOS XE Software"): "C4 edge", ("Cisco", "IOS software"): "C4 edge",
    ("Cisco", "IOS XR"): "C4 edge", ("Juniper", "Junos OS"): "C4 edge",
    ("Ivanti", "Pulse Connect Secure"): "C4 edge", ("Ivanti", "Connect Secure"): "C4 edge",
    ("Citrix", "NetScaler"): "C4 edge", ("Citrix", "Application Delivery Controller (ADC) and Gateway"): "C4 edge",
    ("F5", "BIG-IP"): "C4 edge", ("SonicWall", "SonicOS"): "C4 edge",
    ("Google", "Chromium V8"): "C6 client", ("Google", "Chromium"): "C6 client", ("Google", "Chrome"): "C6 client",
    ("Mozilla", "Firefox"): "C6 client", ("Mozilla", "Firefox and Thunderbird"): "C6 client",
    ("Adobe", "Acrobat and Reader"): "C6 client", ("Adobe", "Reader and Acrobat"): "C6 client",
    ("Adobe", "Flash Player"): "C6 client", ("Foxit", "Reader"): "C6 client",
    ("Microsoft", "Internet Explorer"): "C6 client", ("Microsoft", "Office"): "C6 client",
    ("Microsoft", "Edge"): "C6 client", ("Microsoft", "Word"): "C6 client", ("Microsoft", "Excel"): "C6 client",
    ("Microsoft", "Outlook"): "C6 client",
}  # fmt: skip


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def msrc_by_cve() -> tuple[dict, dict]:
    """CVE -> {'tags', 'impacts', 'docs'} over the 2016–2023 CVRF documents; plus {doc: sha256}."""
    out: dict = defaultdict(lambda: {"tags": set(), "impacts": set(), "docs": set()})
    hashes = {}
    for f in sorted((SRC / "msrc").glob("cvrf_20*.json")):
        if not 2016 <= int(f.name[5:9]) <= 2023:
            continue
        hashes[f.name] = sha(f)
        for v in json.loads(f.read_bytes()).get("Vulnerability") or []:
            c = v.get("CVE")
            if not c:
                continue
            out[c]["docs"].add(f.name)
            for n in v.get("Notes", []):
                if n.get("Type") == NOTE_TAG and n.get("Title"):
                    out[c]["tags"].add(n["Title"])
            for t in v.get("Threats", []):
                if t.get("Type") == THREAT_IMPACT and (t.get("Description") or {}).get("Value"):
                    out[c]["impacts"].add(t["Description"]["Value"])
    return out, hashes


def snapshot_family_cves() -> set[str]:
    """CVE IDs in the snapshot with a positive vulnerable match on a FAMILY_PRODUCTS product (any year, any score)."""
    man = json.loads((SNAP / "manifest.json").read_bytes())
    hit = set()

    def walk(node, neg):
        neg ^= bool(node.get("negate"))
        for m in node.get("cpeMatch", []):
            yield m.get("criteria", ""), bool(m.get("vulnerable")) and not neg
        for ch in [*node.get("nodes", []), *node.get("children", [])]:
            yield from walk(ch, neg)

    for p in man["files"]:
        for v in json.loads(gzip.decompress((SNAP / p["path"]).read_bytes()))["response"]["vulnerabilities"]:
            c = v["cve"]
            for cfg in c.get("configurations", []):
                for n in cfg.get("nodes", []):
                    if any(ok and f":{p['product']}:" in crit for crit, ok in walk(n, bool(cfg.get("negate")))):
                        hit.add(c["id"])
    return hit


def kev_category(k: dict, msrc: dict, current: set[str]) -> str:
    cid = k["cveID"]
    if cid in current:
        return "C1 current FAMILY_PRODUCTS"
    if cid in msrc and k["vendorProject"] == "Microsoft":
        tags, imp = msrc[cid]["tags"], msrc[cid]["impacts"]
        if tags & WIN_SERVICE_TAGS:
            return "C2 windows network service"
        if any(WIN_CLIENT_TAGS_RE.match(t) for t in tags):
            return "C6 client"
        if "Elevation of Privilege" in imp and any(WIN_OS_TAG_RE.match(t) for t in tags):
            return "C5 windows LPE"
        return "OUT microsoft (other MSRC tag)"
    if (k["vendorProject"], k["product"]) in KEV_PRODUCT_CATEGORY:
        return KEV_PRODUCT_CATEGORY[k["vendorProject"], k["product"]]
    if k["vendorProject"] == "Microsoft":
        return "UNRESOLVED microsoft (not in 2016–2023 MSRC data)"
    return "OUT"


def md(rows, head):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
                     + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows])


def main() -> None:
    qlog = SRC / "nvd_count_queries.jsonl"
    queries = [json.loads(l) for l in qlog.read_text().splitlines()]
    msrc, msrc_hashes = msrc_by_cve()
    kev_path = SRC / "kev" / "known_exploited_vulnerabilities.json"
    kev_doc = json.loads(kev_path.read_bytes())
    kev = kev_doc["vulnerabilities"]
    included = {r["cve_id"] for r in csv.DictReader((ROOT / "data" / "derived" / "cves.csv").open())}
    current = snapshot_family_cves()

    raw = {"inputs": {"nvd_count_queries.jsonl": sha(qlog), "kev": sha(kev_path), "kev_catalogVersion":
                      kev_doc.get("catalogVersion"), "kev_dateReleased": kev_doc.get("dateReleased"),
                      "msrc_docs": msrc_hashes, "snapshot_manifest": sha(SNAP / "manifest.json")}}
    rep = ["# Product coverage counts for product_list_v1 (proposal only; nothing adopted)", "",
           "Inputs are stored files only (no network in this run); SHA-256s are in raw.json.gz.", ""]

    # 1. NVD count-only queries.
    raw["nvd_queries"] = queries
    rep += ["## 1. NVD CVE API 2.0 count-only queries", "",
            "`totalResults` only; no record was stored. `virtualMatchString` matches a CPE anywhere in a CVE's "
            "applicability statement, vulnerable or not (the API documentation says `isVulnerable` cannot be combined "
            "with it), so these counts include 'running on/with' platform matches. Counts are all-time with "
            "`noRejected` (not limited to 2016–2023: date ranges are capped at 120 days per query). Counts for "
            "different CPEs overlap and must not be added.", "",
            md([(q["label"], q["totalResults"] if q["totalResults"] is not None else f"FAILED (HTTP {q['http']})",
                 q["time_utc"], f"`{q['query'].split('?', 1)[1]}`") for q in queries],
               ["label", "totalResults", "time (UTC)", "query"]), ""]

    # 2. MSRC per-tag counts.
    in_window = {c: v for c, v in msrc.items()}
    tag_imp: dict[str, Counter] = defaultdict(Counter)
    for c, v in in_window.items():
        for t in v["tags"] or {"(no tag)"}:
            for i in v["impacts"] or {"(no impact)"}:
                tag_imp[t][i] += 1
            tag_imp[t]["CVEs"] += 1
    raw["msrc_tag_impact"] = {t: dict(c) for t, c in tag_imp.items()}
    raw["msrc_cves"] = len(in_window)
    impacts = ["Remote Code Execution", "Elevation of Privilege", "Information Disclosure", "Denial of Service",
               "Spoofing", "Security Feature Bypass", "(no impact)"]
    svc = sorted(WIN_SERVICE_TAGS, key=lambda t: -tag_imp[t]["CVEs"])
    rep += ["## 2. MSRC Security Update Guide (CVRF), 2016–2023: CVEs per component tag × impact", "",
            f"{len(in_window)} distinct CVEs across {len(msrc_hashes)} monthly documents (MSRC has no document for "
            "2016-Feb or 2016-Mar; February 2018 is `2018-FEB`, plus `2017-May-B`). A CVE counts once per tag and once "
            "per impact it carries.", "", "### 2a. Proposed C2 service tags", "",
            md([(t, tag_imp[t]["CVEs"], *(tag_imp[t][i] for i in impacts)) for t in svc],
               ["tag", "CVEs", *impacts]), ""]
    c2 = {c for c, v in in_window.items() if v["tags"] & WIN_SERVICE_TAGS}
    c5 = {c for c, v in in_window.items() if "Elevation of Privilege" in v["impacts"] and not v["tags"] & WIN_SERVICE_TAGS
          and not any(WIN_CLIENT_TAGS_RE.match(t) for t in v["tags"]) and any(WIN_OS_TAG_RE.match(t) for t in v["tags"])}
    c6 = {c for c, v in in_window.items() if any(WIN_CLIENT_TAGS_RE.match(t) for t in v["tags"])}
    rce = lambda s: sum("Remote Code Execution" in in_window[c]["impacts"] for c in s)
    raw["msrc_category_counts"] = {"C2": len(c2), "C2_rce": rce(c2), "C5_windows_eop": len(c5), "C6_ms_client": len(c6),
                                   "C6_rce": rce(c6)}
    rep += ["### 2b. MSRC CVEs per proposed category (distinct CVEs)", "",
            md([("C2 Windows network services (tag in 2a)", len(c2), rce(c2)),
                ("C5 Windows LPE (impact EoP, a Windows tag, not C2/C6)", len(c5), "—"),
                ("C6 Microsoft client-side (IE, Edge, Office, Scripting Engine, RDP client)", len(c6), rce(c6))],
               ["category", "CVEs", "of which Remote Code Execution"]), "",
            "Top 40 tags overall (CVEs): " + ", ".join(f"{t} {c['CVEs']}" for t, c in
                                                     sorted(tag_imp.items(), key=lambda x: -x[1]["CVEs"])[:40]), ""]

    # 3. KEV coverage.
    cat = {k["cveID"]: kev_category(k, in_window, current) for k in kev}
    cc = Counter(cat.values())
    in_current = sum(k["cveID"] in current for k in kev)
    in_included = sum(k["cveID"] in included for k in kev)
    proposed = sum(not v.startswith(("OUT", "UNRESOLVED")) for v in cat.values())
    raw["kev"] = {"total": len(kev), "in_current_family_products": in_current, "in_included_1473": in_included,
                  "in_proposed": proposed, "by_category": dict(cc), "per_cve": cat}
    pairs = Counter((k["vendorProject"], k["product"]) for k in kev)
    top = []
    for (v, p), n in pairs.most_common(20):
        ids = [k["cveID"] for k in kev if (k["vendorProject"], k["product"]) == (v, p)]
        n_in = sum(not cat[i].startswith(("OUT", "UNRESOLVED")) for i in ids)
        mark = "in" if n_in == n else "out" if n_in == 0 else f"partial ({n_in} of {n} in)"
        top.append((f"{v} : {p}", n, mark, "; ".join(f"{c} {m}" for c, m in Counter(cat[i] for i in ids).most_common())))
    raw["kev_top20"] = top
    rep += ["## 3. KEV coverage", "",
            f"CISA KEV catalog version {kev_doc.get('catalogVersion')} (released {kev_doc.get('dateReleased')}), "
            f"{len(kev)} entries.", "",
            md([("in current FAMILY_PRODUCTS (snapshot CVE with a positive vulnerable family-product match, any year)",
                 in_current),
                ("in the 1,473 included CVEs", in_included),
                ("in the proposed list (C1–C6, rules in product_list_v1.md §3)", proposed)], ["KEV entries", "n"]), "",
            "### 3a. KEV entries by assigned category", "", md(sorted(cc.items(), key=lambda x: -x[1]), ["category", "n"]),
            "", "### 3b. The 20 KEV vendor:product pairs with the most entries", "",
            md(top, ["KEV vendorProject : product", "entries", "in proposed list?", "categories"]), ""]

    # 4. Test cases.
    tc = {c: {"msrc": {k: sorted(v) for k, v in in_window[c].items()} if c in in_window else None,
              "kev": next((k for k in kev if k["cveID"] == c), None), "nvd": [q for q in queries if c in q["query"]]}
          for c in ("CVE-2017-0144", "CVE-2019-0708")}
    raw["test_cases"] = tc
    rep += ["## 4. Test cases", ""]
    for c, d in tc.items():
        rep += [f"### {c}", "", f"- MSRC tags: {d['msrc']['tags'] if d['msrc'] else 'not in data'}; impacts: "
                f"{d['msrc']['impacts'] if d['msrc'] else '-'}; document(s): {d['msrc']['docs'] if d['msrc'] else '-'}",
                f"- KEV: {('yes, added ' + d['kev']['dateAdded'] + ', ' + d['kev']['vendorProject'] + ' : ' + d['kev']['product']) if d['kev'] else 'no'}",
                f"- In the 2026-10-21 snapshot (current FAMILY_PRODUCTS): {'yes' if c in current else 'no'}", "",
                md([(q["label"], q["totalResults"]) for q in d["nvd"]], ["NVD count query", "totalResults"]), ""]

    out = runlog.write_run("product_coverage", raw, "\n".join(rep) + "\n", [], {"inputs": raw["inputs"]},
                           root=ROOT / "results" / "cve_semantics")
    print(out)


if __name__ == "__main__":
    main()
