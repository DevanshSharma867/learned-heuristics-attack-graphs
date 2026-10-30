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
from ..dataset import COST_SCALE, LabelBatch, mlp_features, static_graph, wl_colours
from ..heuristics import INF, lmcut, relaxed_costs
from ..search import astar

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


def hmax_inputs(task, states: list[int]) -> tuple[torch.Tensor, torch.Tensor]:
    """D22 residual inputs: [states, facts, 4] (held, is_goal, h_max-reachable, h_max cost / COST_SCALE)
    and h_max(s) in D9 units. One relaxed pass per state with every fact final (stop_at_goal=False)."""
    rows, hm = [], []
    for s in states:
        fc, _ = relaxed_costs(task, s, "max", stop_at_goal=False)
        rows.append([(0.0, 0.0) if c == INF else (1.0, c / COST_SCALE) for c in fc])
        hm.append(max((fc[g] for g in task.goal), default=0))
    return torch.cat([fact_bits(task, states), torch.tensor(rows, dtype=torch.float32)], -1), \
        torch.tensor(hm, dtype=torch.float32)


def gnn_inputs(task, states: list[int], residual: bool) -> dict:
    """Model inputs for states of one instance: fx, and for the residual model glob ([B, 1]) and hm (effort units)."""
    if not residual:
        return {"fx": fact_bits(task, states)}
    fx, hm = hmax_inputs(task, states)
    return {"fx": fx, "glob": (hm / COST_SCALE)[:, None], "hm": hm / SCALE}


def gnn_groups(batch: LabelBatch, cache=None, residual: bool = False) -> list[dict]:
    """Per labelled instance: its static graph, the inputs of its labelled states, and their targets.
    residual: y is h* - h_max (effort units), the D22 variant a target, which is >= 0 (h_max is admissible)."""
    def build():
        by_inst: dict[int, list[int]] = {}
        for k, ex in enumerate(batch.examples):
            by_inst.setdefault(ex.instance, []).append(k)
        y = targets(batch)
        out = []
        for i, ks in sorted(by_inst.items()):
            inst = batch.instances[i]
            x = gnn_inputs(inst.task, [batch.examples[k].state for k in ks], residual)
            yi = y[ks] - x["hm"] if residual else y[ks]
            out.append({"instance": i, "graph": static_graph(inst), **x, "y": yi, "rows": torch.tensor(ks)})
        return out
    return _cached(batch, "gnn_res" if residual else "gnn", build, cache)


def plan_open_pairs(task) -> tuple[list[int], list[tuple[int, int, float]]]:
    """The ranking data of Chrestien et al. (NeurIPS 2023, Eq. 1 and 4) for one task (D22 variant c).

    One optimal plan s_0..s_n (A*+LM-cut, D3 tie-breaking). For each i >= 1, O_i is the open list
    of a search that has expanded exactly s_0..s_{i-1}: every successor generated so far that is
    not a plan state, with the cheapest g through the expanded plan states. Each (s_i, s_j in O_i)
    is one pair. Returns the states (plan states s_1..s_n first, then off-plan states) and pairs
    (index of s_i, index of s_j, g_i - g_j in effort units).
    """
    r = astar(task, lmcut)
    path, g = [task.init], [0]
    for ai in r.plan:
        path.append(path[-1] | task.actions[ai].add_mask)
        g.append(g[-1] + task.actions[ai].cost)
    on_plan = set(path)
    states = path[1:]
    index = {s: k for k, s in enumerate(states)}
    open_g: dict[int, int] = {}
    pairs = []
    for i in range(1, len(path)):
        for ai, s2 in task.successors(path[i - 1]):  # expanding s_{i-1} generates its successors
            if s2 not in on_plan:
                open_g[s2] = min(open_g.get(s2, INF), g[i - 1] + task.actions[ai].cost)
        for s2, g2 in open_g.items():
            if s2 not in index:
                index[s2] = len(states)
                states.append(s2)
            pairs.append((index[path[i]], index[s2], (g[i] - g2) / SCALE))
    return states, pairs


def rank_groups(batch: LabelBatch, cache=None, residual: bool = False) -> list[dict]:
    """Per labelled instance: inputs of its plan and open-list states and the ranking pairs (variant c / d)."""
    def build():
        out = []
        for i, inst in enumerate(batch.instances):
            if batch.manifest["instances"][i]["stats"] is None:
                continue  # unreachable goal: no plan
            states, pairs = plan_open_pairs(inst.task)
            if not pairs:
                continue  # the initial state is a goal, or the plan has no off-plan successor
            pi, pj, dg = zip(*pairs)
            out.append({"instance": i, "graph": static_graph(inst), **gnn_inputs(inst.task, states, residual),
                        "pi": torch.tensor(pi), "pj": torch.tensor(pj), "dg": torch.tensor(dg, dtype=torch.float32)})
        return out
    return _cached(batch, "rank_res" if residual else "rank", build, cache)
