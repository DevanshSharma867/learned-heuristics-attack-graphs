"""Digest of a generated Task, for the D15 byte-identity test.

`python tests/golden.py` rewrites tests/data/golden_tasks.json. It was run
once, at the commit before the D15 knobs existed, and must not be rerun to
make test_knobs_off_byte_identical pass: the point of the file is that it
predates the knobs.
"""

import hashlib
import json
import subprocess
from pathlib import Path

from ahg.attack_graph import UnreachableGoal, make_instance
from ahg.cve import load_table

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "data" / "golden_tasks.json"
FAMILIES = ("flat", "tiered", "hub_and_spoke")
CASES = [(f, n, s, g) for f in FAMILIES for n in (6, 8, 12, 20) for s in range(10) for g in (False, True)]


def task_digest(task) -> str:
    """SHA-256 over facts, actions (in order: name, pre, add, cost), init and goal."""
    blob = json.dumps({"facts": task.facts, "actions": [[a.name, a.pre, a.add, a.cost] for a in task.actions],
                       "init": task.init, "goal": task.goal})
    return hashlib.sha256(blob.encode()).hexdigest()


def case_digest(family, n, seed, pr_gated, pool, **knobs) -> str:
    try:
        return task_digest(make_instance(family, seed, n, pool, pr_gated=pr_gated, **knobs).task)
    except UnreachableGoal as e:
        return "UnreachableGoal: " + hashlib.sha256(str(e).encode()).hexdigest()


def key(family, n, seed, pr_gated) -> str:
    return f"{family}:{n}:{seed}:{'pr' if pr_gated else 'base'}"


if __name__ == "__main__":
    pool = load_table(ROOT / "data" / "derived" / "cves.csv")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    digests = {key(*c): case_digest(*c, pool) for c in CASES}
    GOLDEN.write_text(json.dumps({"commit": commit, "digests": digests}, indent=1) + "\n")
    print(f"{len(digests)} digests at {commit}")
