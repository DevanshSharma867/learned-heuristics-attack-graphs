"""Delete-free planning tasks: the formal object every other module works on.

A task has a set of facts (attacker privileges), actions (exploits) with
conjunctive preconditions and add effects, an initial state and a goal.
There are no delete effects: once the attacker holds a privilege it is never
lost (the monotonicity assumption of attack-graph analysis).

A state is a set of facts, stored as an int bitmask: bit i set means fact i
is held. Bitmasks are hashable, cheap to copy, and make "are all
preconditions held?" a single AND.
"""

from dataclasses import dataclass, field
from functools import cached_property

State = int


@dataclass(frozen=True)
class Action:
    name: str
    pre: tuple[int, ...]
    add: tuple[int, ...]
    cost: int
    pre_mask: int = field(init=False, repr=False, compare=False)
    add_mask: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        if self.cost < 0:
            raise ValueError(f"action {self.name} has negative cost {self.cost}")
        if len(set(self.pre)) != len(self.pre) or len(set(self.add)) != len(self.add):
            raise ValueError(f"action {self.name} lists a fact twice")
        object.__setattr__(self, "pre_mask", to_mask(self.pre))
        object.__setattr__(self, "add_mask", to_mask(self.add))

    def applicable(self, state: State) -> bool:
        return self.pre_mask & ~state == 0

    def useful(self, state: State) -> bool:
        """True if applying the action adds at least one new fact."""
        return self.add_mask & ~state != 0


@dataclass
class Task:
    facts: list[str]
    actions: list[Action]
    init: State
    goal: tuple[int, ...]

    @cached_property
    def goal_mask(self) -> int:
        return to_mask(self.goal)

    @cached_property
    def pre_of(self) -> list[list[int]]:
        """pre_of[f] = indices of actions that have fact f as a precondition."""
        out = [[] for _ in self.facts]
        for i, a in enumerate(self.actions):
            for f in a.pre:
                out[f].append(i)
        return out

    @cached_property
    def achievers(self) -> list[list[int]]:
        """achievers[f] = indices of actions that add fact f."""
        out = [[] for _ in self.facts]
        for i, a in enumerate(self.actions):
            for f in a.add:
                out[f].append(i)
        return out

    def is_goal(self, state: State) -> bool:
        return self.goal_mask & ~state == 0

    def successors(self, state: State):
        """Yield (action index, next state) for applicable actions that add something.

        Skipping useless actions is safe only because the task is delete-free:
        such an action would lead back to the same state.
        """
        for i, a in enumerate(self.actions):
            if a.applicable(state) and a.useful(state):
                yield i, state | a.add_mask

    def describe(self, state: State) -> set[str]:
        return {self.facts[f] for f in facts_of(state)}

    @classmethod
    def from_names(cls, facts, init, goal, actions):
        """Build a task from readable names.

        actions: iterable of (name, pre_names, add_names, cost).
        """
        index = {name: i for i, name in enumerate(facts)}
        if len(index) != len(facts):
            raise ValueError("duplicate fact names")
        acts = [
            Action(name, tuple(index[p] for p in pre), tuple(index[e] for e in add), cost)
            for name, pre, add, cost in actions
        ]
        return cls(list(facts), acts, to_mask(index[f] for f in init), tuple(index[g] for g in goal))


def to_mask(facts) -> int:
    mask = 0
    for f in facts:
        mask |= 1 << f
    return mask


def facts_of(state: State) -> list[int]:
    out = []
    i = 0
    while state:
        if state & 1:
            out.append(i)
        state >>= 1
        i += 1
    return out


def plan_cost(task: Task, plan, start: State | None = None) -> int:
    """Check that the plan is executable and reaches the goal; return its cost."""
    state = task.init if start is None else start
    total = 0
    for i in plan:
        a = task.actions[i]
        if not a.applicable(state):
            raise ValueError(f"action {a.name} not applicable")
        state |= a.add_mask
        total += a.cost
    if not task.is_goal(state):
        raise ValueError("plan does not reach the goal")
    return total
