import os
import subprocess
import sys

import pytest

from ahg.network import INTERNET, Network, host_links, structure_stats
from ahg.topology import GENERATORS, flat, generate, hub_and_spoke, tiered

FAMILIES = sorted(GENERATORS)
SEEDS = range(20)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", SEEDS)
def test_same_seed_byte_identical(family, seed):
    assert generate(family, seed, 15).to_json() == generate(family, seed, 15).to_json()


@pytest.mark.parametrize("family", FAMILIES)
def test_different_seeds_differ(family):
    assert len({generate(family, s, 15).to_json() for s in SEEDS}) == len(SEEDS)


def test_byte_identical_across_processes():
    # Different PYTHONHASHSEED values catch any accidental dependence on
    # set/dict iteration order of strings.
    code = "from ahg.topology import GENERATORS as G; print(''.join(G[f](7, 20).to_json() for f in sorted(G)))"
    outs = {
        subprocess.run(
            [sys.executable, "-c", code], env={**os.environ, "PYTHONHASHSEED": h}, capture_output=True, text=True, check=True
        ).stdout
        for h in ("1", "2")
    }
    assert len(outs) == 1


def test_same_seed_uncorrelated_across_families():
    # Guards the held-out-family split: seed s must not give the same service
    # draw in every family.
    for seed in SEEDS:
        draws = {tuple(s.family for s in generate(f, seed, 15).services) for f in FAMILIES}
        assert len(draws) == len(FAMILIES)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", SEEDS)
def test_json_round_trip(family, seed):
    net = generate(family, seed, 15)
    assert Network.from_json(net.to_json()) == net


@pytest.mark.parametrize("family", FAMILIES)
def test_meta_records_seed_family_params(family):
    net = generate(family, 3, 12, services=(2, 4))
    assert net.meta["family"] == family
    assert net.meta["seed"] == 3
    assert net.meta["params"]["n_hosts"] == 12
    assert net.meta["params"]["services"] == [2, 4]
    # The recorded params regenerate the identical network.
    p = dict(net.meta["params"], services=tuple(net.meta["params"]["services"]))
    assert GENERATORS[family](net.meta["seed"], **p) == net


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("n", [3, 6, 30])  # 3 = smallest valid size for the default 3 tiers
def test_basic_shape(family, seed, n):
    net = generate(family, seed, n)
    assert len(net.hosts) == n + 1 and net.hosts[INTERNET].zone == "internet"
    for h in net.hosts[1:]:
        fams = [s.family for s in net.services if s.host == h.id]
        assert 1 <= len(fams) <= 3 and len(set(fams)) == len(fams)
    # Every host is attackable: reachable from the internet over host links.
    assert structure_stats(net)["reachable_hosts"] == n


@pytest.mark.parametrize("seed", SEEDS)
def test_flat_invariants(seed):
    net = flat(seed, 20)
    assert {h.zone for h in net.hosts[1:]} == {"lan"}


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("n_tiers", [1, 3, 4])
def test_tiered_invariants(seed, n_tiers):
    net = tiered(seed, 20, n_tiers=n_tiers)
    tier = {h.id: (0 if h.zone == "dmz" else int(h.zone.removeprefix("tier"))) for h in net.hosts[1:]}
    for a, b in host_links(net):
        if a == INTERNET:
            assert tier[b] == 0, "only the DMZ is exposed"
        else:
            assert tier[b] - tier[a] in (0, 1), "no tier skipping, no upward edges"
    for t in net.trust:
        assert tier[t.dst] - tier[t.src] in (0, 1)
    assert structure_stats(net)["depth"] >= n_tiers


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("n_hubs", [1, 3])
def test_hub_and_spoke_invariants(seed, n_hubs):
    net = hub_and_spoke(seed, 20, n_hubs=n_hubs)
    zone = {h.id: h.zone for h in net.hosts}
    hub_of = {h.id: 1 + (h.id - 1 - n_hubs) % n_hubs for h in net.hosts if h.zone == "spoke"}
    for a, b in host_links(net):
        if a == INTERNET:
            assert zone[b] == "spoke", "hubs are not exposed"
        elif zone[a] == "spoke":
            assert b == hub_of[a], "a spoke talks only to its own hub"
        elif zone[b] == "spoke":
            assert a == hub_of[b]
    for t in net.trust:
        assert hub_of[t.dst] == t.src


def classify(net: Network) -> str:
    """Guess the family from label-free structure only (no zones, no meta)."""
    st = structure_stats(net)
    if st["hub_share"] == 1.0:
        return "hub_and_spoke"
    return "tiered" if st["deep_share"] >= 0.2 else "flat"


@pytest.mark.parametrize("n", [30, 60])
def test_families_structurally_distinguishable(n):
    # At small n (~10) a sparse flat LAN can look like a chain, so the check
    # is made at realistic sizes, with default parameters.
    for family in FAMILIES:
        for seed in range(50):
            assert classify(generate(family, seed, n)) == family, (family, seed)


@pytest.mark.parametrize(
    "bad",
    [
        lambda: flat(0, 0),
        lambda: flat(0, 5, services=(0, 2)),
        lambda: flat(0, 5, services=(3, 2)),
        lambda: flat(0, 5, p_reach=1.5),
        lambda: tiered(0, 2, n_tiers=3),
        lambda: hub_and_spoke(0, 1, n_hubs=1),
    ],
)
def test_bad_params_rejected(bad):
    with pytest.raises(ValueError):
        bad()


def test_malformed_json_rejected():
    net = flat(0, 5)
    bad = net.to_json().replace('"zone": "internet"', '"zone": "lan"', 1)
    with pytest.raises(ValueError):
        Network.from_json(bad)
