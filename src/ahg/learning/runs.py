"""One training run, written through runlog (D21 §3): results/training/<name>/<stamp>-<commit>/.

The run folder holds raw.json.gz (config, per-epoch history, wall time),
report.md, provenance.json and model.pt (the best-validation checkpoint).
"""

import json
import time
from pathlib import Path

import torch

from ..dataset import open_batch
from ..runlog import write_run
from .train import save, train_model

ROOT = Path(__file__).resolve().parents[3]
TRAINING = ROOT / "results" / "training"
DEFAULTS = json.loads((ROOT / "configs" / "training" / "d21.json").read_text())


def make_config(**over) -> dict:
    cfg = {**DEFAULTS, **over}
    unknown = set(over) - set(DEFAULTS)
    if unknown:
        raise ValueError(f"unknown training config keys {sorted(unknown)}")
    return cfg


def render(raw) -> str:
    c, h = raw["config"], [e for e in raw["history"] if "epoch" in e]
    best = min(h, key=lambda e: e["val_loss"])
    L = [f"# training {raw['name']}", "", "```", json.dumps(c, sort_keys=True), "```", "",
         f"Best val loss {best['val_loss']:.4f} at epoch {best['epoch']} of {len(h)}; wall time "
         f"{raw['wall_seconds']:.1f} s (encoding {raw['encode_seconds']:.1f} s); torch threads {raw['torch_threads']}.", "",
         "| epoch | train loss | val loss | epoch s |", "|---|---|---|---|"]
    L += [f"| {e['epoch']} | {e['train_loss']:.4f} | {e['val_loss']:.4f} | {e['epoch_seconds']:.2f} |" for e in h]
    return "\n".join(L) + "\n"


def train_run(cfg: dict, name: str, batches=None, root: Path | None = None,
              deadline: float | None = None) -> tuple[Path, dict]:
    """Train and write one run. batches: optional preloaded (train, val) to avoid reloading.
    deadline: see train._early_stop; a run it cuts short has raw["stopped"] == "budget"."""
    t0 = time.perf_counter()
    train, val = batches or ([open_batch(ROOT / p) for p in cfg["train_batches"]],
                             [open_batch(ROOT / p) for p in cfg["val_batches"]])
    t1 = time.perf_counter()
    model, history = train_model(cfg, train, val, deadline)
    epochs = [e for e in history if "epoch" in e]
    raw = {"name": name, "config": cfg, "history": history, "wall_seconds": time.perf_counter() - t1,
           "load_seconds": t1 - t0,
           "encode_seconds": 0.0 if not epochs else time.perf_counter() - t1 - sum(
               e["epoch_seconds"] + e["val_seconds"] for e in epochs),
           "torch_threads": torch.get_num_threads(),
           "best_val_loss": min(e["val_loss"] for e in epochs),
           "stopped": next((e["stopped"] for e in history if "stopped" in e), None)}
    out = write_run(name, raw, render(raw), [cfg["seed"]], cfg, root=root or TRAINING)
    save(model, cfg, out / "model.pt")
    return out, raw
