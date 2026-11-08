"""Measure what the CVEs in the pinned NVD snapshot actually say (D26 follow-up; analysis only).

Usage: python scripts/measure_cve_semantics.py [--snapshot 2026-10-21] [--cwe data/raw/cwe/2026-11-08/cwec_v5.0.xml]

Pure analysis. Nothing here is a rule, filter or adopted criterion:
- It reads data/raw/nvd/<snapshot>/, data/derived/cves.csv and the CWE catalogue.
- It writes one run folder, results/cve_semantics/<stamp>-<commit>/, through ahg.runlog.
- It does not import the derivation path (ahg.cve, scripts/derive_cves.py). The D11 score pick
  (NVD Primary v3.1, else v3.0) is re-implemented here and cross-checked against cves.csv.
- It changes no file in data/derived/ or src/ahg/.

The snapshot was queried per product in FAMILY_PRODUCTS (one virtualMatchString query per CPE
product), so "all records in the snapshot" is the union of those queries, not a sample of NVD.

Two populations:
- (a) the 1,473 included CVEs, grouped by their cves.csv family and products;
- (b) every record in the snapshot, grouped by every family and product whose query returned it,
  whether or not NVD marks that product vulnerable.

Definitions used below come from docs/sources.md (S1 CVSS v3.1, S4 NVD schema, S5 CPE 2.3,
S6/S7 CWE, P1–P35 product roles).
"""

import argparse
import gzip
import hashlib
import json
import random
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ahg import runlog  # noqa: E402  (provenance and the append-only run folder only)

NVD = "nvd@nist.gov"
SEED = 20261108  # for the 20-ID samples per disagreement cell
SAMPLE = 20
CODE_EXEC_IMPACT = "Execute Unauthorized Code or Commands"  # CWE TechnicalImpactEnumeration (S7)

# CVSS v3.x base metrics and their legal values (S1 §2).
V3_METRICS = {"AV": "NALP", "AC": "LH", "PR": "NLH", "UI": "NR", "S": "UC", "C": "HLN", "I": "HLN", "A": "HLN"}

# Product roles, exactly as docs/sources.md §2 (rows P1–P35) records them.
ROLES = {
    "isc:bind": "server", "nlnetlabs:unbound": "server", "powerdns:authoritative": "server",
    "powerdns:recursor": "server", "thekelleys:dnsmasq": "server",
    "beasts:vsftpd": "server", "cerberusftp:ftp_server": "server", "crushftp:crushftp": "server",
    "filezilla-project:filezilla_server": "UNAVAILABLE", "proftpd:proftpd": "server", "pureftpd:pure-ftpd": "server",
    "solarwinds:serv-u": "server", "wftpserver:wing_ftp_server": "server", "xlightftpd:xlight_ftp_server": "server",
    "apache:http_server": "server", "apache:tomcat": "unstated", "f5:nginx": "server",
    "microsoft:internet_information_services": "server", "nginx:nginx": "server",
    "dovecot:dovecot": "server", "exim:exim": "server", "microsoft:exchange_server": "unstated",
    "postfix:postfix": "server", "sendmail:sendmail": "server",
    "freerdp:freerdp": "multi", "neutrinolabs:xrdp": "server",
    "samba:samba": "server",
    "mariadb:mariadb": "unstated", "microsoft:sql_server": "server", "mysql:mysql": "multi",
    "oracle:mysql": "multi", "postgresql:postgresql": "unstated",
    "dropbear_ssh_project:dropbear_ssh": "multi", "libssh:libssh": "multi", "openbsd:openssh": "multi",
}  # fmt: skip

# R-TEXT, diagnostic only: the English description mentions code or command execution.
TEXT_RE = re.compile(
    r"\bexecut(?:e|es|ed|ing|ion)\s+(?:of\s+)?(?:(?:arbitrary|remote|malicious|unauthori[sz]ed|os|shell|system)\s+)*"
    r"(?:code|commands?)\b|\b(?:code|command)\s+execution\b|\bcommand\s+injection\b|\brun\s+arbitrary\s+(?:code|commands?)\b",
    re.I)
