"""KEV and MSRC counts for the categories of docs/proposals/product_list_v2.md (D27 scope; proposal only).

Usage: python scripts/measure_scope2_kev.py

Reads only stored inputs: the KEV snapshot (catalogVersion 2026.11.06), the MSRC CVRF documents 2016–2023, the
2026-10-21 NVD snapshot (for the old FAMILY_PRODUCTS match) and the ATT&CK STIX bundle (v20.1, for the procedure
examples quoted in the proposal). Writes results/cve_semantics/scope2_kev/<stamp>-<commit>/ through ahg.runlog.

Each KEV entry gets exactly one category: the first rule in RULE ORDER below that matches. The categories are the
ones product_list_v2 derives from ATT&CK steps; "conditional" categories are counted but not part of the "in" total,
because whether a step needs them depends on host roles the author has not decided. KEV has no CPEs
(docs/sources.md S10), so the non-MSRC rules are regexes over KEV's own "vendorProject : product" strings.
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

ATTACK = pc.SRC / "scope2" / "enterprise-attack.json"

CATS = {  # code: (meaning, status)
    "W-SVC": ("Windows network and domain services (SMB, RDP, RPC, Print Spooler, DNS, LDAP, Kerberos, Netlogon, "
              "NTLM, LSA, AD, AD CS, DCOM)", "in"),
    "W-LPE": ("Windows local privilege escalation (MSRC EoP on a Windows component)", "in"),
    "L-KERNEL": ("Linux kernel (LPE if AV:L; network if AV:N/A)", "in"),
    "L-LPE": ("Linux userland privilege boundaries (sudo, polkit, glibc loader, libuser, ABRT)", "in"),
    "L-SVC": ("Linux remote-access and file-sharing services (SSH, Samba, xrdp, VNC)", "in"),
    "CLIENT": ("client software opened by a user (office, mail, browser, PDF, archive)", "in"),
    "SRC-APP": ("internal server applications named in ATT&CK lateral-movement / PE / credential-access examples "
                "(JBoss, Jenkins, Jira, Confluence, GitLab, vCenter, Configuration Manager)", "conditional"),
    "MS-APP": ("Microsoft server applications (Exchange, SQL Server, SharePoint)", "conditional"),
    "OLD-APP": ("old FAMILY_PRODUCTS server roles other than SSH/SMB/RDP (dns, ftp, http, mail, sql)", "conditional"),
    "VIRT": ("hypervisors and containers (Hyper-V, ESXi, Docker/runc)", "conditional"),
    "MS-OTHER": ("Microsoft, no rule above", "out"),
    "OUT": ("outside the D27 scope or no rule", "out"),
}

W_SVC_TAGS = set(pc.WIN_SERVICE_TAGS) | {
    # T1210 procedure examples: MS10-061 (print spooler), MS08-067 (Server service, "crafted RPC request").
    "Windows Print Spooler Components", "Windows Server Service", "Microsoft RPC", "Windows Remote Procedure Call",
    "Windows Remote Procedure Call Runtime", "Windows RPC API",
    # T1212 / T1558 / T1003 / T1649 / T1557.001: authentication and credential services.
    "Windows NTLM", "Windows Local Security Authority (LSA)", "Windows Local Security Authority",
    "Local Security Authority Subsystem Service", "Windows Local Security Authority Subsystem Service (LSASS)",
    "Microsoft Local Security Authority Server (lsasrv)", "SAM and LSAD Remote Protocols",
    "Windows Active Directory Certificate Services", "Role: Active Directory Certificate Services; Active Directory Domain Services",
    # T1021.003 Distributed Component Object Model.
    "Windows DCOM Server",
}  # fmt: skip
MS_APP_TAG = re.compile(r"^(Microsoft Exchange Server|SQL Server|Microsoft Office SharePoint)$")
VIRT_TAG = re.compile(r"Hyper-V|^Windows Container")
CLIENT_TAG = pc.WIN_CLIENT_TAGS_RE  # product_list_v1 C6 rule, SharePoint excluded

NAME_RULES = [  # (category, regex over "vendorProject : product"), first match wins
    ("W-SVC", r"^Microsoft : (Active Directory$|Netlogon|Kerberos|Win32k Print|.*Print Spooler|SMB|Remote Desktop|"
              r"Server Message Block)"),
    ("MS-APP", r"^Microsoft : (Exchange|SQL Server|SharePoint|\.NET Framework, SharePoint)"),
    ("SRC-APP", r"^Red Hat : JBoss|^Jenkins :|^Atlassian : (Jira|Confluence)|^GitLab :|^(VMware|Broadcom) : .*vCenter"
                r"|^Microsoft : Configuration Manager"),
    ("VIRT", r"^(VMware|Broadcom) : .*(ESX|Workstation|Tools)|^Microsoft : Hyper-V|^Docker :|runc|containerd"),
    ("CLIENT", r"^Google : (Chromium|Chrome)|^Mozilla :|^Adobe : .*(Acrobat|Reader|Flash)|^RARLAB :|^7-Zip :|^Foxit :"
               r"|^Microsoft : (Office|Word|Excel|Outlook|Internet Explorer|Edge|PowerPoint|Publisher)"),
    ("W-LPE", r"^Microsoft : (Win32k|Windows)$"),
    ("L-KERNEL", r"^Linux : Kernel$"),
    ("L-LPE", r"^Sudo : Sudo$|^Red Hat : (Polkit|Libuser|Automatic Bug Reporting Tool)$|^GNU : GNU C Library$"),
    ("L-SVC", r"^Samba :|OpenSSH|libssh|[Dd]ropbear|xrdp|VNC"),
    ("OLD-APP", r"^ISC : BIND|PowerDNS|dnsmasq|Unbound|ProFTPD|vsftpd|Serv-U|CrushFTP|Wing FTP|Cerberus|FileZilla|"
                r"Pure-FTPd|Xlight|^Apache : (HTTP Server|Tomcat)$|nginx|Internet Information Services|^Exim :|Postfix|"
                r"Dovecot|Sendmail|MySQL|MariaDB|PostgreSQL"),
]


def categorise(k: dict, msrc: dict) -> tuple[str, str]:
    """(category, rule that fired) for one KEV entry."""
    cid, name = k["cveID"], f"{k['vendorProject']} : {k['product']}"
    if k["vendorProject"] == "Microsoft" and cid in msrc:
        tags, imp = msrc[cid]["tags"], msrc[cid]["impacts"]
        if tags & W_SVC_TAGS:
            return "W-SVC", "MSRC tag in W_SVC_TAGS"
        if any(MS_APP_TAG.match(t) for t in tags):
            return "MS-APP", "MSRC tag Exchange/SQL Server/SharePoint"
        if any(VIRT_TAG.search(t) for t in tags):
            return "VIRT", "MSRC tag Hyper-V / Windows Container"
        if any(CLIENT_TAG.match(t) for t in tags):
            return "CLIENT", "MSRC client tag (product_list_v1 C6, SharePoint excluded)"
        if "Elevation of Privilege" in imp and any(pc.WIN_OS_TAG_RE.match(t) for t in tags):
            return "W-LPE", "MSRC impact EoP and a Windows component tag"
        return "MS-OTHER", "MSRC data, no rule"
    for cat, rx in NAME_RULES:
        if re.search(rx, name):
            return cat, f"name rule {cat}"
    if k["vendorProject"] == "Microsoft" and re.search(r"Privilege Escalation|Elevation of Privilege",
                                                         k.get("vulnerabilityName", "")):
        # Outside the 2016–2023 MSRC data there is no Impact field; KEV's own vulnerabilityName is used instead.
        return "W-LPE", "Microsoft, no MSRC data, KEV vulnerabilityName says privilege escalation"
    if k["vendorProject"] == "Microsoft":
        return "MS-OTHER", "Microsoft, no MSRC 2016–2023 data, no name rule"
    return "OUT", "no rule"


def msrc_counts(msrc: dict) -> dict:
    """MSRC 2016–2023 CVEs per Microsoft category (same tag rules as categorise, applied to every MSRC CVE)."""
    out: dict[str, Counter] = {c: Counter() for c in ("W-SVC", "MS-APP", "VIRT", "CLIENT", "W-LPE")}
    for v in msrc.values():
        k = {"cveID": "x", "vendorProject": "Microsoft", "product": ""}
        cat, _ = categorise(k, {"x": v})
        if cat in out:
            out[cat]["CVEs"] += 1
            for i in v["impacts"] or {"(no impact)"}:
                out[cat][i] += 1
    return {c: dict(v) for c, v in out.items()}


def attack_examples(ids: list[str]) -> dict:
    """Procedure-example texts ("uses" relationships) for the given ATT&CK technique IDs, from the stored bundle."""
    objs = json.loads(ATTACK.read_bytes())["objects"]
    byid = {o["id"]: o for o in objs}
    tid = {}
    for o in objs:
        if o["type"] == "attack-pattern" and not o.get("revoked"):
            for r in o.get("external_references", []):
                if r.get("source_name") == "mitre-attack":
                    tid[r["external_id"]] = o["id"]
    out = {}
    for t in ids:
        rels = [o for o in objs if o["type"] == "relationship" and o["relationship_type"] == "uses"
                and o["target_ref"] == tid[t] and not o.get("revoked")]
        out[t] = sorted((byid[r["source_ref"]]["name"], re.sub(r"\(Citation:[^)]*\)", "", r.get("description", "")).strip())
                        for r in rels)
    return out


def main() -> None:
    msrc, msrc_hashes = pc.msrc_by_cve()
    kev_path = pc.SRC / "kev" / "known_exploited_vulnerabilities.json"
    kev_doc = json.loads(kev_path.read_bytes())
    kev = kev_doc["vulnerabilities"]
    current = pc.snapshot_family_cves()
    cat = {k["cveID"]: categorise(k, msrc) for k in kev}
    y = lambda c: 2016 <= int(c.split("-")[1]) <= 2023
    cc = Counter(c for c, _ in cat.values())
    cc_y = Counter(cat[k["cveID"]][0] for k in kev if y(k["cveID"]))
    n_y = sum(y(k["cveID"]) for k in kev)
    by_name = {c: Counter(f"{k['vendorProject']} : {k['product']}" for k in kev if cat[k["cveID"]][0] == c).most_common(12)
               for c in CATS}
    in_cats = [c for c, (_, s) in CATS.items() if s == "in"]
    cond_cats = [c for c, (_, s) in CATS.items() if s == "conditional"]
    tot = lambda cs, only_y=False: sum(1 for k in kev if cat[k["cveID"]][0] in cs and (y(k["cveID"]) or not only_y))
    old_c1 = Counter(cat[c][0] for c in cat if c in current)
    ex = attack_examples(["T1210", "T1212", "T1068", "T1072", "T1611", "T1534", "T1080"])
    mc = msrc_counts(msrc)
    raw = {"inputs": {"kev_sha256": pc.sha(kev_path), "kev_catalogVersion": kev_doc.get("catalogVersion"),
                      "msrc_docs": msrc_hashes, "snapshot_manifest_sha256": pc.sha(pc.SNAP / "manifest.json"),
                      "attack_bundle_sha256": pc.sha(ATTACK)},
           "kev_total": len(kev), "kev_cve_year_2016_2023": n_y, "by_category": dict(cc),
           "by_category_2016_2023": dict(cc_y), "in_total": tot(in_cats), "in_total_2016_2023": tot(in_cats, True),
           "conditional_total": tot(cond_cats), "conditional_total_2016_2023": tot(cond_cats, True),
           "old_family_products_kev_by_v2_category": dict(old_c1), "msrc_2016_2023_by_category": mc,
           "top_names": by_name, "attack_examples": ex, "w_svc_tags": sorted(W_SVC_TAGS), "name_rules": NAME_RULES,
           "per_cve": {c: list(v) for c, v in cat.items()}}
    md = pc.md
    imps = ["Remote Code Execution", "Elevation of Privilege", "Information Disclosure", "Security Feature Bypass",
            "Spoofing", "Denial of Service"]
    rep = ["# KEV and MSRC counts for product_list_v2 (D27 scope; proposal only)", "",
           f"KEV catalogVersion {kev_doc.get('catalogVersion')}: {len(kev)} entries; {n_y} have a CVE ID year 2016–2023. "
           "One category per entry, first rule wins (MSRC tag rules for Microsoft CVEs in the 2016–2023 MSRC data, "
           "then the name rules of §3).", "",
           "## 1. KEV entries per category", "",
           md([(c, m, s, cc[c], cc_y[c]) for c, (m, s) in CATS.items()],
              ["category", "meaning", "status", "KEV", "KEV, CVE year 2016–2023"]), "",
           f"- **In** (status in): {tot(in_cats)} ({tot(in_cats, True)}).",
           f"- **Conditional** (host roles undecided): {tot(cond_cats)} ({tot(cond_cats, True)}).",
           f"- KEV entries matching an old FAMILY_PRODUCTS product in the snapshot: {sum(old_c1.values())}; by v2 "
           f"category: {dict(old_c1)}.", "",
           "## 2. MSRC 2016–2023 CVEs per Microsoft category (same tag rules), by impact", "",
           md([(c, v.get("CVEs", 0), *(v.get(i, 0) for i in imps)) for c, v in mc.items()], ["category", "CVEs", *imps]), "",
           "## 3. Rules", "", "W_SVC_TAGS (MSRC Note Type 7):", "", ", ".join(f"`{t}`" for t in sorted(W_SVC_TAGS)), "",
           md([(c, f"`{r}`") for c, r in NAME_RULES], ["category", "name regex over \"vendorProject : product\""]), "",
           "## 4. Largest vendor : product pairs per category", ""]
    for c in CATS:
        rep += [f"- **{c}:** " + "; ".join(f"{n} {v}" for n, v in by_name[c]) if by_name[c] else f"- **{c}:** none"]
    rep += ["", "## 5. ATT&CK procedure examples (stored bundle v20.1)", ""]
    for t, rows in ex.items():
        rep += [f"### {t} ({len(rows)})", ""] + [f"- {n}: {d[:300]}" for n, d in rows] + [""]
    out = runlog.write_run("scope2_kev", raw, "\n".join(rep) + "\n", [], {"inputs": raw["inputs"]},
                           root=ROOT / "results" / "cve_semantics")
    print(out)


if __name__ == "__main__":
    main()
