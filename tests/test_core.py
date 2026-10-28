import pytest

from ahg.examples import toy_network
from ahg.heuristics import ADMISSIBLE, HEURISTICS, hadd, hff, hmax, hsp, lmcut
from ahg.search import INF, astar, gbfs, uniform_cost, weighted_astar
from ahg.task import plan_cost

from helpers import brute_force_optimal, random_task, reachable_states

SEEDS = range(60)


def test_toy_heuristic_values():
    t = toy_network()
    assert hsp(t, t.init) == 90
    assert hmax(t, t.init) == 100
    assert hadd(t, t.init) == 180  # counts exploit_web_rce twice
    assert hff(t, t.init) == 150
    assert hmax(t, t.init) <= lmcut(t, t.init) <= 150


def test_toy_optimal_plan():
    t = toy_network()
    r = uniform_cost(t)
    assert r.cost == 150 == brute_force_optimal(t)
    assert plan_cost(t, r.plan) == 150
    names = [t.actions[i].name for i in r.plan]
    assert "login_db_with_cred" in names


@pytest.mark.parametrize("seed", SEEDS)
def test_search_matches_brute_force(seed):
    t = random_task(seed)
    opt = brute_force_optimal(t)
    assert uniform_cost(t).cost == opt
    for name in ADMISSIBLE:
        r = astar(t, HEURISTICS[name])
        assert r.cost == opt, name
        if r.solved:
            assert plan_cost(t, r.plan) == opt
    for name in ("hadd", "hff"):
        r = gbfs(t, HEURISTICS[name])
        assert r.solved == (opt < INF)
        if r.solved:
            assert plan_cost(t, r.plan) == r.cost >= opt


@pytest.mark.parametrize("seed", SEEDS)
def test_admissibility_and_dominance_on_every_state(seed):
    """hsp <= hmax <= lmcut <= h* in every reachable state."""
    t = random_task(seed)
    for s in reachable_states(t):
        hstar = brute_force_optimal(t, start=s)
        vals = {name: HEURISTICS[name](t, s) for name in HEURISTICS}
        assert vals["hsp"] <= vals["hmax"] <= vals["lmcut"] <= hstar
        if hstar == INF:
            assert vals["hmax"] == INF
        else:
            # Delete-free: hff's relaxed plan is a real plan, so it cannot beat h*.
            assert hstar <= vals["hff"] <= vals["hadd"] < INF


def test_random_tasks_are_not_trivial():
    """Guard: if the generator becomes too easy the tests above prove little."""
    hard = 0
    for seed in SEEDS:
        t = random_task(seed)
        opt = brute_force_optimal(t)
        hard += opt < INF and hmax(t, t.init) < opt
    assert hard >= 15


def test_weighted_astar_bound_with_admissible_h():
    """With admissible h, weighted A* cost <= w * optimal."""
    for seed in SEEDS:
        t = random_task(seed)
        opt = uniform_cost(t).cost
        if opt == INF:
            continue
        assert weighted_astar(t, hmax, 2.0).cost <= 2 * opt


def test_budget():
    t = toy_network()
    r = uniform_cost(t, max_expansions=1)
    assert r.budget_hit and not r.solved


@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("name", sorted(HEURISTICS))
@pytest.mark.parametrize("algo", ["astar", "wastar", "gbfs"])
def test_trace_does_not_change_search(seed, name, algo):
    """trace= only observes: plan, cost and every count are identical with and without it."""
    t = random_task(seed)
    h = HEURISTICS[name]
    run = {"astar": lambda **kw: astar(t, h, **kw), "wastar": lambda **kw: weighted_astar(t, h, 2.0, **kw),
           "gbfs": lambda **kw: gbfs(t, h, **kw)}[algo]
    for budget in (None, 3):
        plain = run(max_expansions=budget)
        trace = []
        traced = run(max_expansions=budget, trace=trace)
        fields = ("plan", "cost", "expanded", "generated", "evaluations", "budget_hit")
        assert [getattr(plain, f) for f in fields] == [getattr(traced, f) for f in fields]
        assert len(trace) == traced.expanded
        assert not trace or trace[0] == t.init
        assert not any(t.is_goal(s) for s in trace)  # D6: the goal is never counted as expanded
