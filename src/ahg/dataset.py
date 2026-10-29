"""Read label batches back as (task, state, h*) examples with model inputs (D19 §4).

open_batch rebuilds every instance with make_instance and refuses the batch
if a task digest or the CVE table's SHA-256 differs from the manifest, so a
label can never be paired with a different graph than the one it was
computed on. Reading a test split goes through the test-access log
(D17 §4, D19 §1).

Model inputs (CLAUDE.md §2):
  - GNN: static_graph() once per instance (edges and action features), plus
    fact_features() per state (held, is_goal).
  - MLP: mlp_features(), the graph-level hand-built features.
  - WL baseline: wl_colours(), a colour histogram from Weisfeiler-Leman
    refinement on the fact-action graph (WL-GOOSE style). Colours become a
    vector only through a WLVocab fitted on train batches (D14 §5).
"""

import gzip
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import torch

from .attack_graph import Instance, make_instance
from .cost import SCALE
from .cve import load_table
from .heuristics import hsp
from .labels import CVES, FAILURES_FILE, LABELS_FILE, MANIFEST
from .splits import SPLITS, cve_pool, record_test_access
from .task import Task, task_digest

COST_SCALE = 10 * SCALE  # the largest action cost (D9), so normalised costs lie in [0.1, 1]
ACTION_KINDS = ("exploit", "login", "harvest")
PR = ("N", "L", "H")
ACTION_DIM = 1 + len(ACTION_KINDS) + len(PR)  # cost, kind one-hot, CVSS privileges-required one-hot
WL_ITERATIONS = 2


@dataclass
class Example:
    instance: int  # index into LabelBatch.instances
    state: int
    hstar: int
    sources: list[str]


@dataclass
class LabelBatch:
    manifest: dict
    instances: list[Instance | None]  # None where generation failed (no labels refer to it)
    examples: list[Example]
    failures: list[dict]

    def task(self, ex: Example) -> Task:
        return self.instances[ex.instance].task

    def __iter__(self):
        """(task, state, h*) triples, in file order."""
        return ((self.task(ex), ex.state, ex.hstar) for ex in self.examples)


def _read_lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]


def open_batch(path: str | Path, purpose: str | None = None, permitted_by: str | None = None,
               log: Path | None = None) -> LabelBatch:
    """Load one batch. Test splits need a purpose and are logged before anything is read."""
    path = Path(path)
    manifest = json.loads((path / MANIFEST).read_text())
    split = manifest["split"]
    if SPLITS[split].is_test:
        record_test_access(manifest["batch_id"], split, purpose, manifest["provenance"]["git_commit"],
                           permitted_by, log)
    labels_gz, failures_gz = (path / LABELS_FILE).read_bytes(), (path / FAILURES_FILE).read_bytes()
    if hashlib.sha256(labels_gz + failures_gz).hexdigest() != manifest["content_sha256"]:
        raise ValueError(f"{path}: label files do not match the manifest's content hash")
    if hashlib.sha256(CVES.read_bytes()).hexdigest() != manifest["cves_csv_sha256"]:
        raise ValueError(f"{path}: data/derived/cves.csv differs from the one the batch was labelled with")
    pool = cve_pool(load_table(CVES), manifest["cve_pool"])
    instances = []
    for rec in manifest["instances"]:
        spec = rec["spec"]
        if rec["task_digest"] is None:
            instances.append(None)
            continue
        inst = make_instance(spec["family"], spec["seed"], spec["n"], pool, cred_levels=spec["D"],
                             coupling=spec["rho"], share_pool=spec["m"], exposed_level0=spec["exposed_level0"],
                             **spec["params"])
        if task_digest(inst.task) != rec["task_digest"]:
            raise ValueError(f"{path}: rebuilt task for seed {spec['seed']} differs from the labelled one")
        instances.append(inst)
    examples = [Example(r["i"], int(r["s"], 16), r["h"], r["src"]) for r in _read_lines(path / LABELS_FILE)]
    return LabelBatch(manifest, instances, examples, _read_lines(path / FAILURES_FILE))


def _action_kind(name: str) -> str:
    return name.split()[0]