# Component naming for multi-role products (item 6): what a description or CPE string mentions.
CLIENT_RE = re.compile(r"\bclients?\b|\bdbclient\b|\bxfreerdp\b|\bwfreerdp\b|\bscp\b", re.I)
SERVER_RE = re.compile(r"\bservers?\b|\bsshd\b|\bmysqld\b|\bshadow\b|\bproxy\b", re.I)


# ---------------------------------------------------------------- parsing helpers (tested)

def parse_v3_vector(vector: str) -> dict[str, str]:
    """'CVSS:3.1/AV:N/...' -> {'AV': 'N', ...}, the eight base metrics, each exactly once and legal (S1)."""
    parts = vector.split("/")
    if not re.fullmatch(r"CVSS:3\.[01]", parts[0]):
        raise ValueError(f"not a CVSS v3.x vector: {vector!r}")
    out: dict[str, str] = {}
    for p in parts[1:]:
        k, _, v = p.partition(":")
        if k in out:
            raise ValueError(f"metric {k} repeated in {vector!r}")
        out[k] = v
    base = {k: out.get(k) for k in V3_METRICS}
    for k, legal in V3_METRICS.items():
        if base[k] is None or len(base[k]) != 1 or base[k] not in legal:
            raise ValueError(f"bad or missing {k} in {vector!r}")
    return base


def cwe_ids(weaknesses: list[dict], source: str | None = None, wtype: str | None = None) -> list[str]:
    """CWE values in NVD 'weaknesses' (S4), optionally filtered by source and type; order kept, deduplicated."""
    seen: dict[str, None] = {}
    for w in weaknesses:
        if source is not None and (w.get("source") == NVD) != (source == NVD):
            continue
        if wtype is not None and w.get("type") != wtype:
            continue
        for d in w.get("description", []):
            if d.get("lang") == "en":
                seen.setdefault(d["value"], None)
    return list(seen)


def load_cwe_impacts(xml_path: Path) -> tuple[dict[str, set[str]], set[str]]:
    """({'CWE-79': {impacts}} for every Weakness, {ids of every Category/Grouping and View}) from the CWE XML (S6, S7)."""
    impacts: dict[str, set[str]] = {}
    other: set[str] = set()
    for _, el in ET.iterparse(xml_path, events=("end",)):
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "Weakness":
            imp = {i.text for i in el.iter() if i.tag.rsplit("}", 1)[-1] == "Impact" and i.text}
            impacts[f"CWE-{el.get('ID')}"] = imp
            el.clear()
        elif tag in ("Category", "Grouping", "View"):  # CWE 5.0 (schema 8.0) calls categories Groupings
            other.add(f"CWE-{el.get('ID')}")
            el.clear()
    return impacts, other


def r_cwe(ids: list[str], impacts: dict[str, set[str]]) -> bool | None:
    """True if a Weakness among ids lists the code-execution impact; False if some id is a Weakness but none does;
    None if no id is a Weakness (only NVD-CWE-*, categories, views or unknown ids)."""
    known = [i for i in ids if i in impacts]
    if not known:
        return None
    return any(CODE_EXEC_IMPACT in impacts[i] for i in known)


# ---------------------------------------------------------------- per-CVE features

def _metric(cve: dict, keys: tuple[str, ...], primary_nvd: bool) -> tuple[str, dict] | None:
    for key in keys:
        for m in cve.get("metrics", {}).get(key, []):
            if primary_nvd == (m.get("source") == NVD and m.get("type") == "Primary"):
                return key, m
    return None


def _walk(node: dict, negated: bool):
    """(criteria, vulnerable, positive) for every cpeMatch at any depth (nested 'nodes'/'children' too)."""
    negated ^= bool(node.get("negate"))
    for m in node.get("cpeMatch", []):
        yield m.get("criteria", ""), bool(m.get("vulnerable")), not negated
    for child in [*node.get("nodes", []), *node.get("children", [])]:
        yield from _walk(child, negated)


