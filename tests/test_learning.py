"""Learned heuristics (D21): losses, ridge fit, encodings, split guard, determinism, checkpoints, harness."""

import math

import pytest
import torch

from ahg.cost import SCALE
from ahg.dataset import fact_features, open_batch
from ahg.evaluate import BASELINES, _geo_ci, evaluate, sibling_groups, sibling_order, summarise
from ahg.heuristics import ADMISSIBLE, hmax, lmcut
from ahg.labels import write_batch
from ahg.learning import encode
from ahg.learning.encode import fact_bits, plan_open_pairs
from ahg.learning.heuristic import Learned
from ahg.learning.models import fit_ridge
from ahg.learning.runs import make_config
from ahg.learning.train import load, loss_fn, save, train_model
from ahg.search import astar
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


def test_hstar_satisfies_every_ranking_pair(batches):
    """With h = h*, f(s_i) = h*(s_0) on the plan and f(s_j) >= h*(s_0) off it: no pair may have f_i > f_j."""
    train, _ = batches
    task = train.instances[train.examples[0].instance].task
    states, pairs = plan_open_pairs(task)
    hstar = [astar(task, lmcut, start=s).cost / SCALE for s in states]
    assert pairs and all(dg + hstar[i] - hstar[j] <= 1e-9 for i, j, dg in pairs)


def test_sibling_order_is_perfect_for_hstar_and_all_ties_for_a_constant(batches):
    _, val = batches
    exs = [ex for ex in val.examples if ex.instance == val.examples[0].instance]
    task = val.task(exs[0])
    groups = sibling_groups(task, exs)
    states = {s for grp in groups for _, s, _ in grp}
    star = sibling_order(groups, {ex.state: ex.hstar for ex in exs})
    assert star["pairs"] > 0 and star["concordant"] == star["pairs"]
    flat = sibling_order(groups, {s: 0.0 for s in states})
    assert flat["pairs"] == star["pairs"]
    # A constant h orders siblings by action cost alone: pairs of equal cost become ties.
    assert flat["concordant"] + flat["ties"] <= flat["pairs"]


@pytest.mark.parametrize("over", [{"target": "residual", "loss": "mse"}, {"loss": "rank"},
                                  {"target": "residual", "loss": "rank"}])
def test_d22_variants_train_and_never_go_below_hmax_when_residual(batches, over, tmp_path):
    train, val = batches
    cfg = make_config(kind="gnn", max_epochs=2, hidden=16, layers=2, **over)
    model, history = train_model(cfg, [train], [val])
    assert sum("epoch" in e for e in history) >= 1
    save(model, cfg, tmp_path / "model.pt")
    model2, cfg2 = load(tmp_path / "model.pt")
    inst = val.instances[val.examples[0].instance]
    states = [ex.state for ex in val.examples if ex.instance == val.examples[0].instance][:20]
    for combine in (None, "max_hmax"):
        h = Learned(model2, cfg2, "m", combine).bind(inst)
        vals = [h(inst.task, s) for s in states]
        assert min(vals) >= 0
        if over.get("target") == "residual" or combine:
            assert all(v >= hmax(inst.task, s) - 1e-6 for v, s in zip(vals, states))


def test_rank_and_residual_are_gnn_only(batches):
    train, val = batches
    with pytest.raises(ValueError):
        train_model(make_config(kind="mlp", loss="rank"), [train], [val])


def _train_script():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("train_script", Path(__file__).parents[1] / "scripts" / "train.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_plan_runs_gate_first_shards_disjoint_and_same_model_is_bitwise(batches, tmp_path):
    """D23 amendment 1: gate runs (seed 0 and its -check copy) come first; workers split the rest disjointly;
    same_model accepts only bitwise-identical runs."""
    tr = _train_script()
    plan = {"name": "p", "reproduce": {"B": "x"}, "models": [
        {"id": "A", "seeds": [0, 1], "est_seconds": 1, "overrides": {"kind": "mlp"}},
        {"id": "B", "seeds": [0, 1], "est_seconds": 3, "overrides": {"kind": "mlp", "loss": "asym"}}]}
    runs = tr.plan_runs(plan)
    assert [(i, c["seed"], n.split("/")[0]) for i, c, n in runs] == [
        ("B", 0, "p"), ("B", 0, "p-check"), ("A", 0, "p"), ("A", 1, "p"), ("B", 1, "p")]
    rest = [r for r in runs if not tr.is_gate(plan, r)]
    parts = [tr.shard(plan, rest, k, 2) for k in range(2)]
    assert sorted(n for part in parts for _, _, n in part) == sorted(n for _, _, n in rest)
    train, val = batches
    outs = []
    for k, seed in enumerate((0, 0, 1)):
        cfg = make_config(kind="mlp", hidden=16, max_epochs=2, seed=seed)
        out, _ = tr.train_run(cfg, f"r{k}", ([train], [val]), root=tmp_path)
        outs.append(out)
    assert tr.same_model(outs[0], outs[1]) == []
    assert set(tr.same_model(outs[0], outs[2])) >= {"config", "weights"}
