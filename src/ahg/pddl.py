"""Export a Task to grounded PDDL, for external planners such as Fast Downward (CLAUDE.md §5).

The export is grounded: each fact becomes a 0-ary predicate (f<i>), each action
a parameterless action (a<i>) with its conjunctive preconditions, add effects
and its integer D9 cost as an (increase (total-cost) c) effect. There are no
delete effects, exactly as in the Task. Names are indices, so the mapping back
to the Task is the identity; the readable names go in comments.
"""

from ahg.task import State, Task, facts_of


def _conj(atoms):
    return "(and " + " ".join(f"(f{i})" for i in atoms) + ")"


def domain_pddl(task: Task, name: str = "attackgraph") -> str:
    lines = [f"(define (domain {name})", "  (:requirements :strips :action-costs)",
             "  (:predicates " + " ".join(f"(f{i})" for i in range(len(task.facts))) + ")",
             "  (:functions (total-cost))"]
    for i, a in enumerate(task.actions):
        lines += [f"  ; {a.name}", f"  (:action a{i}", "   :parameters ()",
                  f"   :precondition {_conj(a.pre)}",
                  f"   :effect (and {' '.join(f'(f{j})' for j in a.add)} (increase (total-cost) {a.cost})))"]
    return "\n".join(lines + [")"]) + "\n"


def problem_pddl(task: Task, state: State | None = None, name: str = "p", domain: str = "attackgraph") -> str:
    """The problem from `state` (default: the task's initial state) to the task's goal."""
    s = task.init if state is None else state
    init = " ".join(f"(f{i})" for i in facts_of(s))
    return (f"(define (problem {name}) (:domain {domain})\n  (:init {init} (= (total-cost) 0))\n"
            f"  (:goal {_conj(task.goal)})\n  (:metric minimize (total-cost)))\n")
