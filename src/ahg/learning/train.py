"""Training (D21 §2–§3) and loading of the three model kinds.

train_model(cfg, train_batches, val_batches) -> (model, history). Train
batches are the only data the weights, standardisation statistics or WL
vocabulary are fitted on; val batches are read only to compute the
early-stopping (or, for WL, selection) loss.
"""

import random
import time

import torch
from torch.nn.functional import softplus

from ..cost import SCALE
from ..dataset import LabelBatch
from . import encode
from .models import GNN, MLP, WLLinear, fit_ridge, sparse_matrix

KINDS = ("mlp", "wl", "gnn")
LOSSES = ("mse", "asym", "rank")  # rank: GNN only (D22 c, d)


def loss_fn(pred, y, loss: str, w_over: float):
    """MSE, or the squared error with overestimates (pred > h*) weighted w_over (D21 §2)."""
    err2 = (pred - y) ** 2
    if loss == "asym":
        err2 = torch.where(pred > y, w_over * err2, err2)
    return err2.mean()


def _cat(xs):
    return torch.cat(xs) if len(xs) > 1 else xs[0]


def _train_mlp(cfg, train, val, history, deadline=None):
    X = _cat([encode.mlp_matrix(b) for b in train])
    y = _cat([encode.targets(b) for b in train])
    Xv = _cat([encode.mlp_matrix(b) for b in val])
    yv = _cat([encode.targets(b) for b in val])
    dev = torch.device(cfg["device"])
    mean, std = X.mean(0), X.std(0).clamp_min(1e-6)  # train-only statistics (D14 §5)
    model = MLP(X.shape[1], cfg["hidden"], mean, std).to(dev)
    X, y, Xv, yv = X.to(dev), y.to(dev), Xv.to(dev), yv.to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    gen = torch.Generator().manual_seed(cfg["seed"])

    def epoch():
        model.train()
        total = 0.0
        for idx in torch.randperm(len(y), generator=gen).split(cfg["batch_size"]):
            idx = idx.to(dev)
            loss = loss_fn(model(X[idx]), y[idx], cfg["loss"], cfg["w_over"])
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss) * len(idx)
        return total / len(y)

    def val_loss():
        model.eval()
        with torch.no_grad():
            return float(loss_fn(model(Xv), yv, cfg["loss"], cfg["w_over"]))

    return _early_stop(model, epoch, val_loss, cfg, history, deadline)


def rank_loss(h, g):
    """Chrestien et al. (2023) Eq. 4 with alpha = beta = 1: sum over pairs of log(1 + exp(f(s_i) - f(s_j))),
    f = g + h, for one instance; s_i is a plan state and s_j an off-plan state of its open list."""
    return softplus(g["dg"] + h[g["pi"]] - h[g["pj"]]).sum()


def gnn_h(model, g, residual: bool, sl=slice(None)):
    """Raw model output for states sl of group g (the residual r, or h itself)."""
    return model(g["fx"][sl], g["graph"], g["glob"][sl] if residual else None)


def _train_gnn(cfg, train, val, history, deadline=None):
    dev = torch.device(cfg["device"])
    residual, rank = cfg.get("target", "hstar") == "residual", cfg["loss"] == "rank"
    move = lambda gr: {k: ({kk: vv.to(dev) for kk, vv in v.items()} if k == "graph" else
                           v.to(dev) if torch.is_tensor(v) else v) for k, v in gr.items()}
    enc = encode.rank_groups if rank else encode.gnn_groups
    groups = [move(g) for b in train for g in enc(b, residual=residual)]
    vgroups = [move(g) for b in val for g in enc(b, residual=residual)]
    model = new_gnn(cfg).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    rng = random.Random(f"train:{cfg['seed']}")
    chunk = cfg["batch_size"]

    def group_rank_loss(g):
        out = gnn_h(model, g, residual)
        # Variant d trains h = h_max + softplus(r): a strictly positive residual keeps the gradient (D22 §4).
        return rank_loss(g["hm"] + softplus(out) if residual else out, g)

    def epoch():
        model.train()
        order = list(range(len(groups)))
        rng.shuffle(order)
        total = n = 0
        for gi in order:
            g = groups[gi]
            if rank:  # one instance per minibatch, all its pairs (Chrestien et al. §6)
                loss = group_rank_loss(g)
                opt.zero_grad()
                loss.backward()
                opt.step()
                total, n = total + float(loss), n + 1
                continue
            for s in range(0, len(g["y"]), chunk):
                sl = slice(s, s + chunk)
                loss = loss_fn(gnn_h(model, g, residual, sl), g["y"][sl], cfg["loss"], cfg["w_over"])
                opt.zero_grad()
                loss.backward()
                opt.step()
                total, n = total + float(loss) * len(g["y"][sl]), n + len(g["y"][sl])
        return total / n

    def val_loss():
        model.eval()
        total = n = 0
        with torch.no_grad():
            for g in vgroups:
                if rank:  # mean over instances of the per-instance summed loss
                    total, n = total + float(group_rank_loss(g)), n + 1
                else:
                    total += float(loss_fn(gnn_h(model, g, residual), g["y"], cfg["loss"], cfg["w_over"])) * len(g["y"])
                    n += len(g["y"])
        return total / n

    return _early_stop(model, epoch, val_loss, cfg, history, deadline)


