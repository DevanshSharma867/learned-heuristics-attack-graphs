"""Split isolation (CLAUDE.md rule 1, D19 §1): disjoint topology seeds, one-factor shifts, CVE pools, test log."""

import itertools
import json

import pytest

from ahg.cve import load_table
from ahg.labels import CVES
from ahg.splits import RESERVED_SEEDS, SPLITS, cve_pool, record_test_access


def test_no_seed_in_two_splits():
    ranges = {name: set(s.seeds) for name, s in SPLITS.items()}
    ranges.update({f"reserved{i}": set(r) for i, r in enumerate(RESERVED_SEEDS)})
    for (a, sa), (b, sb) in itertools.combinations(ranges.items(), 2):
        assert not sa & sb, f"{a} and {b} share seeds {sorted(sa & sb)[:5]}"


def test_instance_spec_is_the_seed_and_round_robin():
    train = SPLITS["train"]
    cells = train.cells()
    assert len(cells) == 3 * 2 * 2 * 7
    specs = [train.instance_spec(s) for s in range(1000, 1000 + len(cells))]
    assert [{k: sp[k] for k in cells[0]} for sp in specs] == cells  # every cell exactly once
    assert all(sp["seed"] == s and sp["split"] == "train" for sp, s in zip(specs, range(1000, 1084)))
    assert train.instance_spec(1000) == train.instance_spec(1000)


def test_d20_extension_keeps_d19_cells():
    train = SPLITS["train"]
    assert len(train.seeds) == 3000 and len(set(train.seeds)) == 3000
    assert train.index(1599) == 599 and train.index(10000) == 600
    # the extension continues the round-robin where the D19 range stops
    assert train.instance_spec(10000)["variant"] == train.cells()[600 % 84]["variant"]


def test_seed_outside_split_is_refused():
    for seed in (1700, 999, 12400):
        with pytest.raises(ValueError):
            SPLITS["train"].instance_spec(seed)


def test_each_test_split_changes_one_factor():
    base = SPLITS["train"]
    factors = lambda s: {"variants": s.variants, "sizes": s.sizes, "levels": s.levels, "pool": s.pool}
    for name in ("val", "test_id"):
        assert factors(SPLITS[name]) == factors(base)
    for name, changed in (("test_size", "sizes"), ("test_structure", "variants"), ("test_vuln", "pool"),
                          ("test_vuln_cost", "pool")):
        diff = [k for k, v in factors(SPLITS[name]).items() if v != factors(base)[k]]
        assert diff == [changed], name
    assert "hub_and_spoke" not in base.variants and 30 not in base.sizes


def test_cve_pools_disjoint_and_cover_every_family():
    table = load_table(CVES)
    train, held, costly = (cve_pool(table, p) for p in ("train", "heldout", "heldout_costly"))
    ids = lambda pool: {r.cve_id for r in pool}
    assert not ids(train) & ids(held) and ids(train) | ids(held) == ids(table)
    assert ids(costly) <= ids(held) and all(r.exploitability_score <= 2.8 for r in costly)
    families = {r.family for r in table}
    for pool in (train, held, costly):
        assert {r.family for r in pool} == families


def test_test_access_log(tmp_path):
    log = tmp_path / "log.jsonl"
    with pytest.raises(PermissionError):
        record_test_access("b", "test_id", None, "c", log=log)
    assert not log.exists()
    record_test_access("b", "test_id", "evaluation", "c", log=log)
    with pytest.raises(PermissionError):
        record_test_access("b", "test_id", "evaluation", "c", log=log)
    record_test_access("b", "test_id", "evaluation", "c", permitted_by="D99", log=log)
    record_test_access("b", "test_size", "evaluation", "c", log=log)
    entries = [json.loads(line) for line in log.read_text().splitlines()]
    assert [(e["split"], e["permitted_by"]) for e in entries] == [("test_id", None), ("test_id", "D99"),
                                                                  ("test_size", None)]
