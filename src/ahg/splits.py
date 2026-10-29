"""Topology-level splits, CVE pools and the test-access log (D17 §3, D19 §1).

A split is a range of topology seeds plus the instance distribution its
seeds are drawn into. One seed gives exactly one instance, and the seed fixes
the instance's knob cell, so a state's split is decided before any state
exists (CLAUDE.md rule 1). Test splits change exactly one factor against
`train` (CLAUDE.md §3).
"""

import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .cve import CveRecord

ROOT = Path(__file__).resolve().parents[2]
TEST_ACCESS_LOG = ROOT / "results" / "test_access_log.jsonl"

# (family, variant, generator params), as in the D15 sweep (scripts/measure_depth_coupling.py).
VARIANTS = {"flat": ("flat", {}), "tiered3": ("tiered", {}), "tiered5": ("tiered", {"n_tiers": 5}),
            "hub_and_spoke": ("hub_and_spoke", {})}
COUPLINGS = [(0.0, None), (0.25, 1), (0.25, None), (0.5, 1), (0.5, None), (1.0, 1), (1.0, None)]  # D15 §1(c)
TRAIN_VARIANTS = ("flat", "tiered3", "tiered5")
HELDOUT_MOD, HELDOUT_BELOW = 10, 3  # CVEs with hash mod 10 < 3 (about 30%) are held out
COSTLY_MAX_E = 2.8  # heldout_costly: exploitability at most this (D19 §1)


@dataclass(frozen=True)
class Split:
    name: str
    seeds: range
    variants: tuple[str, ...]
    sizes: tuple[int, ...]
    levels: tuple[int, ...] = (2, 3)
    pool: str = "train"

    @property
    def is_test(self) -> bool:
        return self.name.startswith("test")

    def cells(self) -> list[dict]:
        """Every knob cell of the split, in a fixed order."""
        return [{"variant": v, "n": n, "D": D, "rho": rho, "m": m}
                for v in self.variants for n in self.sizes for D in self.levels for rho, m in COUPLINGS]

    def instance_spec(self, seed: int) -> dict:
        """The instance a seed stands for: cells round-robin over the seed range, so no rng is needed."""
        if seed not in self.seeds:
            raise ValueError(f"seed {seed} is not in split {self.name}")
        cells = self.cells()
        cell = cells[(seed - self.seeds.start) % len(cells)]
        family, params = VARIANTS[cell["variant"]]
        return {"split": self.name, "seed": seed, "family": family, "params": params, **cell,
                "exposed_level0": True, "pool": self.pool}


SPLITS = {s.name: s for s in [
    Split("train", range(1000, 1600), TRAIN_VARIANTS, (12, 20)),
    Split("val", range(1600, 1700), TRAIN_VARIANTS, (12, 20)),
    Split("test_id", range(1700, 1800), TRAIN_VARIANTS, (12, 20)),
    Split("test_size", range(1800, 1900), TRAIN_VARIANTS, (30,)),
    Split("test_structure", range(1900, 2000), ("hub_and_spoke",), (12, 20)),
    Split("test_vuln", range(2000, 2100), TRAIN_VARIANTS, (12, 20), pool="heldout"),
    Split("test_vuln_cost", range(2100, 2200), TRAIN_VARIANTS, (12, 20), pool="heldout_costly"),
]}
# Seeds already used for measurement and decisions (D15 sweeps, D17 replication); never in a split.
RESERVED_SEEDS = (range(0, 20), range(100, 120))


def is_heldout(cve_id: str) -> bool:
    return int(hashlib.sha256(f"cvepool:{cve_id}".encode()).hexdigest(), 16) % HELDOUT_MOD < HELDOUT_BELOW


def cve_pool(pool: list[CveRecord], name: str) -> list[CveRecord]:
    """The named subset of the CVE table: train, heldout or heldout_costly (D19 §1)."""
    if name == "train":
        return [r for r in pool if not is_heldout(r.cve_id)]
    if name == "heldout":
        return [r for r in pool if is_heldout(r.cve_id)]
    if name == "heldout_costly":
        return [r for r in pool if is_heldout(r.cve_id) and r.exploitability_score <= COSTLY_MAX_E]
    raise ValueError(f"unknown CVE pool {name!r}")


def record_test_access(batch_id: str, split: str, purpose: str, commit: str,
                       permitted_by: str | None = None, log: Path | None = None) -> None:
    """Append one read of a test split to the log, or refuse it (D17 §4, D19 §1).

    purpose: why the split is read; "evaluation" is the once-only final test.
    A second evaluation read of the same split needs permitted_by, the
    D-entry that allows it.
    """
    log = log or TEST_ACCESS_LOG
    if not purpose:
        raise PermissionError(f"reading test split {split} needs a stated purpose")
    past = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
    if purpose == "evaluation" and permitted_by is None and any(
            e["split"] == split and e["purpose"] == "evaluation" for e in past):
        raise PermissionError(f"test split {split} was already read for evaluation; "
                              "a second read needs permitted_by=<D-entry>")
    entry = {"date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "batch_id": batch_id,
             "split": split, "purpose": purpose, "permitted_by": permitted_by, "git_commit": commit,
             "argv": sys.argv}
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(json.dumps(entry) + "\n")
