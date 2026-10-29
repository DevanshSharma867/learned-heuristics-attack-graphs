"""Digest of a generated Task, for the D15 byte-identity test.

`python tests/golden.py` rewrites tests/data/golden_tasks.json. It was run
once, at the commit before the D15 knobs existed, and must not be rerun to
make test_knobs_off_byte_identical pass: the point of the file is that it
predates the knobs.

`python tests/golden.py d15` rewrites tests/data/golden_d15_tasks.json:
digests of D15-mode knob instances (D16 off), taken once at the commit
before D16 was implemented, whose attack_graph.py is the D15 pilot's.
"""

import hashlib
import json
import subprocess
from pathlib import Path

from ahg.attack_graph import UnreachableGoal, make_instance
from ahg.cve import load_table
from ahg.task import task_digest

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "data" / "golden_tasks.json"
FAMILIES = ("flat", "tiered", "hub_and_spoke")
CASES = [(f, n, s, g) for f in FAMILIES for n in (6, 8, 12, 20) for s in range(10) for g in (False, True)]


def case_digest(family, n, seed, pr_gated, pool, **knobs) -> str:
    try:
        return task_digest(make_instance(family, seed, n, pool, pr_gated=pr_gated, **knobs).task)
    except UnreachableGoal as e:
        return "UnreachableGoal: " + hashlib.sha256(str(e).encode()).hexdigest()


GOLDEN_D15 = ROOT / "tests" / "data" / "golden_d15_tasks.json"
# (variant, family, topology params, n, D, rho, m) - a few D15 pilot cells, seeds 0-4 each.
D15_CELLS = [("flat", "flat", {}, 12, 2, 0.5, None), ("tiered3", "tiered", {}, 20, 3, 1.0, 1),
             ("hub_and_spoke", "hub_and_spoke", {}, 8, 1, 0.25, 1), ("tiered5", "tiered", {"n_tiers": 5}, 12, 3, 0.0, None),
             ("flat", "flat", {}, 20, 1, 0.0, None), ("hub_and_spoke", "hub_and_spoke", {}, 20, 2, 0.5, None)]
D15_SEEDS = range(5)


def d15_key(variant, n, D, rho, m, seed) -> str:
    return f"{variant}:{n}:D{D}:rho{rho}:m{'all' if m is None else m}:{seed}"


def d15_digest(family, params, n, D, rho, m, seed, pool, **extra) -> str:
    try:
        inst = make_instance(family, seed, n, pool, cred_levels=D, coupling=rho, share_pool=m, **params, **extra)
        return task_digest(inst.task)
    except UnreachableGoal as e:
        return "UnreachableGoal: " + hashlib.sha256(str(e).encode()).hexdigest()


def key(family, n, seed, pr_gated) -> str:
    return f"{family}:{n}:{seed}:{'pr' if pr_gated else 'base'}"


if __name__ == "__main__":
    import sys
    pool = load_table(ROOT / "data" / "derived" / "cves.csv")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if sys.argv[1:] == ["d15"]:
        digests = {d15_key(v, n, D, rho, m, s): d15_digest(f, p, n, D, rho, m, s, pool)
                   for v, f, p, n, D, rho, m in D15_CELLS for s in D15_SEEDS}
        out = GOLDEN_D15
    else:
        digests = {key(*c): case_digest(*c, pool) for c in CASES}
        out = GOLDEN
    out.write_text(json.dumps({"commit": commit, "digests": digests}, indent=1) + "\n")
    print(f"{len(digests)} digests at {commit}")
