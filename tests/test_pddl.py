import re

from ahg.pddl import domain_pddl, problem_pddl
from ahg.task import Task


def toy():
    return Task.from_names(["a", "b", "c", "g"], ["a"], ["g"],
                           [("x", ["a"], ["b"], 3), ("y", ["a"], ["c"], 4), ("z", ["b", "c"], ["g"], 5)])


def test_domain_lists_every_action_with_pre_add_and_cost():
    t = toy()
    d = domain_pddl(t)
    assert d.count("(:action a") == len(t.actions)
    for i, a in enumerate(t.actions):
        block = d.split(f"(:action a{i}\n")[1].split("(:action")[0]
        pre = re.search(r":precondition \(and ([^)]*(?:\)[^)]+)*)\)", block).group(0)
        assert all(f"(f{f})" in pre for f in a.pre)
        assert all(f"(f{f})" in block.split(":effect")[1] for f in a.add)
        assert f"(increase (total-cost) {a.cost})" in block
    assert "(not " not in d  # delete-free


def test_problem_init_is_the_given_state():
    t = toy()
    s = t.init | (1 << 1)
    p = problem_pddl(t, s)
    init = p.split("(:init")[1].split("(= (total-cost)")[0]
    assert sorted(int(i) for i in re.findall(r"\(f(\d+)\)", init)) == [0, 1]
    assert "(:goal (and (f3)))" in p
