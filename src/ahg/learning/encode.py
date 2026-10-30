"""Turn label batches into model inputs once, and cache them (D21 §1).

Targets are h* in effort units (D9 units / 38), a fixed constant rather than
a fitted scale (D14 §5). Encodings are cached under data/cache/<content
sha256 of the batch>/, so a batch is encoded once whatever runs read it; the
cache key is the batch's own content hash, so a stale cache cannot be
mistaken for a different batch.
"""

from collections import Counter
from pathlib import Path

import torch

from ..cost import SCALE
from ..dataset import LabelBatch, mlp_features, static_graph, wl_colours

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / "data" / "cache"


def _cached(batch: LabelBatch, kind: str, build, cache: Path | None):
    if cache is False:
        return build()
    path = (cache or CACHE) / batch.manifest["content_sha256"] / f"{kind}.pt"
    if path.exists():
        return torch.load(path, weights_only=False)
    out = build()
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(out, path)
    return out


def targets(batch: LabelBatch) -> torch.Tensor:
    return torch.tensor([ex.hstar / SCALE for ex in batch.examples], dtype=torch.float32)


def mlp_matrix(batch: LabelBatch, cache=None) -> torch.Tensor:
    """[states, 7] hand-built features, unstandardised (standardisation is fitted on train by the model)."""
    return _cached(batch, "mlp", lambda: torch.tensor([mlp_features(batch.task(ex), ex.state)
                                                       for ex in batch.examples], dtype=torch.float32), cache)


def wl_histograms(batch: LabelBatch, cache=None) -> list[Counter]:
    return _cached(batch, "wl", lambda: [wl_colours(batch.task(ex), ex.state) for ex in batch.examples], cache)


def fact_bits(task, states: list[int]) -> torch.Tensor:
    """[states, facts, 2]: held, is_goal. Built with bit operations, the same values as dataset.fact_features."""
    n = len(task.facts)
    held = torch.tensor([[s >> f & 1 for f in range(n)] for s in states], dtype=torch.float32)
    goal = torch.zeros(n)
    goal[list(task.goal)] = 1.0
    return torch.stack([held, goal.expand_as(held)], dim=-1)


def gnn_groups(batch: LabelBatch, cache=None) -> list[dict]:
    """Per labelled instance: its static graph, the fact features of its labelled states, and their targets."""
    def build():
        by_inst: dict[int, list[int]] = {}
        for k, ex in enumerate(batch.examples):
            by_inst.setdefault(ex.instance, []).append(k)
        y = targets(batch)
        out = []
        for i, ks in sorted(by_inst.items()):
            inst = batch.instances[i]
            out.append({"instance": i, "graph": static_graph(inst),
                        "fx": fact_bits(inst.task, [batch.examples[k].state for k in ks]), "y": y[ks],
                        "rows": torch.tensor(ks)})
        return out
    return _cached(batch, "gnn", build, cache)
