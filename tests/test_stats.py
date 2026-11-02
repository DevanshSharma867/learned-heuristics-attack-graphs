"""The D23 §2 statistics (src/ahg/stats.py), checked against published reference values and hand computations."""

import math

import pytest

from ahg.stats import BEATS, LOSES, NO_DIFFERENCE, holm, nested_bootstrap, verdict, wilcoxon

# Fisher's (Darwin's Zea mays) differences, the example in scipy.stats.wilcoxon's documentation:
# statistic min(W+, W-) = 24, exact two-sided p = 0.041259765625.
DARWIN = [6, 8, 14, 16, 23, 24, 28, 29, 41, -48, 49, 56, 60, -67, 75]


def test_wilcoxon_exact_matches_reference():
    w = wilcoxon(DARWIN)
    assert w["method"] == "exact" and w["w_minus"] == 24 and w["w_plus"] == 120 - 24
    assert w["p"] == pytest.approx(0.041259765625, abs=1e-12)
    assert w["rank_biserial"] == pytest.approx((96 - 24) / 120)


def test_wilcoxon_is_symmetric_and_drops_zeros():
    a, b = wilcoxon(DARWIN), wilcoxon([-x for x in DARWIN])
    assert a["p"] == pytest.approx(b["p"]) and a["rank_biserial"] == pytest.approx(-b["rank_biserial"])
    z = wilcoxon(DARWIN + [0, 0])
    assert z["zeros"] == 2 and z["n_nonzero"] == 15 and z["p"] == pytest.approx(a["p"])


def test_wilcoxon_exact_small_cases():
    # n = 3, all positive: W+ = 6 is the most extreme of 8 equally likely subsets, two-sided p = 2/8.
    assert wilcoxon([1, 2, 3])["p"] == pytest.approx(0.25)
    assert wilcoxon([1, 2, 3])["rank_biserial"] == 1.0
    assert wilcoxon([0, 0])["p"] == 1.0


def test_wilcoxon_normal_approximation_with_ties_by_hand():
    d = [1, 1, 2, 2, 2, 3, -1, 4, 5, 6] * 6  # n = 60 and tied |d|: normal approximation
    w = wilcoxon(d)
    assert w["method"] == "normal"
    n = 60
    abs_d = [abs(x) for x in d]
    ties = sum(abs_d.count(v) ** 3 - abs_d.count(v) for v in set(abs_d))
    sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24 - ties / 48)
    z = (abs(w["w_plus"] - n * (n + 1) / 4) - 0.5) / sd
    assert w["p"] == pytest.approx(math.erfc(z / math.sqrt(2)))
    assert w["w_plus"] + w["w_minus"] == n * (n + 1) / 2


def test_holm_by_hand():
    # sorted 0.005*4 = 0.02, 0.01*3 = 0.03, 0.03*2 = 0.06, 0.04*1 = 0.04 -> monotone 0.02, 0.03, 0.06, 0.06
    assert holm([0.01, 0.04, 0.03, 0.005]) == pytest.approx([0.03, 0.06, 0.06, 0.02])
    assert holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    assert holm([]) == []


def test_nested_bootstrap_constant_and_determinism():
    logs = [[math.log(2.0)] * 3 for _ in range(10)]
    assert nested_bootstrap(logs, "k", n=500) == pytest.approx([2.0, 2.0, 2.0])
    noisy = [[0.1 * i - 0.2 * s for s in range(3)] for i in range(8)]
    assert nested_bootstrap(noisy, "k", n=500) == nested_bootstrap(noisy, "k", n=500)
    est, lo, hi = nested_bootstrap(noisy, "k", n=500)
    assert lo <= est <= hi


def test_nested_bootstrap_carries_seed_variation():
    """Identical instances, varying seeds: an instance bootstrap of seed means has a zero-width CI;
    the nested bootstrap does not, because it resamples seeds too (D23 §2)."""
    logs = [[-0.3, 0.0, 0.3] for _ in range(20)]
    seed_means = [[sum(r) / 3] for r in logs]
    assert nested_bootstrap(seed_means, "k", n=2000)[1:] == pytest.approx([1.0, 1.0])
    _, lo, hi = nested_bootstrap(logs, "k", n=2000)
    assert lo < 1.0 < hi


def test_nested_bootstrap_ignores_missing():
    logs = [[math.log(2.0), float("nan")], [math.log(2.0), math.log(2.0)]]
    assert nested_bootstrap(logs, "k", n=200)[0] == pytest.approx(2.0)


def test_verdicts():
    assert verdict([0.6, 0.5, 0.7], 0.001) == BEATS
    assert verdict([0.6, 0.5, 1.01], 0.001) == NO_DIFFERENCE  # CI crosses 1
    assert verdict([0.95, 0.9, 0.99], 0.001) == NO_DIFFERENCE  # above the 0.90 threshold
    assert verdict([0.6, 0.5, 0.7], 0.02) == NO_DIFFERENCE  # not significant after Holm
    assert verdict([1.3, 1.2, 1.4], 0.001) == LOSES
    assert verdict([1.1, 1.05, 1.2], 0.001) == NO_DIFFERENCE  # below 1/0.90


def _analyse_module():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("analyse", Path(__file__).parents[1] / "scripts" / "analyse.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_analyse_pairs_seeds_and_builds_the_holm_family():
    """Two primaries with two seeds each and one ablation: the H1 family holds primaries x comparators only,
    the per-seed ratios are each seed's own geometric mean, and the Wilcoxon d_i uses the seed-mean log."""
    from ahg.evaluate import COMPARATORS
    run = lambda e, c=100: {"expanded": e, "cost": c, "seconds": e / 1000, "budget_hit": False}
    over = {"walk": {"rate": 0.5}, "astar_expanded": {"rate": 0.5}, "successor": {"rate": 0.5}}
    names = {"A": ["a0", "a1"], "B": ["b0", "b1"], "mlp": ["m0", "m1"]}
    recs = []
    for i in range(12):
        runs = {c: run(100 + i) for c in COMPARATORS}
        runs.update({"a0": run(50 + i), "a1": run(60 + i), "b0": run(90 + i), "b1": run(90 + i, 110),
                     "m0": run(300), "m1": run(300)})
        recs.append({"hstar": 100, "runs": runs})
    frozen = {"runs": [{"id": g, "role": "primary" if g in "AB" else "ablation", "seed": s, "run": f"r/{n}"}
                       for g, ns in names.items() for s, n in enumerate(ns)]}
    raw = {"split": "val", "budget": 10_000, "records": recs,
           "models": [{"name": n, "run": f"/x/r/{n}", "combine": None} for ns in names.values() for n in ns],
           "summary": {n: {"overestimation": over} for ns in names.values() for n in ns}}
    a = _analyse_module().analyse(raw, frozen)
    assert len(a["h1"]) == 2 * len(COMPARATORS) and {t["model"] for t in a["h1"]} == {"A", "B"}
    per_seed = a["models"]["A"]["vs"]["hmax"]["expansions"]["per_seed"]
    assert per_seed[0] == pytest.approx(math.exp(sum(math.log((50 + i) / (100 + i)) for i in range(12)) / 12))
    t = next(t for t in a["h1"] if t["model"] == "A" and t["comparator"] == "hmax")
    assert t["n_nonzero"] == 12 and t["rank_biserial"] == -1.0 and t["w_plus"] == 0
    assert a["models"]["B"]["h2"]["optimal_per_seed"] == [12, 0]
    assert a["models"]["B"]["h2"]["plan_cost"][0] == pytest.approx(math.sqrt(1.1))
