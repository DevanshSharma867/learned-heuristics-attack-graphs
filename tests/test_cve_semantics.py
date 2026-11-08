"""Parsing helpers of scripts/measure_cve_semantics.py: CVSS v3 vector parsing and the CWE join."""

import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "measure_cve_semantics", Path(__file__).parents[1] / "scripts" / "measure_cve_semantics.py")
mcs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcs)


def test_parse_v3_vector_reads_all_eight_base_metrics():
    v = mcs.parse_v3_vector("CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:L/A:N")
    assert v == {"AV": "L", "AC": "H", "PR": "L", "UI": "R", "S": "C", "C": "H", "I": "L", "A": "N"}
    assert mcs.parse_v3_vector("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")["AV"] == "N"


def test_parse_v3_vector_ignores_temporal_metrics():
    v = mcs.parse_v3_vector("CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:P/RL:O")
    assert v["AV"] == "A" and set(v) == set(mcs.V3_METRICS)


@pytest.mark.parametrize("bad", [
    "CVSS:2.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",   # not v3
    "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",            # no prefix
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H",       # A missing
    "CVSS:3.1/AV:X/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",   # illegal AV
    "CVSS:3.1/AV:N/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",  # repeated
])
def test_parse_v3_vector_rejects_malformed(bad):
    with pytest.raises(ValueError):
        mcs.parse_v3_vector(bad)


WEAK = [
    {"source": "nvd@nist.gov", "type": "Primary", "description": [{"lang": "en", "value": "CWE-787"}]},
    {"source": "cna@example.org", "type": "Secondary",
     "description": [{"lang": "en", "value": "CWE-79"}, {"lang": "en", "value": "CWE-787"}]},
    {"source": "nvd@nist.gov", "type": "Primary", "description": [{"lang": "es", "value": "CWE-1"}]},
]


def test_cwe_ids_filters_by_source_and_type_and_dedups():
    assert mcs.cwe_ids(WEAK) == ["CWE-787", "CWE-79"]
    assert mcs.cwe_ids(WEAK, source="nvd@nist.gov") == ["CWE-787"]
    assert mcs.cwe_ids(WEAK, source="other") == ["CWE-79", "CWE-787"]
    assert mcs.cwe_ids(WEAK, wtype="Secondary") == ["CWE-79", "CWE-787"]
    assert mcs.cwe_ids([]) == []


CWE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Weakness_Catalog xmlns="http://cwe.mitre.org/cwe-8" Name="CWE" Version="t">
 <Weaknesses>
  <Weakness ID="787" Name="OOB write"><Common_Consequences>
   <Consequence><Scope>Integrity</Scope><Impact>Modify Memory</Impact>
    <Impact>Execute Unauthorized Code or Commands</Impact></Consequence>
  </Common_Consequences></Weakness>
  <Weakness ID="79" Name="XSS"><Common_Consequences>
   <Consequence><Scope>Confidentiality</Scope><Impact>Read Application Data</Impact></Consequence>
  </Common_Consequences></Weakness>
  <Weakness ID="1" Name="no consequences"/>
 </Weaknesses>
 <Categories><Category ID="264" Name="Permissions"/></Categories>
 <Groupings><Grouping ID="310" Name="Crypto"/></Groupings>
 <Views><View ID="1003" Name="NVD view"/></Views>
</Weakness_Catalog>
"""


def test_cwe_join(tmp_path):
    p = tmp_path / "cwe.xml"
    p.write_text(CWE_XML)
    impacts, other = mcs.load_cwe_impacts(p)
    assert impacts == {"CWE-787": {"Modify Memory", "Execute Unauthorized Code or Commands"},
                       "CWE-79": {"Read Application Data"}, "CWE-1": set()}
    assert other == {"CWE-264", "CWE-310", "CWE-1003"}
    assert mcs.r_cwe(["CWE-79", "CWE-787"], impacts) is True
    assert mcs.r_cwe(["CWE-79", "CWE-1"], impacts) is False
    # Only NVD placeholders, categories or unknown ids: undetermined, not False.
    assert mcs.r_cwe(["NVD-CWE-Other", "NVD-CWE-noinfo", "CWE-264", "CWE-310", "CWE-99999"], impacts) is None
    assert mcs.r_cwe([], impacts) is None
