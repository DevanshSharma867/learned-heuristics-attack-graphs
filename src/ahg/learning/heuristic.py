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
from .encode import fact_bits
from .models import WLLinear


class Learned:
    def __init__(self, model, cfg: dict, name: str):
        self.model, self.cfg, self.name = model, cfg, name

    def bind(self, inst):
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
