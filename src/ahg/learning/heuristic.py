"""A trained model as a search heuristic h(task, state) -> D9 cost units (D21 §4).

bind(instance) returns the callable best_first_search takes. Everything the
model needs per instance (the GNN's static graph) is built lazily inside the
first call, so it is inside the search's own timing, as rule 7 requires.
One state per call: no batching across successors, so the measured time is
what plain A* pays.
"""

import torch

from ..cost import SCALE
from ..dataset import mlp_features, static_graph, wl_colours
from ..heuristics import hmax
from .encode import fact_bits, gnn_inputs
from .models import WLLinear


class Learned:
    """combine="max_hmax": search with max(h_max, h_θ) (D22 variant b); h_max is then inside the timing."""

    def __init__(self, model, cfg: dict, name: str, combine: str | None = None):
        assert combine in (None, "max_hmax")
        self.model, self.cfg, self.name, self.combine = model, cfg, name, combine

    def bind(self, inst):
        h = self._bind(inst)
        if self.combine == "max_hmax":
            return lambda task, s: max(hmax(task, s), h(task, s))
        return h

    def _bind(self, inst):
        kind, model = self.cfg["kind"], self.model
        if kind == "wl":
            assert isinstance(model, WLLinear)
            return lambda task, s: SCALE * model.predict_one(wl_colours(task, s))
        if kind == "mlp":
            def h(task, s):
                with torch.no_grad():
                    return SCALE * float(model(torch.tensor([mlp_features(task, s)], dtype=torch.float32)))
            return h
        graph = {}
        if self.cfg.get("target", "hstar") == "residual":
            def h(task, s):  # D22 a, d: h_max + max(0, r), with h_max computed here, inside the timing
                if not graph:
                    graph.update(static_graph(inst))
                x = gnn_inputs(task, [s], residual=True)
                with torch.no_grad():
                    r = float(model(x["fx"], graph, x["glob"]))
                return SCALE * (float(x["hm"][0]) + max(0.0, r))
            return h

        def h(task, s):
            if not graph:
                graph.update(static_graph(inst))
            with torch.no_grad():
                return SCALE * float(model(fact_bits(task, [s]), graph))
        return h

    def predict_states(self, inst, states: list[int]) -> list[float]:
        """h_θ in effort units for many states of one instance (overestimation statistics; not timed)."""
        h = self.bind(inst)
        return [h(inst.task, s) / SCALE for s in states]
