"""Best-first search over the state space of a delete-free task.

One function covers every algorithm in the study, because they differ only in
how a node's priority f is computed from its path cost g and heuristic h:

    uniform-cost search   f = g          (pass h = zero)
    A*                    f = g + h
    weighted A*           f = g + w*h    (w > 1)
    greedy best-first     f = h          (w_g = 0)

Ties on f are broken towards lower h (nodes believed closer to the goal),
then towards the node generated first. Tie-breaking changes node counts a lot
on these tasks, so it is fixed here and documented.
"""

import heapq
import itertools
import time
from dataclasses import dataclass

from .task import State, Task

INF = float("inf")


@dataclass
class SearchResult:
    plan: list[int] | None  # action indices, None if unsolved
    cost: float  # INF if unsolved
    expanded: int  # nodes taken off the open list and expanded
    generated: int  # successor nodes created
    evaluations: int  # heuristic calls
    seconds: float
    budget_hit: bool  # stopped by max_expansions, not by exhausting the space

    @property
    def solved(self) -> bool:
        return self.plan is not None


def best_first_search(task: Task, h, *, w_g=1.0, w_h=1.0, start: State | None = None,
                      max_expansions: int | None = None, trace: list[State] | None = None) -> SearchResult:
    """h(task, state) -> estimated remaining cost (INF means dead end).

    trace: if given, every expanded state is appended to it in expansion
    order, at the point where it is counted, so len(trace) == expanded. A
    reopened state appears once per expansion. Tracing only observes: it
    never changes the order, the counts or the result.
    """
    t0 = time.perf_counter()
    s0 = task.init if start is None else start
    h_cache = {s0: h(task, s0)}
    tie = itertools.count()
    g_best = {s0: 0}
    parent: dict[State, tuple[State, int] | None] = {s0: None}
    closed: dict[State, float] = {}  # state -> g at which it was expanded
    open_list = [(w_h * h_cache[s0], h_cache[s0], next(tie), 0, s0)]
    expanded = generated = 0

    def result(plan, cost, budget_hit=False):
        return SearchResult(plan, cost, expanded, generated, len(h_cache),
                            time.perf_counter() - t0, budget_hit)

    if h_cache[s0] == INF:
        return result(None, INF)

    while open_list:
        _, _, _, g, s = heapq.heappop(open_list)
        if g > g_best[s] or closed.get(s, INF) <= g:
            continue  # stale entry: a cheaper path to s is already known
        # Goal test on expansion, not generation: required for A* optimality.
        if task.is_goal(s):
            return result(_extract_plan(parent, s), g)
        if max_expansions is not None and expanded >= max_expansions:
            return result(None, INF, budget_hit=True)
        closed[s] = g
        expanded += 1
        if trace is not None:
            trace.append(s)
        for ai, s2 in task.successors(s):
            g2 = g + task.actions[ai].cost
            generated += 1
            if g2 >= g_best.get(s2, INF):
                continue
            # A cheaper path to s2. If s2 was already expanded this reopens it,
            # which is needed for optimality when h is admissible but inconsistent.
            g_best[s2] = g2
            parent[s2] = (s, ai)
            if s2 not in h_cache:
                h_cache[s2] = h(task, s2)
            h2 = h_cache[s2]
            if h2 == INF:
                continue
            heapq.heappush(open_list, (w_g * g2 + w_h * h2, h2, next(tie), g2, s2))

    return result(None, INF)


def _extract_plan(parent, s):
    plan = []
    while parent[s] is not None:
        s, ai = parent[s]
        plan.append(ai)
    plan.reverse()
    return plan


def astar(task, h, **kw):
    return best_first_search(task, h, **kw)


def uniform_cost(task, **kw):
    return best_first_search(task, lambda t, s: 0, **kw)


def weighted_astar(task, h, w, **kw):
    return best_first_search(task, h, w_h=w, **kw)


def gbfs(task, h, **kw):
    return best_first_search(task, h, w_g=0.0, **kw)