def new_gnn(cfg: dict) -> GNN:
    """The GNN a config describes; the residual target (D22 a, d) adds the h_max inputs and a raw output."""
    if cfg.get("target", "hstar") == "residual":
        return GNN(cfg["hidden"], cfg["layers"], fact_dim=4, global_dim=1, positive=False)
    return GNN(cfg["hidden"], cfg["layers"])


def _early_stop(model, epoch, val_loss, cfg, history, deadline=None):
    """Train up to max_epochs; keep the weights of the best validation loss; stop after `patience` bad epochs.

    deadline: a time.time() past which no new epoch starts (the D21 §5 search budget).
    """
    best, best_state, bad = float("inf"), None, 0
    for e in range(cfg["max_epochs"]):
        if e > 0 and deadline is not None and time.time() >= deadline:
            history.append({"stopped": "budget"})  # a search budget ran out (D21 §5): the run is partial
            break
        t0 = time.perf_counter()
        tr = epoch()
        t_train = time.perf_counter() - t0
        vl = val_loss()
        history.append({"epoch": e, "train_loss": tr, "val_loss": vl, "epoch_seconds": t_train,
                        "val_seconds": time.perf_counter() - t0 - t_train})
        if vl < best:
            best, bad = vl, 0
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= cfg["patience"]:
                break
    model.load_state_dict(best_state)
    return model.cpu().eval()


def _train_wl(cfg, train, val, history, deadline=None):  # minutes, not hours: no deadline check
    hists = [h for b in train for h in encode.wl_histograms(b)]
    y = _cat([encode.targets(b) for b in train]).double()
    vocab: dict[str, int] = {}
    for h in hists:  # fitted on train only; colours unseen in train are dropped later
        for c in sorted(h):
            vocab.setdefault(c, len(vocab))
    X = sparse_matrix(hists, vocab)
    Xv = sparse_matrix([h for b in val for h in encode.wl_histograms(b)], vocab)
    yv = _cat([encode.targets(b) for b in val]).double()
    w = None
    rounds = cfg["irls_rounds"] if cfg["loss"] == "asym" else 1
    for r in range(rounds):
        t0 = time.perf_counter()
        beta, bias = fit_ridge(X, y, cfg["lam"], w)
        pred = (X @ beta + bias).clamp_min(0)
        # IRLS for the asymmetric loss: reweight by which side of h* each state now falls on.
        w = torch.where(pred > y, torch.full_like(y, cfg["w_over"]), torch.ones_like(y))
        pv = (Xv @ beta + bias).clamp_min(0)
        history.append({"epoch": r, "train_loss": float(loss_fn(pred, y, cfg["loss"], cfg["w_over"])),
                        "val_loss": float(loss_fn(pv, yv, cfg["loss"], cfg["w_over"])),
                        "epoch_seconds": time.perf_counter() - t0, "val_seconds": 0.0})
    history.append({"vocab_size": len(vocab)})
    return WLLinear(vocab, beta, bias)


def train_model(cfg: dict, train: list[LabelBatch], val: list[LabelBatch], deadline: float | None = None):
    """Train one model; returns (model, history). cfg["kind"] in KINDS, cfg["loss"] in LOSSES."""
    if any(b.manifest["split"] != "train" for b in train) or any(b.manifest["split"] != "val" for b in val):
        raise ValueError("train_model takes train batches to fit and val batches to stop on, nothing else")
    if cfg["kind"] != "gnn" and (cfg["loss"] == "rank" or cfg.get("target", "hstar") != "hstar"):
        raise ValueError("the ranking loss and the residual target are implemented for the GNN only (D22)")
    torch.manual_seed(cfg["seed"])
    history: list[dict] = []
    fit = {"mlp": _train_mlp, "gnn": _train_gnn, "wl": _train_wl}[cfg["kind"]]
    return fit(cfg, train, val, history, deadline), history


def save(model, cfg: dict, path) -> None:
    sd = model.state_dict()
    torch.save({"kind": cfg["kind"], "config": cfg, "state_dict": sd}, path)


def load(path):
    ck = torch.load(path, weights_only=False)
    cfg, sd = ck["config"], ck["state_dict"]
    if ck["kind"] == "wl":
        return WLLinear(sd["vocab"], sd["beta"], sd["bias"]), cfg
    if ck["kind"] == "mlp":
        model = MLP(sd["mean"].shape[0], cfg["hidden"], sd["mean"], sd["std"])
    else:
        model = new_gnn(cfg)
    model.load_state_dict(sd)
    return model.eval(), cfg


def effort_to_units(h: float) -> float:
    return h * SCALE
