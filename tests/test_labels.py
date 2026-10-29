"""Label batches (D19): correctness against brute force, determinism, append-only, hard failure, loader."""

import json

import pytest
import torch

from ahg import labels
from ahg.dataset import ACTION_DIM, WLVocab, fact_features, mlp_features, open_batch, static_graph, wl_colours
from ahg.labels import CONFIG_KEYS, label_instance, write_batch
from ahg.measure import HardFailure
from ahg.search import astar
from ahg.heuristics import lmcut
from helpers import brute_force_optimal, random_task

CFG = {"walk_cap": 15, "walks_per_sample": 10, "successor_cap": 20, "init_budget": 200_000,
       "state_budget": 20_000, "oracle_all_max_n": 12, "oracle_states": 5, "oracle_max_pops": 200_000,
       "enum_cap": 20_000}
SEEDS = [1000, 1001]  # train: flat, n = 12, D = 2, two coupling cells


def test_config_fixture_has_every_key():
    assert set(CFG) == CONFIG_KEYS


def test_labels_match_brute_force_on_tiny_tasks():
    checked = 0
    for seed in range(60):
        task = random_task(seed, n_facts=8, n_actions=10)
        if not astar(task, lmcut).solved:
            continue
        out = label_instance(task, f"tiny:{seed}", 1, CFG)
        for s, h, src in out["rows"]:
            assert h == brute_force_optimal(task, s), (seed, s, src)
            checked += 1
    assert checked > 100


@pytest.fixture(scope="module")
def batches(tmp_path_factory):
    roots = [tmp_path_factory.mktemp(r) for r in ("a", "b")]
    return [write_batch("train", SEEDS, CFG, root=r, allow_dirty=True) for r in roots]


def test_same_config_gives_identical_batch(batches):
    a, b = batches
    ma, mb = (json.loads((d / "manifest.json").read_text()) for d in (a, b))
    assert ma["content_sha256"] == mb["content_sha256"] and ma["batch_id"] == mb["batch_id"]
    for f in ("labels.jsonl.gz", "failures.jsonl.gz"):
        assert (a / f).read_bytes() == (b / f).read_bytes()
    assert ma["counts"]["states"] > 0


def test_batches_are_append_only(batches):
    with pytest.raises(FileExistsError):
        write_batch("train", SEEDS, CFG, root=batches[0].parent, allow_dirty=True)


def test_seeds_outside_the_split_are_refused(tmp_path):
    with pytest.raises(ValueError):
        write_batch("train", [1700], CFG, root=tmp_path, allow_dirty=True)


def test_mismatch_hard_fails_and_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(labels, "optimal_cost", lambda task, s, max_pops=None: -1)
    with pytest.raises(HardFailure):
        write_batch("train", SEEDS[:1], CFG, root=tmp_path, allow_dirty=True)
    assert not any(tmp_path.iterdir())


def test_loader_rebuilds_tasks_and_features(batches):
    batch = open_batch(batches[0])
    assert len(batch.examples) == batch.manifest["counts"]["states"]
    task, state, hstar = next(iter(batch))
    inst = batch.instances[batch.examples[0].instance]
    g = static_graph(inst)
    assert g["act_x"].shape == (len(task.actions), ACTION_DIM)
    assert fact_features(task, state).shape == (len(task.facts), 2)
    assert len(mlp_features(task, state)) == 7
    vocab = WLVocab().fit(wl_colours(t, s) for t, s, _ in batch)
    v = vocab.transform(wl_colours(task, state))
    assert len(v) == len(vocab.index) and sum(v) == sum(wl_colours(task, state).values())
    assert isinstance(g["pre_src"], torch.Tensor)


def test_loader_refuses_tampered_labels(batches, tmp_path):
    import shutil
    d = tmp_path / batches[0].name
    shutil.copytree(batches[0], d)
    (d / "failures.jsonl.gz").write_bytes(b"")
    with pytest.raises(ValueError):
        open_batch(d)


def test_reading_a_test_split_is_logged(tmp_path):
    out = write_batch("test_id", [1700], CFG, root=tmp_path / "labels", allow_dirty=True)
    log = tmp_path / "log.jsonl"
    with pytest.raises(PermissionError):
        open_batch(out, log=log)
    open_batch(out, purpose="pipeline test", log=log)
    (entry,) = [json.loads(line) for line in log.read_text().splitlines()]
    assert entry["split"] == "test_id" and entry["batch_id"] == out.name
