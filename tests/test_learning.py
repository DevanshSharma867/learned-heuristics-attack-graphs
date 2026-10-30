"""Learned heuristics (D21): losses, ridge fit, encodings, split guard, determinism, checkpoints, harness."""

import math

import pytest
import torch

from ahg.dataset import fact_features, open_batch
from ahg.evaluate import BASELINES, _geo_ci, evaluate, summarise
from ahg.heuristics import ADMISSIBLE
from ahg.labels import write_batch
from ahg.learning import encode
from ahg.learning.encode import fact_bits
from ahg.learning.heuristic import Learned
from ahg.learning.models import fit_ridge
from ahg.learning.runs import make_config
from ahg.learning.train import load, loss_fn, save, train_model
from test_labels import CFG


@pytest.fixture(scope="module")
def batches(tmp_path_factory):
    root = tmp_path_factory.mktemp("labels")
    train = open_batch(write_batch("train", [1000, 1001], CFG, root=root, allow_dirty=True))
    val = open_batch(write_batch("val", [1600], CFG, root=root, allow_dirty=True))
    return train, val


@pytest.fixture(autouse=True)
def no_shared_cache(tmp_path, monkeypatch):
    """Encodings go to a per-test cache, never to data/cache/."""
    monkeypatch.setattr(encode, "CACHE", tmp_path / "cache")


def test_asymmetric_loss_weights_only_overestimates():
    y = torch.tensor([1.0, 1.0])
    assert float(loss_fn(torch.tensor([0.0, 1.0]), y, "asym", 4.0)) == pytest.approx(0.5)  # under: weight 1
    assert float(loss_fn(torch.tensor([2.0, 1.0]), y, "asym", 4.0)) == pytest.approx(2.0)  # over: weight 4
    assert float(loss_fn(torch.tensor([2.0, 1.0]), y, "mse", 4.0)) == pytest.approx(0.5)


def test_ridge_matches_closed_form():
    g = torch.Generator().manual_seed(0)
    Xd = (torch.rand(40, 6, generator=g) < 0.4).double() * torch.randint(1, 4, (40, 6), generator=g)
    y = torch.randn(40, generator=g, dtype=torch.float64)
    w = torch.rand(40, generator=g, dtype=torch.float64) + 0.5
    beta, bias = fit_ridge(Xd.to_sparse_csr(), y, lam=0.7, w=w)
    # Closed form with an unpenalised intercept: augment with a ones column, zero its penalty.
    Xa = torch.cat([Xd, torch.ones(40, 1, dtype=torch.float64)], 1)
    P = torch.diag(torch.tensor([0.7] * 6 + [0.0], dtype=torch.float64))
    sol = torch.linalg.solve(Xa.T @ (w[:, None] * Xa) + P, Xa.T @ (w * y))
    assert torch.allclose(beta, sol[:6], atol=1e-6) and bias == pytest.approx(float(sol[6]), abs=1e-6)


def test_fact_bits_equal_fact_features(batches):
    train, _ = batches
    for ex in train.examples[:50]:
        task = train.task(ex)
        assert torch.equal(fact_bits(task, [ex.state])[0], fact_features(task, ex.state))


def test_training_refuses_anything_but_train_and_val(batches):
    train, val = batches
    cfg = make_config(kind="mlp", max_epochs=1)
    with pytest.raises(ValueError):
        train_model(cfg, [val], [val])
    with pytest.raises(ValueError):
        train_model(cfg, [train], [train])


@pytest.mark.parametrize("kind", ["mlp", "wl", "gnn"])
@pytest.mark.parametrize("loss", ["mse", "asym"])
def test_training_is_seeded_and_checkpoints_round_trip(batches, kind, loss, tmp_path):
    train, val = batches
    cfg = make_config(kind=kind, loss=loss, max_epochs=2, irls_rounds=2, hidden=16, layers=2)
    m1, h1 = train_model(cfg, [train], [val])
    _, h2 = train_model(cfg, [train], [val])
    strip = lambda h: [{k: v for k, v in e.items() if not k.endswith("seconds")} for e in h]
    assert strip(h1) == strip(h2)
    save(m1, cfg, tmp_path / "model.pt")
    m2, cfg2 = load(tmp_path / "model.pt")
    inst = val.instances[val.examples[0].instance]
    states = [ex.state for ex in val.examples if ex.instance == val.examples[0].instance][:20]
    p1, p2 = Learned(m1, cfg, "a").predict_states(inst, states), Learned(m2, cfg2, "b").predict_states(inst, states)
    assert p1 == pytest.approx(p2) and min(p1) >= 0


def test_search_deadline_stops_after_one_epoch_and_is_marked(batches):
    train, val = batches
    _, history = train_model(make_config(kind="mlp", max_epochs=5, hidden=16), [train], [val], deadline=0.0)
    assert sum("epoch" in e for e in history) == 1 and history[-1] == {"stopped": "budget"}


def test_harness_checks_baselines_and_summarises(batches):
    train, val = batches
    cfg = make_config(kind="mlp", max_epochs=1, hidden=16)
    model, _ = train_model(cfg, [train], [val])
    recs = evaluate([val], [Learned(model, cfg, "mlp")])
    assert len(recs) == val.manifest["counts"]["labelled_instances"]
    for r in recs:
        for b in ADMISSIBLE & set(BASELINES):
            assert r["runs"][b]["cost"] == r["hstar"]
        assert r["runs"]["mlp"]["cost"] >= r["hstar"]  # any plan costs at least the optimum
        assert sum(map(len, r["over"]["mlp"].values())) > 0
    s = summarise(recs, ["mlp"], 200_000)["mlp"]
    assert set(s["vs"]) == set(BASELINES) and s["solved"] == len(recs)
    assert s["plan_cost"][0] >= 1.0


def test_bootstrap_ci_of_a_constant_is_that_constant():
    assert _geo_ci([math.log(2.0)] * 10, "k") == pytest.approx([2.0, 2.0, 2.0])
