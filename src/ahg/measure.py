"""Measurement helpers shared by the landscape scripts (measure_landscape.py, measure_depth_coupling.py).

h* of a state is computed by A*+LM-cut and cross-checked against A*+h_max.
Both are admissible, so the two optimal costs must be equal; a mismatch, or
an admissible heuristic above h*, raises HardFailure, and the calling script
aborts before writing anything. enumerate_exact gives a third, independent
h* by backward induction where the reachable space is small enough.
"""

from .heuristics import hmax, lmcut
from .search import INF, astar


class HardFailure(Exception):
    pass


def exact_cost(task, start, budget, traces=None):
    """h*(start) by A*+LM-cut, cross-checked by A*+h_max. None if a search hit the budget.

    traces: optional (lmcut_list, hmax_list) receiving each search's expanded states.
    """
    t_lm, t_hm = traces if traces is not None else (None, None)
    r_lm = astar(task, lmcut, start=start, max_expansions=budget, trace=t_lm)
    r_hm = astar(task, hmax, start=start, max_expansions=budget, trace=t_hm)
    if r_lm.budget_hit or r_hm.budget_hit:
        # Not silently dropped: the caller counts it as "h* unknown".
        return None, r_lm, r_hm
    if r_lm.cost != r_hm.cost:
        raise HardFailure(f"A*+LM-cut {r_lm.cost} != A*+h_max {r_hm.cost} from state {start:#x}")
    if r_lm.cost == INF:
        # Delete-free with a reachable goal: every reachable state reaches it (D14 §1).
        raise HardFailure(f"reachable state {start:#x} cannot reach the goal")
    return r_lm.cost, r_lm, r_hm


def check_admissible(task, s, hstar):
    vals = (hmax(task, s), lmcut(task, s))
    for name, v in zip(("h_max", "LM-cut"), vals):
        if v > hstar:
            raise HardFailure(f"{name}={v} > h*={hstar} at state {s:#x}")
    return vals


def sample_states(task, rng, cap, walks_per_sample):
    """Distinct reachable non-goal states from random-depth walks (D14 §2 off-optimal rollouts).

    Each walk applies uniformly chosen applicable, useful actions from the
    initial state for a uniformly drawn number of steps in [1, max depth],
    where max depth = facts not held initially (each useful action adds at
    least one fact). The walk stops early at a goal or dead end; goal states
    are skipped. Returns (states, cap_bound): cap_bound is True if cap was
    reached, False if the walk budget (cap * walks_per_sample walks) ran out
    first (few distinct states).
    """
    max_depth = len(task.facts) - bin(task.init).count("1")
    seen = set()
    for _ in range(cap * walks_per_sample):
        s = task.init
        for _ in range(rng.randint(1, max_depth)):
            succ = [s2 for _, s2 in task.successors(s)]
            if not succ or task.is_goal(s):
                break
            s = rng.choice(succ)
        if s != task.init and not task.is_goal(s):
            seen.add(s)
            if len(seen) == cap:
                return sorted(seen), True
    return sorted(seen), False


def enumerate_exact(task, cap):
    """h* of every reachable state by backward induction; None if more than cap states.

    Independent of A*: states of a delete-free task form a DAG (every useful
    action strictly grows the state), so processing states from most facts to
    fewest gives h*(s) = min over successors s' of c(a) + h*(s').
    """
    seen, stack = {task.init}, [task.init]
    while stack:
        for _, s2 in task.successors(stack.pop()):
            if s2 not in seen:
                if len(seen) >= cap:
                    return None
                seen.add(s2)
                stack.append(s2)
    hstar = {}
    for s in sorted(seen, key=lambda s: -bin(s).count("1")):
        if task.is_goal(s):
            hstar[s] = 0
            continue
        hstar[s] = min((task.actions[ai].cost + hstar[s2] for ai, s2 in task.successors(s)), default=INF)
    return hstar


def gap_stats(triples):
    """triples: (h*, h_max, LM-cut). Per heuristic: count with h < h*, sum and max of h* - h."""
    out = {"n": len(triples)}
    for i, name in ((1, "hmax"), (2, "lmcut")):
        gaps = [t[0] - t[i] for t in triples]
        out[name] = {"lt": sum(g > 0 for g in gaps), "gap_sum": sum(gaps), "gap_max": max(gaps, default=0)}
    return out
