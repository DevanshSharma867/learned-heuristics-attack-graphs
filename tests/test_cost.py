from fractions import Fraction
from pathlib import Path

import pytest

from ahg.cost import K_MAX, K_MIN, SCALE, cost_units, exploitability_k
from ahg.cve import load_table

TABLE = Path(__file__).resolve().parent.parent / "data" / "derived" / "cves.csv"


def test_endpoints():
    assert exploitability_k(0.1) == 1 and cost_units(0.1) == 380  # hardest to exploit: c = 10
    assert exploitability_k(3.9) == 39 and cost_units(3.9) == 38  # easiest: c = 1


@pytest.mark.parametrize("k", range(K_MIN, K_MAX + 1))
def test_encoding_equals_frozen_model_exactly(k):
    # C = 38·c with c = 1 + 9·(1 − x), x = (k − 1)/38, in exact rational arithmetic.
    x = Fraction(k - 1, 38)
    c = 1 + 9 * (1 - x)
    assert SCALE * c == cost_units(k / 10)
    assert 1 <= c <= 10


def test_round_not_int_pitfall():
    e = 4.35 - 1.15  # prints as ~3.2, but is 3.1999999999999997
    assert int(10 * e) == 31  # the trap D9 warns about
    assert exploitability_k(e) == 32
    assert cost_units(e) == 389 - 9 * 32 == 101


@pytest.mark.parametrize("e", [0.0, 0.05, 1.25, 4.0, -0.1])
def test_off_grid_or_out_of_range_rejected(e):
    with pytest.raises(ValueError):
        cost_units(e)


def test_hand_checked_real_cve():
    """CVE-2016-10012 (OpenSSH), NVD Primary CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U.

    By hand:
      E = 8.22·0.55·0.77·0.62·0.85 = 1.8346 → NVD reports 1.8
      k = round(10·1.8) = 18
      x = (18 − 1)/38 = 17/38
      c = 1 + 9·(1 − 17/38) = 1 + 189/38 = 227/38 ≈ 5.97 effort units
      C = 38·c = 227  (= 389 − 9·18)
    """
    row = {r.cve_id: r for r in load_table(TABLE)}["CVE-2016-10012"]
    assert (row.family, row.cvss_version, row.exploitability_score) == ("ssh", "3.0", 1.8)
    assert round(8.22 * 0.55 * 0.77 * 0.62 * 0.85, 1) == 1.8
    assert exploitability_k(row.exploitability_score) == 18
    assert cost_units(row.exploitability_score) == 227
    assert Fraction(227, SCALE) == 1 + 9 * (1 - Fraction(17, 38))


def test_every_derived_score_maps_to_integer_cost_in_range():
    rows = load_table(TABLE)
    assert rows, "derived table is empty"
    for r in rows:
        c = cost_units(r.exploitability_score)
        assert isinstance(c, int) and 38 <= c <= 380, r
