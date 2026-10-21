import dataclasses
import random
from datetime import date
from pathlib import Path

import pytest

from ahg.assign import assign_cves
from ahg.cve import CveRecord, load_table
from ahg.network import SERVICE_FAMILIES
from ahg.topology import GENERATORS, generate

TABLE = Path(__file__).resolve().parent.parent / "data" / "derived" / "cves.csv"

# Synthetic pool: 10 CVEs per family, independent of the real table.
POOL = [
    CveRecord(f"CVE-2019-{fam}-{i:02d}", fam, "v:p", "3.1", 0.1 * (1 + i), date(2019, 1, 1), "N")
    for fam in SERVICE_FAMILIES
    for i in range(10)
]


def ids(assignment):
    return [(sid, r.cve_id) for sid, r in sorted(assignment.items())]


@pytest.mark.parametrize("family", sorted(GENERATORS))
def test_deterministic_and_family_consistent(family):
    net = generate(family, 4, 20)
    a = assign_cves(net, POOL, seed=4)
    assert ids(a) == ids(assign_cves(net, POOL, seed=4))
    assert set(a) == {s.id for s in net.services}
    for s in net.services:
        assert a[s.id].family == s.family


def test_independent_of_pool_order():
    net = generate("flat", 1, 20)
    shuffled = POOL[:]
    random.Random(0).shuffle(shuffled)
    assert ids(assign_cves(net, POOL, seed=1)) == ids(assign_cves(net, shuffled, seed=1))


def test_seed_changes_assignment():
    net = generate("tiered", 2, 20)
    assert ids(assign_cves(net, POOL, seed=2)) != ids(assign_cves(net, POOL, seed=3))


def test_same_seed_uncorrelated_across_topology_families():
    # Identical services, only the topology-family label differs, so any
    # difference comes from the family:seed seeding alone.
    net = generate("flat", 5, 30)
    other = dataclasses.replace(net, meta={**net.meta, "family": "tiered"})
    assert ids(assign_cves(net, POOL, seed=5)) != ids(assign_cves(other, POOL, seed=5))


def test_empty_family_pool_rejected():
    net = generate("flat", 0, 10)
    with pytest.raises(ValueError):
        assign_cves(net, [r for r in POOL if r.family != net.services[0].family], seed=0)


@pytest.mark.parametrize("family", sorted(GENERATORS))
def test_real_table_covers_every_service_family(family):
    pool = load_table(TABLE)
    assert {r.family for r in pool} == set(SERVICE_FAMILIES)
    net = generate(family, 0, 30)
    assert len(assign_cves(net, pool, seed=0)) == len(net.services)
