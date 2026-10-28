"""D15 generator knobs: byte-identity when off, semantics when on, labels on knob instances."""

import json
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pytest

import golden
from ahg.attack_graph import KnobInfeasible, UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.heuristics import ADMISSIBLE, HEURISTICS
from ahg.network import INTERNET
from ahg.oracle import optimal_cost
from ahg.search import astar

from helpers import reachable_states

POOL = load_table(golden.ROOT / "data" / "derived" / "cves.csv")
GOLDEN = json.loads(golden.GOLDEN.read_text())["digests"]
FAMILIES = golden.FAMILIES


@pytest.mark.parametrize("case", golden.CASES, ids=lambda c: golden.key(*c))
def test_knobs_off_byte_identical(case):
    """Knobs at their defaults, implicit or explicit, reproduce the pre-knob Task exactly (D15 §1)."""
    want = GOLDEN[golden.key(*case)]
    assert golden.case_digest(*case, POOL) == want
    assert golden.case_digest(*case, POOL, cred_levels=0, coupling=0.0, share_pool=None) == want


def build(family, seed, n, **knobs):
    try:
        return make_instance(family, seed, n, POOL, **knobs)
    except UnreachableGoal:
        return None


def first_reachable(family, n, k, **knobs):
    out, seed = [], 0
    while len(out) < k and seed < 200:
        i = build(family, seed, n, **knobs)
        if i is not None:
            out.append(i)
        seed += 1
    assert len(out) == k, f"fewer than {k} reachable {family} n={n} {knobs} in 200 seeds"
    return out


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", range(5))
def test_knobs_leave_network_cves_and_target_alone(family, seed):
    """Each knob has its own rng stream: topology, CVE and goal draws are unchanged (D15 §1)."""
    base = make_instance(family, seed, 12, POOL)
    try:
        on = make_instance(family, seed, 12, POOL, cred_levels=3, coupling=0.5, share_pool=2)
    except UnreachableGoal:
        pytest.skip("goal unreachable with knobs on; the draws are checked on the reachable seeds")
    assert (on.network, on.cves, on.target) == (base.network, base.cves, base.target)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("D", [1, 2, 3])
def test_depth_semantics(family, D):
    for inst in first_reachable(family, 12, 3, cred_levels=D):
        t, lv, net = inst.task, inst.levels, inst.network
        assert lv[inst.target] == D and set(lv.values()) == set(range(D + 1))
        assert set(lv) == {h.id for h in net.hosts[1:]}
        n = len(net.hosts)
        assert t.facts[n:] == [f"cred({k})" for k in range(1, D + 1)]
        cred = {n + k - 1: k for k in range(1, D + 1)}
        for a in t.actions:
            creds_pre = [cred[f] for f in a.pre if f in cred]
            if a.name.startswith("harvest cred"):
                (k,) = [cred[f] for f in a.add]
                assert a.add == (n + k - 1,) and len(a.pre) == 1 and lv[a.pre[0]] == k - 1
            else:
                (h,) = a.add  # exploit or login: adds execCode(h)
                assert creds_pre == ([lv[h]] if lv[h] else [])
        # every level-(k-1) host has a harvest action for cred(k)
        harvests = {(a.pre[0], cred[a.add[0]]) for a in t.actions if a.name.startswith("harvest cred")}
        assert harvests == {(h, lv[h] + 1) for h in lv if lv[h] < D}


def test_depth_infeasible_is_a_knob_failure():
    with pytest.raises(KnobInfeasible):
        make_instance("flat", 0, 3, POOL, cred_levels=3)  # 3 internal hosts, 4 levels


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("rho,m", [(0.5, 1), (0.5, None), (1.0, None), (1.0, 2)])
def test_coupling_semantics(family, rho, m):
    for seed in range(10):
        inst = build(family, seed, 12, coupling=rho, share_pool=m)
        if inst is None:
            continue
        net, t = inst.network, inst.task
        n_reach = len(net.reach)
        exploits = t.actions[:n_reach]  # build_task emits one exploit per reach edge, in order
        holders = set(inst.coupled.values())
        if m is not None:
            assert len(holders) <= m
        for i, r in enumerate(net.reach):
            h = net.services[r.service].host
            if i in inst.coupled:
                k = inst.coupled[i]
                assert r.src != INTERNET and k not in (r.src, h, INTERNET)
                assert exploits[i].pre == (r.src, k) and f"needs@{net.hosts[k].name}" in exploits[i].name
            else:
                assert exploits[i].pre == (r.src,)
        internal_src = sum(r.src != INTERNET for r in net.reach)
        if rho == 1.0:
            assert len(inst.coupled) + inst.coupled_unchanged == internal_src
        if rho == 1.0 and m is None:
            assert inst.coupled_unchanged == 0  # >= 3 internal hosts always leave an eligible holder


def test_share_pool_out_of_range_is_a_knob_failure():
    with pytest.raises(KnobInfeasible):
        make_instance("flat", 0, 6, POOL, coupling=0.5, share_pool=7)  # only 6 internal hosts


KNOBS = [dict(cred_levels=2), dict(coupling=0.5), dict(cred_levels=2, coupling=0.5, share_pool=1),
         dict(cred_levels=3, coupling=1.0), dict(cred_levels=1, pr_gated=True)]
LABEL_CASES = [(f, n, i, k) for f in FAMILIES for i, k in enumerate(KNOBS) for n in (6, 8)]


@cache
def label_instances(family, n, knob_id):
    return first_reachable(family, n, 3 if n == 6 else 2, **KNOBS[knob_id])


@pytest.mark.parametrize("family,n,knob_id,_", LABEL_CASES)
def test_oracle_matches_search_on_every_state(family, n, knob_id, _):
    """Independent oracle = A*+LM-cut = A*+h_max on every reachable state; admissible h <= h*."""
    for inst in label_instances(family, n, knob_id):
        t = inst.task
        for s in reachable_states(t):
            hstar = optimal_cost(t, s)
            assert astar(t, HEURISTICS["lmcut"], start=s).cost == hstar
            assert astar(t, HEURISTICS["hmax"], start=s).cost == hstar
            for name in ADMISSIBLE:
                assert HEURISTICS[name](t, s) <= hstar, (name, s)
