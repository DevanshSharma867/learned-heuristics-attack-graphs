import sys
from datetime import date
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pytest

from ahg import search
from ahg.attack_graph import LOGIN_COST, LOGIN_FAMILIES, UnreachableGoal, build_task, make_instance
from ahg.cost import cost_units
from ahg.cve import CveRecord, load_table
from ahg.heuristics import ADMISSIBLE, HEURISTICS, h0
from ahg.network import INTERNET, Host, Network, Reach, Service, Trust, hop_distances
from ahg.oracle import optimal_cost
from ahg.search import INF, astar, gbfs, uniform_cost, weighted_astar
from ahg.task import plan_cost

from helpers import brute_force_optimal, reachable_states

POOL = load_table(Path(__file__).resolve().parent.parent / "data" / "derived" / "cves.csv")
FAMILIES = ("flat", "tiered", "hub_and_spoke")
# Generated instances the label/heuristic checks run on. Tiered n = 8 is
# included because it is where hmax and LM-cut fall below h* (D12).
CASES = [(f, s, 6) for f in FAMILIES for s in range(8)] + [("tiered", s, 8) for s in range(20)]


@cache
def inst(family, seed, n):
    return make_instance(family, seed, n, POOL)


@cache
def labels(family, seed, n):
    """h* of every reachable state, from the independent oracle."""
    t = inst(family, seed, n).task
    return {s: optimal_cost(t, s) for s in reachable_states(t)}


def rec(cid, e):
    return CveRecord(cid, "x", "v:p", "3.1", e, date(2019, 1, 1))


def tiny_network(trust):
    """internet -> a:http; a -> b:ssh, b:http, c:http."""
    hosts = (Host(0, "internet", "internet"), Host(1, "a", "lan"), Host(2, "b", "lan"), Host(3, "c", "lan"))
    services = (Service(0, 1, "http"), Service(1, 2, "ssh"), Service(2, 2, "http"), Service(3, 3, "http"))
    reach = (Reach(0, 0), Reach(1, 1), Reach(1, 2), Reach(1, 3))
    meta = {"family": "flat", "seed": 0, "params": {}, "schema_version": 1}
    return Network(hosts, services, reach, trust, meta)


# --- generator ------------------------------------------------------------------


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", range(3))
def test_schema_matches_d12(family, seed):
    i = inst(family, seed, 8)
    net, t = i.network, i.task
    assert t.facts[INTERNET] == "attackerLocated(internet)"
    assert t.facts[1:] == [f"execCode({h.name})" for h in net.hosts[1:]]
    assert t.init == 1 << INTERNET and t.goal == (i.target,)
    exploits = [a for a in t.actions if a.name.startswith("exploit")]
    logins = [a for a in t.actions if a.name.startswith("login")]
    assert len(exploits) + len(logins) == len(t.actions)
    # One exploit per reach edge, cost from the assigned CVE (D9).
    assert [(a.pre, a.add, a.cost) for a in exploits] == [
        ((r.src,), (net.services[r.service].host,), cost_units(i.cves[r.service].exploitability_score))
        for r in net.reach
    ]
    # One login per (trust edge, reach edge into a login service on the trusted host).
    expected = sorted(
        (tuple(sorted({tr.src, r.src})), (tr.dst,))
        for tr in net.trust for r in net.reach
        if net.services[r.service].host == tr.dst and net.services[r.service].family in LOGIN_FAMILIES
    )  # fmt: skip
    assert sorted((a.pre, a.add) for a in logins) == expected
    assert all(a.cost == LOGIN_COST for a in logins)
    assert all(38 <= a.cost <= 380 for a in t.actions)


def test_deterministic():
    a, b = make_instance("tiered", 3, 10, POOL).task, make_instance("tiered", 3, 10, POOL).task
    assert (a.facts, a.actions, a.init, a.goal) == (b.facts, b.actions, b.init, b.goal)


@pytest.mark.parametrize("family", FAMILIES)
def test_goal_reachable_by_construction_and_deepest(family):
    for n in (4, 8, 20):
        for seed in range(30):
            i = make_instance(family, seed, n, POOL)  # raises UnreachableGoal otherwise
            dist = hop_distances(i.network)
            assert dist[i.target] == max(dist.values())
            assert optimal_cost(i.task) < INF


