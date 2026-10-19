import itertools
import random

from ahg.task import Task


def random_task(seed, n_facts=9, n_actions=13, max_pre=2, max_add=2, goal_size=2) -> Task:
    """Small random delete-free task; may be unsolvable.

    Defaults chosen so hmax is usually below h*, so the tests exercise the
    cases where heuristics disagree.
    """
    rng = random.Random(seed)
    facts = [f"f{i}" for i in range(n_facts)]
    init = rng.sample(facts, rng.randint(1, 2))
    goal = rng.sample([f for f in facts if f not in init], goal_size)
    actions = []
    for i in range(n_actions):
        pre = rng.sample(facts, rng.randint(0, max_pre))
        add = rng.sample(facts, rng.randint(1, max_add))
        actions.append((f"a{i}", pre, add, rng.randint(1, 20)))
    return Task.from_names(facts, init, goal, actions)


def brute_force_optimal(task: Task, start=None) -> float:
    """Optimal cost by trying every subset of actions.

    In a delete-free task order only matters for applicability, so a subset S
    is a valid plan iff repeatedly applying applicable actions of S from the
    start reaches the goal. Independent of all search code.
    """
    s0 = task.init if start is None else start
    best = float("inf")
    n = len(task.actions)
    for r in range(n + 1):
        for subset in itertools.combinations(range(n), r):
            cost = sum(task.actions[i].cost for i in subset)
            if cost >= best:
                continue
            state, changed = s0, True
            while changed:
                changed = False
                for i in subset:
                    a = task.actions[i]
                    if a.applicable(state) and a.useful(state):
                        state |= a.add_mask
                        changed = True
            if task.is_goal(state):
                best = cost
    return best


def reachable_states(task: Task):
    seen = {task.init}
    stack = [task.init]
    while stack:
        s = stack.pop()
        for _, s2 in task.successors(s):
            if s2 not in seen:
                seen.add(s2)
                stack.append(s2)
    return seen
