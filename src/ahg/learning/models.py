"""The three learned heuristics of D21 §1. Each predicts h*(s) in effort units and is ≥ 0.

softplus (not ReLU) on the output keeps h_θ ≥ 0 while still passing a
gradient when the raw output is negative; the WL model is linear and is
clamped at 0 instead.
"""

from collections import Counter

import torch
from torch import nn
from torch.nn.functional import softplus

from ..dataset import ACTION_DIM

FACT_DIM = 2


class MLP(nn.Module):
    """Graph-level hand-built features -> h. Standardisation stats are buffers, saved with the weights."""

    def __init__(self, n_in: int, hidden: int, mean: torch.Tensor, std: torch.Tensor):
        super().__init__()
        self.register_buffer("mean", mean)
        self.register_buffer("std", std)
        self.net = nn.Sequential(nn.Linear(n_in, hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, 1))

    def forward(self, x):
        return softplus(self.net((x - self.mean) / self.std)).squeeze(-1)


class GNN(nn.Module):
    """Message passing over the fact-action graph; one instance's states per call (shared graph).

    fact_dim/global_dim > their defaults give the D22 residual model its h_max inputs (per-fact and
    global); positive=False returns the raw output (the residual r), otherwise softplus(output) >= 0.
    """

    def __init__(self, hidden: int, layers: int, fact_dim: int = FACT_DIM, global_dim: int = 0,
                 positive: bool = True):
        super().__init__()
        self.positive = positive
        self.enc_f = nn.Linear(fact_dim, hidden)
        self.enc_a = nn.Linear(ACTION_DIM, hidden)
        self.up_a = nn.ModuleList(nn.Linear(2 * hidden, hidden) for _ in range(layers))
        self.up_f = nn.ModuleList(nn.Linear(2 * hidden, hidden) for _ in range(layers))
        self.head = nn.Sequential(nn.Linear(3 * hidden + global_dim, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def forward(self, fx, g, glob=None):
        """fx: [B, facts, fact_dim]; g: dataset.static_graph of the instance; glob: [B, global_dim] or None."""
        b, n_f, n_a = fx.shape[0], fx.shape[1], g["act_x"].shape[0]
        f = torch.relu(self.enc_f(fx))
        a = torch.relu(self.enc_a(g["act_x"])).expand(b, -1, -1)
        for up_a, up_f in zip(self.up_a, self.up_f):
            # An action sees the mean of its preconditions: the AND side of the graph.
            m_a = f.new_zeros(b, n_a, f.shape[2]).index_add_(1, g["pre_dst"], f[:, g["pre_src"]]) * g["inv_deg_pre"]
            a = torch.relu(up_a(torch.cat([a, m_a], -1)))
            # A fact sees the mean of the actions that add it: the OR side.
            m_f = f.new_zeros(b, n_f, f.shape[2]).index_add_(1, g["add_dst"], a[:, g["add_src"]]) * g["inv_deg_add"]
            f = torch.relu(up_f(torch.cat([f, m_f], -1)))
        pooled = [f.mean(1), a.mean(1), f[:, g["goal"]].mean(1)] + ([glob] if glob is not None else [])
        out = self.head(torch.cat(pooled, -1)).squeeze(-1)
        return softplus(out) if self.positive else out


class WLLinear:
    """Linear model on WL colour counts (WL-GOOSE style). vocab: colour -> column, fitted on train only."""

    def __init__(self, vocab: dict[str, int], beta: torch.Tensor, bias: float):
        self.vocab, self.beta, self.bias = vocab, beta, bias
        self._w = {c: float(beta[k]) for c, k in vocab.items()}  # dict lookup is faster than a sparse dot here

    def predict_one(self, hist: Counter) -> float:
        return max(0.0, self.bias + sum(n * self._w.get(c, 0.0) for c, n in hist.items()))

    def state_dict(self) -> dict:
        return {"vocab": self.vocab, "beta": self.beta, "bias": self.bias}


def sparse_matrix(hists: list[Counter], vocab: dict[str, int]) -> torch.Tensor:
    """CSR [states, |vocab|] of colour counts; colours outside the vocabulary are dropped."""
    crow, col, val = [0], [], []
    for h in hists:
        for c, n in sorted((vocab[c], n) for c, n in h.items() if c in vocab):
            col.append(c)
            val.append(float(n))
        crow.append(len(col))
    return torch.sparse_csr_tensor(torch.tensor(crow), torch.tensor(col, dtype=torch.long),
                                   torch.tensor(val, dtype=torch.float64), size=(len(hists), len(vocab)))


def fit_ridge(X: torch.Tensor, y: torch.Tensor, lam: float, w: torch.Tensor | None = None, iters: int = 300,
              tol: float = 1e-10) -> tuple[torch.Tensor, float]:
    """Weighted ridge regression, min sum w_i (x_i b + c - y_i)^2 + lam |b|^2, by conjugate gradients.

    The bias c is unpenalised: it is solved exactly by centring with the weights,
    then CG solves the centred normal equations (X'WX + lam I) b = X'W y on the
    sparse X without ever forming X'X.
    """
    y = y.double()
    w = torch.ones_like(y) if w is None else w.double()
    sw = w.sum()
    Xt = X.t().to_sparse_csr()
    xbar = (Xt @ w) / sw  # weighted column means
    ybar = float((w * y).sum() / sw)
    yc = y - ybar

    def A(v):
        xv = X @ v - float(xbar @ v)  # centred columns applied implicitly
        r = Xt @ (w * xv) - xbar * float((w * xv).sum())
        return r + lam * v

    b_rhs = Xt @ (w * yc) - xbar * float((w * yc).sum())
    beta = torch.zeros(X.shape[1], dtype=torch.float64)
    r = b_rhs - A(beta)
    p, rs = r.clone(), float(r @ r)
    for _ in range(iters):
        if rs <= tol * max(1.0, float(b_rhs @ b_rhs)):
            break
        ap = A(p)
        alpha = rs / float(p @ ap)
        beta += alpha * p
        r -= alpha * ap
        rs_new = float(r @ r)
        p = r + (rs_new / rs) * p
        rs = rs_new
    return beta, ybar - float(xbar @ beta)