def features(cve: dict, family_products: dict[str, list[str]], impacts: dict) -> dict:
    m = cve.get("metrics", {})
    nvd31 = _metric(cve, ("cvssMetricV31",), True)
    nvd30 = _metric(cve, ("cvssMetricV30",), True)
    d11 = nvd31 or nvd30  # D11: NVD Primary v3.1, else v3.0
    cna = _metric(cve, ("cvssMetricV31", "cvssMetricV30"), False)
    vec = parse_v3_vector(d11[1]["cvssData"]["vectorString"]) if d11 else None
    cvec = parse_v3_vector(cna[1]["cvssData"]["vectorString"]) if cna else None
    w = cve.get("weaknesses", [])
    ids = cwe_ids(w)
    desc = next((d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"), "")
    matches = [x for cfg in cve.get("configurations", []) for n in cfg.get("nodes", [])
               for x in _walk(n, bool(cfg.get("negate")))]
    and_with_platform = any(
        (cfg.get("operator") == "AND" or any(n.get("operator") == "AND" for n in cfg.get("nodes", [])))
        and any(not v for n in cfg.get("nodes", []) for _, v, _ in _walk(n, False))
        for cfg in cve.get("configurations", []))
    pos_vuln = [c for c, v, pos in matches if v and pos]
    vuln_products = {fam: sorted({p for p in prods if any(f":{p}:" in c for c in pos_vuln)})
                     for fam, prods in family_products.items()}
    return {
        "scores": {"nvd_primary_v31": bool(nvd31), "nvd_primary_v30": bool(nvd30), "cna_v3": bool(cna),
                   "v2": bool(m.get("cvssMetricV2")), "v4": bool(m.get("cvssMetricV40"))},
        "d11_version": (d11[0][-2] + "." + d11[0][-1]) if d11 else None,
        "d11_exploitability": float(d11[1]["exploitabilityScore"]) if d11 else None,
        "vec": vec,
        "cna_disagree": ({k: vec[k] != cvec[k] for k in ("AV", "PR", "UI", "C", "I", "A")} if vec and cvec else None),
        "status": cve.get("vulnStatus", "MISSING"),
        "kev": "cisaExploitAdd" in cve,
        "cwe": ids,
        "cwe_primary_type": cwe_ids(w, wtype="Primary"),
        "cwe_secondary_type": cwe_ids(w, wtype="Secondary"),
        "cwe_nvd": cwe_ids(w, source=NVD),
        "r_cwe": r_cwe(ids, impacts),
        "r_cia": bool(vec and vec["C"] == "H" and vec["I"] == "H"),
        "r_text": bool(TEXT_RE.search(desc)),
        "desc": desc,
        "parts": sorted({c.split(":")[2] for c in pos_vuln if c.count(":") >= 4}),
        "has_nonvuln_cpe": any(not v for _, v, _ in matches),
        "and_with_platform": and_with_platform,
        "pos_vuln_criteria": pos_vuln,
        "vuln_products": vuln_products,
    }


def cve_role(products: list[str]) -> str:
    """One role if all products share it, 'mixed' otherwise, 'platform_only' if none is vulnerable."""
    roles = {ROLES[p] for p in products}
    return "platform_only" if not roles else roles.pop() if len(roles) == 1 else "mixed"


def component(f: dict, product: str) -> str:
    """Which component a CVE's description and positive vulnerable CPEs name: client / server / both / neither."""
    cpe_text = " ".join(c.replace(f":{product}:", ":") for c in f["pos_vuln_criteria"] if f":{product}:" in c)
    text = f["desc"] + " " + cpe_text.replace("_", " ")
    c, s = bool(CLIENT_RE.search(text)), bool(SERVER_RE.search(text))
    return "both" if c and s else "client" if c else "server" if s else "neither"


# ---------------------------------------------------------------- tables

def grouped(pop: dict[str, tuple[list[str], list[str]]], fn) -> dict[str, Counter]:
    """pop: cve_id -> (families, products). fn(cid) -> iterable of keys. Counts per 'all' / family / product."""
    out: dict[str, Counter] = defaultdict(Counter)
    for cid, (fams, prods) in pop.items():
        keys = list(fn(cid))
        for g in ["all", *(f"family {x}" for x in fams), *(f"product {x}" for x in prods)]:
            out[g].update(keys)
    return out


def order(groups) -> list[str]:
    fam = sorted(g for g in groups if g.startswith("family "))
    prod = sorted(g for g in groups if g.startswith("product "))
    return [g for g in ["all"] if g in groups] + fam + prod


def md_table(counts: dict[str, Counter], cols: list[str] | None = None, totals: dict[str, int] | None = None) -> str:
    cols = cols or sorted({k for c in counts.values() for k in c}, key=str)
    head = ["group"] + (["n"] if totals else []) + [str(c) for c in cols]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for g in order(counts):
        row = [g] + ([str(totals.get(g, 0))] if totals else []) + [str(counts[g].get(c, 0)) for c in cols]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default="2026-10-21")
    ap.add_argument("--cwe", default="data/raw/cwe/2026-11-08/cwec_v5.0.xml")
    args = ap.parse_args()
    snap = ROOT / "data" / "raw" / "nvd" / args.snapshot
    build_log = json.loads((ROOT / "data" / "derived" / "build_log.json").read_text())
    manifest_bytes = (snap / "manifest.json").read_bytes()
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    if manifest_sha != build_log["manifest_sha256"]:
        sys.exit(f"snapshot manifest SHA-256 {manifest_sha} != build_log {build_log['manifest_sha256']}: STOP")
    manifest = json.loads(manifest_bytes)
    cwe_path = ROOT / args.cwe
    cwe_sha = hashlib.sha256(cwe_path.read_bytes()).hexdigest()
    impacts, cwe_other = load_cwe_impacts(cwe_path)

    family_products: dict[str, list[str]] = defaultdict(list)
    for page in manifest["files"]:
        if page["product"] not in family_products[page["family"]]:
            family_products[page["family"]].append(page["product"])
    assert set(ROLES) == {p for ps in family_products.values() for p in ps}, "ROLES must cover the snapshot products"

    cves: dict[str, dict] = {}
    returned_by: dict[str, tuple[set, set]] = defaultdict(lambda: (set(), set()))
    for page in manifest["files"]:
        raw = (snap / page["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == page["sha256"], page["path"]
        for v in json.loads(gzip.decompress(raw))["response"]["vulnerabilities"]:
            c = v["cve"]
            cves[c["id"]] = c
            returned_by[c["id"]][0].add(page["family"])
            returned_by[c["id"]][1].add(page["product"])
    F = {cid: features(c, family_products, impacts) for cid, c in cves.items()}

    import csv
    included = {r["cve_id"]: r for r in csv.DictReader((ROOT / "data" / "derived" / "cves.csv").open())}
    mism = [cid for cid, r in included.items()
            if F[cid]["d11_version"] != r["cvss_version"] or F[cid]["d11_exploitability"] != float(r["exploitability_score"])
            or F[cid]["vec"]["PR"] != r["privileges_required"]]
    assert not mism, f"re-implemented D11 score pick disagrees with cves.csv on {mism[:5]}"

    pops = {
        "a_included": {cid: ([r["family"]], r["products"].split(";")) for cid, r in included.items()},
        "b_snapshot": {cid: (sorted(fs), sorted(ps)) for cid, (fs, ps) in returned_by.items()},
    }
    # Role and vulnerable products, per population: (a) the cves.csv products; (b) every vulnerable
    # FAMILY_PRODUCTS product of the families whose query returned the CVE.
    vprods = {"a_included": {cid: r["products"].split(";") for cid, r in included.items()},
              "b_snapshot": {cid: sorted({p for fam in pops["b_snapshot"][cid][0] for p in F[cid]["vuln_products"][fam]})
                             for cid in cves}}

    raw: dict = {"snapshot": args.snapshot, "manifest_sha256": manifest_sha, "cwe_xml_sha256": cwe_sha,
                 "cwe_weaknesses": len(impacts), "records": len(cves), "included": len(included), "tables": {}}
    rep = [f"# CVE semantics in the pinned NVD snapshot ({args.snapshot})", "",
           "**Analysis only. No exclusion, filter or criterion is adopted here; every count is descriptive.**", "",
           f"- Snapshot `data/raw/nvd/{args.snapshot}/`, manifest SHA-256 `{manifest_sha}` (matches "
           "`data/derived/build_log.json`). Every page's SHA-256 was checked against the manifest.",
           f"- **The snapshot was queried per product in FAMILY_PRODUCTS** ({len(manifest['files'])} pages, "
           f"{len(ROLES)} CPE products, 8 families), **so it is not a sample of all of NVD.**",
           f"- Population (a): the {len(included)} included CVEs of `data/derived/cves.csv`, grouped by their family "
           "and products. Population (b): all "
           f"{len(cves)} distinct records in the snapshot, grouped by every family / product whose query returned "
           "them (a record can count under several groups; 'all' counts it once).",
           f"- CWE catalogue: `{args.cwe}`, SHA-256 `{cwe_sha}`, {len(impacts)} Weaknesses, "
           f"{len(cwe_other)} Groupings (categories)/Views (docs/sources.md S6, S7).",
           "- D11 score = NVD Primary (`source == nvd@nist.gov`, `type == Primary`) v3.1, else v3.0; re-implemented here "
           "and identical to `cves.csv` (version, exploitability, PR) for all included CVEs.",
           "- Product roles: docs/sources.md §2 (P1–P35).", ""]

    def put(key: str, title: str, fn, cols=None, note: str = ""):
        rep.append(f"### {title}")
        if note:
            rep.append(note)
        for pname, pop in pops.items():
            f1 = (lambda cid, pname=pname: fn(cid, pname)) if "pname" in fn.__code__.co_varnames[:fn.__code__.co_argcount] else fn
            counts = grouped(pop, f1)
            totals = dict(grouped(pop, lambda cid: ["n"]))
            totals = {g: c["n"] for g, c in totals.items()}
            raw["tables"].setdefault(key, {})[pname] = {g: dict(c) for g, c in counts.items()}
            rep.extend(["", f"**({pname[0]}) {'1,473 included CVEs' if pname[0] == 'a' else 'all snapshot records'}**",
                        "", md_table(counts, cols, totals), ""])

    # 1. Scores present, and NVD vs CNA disagreement.
    rep.append("## 1. Which scores exist; NVD Primary vs CNA v3 disagreement")
    put("1_scores", "1a. Score presence (a CVE can have several)",
        lambda cid: [k for k, v in F[cid]["scores"].items() if v] + ([] if any(F[cid]["scores"].values()) else ["none"]),
        ["nvd_primary_v31", "nvd_primary_v30", "cna_v3", "v2", "v4", "none"],
        "nvd_primary_v30 counts a v3.0 NVD Primary score whether or not a v3.1 one also exists.")
    put("1_disagree", "1b. NVD Primary v3 vs CNA v3 on the same CVE: metrics that differ",
        lambda cid: (["both_present"] + [k for k, d in F[cid]["cna_disagree"].items() if d]
                     + (["any_differs"] if any(F[cid]["cna_disagree"].values()) else []))
        if F[cid]["cna_disagree"] else [],
        ["both_present", "any_differs", "AV", "PR", "UI", "C", "I", "A"])

    # 2. Base vector from the D11 score.
    rep.append("## 2. Base vector distribution (D11 score: NVD Primary v3.1, else v3.0)")
    for k in V3_METRICS:
        put(f"2_{k}", f"2. {k}", lambda cid, k=k: [F[cid]["vec"][k] if F[cid]["vec"] else "no_d11_score"],
            [*V3_METRICS[k], "no_d11_score"])
    put("2_joint", "2. Joint (AV, PR, UI)",
        lambda cid: ["/".join(F[cid]["vec"][x] for x in ("AV", "PR", "UI")) if F[cid]["vec"] else "no_d11_score"])

    # 3. vulnStatus and KEV.
    rep.append("## 3. vulnStatus distribution (and CISA KEV fields present)")
    put("3_status", "3. vulnStatus", lambda cid: [F[cid]["status"]])
    put("3_kev", "3b. Records with a `cisaExploitAdd` field", lambda cid: ["kev"] if F[cid]["kev"] else ["no_kev"],
        ["kev", "no_kev"])

    # 4. CWE.
    rep.append("## 4. CWE")

    def cwe_keys(cid):
        f = F[cid]
        ks = []
        ks += ["no_weakness"] if not f["cwe"] else []
        ks += ["has_type_Primary"] if f["cwe_primary_type"] else []
        ks += ["has_type_Secondary"] if f["cwe_secondary_type"] else []
        ks += ["has_nvd_source"] if f["cwe_nvd"] else []
        ks += ["has_cna_source"] if any(x for x in cves[cid].get("weaknesses", []) if x.get("source") != NVD) else []
        ks += ["NVD-CWE-Other"] if "NVD-CWE-Other" in f["cwe"] else []
        ks += ["NVD-CWE-noinfo"] if "NVD-CWE-noinfo" in f["cwe"] else []
        ks += ["only_NVD-CWE-*"] if f["cwe"] and all(i.startswith("NVD-CWE-") for i in f["cwe"]) else []
        ks += ["grouping_or_view"] if any(i in cwe_other for i in f["cwe"]) else []
        ks += ["unknown_id"] if any(i not in impacts and i not in cwe_other and not i.startswith("NVD-CWE-")
                                    for i in f["cwe"]) else []
        return ks
    put("4_cwe", "4a. CWE source and type (per CVE; columns are not exclusive)", cwe_keys,
        ["no_weakness", "has_type_Primary", "has_type_Secondary", "has_nvd_source", "has_cna_source",
         "NVD-CWE-Other", "NVD-CWE-noinfo", "only_NVD-CWE-*", "grouping_or_view", "unknown_id"])
    rep.append("### 4b. Top 5 CWEs per family (all weakness entries, any source; CVEs per CWE)")
    for pname, pop in pops.items():
        counts = grouped(pop, lambda cid: F[cid]["cwe"])
        raw["tables"].setdefault("4_top_cwe", {})[pname] = {g: dict(c) for g, c in counts.items()}
        rep += ["", f"**({pname[0]})**", "", "| group | top 5 |", "|---|---|"]
        for g in order(counts):
            if not g.startswith("product "):
                rep.append(f"| {g} | " + ", ".join(f"{i} {n}" for i, n in counts[g].most_common(5)) + " |")
    rep.append("")

    # 5. Code-execution candidates.
    rep += ["## 5. Code-execution candidates, side by side (no choice made)", "",
            f"- **R-CWE**: some CWE on the CVE (any weakness entry, any source) is a Weakness whose Common_Consequences "
            f"list the Impact \"{CODE_EXEC_IMPACT}\" (S6, S7). This is a property of the weakness *type*. `undetermined` "
            "= no CWE on the CVE is a Weakness (none, only NVD-CWE-*, groupings/views or unknown ids); it counts as "
            "False in the agreement cells.",
            "- **R-CIA**: D11 vector has C:H and I:H. **CVSS defines C/I/A as impact severity on the impacted "
            "component, not as code execution (S1 §2.3).** No D11 score counts as False.",
            "- **R-TEXT** (diagnostic only, not a rule): the English description matches "
            f"`{TEXT_RE.pattern}` (case-insensitive).", ""]
    put("5_rules", "5a. Each candidate",
        lambda cid: [f"R-CWE={F[cid]['r_cwe']}", f"R-CIA={F[cid]['r_cia']}", f"R-TEXT={F[cid]['r_text']}"],
        ["R-CWE=True", "R-CWE=False", "R-CWE=None", "R-CIA=True", "R-CIA=False", "R-TEXT=True", "R-TEXT=False"],
        "R-CWE=None is `undetermined`.")
    cell = lambda cid: "CWE{:d}/CIA{:d}/TEXT{:d}".format(bool(F[cid]["r_cwe"]), F[cid]["r_cia"], F[cid]["r_text"])
    cells = [f"CWE{a}/CIA{b}/TEXT{c}" for a in (1, 0) for b in (1, 0) for c in (1, 0)]
    put("5_agree", "5b. Three-way agreement (cell = CWE/CIA/TEXT, 1 = True)", lambda cid: [cell(cid)], cells)
    rng = random.Random(SEED)
    raw["disagreement_samples"] = {}
    rep.append(f"### 5c. Disagreement cells: up to {SAMPLE} random CVE IDs each (seed {SEED}), for manual check")
    for pname in pops:
        rep += ["", f"**({pname[0]})**", ""]
        for c in cells:
            if c in ("CWE1/CIA1/TEXT1", "CWE0/CIA0/TEXT0"):
                continue
            ids = sorted(cid for cid in pops[pname] if cell(cid) == c)
            pick = sorted(rng.sample(ids, min(SAMPLE, len(ids))))
            raw["disagreement_samples"].setdefault(pname, {})[c] = {"n": len(ids), "sample": pick}
            rep.append(f"- `{c}` (n = {len(ids)}): " + (", ".join(pick) or "none"))
    rep.append("")

    # 6. Product role.
    rep += ["## 6. Product role (docs/sources.md §2)", "",
            "Role per CVE: the role shared by all its vulnerable family products; `mixed` if they differ; "
            "`platform_only` if no family product is a positive vulnerable match. (a) uses the cves.csv products; "
            "(b) the vulnerable FAMILY_PRODUCTS products of the families whose query returned the record.", ""]
    for pname in pops:
        roles = {cid: cve_role(vprods[pname][cid]) for cid in pops[pname]}
        counts = grouped(pops[pname], lambda cid: [roles[cid]])
        totals = {g: c["n"] for g, c in grouped(pops[pname], lambda cid: ["n"]).items()}
        raw["tables"].setdefault("6_role", {})[pname] = {g: dict(c) for g, c in counts.items()}
        rep += [f"**6a ({pname[0]}) role**", "",
                md_table(counts, ["server", "multi", "unstated", "UNAVAILABLE", "mixed", "platform_only"], totals), ""]
    rep += ["### 6b. Multi-role products: which component the description / CPEs name", "",
            f"Client terms `{CLIENT_RE.pattern}`; server terms `{SERVER_RE.pattern}` (case-insensitive), searched in the "
            "English description and the positive vulnerable CPE strings with the vendor:product token removed. "
            "`both` and `neither` cannot be resolved this way and are listed in full.", ""]
    multi = [p for p, r in ROLES.items() if r == "multi"]
    raw["component"] = {}
    for pname in pops:
        rep += [f"**({pname[0]})**", "", "| product | CVEs | client | server | both | neither |", "|---|---|---|---|---|---|"]
        unresolved_lines = []
        for p in multi:
            ids = sorted(cid for cid in pops[pname] if p in vprods[pname][cid])
            comp = {cid: component(F[cid], p) for cid in ids}
            c = Counter(comp.values())
            raw["component"].setdefault(pname, {})[p] = comp
            rep.append(f"| {p} | {len(ids)} | {c['client']} | {c['server']} | {c['both']} | {c['neither']} |")
            for k in ("both", "neither"):
                lst = [cid for cid in ids if comp[cid] == k]
                unresolved_lines.append(f"- {p}, `{k}` ({len(lst)}): " + (", ".join(lst) or "none"))
        rep += ["", "Unresolved:", "", *unresolved_lines, ""]

    # 7. Configurations.
    rep.append("## 7. Configurations")
    put("7_parts", "7a. CPE part of positive vulnerable matches (S5: a application, o OS, h hardware; per CVE, not exclusive)",
        lambda cid: (F[cid]["parts"] or ["no_positive_vulnerable_cpe"]), ["a", "o", "h", "no_positive_vulnerable_cpe"])
    put("7_platform", "7b. Platform CPEs ('running on/with')",
        lambda cid: (["has_vulnerable_false_cpe"] if F[cid]["has_nonvuln_cpe"] else [])
        + (["AND_config_with_vulnerable_false"] if F[cid]["and_with_platform"] else []),
        ["has_vulnerable_false_cpe", "AND_config_with_vulnerable_false"],
        "NVD's prose definition of 'running on/with' was UNAVAILABLE (docs/sources.md S3). Operational stand-in: a "
        "cpeMatch with `vulnerable: false`, and, stricter, one inside an AND configuration or node.")
    put("7_multi", "7c. Vulnerable family products per CVE within its family",
        lambda cid, pname: [f"{len(vprods[pname][cid])}_products"],
        note="(a): products in cves.csv; (b): vulnerable FAMILY_PRODUCTS products over the families that returned it.")

    # 8. Funnel.
    rep += ["## 8. Funnel: 'usable as a remote foothold' = AV:N ∧ PR:N ∧ UI:N ∧ code-exec ∧ server role", "",
            "**This is a count, not an adopted criterion.** Each column counts CVEs that pass every condition to its "
            "left. Server role = the CVE's role (§6) is `server`. One funnel per code-exec candidate; R-TEXT is "
            "diagnostic only. R-CWE `undetermined` fails the code-exec step.", ""]
    steps = ["n", "d11_score", "AV:N", "PR:N", "UI:N", "code_exec", "server_role"]
    raw["funnel"] = {}
    for rule in ("r_cwe", "r_cia", "r_text"):
        for pname in pops:
            def passed(cid, rule=rule, pname=pname):
                f, out = F[cid], ["n"]
                for name, ok in (("d11_score", f["vec"] is not None), ("AV:N", f["vec"] and f["vec"]["AV"] == "N"),
                                 ("PR:N", f["vec"] and f["vec"]["PR"] == "N"), ("UI:N", f["vec"] and f["vec"]["UI"] == "N"),
                                 ("code_exec", f[rule] is True), ("server_role", cve_role(vprods[pname][cid]) == "server")):
                    if not ok:
                        break
                    out.append(name)
                return out
            counts = grouped(pops[pname], passed)
            raw["funnel"].setdefault(rule, {})[pname] = {g: dict(c) for g, c in counts.items()}
            empty = [g[7:] for g in order(counts) if g.startswith("family ") and counts[g].get("server_role", 0) == 0]
            rep += [f"**8 ({pname[0]}) code-exec = {rule.upper().replace('_', '-')}**", "", md_table(counts, steps), "",
                    f"Families with 0 CVEs at the end: {', '.join(empty) or 'none'}.", ""]

    # D26 re-verification (E1, E5).
    av = Counter(F[cid]["vec"]["AV"] for cid in included)
    rdp = [cid for cid, r in included.items() if r["family"] == "rdp"]
    fr = [cid for cid in rdp if "freerdp:freerdp" in included[cid]["products"].split(";")]
    raw["d26_check"] = {"AV": dict(av), "rdp": len(rdp), "rdp_freerdp": len(fr)}
    rep += ["## D26 re-verification from the raw snapshot", "",
            f"- E1: AV among the {len(included)} included CVEs (D11 vector): " + ", ".join(f"{k} {v}" for k, v in sorted(av.items()))
            + f". D26 states 160 AV:L and 13 AV:A: **{'match' if (av['L'], av['A']) == (160, 13) else 'MISMATCH'}**.",
            f"- E5: {len(fr)} of {len(rdp)} included rdp CVEs list freerdp:freerdp. D26 states 89 of 106: "
            f"**{'match' if (len(fr), len(rdp)) == (89, 106) else 'MISMATCH'}**.", ""]

    out = runlog.write_run("cve_semantics", raw, "\n".join(rep) + "\n", [SEED],
                           {"snapshot": args.snapshot, "cwe": args.cwe, "cwe_sha256": cwe_sha, "sample": SAMPLE},
                           root=ROOT / "results")
    print(out)


if __name__ == "__main__":
    main()
