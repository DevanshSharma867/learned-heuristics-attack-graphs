"""Independent uniform-cost search: the oracle labels are checked against (CLAUDE.md rule 6).

It deliberately shares no code with search.py or with Task's bitmask
methods. States are frozensets of fact indices, and applicability is checked
on the actions' pre/add tuples. So a bug in the main search's bookkeeping
(stale entries, reopening, bitmask tests) cannot also be present here and
hide itself in an agreement test.
"""

import heapq
import itertools

from .task import Task

INF = float("inf")


def optimal_cost(task: Task, start: int | None = None, max_pops: int | None = None) -> float | None:
    """Cheapest cost from start (default: the initial state) to the goal, INF if unreachable.

    max_pops: stop after this many heap pops and return None (not checked),
    so a caller can never mistake a budget stop for an answer.
    """
    bits = task.init if start is None else start
    s0 = frozenset(i for i in range(len(task.facts)) if bits >> i & 1)
    goal = frozenset(task.goal)
    acts = [(frozenset(a.pre), frozenset(a.add), a.cost) for a in task.actions]
    best = {s0: 0}
    tie = itertools.count()  # frozensets are not totally ordered, so never compare them
    heap = [(0, next(tie), s0)]
    pops = 0
    while heap:
        if max_pops is not None and pops >= max_pops:
            return None
        pops += 1
        g, _, s = heapq.heappop(heap)
        if g > best[s]:
            continue
        if goal <= s:  # Dijkstra: the first goal state popped is the cheapest
            return g
        for pre, add, cost in acts:
            if pre <= s and not add <= s:
                s2, g2 = s | add, g + cost
                if g2 < best.get(s2, INF):
                    best[s2] = g2
                    heapq.heappush(heap, (g2, next(tie), s2))
    return INF