def action_features(inst: Instance) -> list[list[float]]:
    """Per action: normalised cost, kind one-hot, CVSS privileges-required one-hot (zeros if no CVE)."""
    by_id = {c.cve_id: c for c in inst.cves.values()}
    out = []
    for a in inst.task.actions:
        kind = _action_kind(a.name)
        row = [a.cost / COST_SCALE] + [float(kind == k) for k in ACTION_KINDS]
        pr = by_id[a.name.split()[1]].privileges_required if kind == "exploit" else None
        out.append(row + [float(pr == p) for p in PR])
    return out


def static_graph(inst: Instance, device="cpu") -> dict[str, torch.Tensor]:
    """The state-independent GNN input: precondition and add edges, degrees, action features, goal facts."""
    task = inst.task
    pre = [(f, i) for i, a in enumerate(task.actions) for f in a.pre]
    add = [(i, f) for i, a in enumerate(task.actions) for f in a.add]
    t = lambda xs, dt=torch.long: torch.tensor(xs, dtype=dt, device=device)
    deg_pre = Counter(i for _, i in pre)
    deg_add = Counter(f for _, f in add)
    return {"pre_src": t([f for f, _ in pre]), "pre_dst": t([i for _, i in pre]),
            "add_src": t([i for i, _ in add]), "add_dst": t([f for _, f in add]),
            "inv_deg_pre": t([[1 / max(1, deg_pre[i])] for i in range(len(task.actions))], torch.float32),
            "inv_deg_add": t([[1 / max(1, deg_add[f])] for f in range(len(task.facts))], torch.float32),
            "act_x": t(action_features(inst), torch.float32), "goal": t(list(task.goal))}


def fact_features(task: Task, state: int) -> torch.Tensor:
    """[facts, 2]: held in the state, is a goal fact."""
    return torch.tensor([[float(state >> f & 1), float(f in task.goal)] for f in range(len(task.facts))])


def mlp_features(task: Task, state: int) -> list[float]:
    """CLAUDE.md §2 graph-level features: #facts, #actions, #held, h_sp(s), and the number, mean
    and min cost of applicable useful actions (costs in effort units)."""
    costs = [task.actions[ai].cost / SCALE for ai, _ in task.successors(state)]
    return [len(task.facts), len(task.actions), bin(state).count("1"), hsp(task, state) / SCALE,
            len(costs), sum(costs) / len(costs) if costs else 0.0, min(costs, default=0.0)]


def wl_colours(task: Task, state: int, iterations: int = WL_ITERATIONS) -> Counter:
    """Histogram of WL colours over all refinement rounds, on the fact-action graph.

    Initial colours: a fact is (held, goal); an action is (kind, cost). Each round
    a node's colour becomes a hash of its colour and the sorted colours of its
    neighbours, by edge type (precondition in, add out). Colours are short
    SHA-256 prefixes, so they are the same in every process.
    """
    h = lambda x: hashlib.sha256(repr(x).encode()).hexdigest()[:16]
    fc = [h(("f", state >> f & 1, f in task.goal)) for f in range(len(task.facts))]
    ac = [h(("a", _action_kind(a.name), a.cost)) for a in task.actions]
    hist = Counter(fc) + Counter(ac)
    adders = task.achievers
    for _ in range(iterations):
        ac2 = [h((ac[i], sorted(fc[f] for f in a.pre))) for i, a in enumerate(task.actions)]
        fc = [h((fc[f], sorted(ac[i] for i in adders[f]))) for f in range(len(task.facts))]
        ac = ac2
        hist += Counter(fc) + Counter(ac)
    return hist


class WLVocab:
    """Colour -> column, fitted on train batches only; unseen colours are dropped (as in WL-GOOSE)."""

    def __init__(self):
        self.index: dict[str, int] = {}

    def fit(self, histograms) -> "WLVocab":
        for hist in histograms:
            for c in sorted(hist):
                self.index.setdefault(c, len(self.index))
        return self

    def transform(self, hist: Counter) -> list[float]:
        v = [0.0] * len(self.index)
        for c, k in hist.items():
            if c in self.index:
                v[self.index[c]] = float(k)
        return v
