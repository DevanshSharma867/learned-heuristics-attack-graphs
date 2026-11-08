"""KEV coverage of the scope options in docs/proposals/scope_v1.md (proposal only; nothing adopted).

Usage: python scripts/measure_scope_kev.py

Reads only stored inputs: the KEV snapshot, the MSRC CVRF documents 2016–2023 and the 2026-10-21 NVD snapshot,
through the functions of scripts/measure_product_coverage.py. Writes
results/cve_semantics/scope_kev/<stamp>-<commit>/ through ahg.runlog.

Each KEV entry gets exactly one category (first rule that matches, in CATEGORY_ORDER below). An option's KEV
coverage is the number of entries whose category is in the option's category set. All name rules are explicit
regexes over KEV's own vendorProject / product strings (KEV has no CPEs, docs/sources.md S10), so they are a name
match and are listed in the report for checking.
"""

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ahg import runlog  # noqa: E402

_spec = importlib.util.spec_from_file_location("pc", ROOT / "scripts" / "measure_product_coverage.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

# Categories. C1–C6 as in docs/proposals/product_list_v1.md §2, except that SharePoint goes to WEBAPP (product_list_v1's
# C6 tag rule `^Microsoft Office` also matched "Microsoft Office SharePoint", a server product; counted below).
CATS = {
    "C1": "current FAMILY_PRODUCTS (snapshot match)",
    "C2": "Windows network services (MSRC tag)",
    "C3/C5-linux": "Linux kernel (network vs LPE unresolved)",
    "C4": "edge devices (VPN, firewall, gateway, router OS)",
    "C5-win": "Windows local privilege escalation (MSRC)",
    "C6": "client-side (browser, office, mail client, PDF, archive)",
    "WEBAPP": "enterprise web / server applications not in FAMILY_PRODUCTS",
    "SOHO": "small-office routers and NAS",
    "MOBILE": "mobile OS / chipsets",
    "CLOUD": "cloud / Azure",
    "MS-OTHER": "Microsoft, other component",
    "OTHER": "none of the above",
}
WEBAPP_SHAREPOINT_TAG = re.compile(r"SharePoint")
NAME_RULES = [  # (category, regex over "vendorProject : product"), first match wins
    ("MOBILE", r"^(Android|Samsung|Qualcomm|Arm|MediaTek) :|^Google : (Pixel|Android)|^Apple : (iOS|iPadOS|watchOS)"),
    ("CLOUD", r"Azure|Kubernetes|\bAWS\b|Cloud (Services|Platform)"),
    ("C4", r"^(Fortinet|Palo Alto Networks|SonicWall|WatchGuard|Sophos|Check Point|Juniper|F5|Zyxel|Arista) :"
           r"|^Cisco : .*(ASA|Adaptive Security|Firepower|IOS|Small Business RV|AnyConnect|Secure Firewall|SD-WAN)"
           r"|^Ivanti : .*(Connect Secure|Pulse|Policy Secure)|^Pulse Secure :|^Citrix : .*(NetScaler|ADC|Gateway)"),
    ("SOHO", r"^(D-Link|NETGEAR|TP-Link|DrayTek|MikroTik|Ubiquiti|ASUS|Synology|QNAP|Tenda|Linksys|TOTOLINK|Buffalo) :"),
    ("C6", r"^Google : (Chromium|Chrome)|^Mozilla :|^Adobe : .*(Acrobat|Reader|Flash)|^RARLAB :|^7-Zip :|^Foxit :"
           r"|^Microsoft : (Office|Word|Excel|Outlook|Internet Explorer|Edge|PowerPoint|Publisher)"
           r"|^Apple : (Safari|WebKit)"),
    ("WEBAPP", r"^(Oracle|Atlassian|Synacor|SAP|Zoho|SolarWinds|GitLab|Jenkins|JetBrains|Roundcube|WordPress|Drupal|"
               r"Sitecore|Kentico|Craft CMS|Laravel|PHP Group|Accellion|Fortra|Gladinet|PaperCut|Progress|VMware|"
               r"Telerik|ConnectWise|BeyondTrust|N-able|SimpleHelp ?|Veeam|Nagios|Langflow|BerriAI|JFrog|Kaseya|IBM|"
               r"Mitel|Plex|Apache|Adobe|Citrix|Ivanti|Trend Micro|Broadcom|Red Hat|Smartertools|SmarterTools) :"
               r"|^Microsoft : SharePoint"),
    ("C5-win", r"^Microsoft : (Win32k|Windows)$"),
]
CATEGORY_ORDER = list(CATS)

# Options (scope_v1.md): the categories each pulls into the CVE pool.
OPTIONS = {
    "N1 Windows/AD enterprise with DMZ": {"C1", "C2", "C4", "C5-win", "C6", "WEBAPP"},
    "N2 mixed Linux/Windows enterprise": {"C1", "C2", "C3/C5-linux", "C4", "C5-win", "C6", "WEBAPP"},
    "N3 small office": {"C2", "C5-win", "C6", "SOHO"},
    "A1 external opportunistic": {"C1", "C4", "WEBAPP", "SOHO"},
    "A2 external targeted": {"C1", "C2", "C3/C5-linux", "C4", "C5-win", "C6", "WEBAPP"},
    "A3 phished / malicious insider": {"C1", "C2", "C3/C5-linux", "C5-win", "C6"},
    "E1 T1190 + T1133 (internet-facing)": {"C1", "C4", "WEBAPP", "SOHO"},
    "E2 E1 + T1566 + T1189 (phishing, drive-by)": {"C1", "C4", "WEBAPP", "SOHO", "C6"},
    "E3 E2 + T1078 (valid accounts)": {"C1", "C4", "WEBAPP", "SOHO", "C6"},
    "E4 assume breach (no Initial Access)": {"C1", "C2", "C3/C5-linux", "C5-win"},
    "S1 servers only": {"C1", "C2", "C3/C5-linux"},
    "S2 servers + workstations": {"C1", "C2", "C3/C5-linux", "C5-win", "C6"},
    "S3 S2 + edge devices + enterprise web apps": {"C1", "C2", "C3/C5-linux", "C5-win", "C6", "C4", "WEBAPP"},
    "S4 S3 + mobile + cloud": {"C1", "C2", "C3/C5-linux", "C5-win", "C6", "C4", "WEBAPP", "MOBILE", "CLOUD"},
}
PACKAGES = {
    "P1 AD enterprise, targeted external": ["N1 Windows/AD enterprise with DMZ", "A2 external targeted",
                                            "E3 E2 + T1078 (valid accounts)", "S3 S2 + edge devices + enterprise web apps"],
    "P2 internet-facing perimeter, opportunistic": ["N2 mixed Linux/Windows enterprise", "A1 external opportunistic",
                                                    "E1 T1190 + T1133 (internet-facing)",
                                                    "S3 S2 + edge devices + enterprise web apps"],
    "P3 assume breach, insider": ["N2 mixed Linux/Windows enterprise", "A3 phished / malicious insider",
                                  "E4 assume breach (no Initial Access)", "S2 servers + workstations"],
}


def categorise(k: dict, msrc: dict, current: set[str]) -> tuple[str, str]:
    """(category, rule that fired) for one KEV entry."""
    cid, name = k["cveID"], f"{k['vendorProject']} : {k['product']}"
    if cid in current:
        return "C1", "snapshot FAMILY_PRODUCTS match"
    if k["vendorProject"] == "Microsoft" and cid in msrc:
        tags, imp = msrc[cid]["tags"], msrc[cid]["impacts"]
        if any(WEBAPP_SHAREPOINT_TAG.search(t) for t in tags):
            return "WEBAPP", "MSRC tag SharePoint"
        if any(t.startswith("Azure") for t in tags):
            return "CLOUD", "MSRC tag Azure*"
        base = pc.kev_category(k, msrc, current)
        return {"C2 windows network service": "C2", "C6 client": "C6", "C5 windows LPE": "C5-win"}.get(
            base, "MS-OTHER"), "MSRC tag rule (product_list_v1)"
    for cat, rx in NAME_RULES:
        if re.search(rx, name):
            return cat, f"name rule {cat}"
    if name == "Linux : Kernel":
        return "C3/C5-linux", "name Linux : Kernel"
    if k["vendorProject"] == "Microsoft":
        return "MS-OTHER", "Microsoft, no MSRC 2016–2023 data, no name rule"
    return "OTHER", "no rule"


def main() -> None:
    msrc, msrc_hashes = pc.msrc_by_cve()
    kev_path = pc.SRC / "kev" / "known_exploited_vulnerabilities.json"
    kev_doc = json.loads(kev_path.read_bytes())
    kev = kev_doc["vulnerabilities"]
    current = pc.snapshot_family_cves()
    cat = {k["cveID"]: categorise(k, msrc, current) for k in kev}
    y = lambda c: 2016 <= int(c.split("-")[1]) <= 2023
    cc = Counter(c for c, _ in cat.values())
    cc_y = Counter(cat[k["cveID"]][0] for k in kev if y(k["cveID"]))
    n_y = sum(y(k["cveID"]) for k in kev)
    sharepoint_in_old_c6 = sum(1 for k in kev if k["vendorProject"] == "Microsoft" and k["cveID"] in msrc
                               and any("SharePoint" in t for t in msrc[k["cveID"]]["tags"])
                               and pc.kev_category(k, msrc, current) == "C6 client")
    cover = lambda cats, only_y=False: sum(1 for k in kev if cat[k["cveID"]][0] in cats and (y(k["cveID"]) or not only_y))
    opt = {o: {"categories": sorted(c), "kev": cover(c), "kev_2016_2023": cover(c, True)} for o, c in OPTIONS.items()}
    pkg = {}
    for p, (n, a, e, s_) in PACKAGES.items():
        # Network and assets decide the CVE pool; attacker and entry points only restrict which pool categories
        # can be the attacker's first step (initial access). Later steps may use any pool category.
        pool = OPTIONS[n] & OPTIONS[s_]
        first = pool & OPTIONS[a] & OPTIONS[e]
        pkg[p] = {"options": [n, a, e, s_], "pool": sorted(pool), "kev_pool": cover(pool),
                  "kev_pool_2016_2023": cover(pool, True), "initial_access": sorted(first), "kev_initial": cover(first),
                  "kev_initial_2016_2023": cover(first, True)}
    other_top = Counter(f"{k['vendorProject']} : {k['product']}" for k in kev if cat[k["cveID"]][0] == "OTHER").most_common(25)
    raw = {"inputs": {"kev_sha256": pc.sha(kev_path), "kev_catalogVersion": kev_doc.get("catalogVersion"),
                      "msrc_docs": msrc_hashes, "snapshot_manifest_sha256": pc.sha(pc.SNAP / "manifest.json")},
           "kev_total": len(kev), "kev_cve_year_2016_2023": n_y, "by_category": dict(cc),
           "by_category_2016_2023": dict(cc_y), "options": opt, "packages": pkg, "other_top25": other_top,
           "sharepoint_in_product_list_v1_C6": sharepoint_in_old_c6,
           "per_cve": {c: list(v) for c, v in cat.items()}, "name_rules": NAME_RULES}
    md = pc.md
    rep = ["# KEV coverage of the scope options (proposal only; nothing adopted)", "",
           f"KEV catalogVersion {kev_doc.get('catalogVersion')}: {len(kev)} entries; {n_y} have a CVE ID year 2016–2023 "
           "(the ID year, not the publication date). One category per entry, first rule wins.", "",
           "## 1. KEV entries per category", "",
           md([(c, CATS[c], cc[c], cc_y[c]) for c in CATEGORY_ORDER], ["category", "meaning", "KEV", "KEV, CVE year 2016–2023"]),
           "", f"Correction to product_list_v1: its C6 rule (`^Microsoft Office` tag prefix) also matched SharePoint, "
           f"a server product. **{sharepoint_in_old_c6} KEV entries** were counted as C6 there; here they are WEBAPP.", "",
           "## 2. Name rules (regex over \"vendorProject : product\", first match wins)", "",
           md([(c, f"`{r}`") for c, r in NAME_RULES], ["category", "regex"]), "",
           "## 3. Options", "", md([(o, ", ".join(v["categories"]), v["kev"], v["kev_2016_2023"]) for o, v in opt.items()],
                                   ["option", "categories pulled in", "KEV", "KEV 2016–2023"]), "",
           "## 4. Packages", "", "Pool = network option ∩ asset option. Initial access = pool ∩ attacker option ∩ entry-point "
           "option (the categories a first step may use). KEV counted per set.", "",
           md([(p, " / ".join(v["options"]), ", ".join(v["pool"]), f"{v['kev_pool']} ({v['kev_pool_2016_2023']})",
                ", ".join(v["initial_access"]), f"{v['kev_initial']} ({v['kev_initial_2016_2023']})") for p, v in pkg.items()],
              ["package", "options", "pool categories", "KEV in pool (2016–2023)", "initial-access categories",
               "KEV initial (2016–2023)"]), "",
           "## 5. Largest uncovered (OTHER) vendor : product pairs", "", md(other_top, ["vendorProject : product", "KEV"]), ""]
    out = runlog.write_run("scope_kev", raw, "\n".join(rep) + "\n", [], {"inputs": raw["inputs"]},
                           root=ROOT / "results" / "cve_semantics")
    print(out)


if __name__ == "__main__":
    main()
