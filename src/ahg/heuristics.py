"""Classical heuristics derived from the delete relaxation.

All take (task, state) and return an estimate of the cheapest cost from
state to the goal, or INF if the goal is unreachable.

    h0     always 0                                  admissible, uninformed
    hsp    AND treated as OR (plain shortest path)    admissible, weak
    hmax   cost of the most expensive precondition    admissible
    hadd   sum of precondition costs                  inadmissible
    hff    cost of one relaxed plan                   inadmissible
    lmcut  sum of disjoint action landmarks           admissible

Our tasks are already delete-free, so the "relaxed" problem is the real
problem: h+ (optimal relaxed cost) equals h* (true optimal cost). Every
heuristic here is a cheap approximation of that NP-hard quantity.
"""

import heapq

from .task import Task, facts_of

INF = float("inf")


def h0(task: Task, state: int) -> float:
    return 0


def relaxed_costs(task: Task, state: int, mode: str, costs=None, stop_at_goal=True):
    """Generalised Dijkstra over facts.

    Returns (fact_cost, supporter): fact_cost[f] is the estimated cost of
    reaching fact f from state, supporter[f] the action achieving that cost.
    mode decides an action's cost from its preconditions' costs:
        "max": max over preconditions      (hmax)
        "add": sum over preconditions      (hadd)
        "min": cheapest precondition only  (hsp: ignore the AND)
    costs overrides action costs (LM-cut changes them between rounds).
    stop_at_goal stops once every goal fact is final; other facts may then
    hold unfinished values. LM-cut needs every fact final, so it passes False.
    """
    actions = task.actions
    if costs is None:
        costs = [a.cost for a in actions]
    n = len(task.facts)
    fact_cost = [INF] * n
    supporter = [None] * n
    done = [False] * n
    # Number of preconditions still unreached before the action can fire.
    need = [min(1, len(a.pre)) if mode == "min" else len(a.pre) for a in actions]
    acc = [0] * len(actions)
    heap = []

    def fire(ai):
        c = costs[ai] + acc[ai]
        for e in actions[ai].add:
            if c < fact_cost[e]:
                fact_cost[e] = c
                supporter[e] = ai
                heapq.heappush(heap, (c, e))

    for f in facts_of(state):
        fact_cost[f] = 0
        heapq.heappush(heap, (0, f))
    for ai, k in enumerate(need):
        if k == 0:
            fire(ai)

    is_goal = set(task.goal)
    goals_left = len(is_goal) if stop_at_goal else -1
    while heap and goals_left != 0:
        c, f = heapq.heappop(heap)
        if done[f] or c > fact_cost[f]:
            continue
        done[f] = True
        if f in is_goal:
            goals_left -= 1
        for ai in task.pre_of[f]:
            if need[ai] == 0:
                continue  # "min" mode: already fired from an earlier precondition
            # Facts are popped in non-decreasing cost order, so for "min" the
            # first precondition seen is the cheapest.
            acc[ai] = c if mode == "min" else (max(acc[ai], c) if mode == "max" else acc[ai] + c)
            need[ai] -= 1
            if need[ai] == 0:
                fire(ai)
    return fact_cost, supporter


def _goal_value(task, fact_cost, combine):
    vals = [fact_cost[g] for g in task.goal]
    return combine(vals) if vals else 0


def hmax(task: Task, state: int) -> float:
    return _goal_value(task, relaxed_costs(task, state, "max")[0], max)


def hadd(task: Task, state: int) -> float:
    return _goal_value(task, relaxed_costs(task, state, "add")[0], sum)


def hsp(task: Task, state: int) -> float:
    return _goal_value(task, relaxed_costs(task, state, "min")[0], max)


def hff(task: Task, state: int) -> float:
    """Extract a relaxed plan backwards from the goal using hadd's best supporters."""
    fact_cost, supporter = relaxed_costs(task, state, "add")
    if any(fact_cost[g] == INF for g in task.goal):
        return INF
    plan = set()
    seen = set()
    stack = [g for g in task.goal]
    while stack:
        f = stack.pop()
        if f in seen or (state >> f) & 1:
            continue
        seen.add(f)
        ai = supporter[f]
        if ai not in plan:
            plan.add(ai)
            stack.extend(task.actions[ai].pre)
    return sum(task.actions[ai].cost for ai in plan)


def lmcut(task: Task, state: int) -> float:
    """LM-cut (Helmert & Domshlak 2009).

    Repeat until the goal has hmax 0 under the reduced costs:
      1. Compute hmax with the current costs.
      2. Each action points from its costliest precondition (its "precondition
         choice") to each of its add effects: the justification graph.
      3. The goal zone is every fact that reaches the goal along zero-cost edges.
      4. The cut is every action leading from the part reachable from the state
         (without entering the goal zone) into the goal zone. Every plan uses at
         least one cut action, so the cut is a disjunctive action landmark.
      5. Add the cheapest cut cost m to h and subtract m from every cut action.
    Each landmark pays for itself with cost that no other landmark reuses, so
    the sum never exceeds h*.
    """
    actions = task.actions
    costs = [a.cost for a in actions]
    h = 0
    while True:
        fact_cost, _ = relaxed_costs(task, state, "max", costs, stop_at_goal=False)
        goal_cost = max((fact_cost[g] for g in task.goal), default=0)
        if goal_cost == INF:
            return INF
        if goal_cost == 0:
            return h

        # Precondition choice; None means no preconditions (fires from the state).
        pcf = [None] * len(actions)
        reachable = [False] * len(actions)
        for ai, a in enumerate(actions):
            if all(fact_cost[p] < INF for p in a.pre):
                reachable[ai] = True
                if a.pre:
                    pcf[ai] = max(a.pre, key=lambda p: fact_cost[p])

        # Goal zone, grown backwards from the costliest goal fact.
        top_goal = max(task.goal, key=lambda g: fact_cost[g])
        zone = {top_goal}
        stack = [top_goal]
        while stack:
            f = stack.pop()
            for ai in task.achievers[f]:
                p = pcf[ai]
                if reachable[ai] and costs[ai] == 0 and p is not None and p not in zone:
                    zone.add(p)
                    stack.append(p)

        # Forward from the state without entering the goal zone.
        n0 = set(facts_of(state))
        stack = list(n0)
        frontier_actions = [ai for ai in range(len(actions)) if reachable[ai] and pcf[ai] is None]
        cut = []

        def visit(ai):
            if any(e in zone for e in actions[ai].add):
                cut.append(ai)
            for e in actions[ai].add:
                if e not in zone and e not in n0:
                    n0.add(e)
                    stack.append(e)

        for ai in frontier_actions:
            visit(ai)
        pcf_index = {}
        for ai, p in enumerate(pcf):
            if p is not None and reachable[ai]:
                pcf_index.setdefault(p, []).append(ai)
        while stack:
            f = stack.pop()
            for ai in pcf_index.get(f, ()):
                visit(ai)

        cut = list(set(cut))
        assert cut, "LM-cut found no cut although goal cost > 0"
        m = min(costs[ai] for ai in cut)
        assert m > 0, "cut action with zero cost: goal zone construction is wrong"
        h += m
        for ai in cut:
            costs[ai] -= m


HEURISTICS = {"h0": h0, "hsp": hsp, "hmax": hmax, "hadd": hadd, "hff": hff, "lmcut": lmcut}
ADMISSIBLE = {"h0", "hsp", "hmax", "lmcut"}
