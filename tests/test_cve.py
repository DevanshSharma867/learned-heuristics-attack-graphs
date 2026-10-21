from datetime import date

import pytest

from ahg.cve import FAMILY_PRODUCTS, OUTCOMES, derive, nvd_primary_v3, privileges_required, score_status
from ahg.network import SERVICE_FAMILIES


def metric(source, typ, score, pr="N"):
    word = {"N": "NONE", "L": "LOW", "H": "HIGH"}[pr]
    vector = f"CVSS:3.1/AV:N/AC:L/PR:{pr}/UI:N/S:U/C:H/I:H/A:H"
    return {"source": source, "type": typ, "exploitabilityScore": score,
            "cvssData": {"vectorString": vector, "privilegesRequired": word}}


def cve(cid, products, metrics, published="2019-05-01T10:00:00.000", vulnerable=True):
    cfg = [{"nodes": [{"cpeMatch": [{"vulnerable": vulnerable, "criteria": f"cpe:2.3:a:{p}:1.0:*:*:*:*:*:*:*"} for p in products]}]}]
    return {"id": cid, "published": published, "metrics": metrics, "configurations": cfg}


NVD31 = {"cvssMetricV31": [metric("cna@example.org", "Secondary", 3.9), metric("nvd@nist.gov", "Primary", 1.8, "L")]}


def test_mapping_covers_exactly_the_service_families():
    assert set(FAMILY_PRODUCTS) == set(SERVICE_FAMILIES)


def test_nvd_primary_preferred_over_cna_and_v31_over_v30():
    assert nvd_primary_v3({"metrics": NVD31}) == ("3.1", 1.8, "L")
    both = {"cvssMetricV30": [metric("nvd@nist.gov", "Primary", 2.8)], **NVD31}
    assert nvd_primary_v3({"metrics": both}) == ("3.1", 1.8, "L")
    assert nvd_primary_v3({"metrics": {"cvssMetricV30": [metric("nvd@nist.gov", "Primary", 2.8)]}}) == ("3.0", 2.8, "N")


def test_score_exclusion_reasons():
    assert score_status({"metrics": {"cvssMetricV31": [metric("cna@example.org", "Secondary", 3.9)]}}) == "v3_cna_only"
    assert score_status({"metrics": {"cvssMetricV2": [metric("nvd@nist.gov", "Primary", 10.0)]}}) == "v2_only"
    assert score_status({"metrics": {"cvssMetricV40": [{}]}}) == "v4_only"
    assert score_status({"metrics": {}}) == "no_score"


def test_derive_rules_and_counts():
    matches = [
        ("ssh", "openbsd:openssh", cve("CVE-2019-0001", ["openbsd:openssh"], NVD31)),
        # same CVE returned twice within a family: one record, products merged
        ("sql", "oracle:mysql", cve("CVE-2019-0002", ["oracle:mysql", "mariadb:mariadb"], NVD31)),
        ("sql", "mariadb:mariadb", cve("CVE-2019-0002", ["oracle:mysql", "mariadb:mariadb"], NVD31)),
        ("ssh", "openbsd:openssh", cve("CVE-2019-0003", ["openbsd:openssh"], NVD31, vulnerable=False)),
        ("ssh", "openbsd:openssh", cve("CVE-2019-0004", ["openbsd:openssh", "samba:samba"], NVD31)),
        ("smb", "samba:samba", cve("CVE-2019-0004", ["openbsd:openssh", "samba:samba"], NVD31)),
        ("ssh", "openbsd:openssh", cve("CVE-2019-0005", ["openbsd:openssh"], {"cvssMetricV2": [{}]})),
        ("ssh", "openbsd:openssh", cve("CVE-2024-0006", ["openbsd:openssh"], NVD31, published="2024-01-01T00:00:00")),
        ("ssh", "openbsd:openssh", cve("CVE-2015-0007", ["openbsd:openssh"], NVD31, published="2015-12-31T23:59:59")),
    ]
    records, counts = derive(matches)
    assert [(r.cve_id, r.family, r.products) for r in records] == [
        ("CVE-2019-0001", "ssh", "openbsd:openssh"),
        ("CVE-2019-0002", "sql", "mariadb:mariadb;oracle:mysql"),
    ]
    assert records[0].cvss_version == "3.1" and records[0].exploitability_score == 1.8
    assert records[0].published == date(2019, 5, 1)
    assert records[0].privileges_required == "L"  # from the NVD Primary vector, not the CNA's
    assert counts == {
        ("ssh", "included"): 1, ("sql", "included"): 1, ("ssh", "platform_only"): 1,
        ("ssh", "multi_family"): 1, ("smb", "multi_family"): 1, ("ssh", "v2_only"): 1,
        ("ssh", "outside_window"): 2,
    }  # fmt: skip
    assert {reason for _, reason in counts} <= set(OUTCOMES)  # build log lists every OUTCOME, zeros included


def test_pr_read_from_vector_and_cross_checked():
    assert privileges_required(metric("nvd@nist.gov", "Primary", 1.2, "H")) == "H"
    bad = metric("nvd@nist.gov", "Primary", 1.2, "H")
    bad["cvssData"]["privilegesRequired"] = "LOW"
    with pytest.raises(ValueError):
        privileges_required(bad)