def test_unreachable_goal_raises():
    net = tiny_network(())
    net = Network(net.hosts, net.services, (Reach(0, 0),), (), net.meta)  # only a is reachable
    cves = {s.id: rec(f"CVE-0-{s.id}", 1.0) for s in net.services}
    with pytest.raises(UnreachableGoal):
        build_task(net, cves, target=2)


def test_login_is_conjunctive_hand_checked():
    """Credentials for b sit on c; b's ssh is reachable only from a.

    Costs: E = 0.1 everywhere (C = 380), except c's http with E = 3.9 (C = 38).
      exploit a                          380
      exploit c from a                    38
      login b from a with creds from c    38   needs execCode(c) AND execCode(a)
    h* = 380 + 38 + 38 = 456. Without the trust edge the only way to b is
    exploiting b's ssh or http from a: 380 + 380 = 760.
    hmax at the start: max(cost(a), cost(c)) + 38 = 418 + 38 = 456 here too,
    since c's precondition already includes a.
    """
    cves = {0: rec("CVE-0-0", 0.1), 1: rec("CVE-0-1", 0.1), 2: rec("CVE-0-2", 0.1), 3: rec("CVE-0-3", 3.9)}
    t = build_task(tiny_network((Trust(3, 2),)), cves, target=2)
    login = [a for a in t.actions if a.name.startswith("login")]
    assert [(a.pre, a.add, a.cost) for a in login] == [((1, 3), (2,), 38)]
    assert optimal_cost(t) == uniform_cost(t).cost == brute_force_optimal(t) == 456
    assert HEURISTICS["hmax"](t, t.init) == 456
    names = [t.actions[i].name for i in uniform_cost(t).plan]
    assert names[-1].startswith("login ssh@b from a creds@c")
    assert optimal_cost(build_task(tiny_network(()), cves, target=2)) == 760


# --- independent oracle -----------------------------------------------------------


@pytest.mark.parametrize("case", CASES)
def test_oracle_agrees_with_search_on_every_state(case):
    t = inst(*case).task
    for s, hstar in labels(*case).items():
        assert uniform_cost(t, start=s).cost == hstar


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("seed", range(10))
def test_oracle_agrees_with_brute_force_on_small_graphs(family, seed):
    t = make_instance(family, seed, 4, POOL).task
    assert len(t.actions) <= 16, "graph too big for brute force; shrink n"
    assert optimal_cost(t) == uniform_cost(t).cost == brute_force_optimal(t)


# --- heuristics on generated graphs -------------------------------------------------


@pytest.mark.parametrize("case", CASES)
def test_admissibility_and_dominance_on_every_state(case):
    t = inst(*case).task
    for s, hstar in labels(*case).items():
        v = {name: h(t, s) for name, h in HEURISTICS.items()}
        assert v["h0"] <= v["hsp"] <= v["hmax"] <= v["lmcut"] <= hstar < INF
        assert hstar <= v["hff"] <= v["hadd"]


@pytest.mark.parametrize("case", CASES)
def test_astar_admissible_returns_optimal(case):
    t = inst(*case).task
    opt = labels(*case)[t.init]
    for name in sorted(ADMISSIBLE):
        r = astar(t, HEURISTICS[name])
        assert r.cost == opt == plan_cost(t, r.plan), name


def test_generated_checks_are_not_vacuous():
    """Guard: the cases above must include states where hmax and lmcut are below h*."""
    gaps = {"hmax": 0, "lmcut": 0}
    for case in CASES:
        t = inst(*case).task
        for s, hstar in labels(*case).items():
            for name in gaps:
                gaps[name] += HEURISTICS[name](t, s) < hstar
    assert gaps["hmax"] > 0 and gaps["lmcut"] > 0, gaps


def test_every_method_runs_through_the_shared_search(monkeypatch):
    """Identical node counting is structural: every wrapper calls best_first_search (D2)."""
    calls = []
    real = search.best_first_search

    def spy(*args, **kw):
        calls.append(kw)
        return real(*args, **kw)

    monkeypatch.setattr(search, "best_first_search", spy)
    t = inst("tiered", 0, 8).task
    for name, h in HEURISTICS.items():
        astar(t, h)
    uniform_cost(t)
    weighted_astar(t, HEURISTICS["hmax"], 2.0)
    gbfs(t, HEURISTICS["hff"])
    assert len(calls) == len(HEURISTICS) + 3
    # A* with h0 is UCS, node for node.
    a, u = real(t, h0), real(t, lambda task, s: 0)
    assert (a.plan, a.cost, a.expanded, a.generated) == (u.plan, u.cost, u.expanded, u.generated)
