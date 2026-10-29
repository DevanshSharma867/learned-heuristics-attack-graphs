"""Write one label batch (D19) for a split, a seed range or a SLURM array shard.

Usage: python scripts/make_labels.py --split SPLIT --config configs/labels/d19.json
           [--seeds A-B[:STEP] | --shard K/N] [--workers W] [--tag TAG] [--allow-dirty]

  --seeds A-B:STEP  seeds A..B inclusive, every STEP-th (default: the whole split)
  --shard K/N       the K-th of N strided shards of the split's seeds (K = 0..N-1);
                    with SLURM, K is $SLURM_ARRAY_TASK_ID. Strided, so every shard
                    gets every knob cell in turn.
The batch goes to data/labels/<split>-<config sha[:8]>-<commit[:7]>[-s<K>of<N>][-<tag>]/.
A cross-check mismatch aborts before anything is written (exit status 2).
"""

import argparse
import json
import sys
from pathlib import Path

from ahg.labels import write_batch
from ahg.measure import HardFailure
from ahg.splits import SPLITS


def parse_seeds(text: str) -> list[int]:
    span, _, step = text.partition(":")
    a, b = map(int, span.split("-"))
    return list(range(a, b + 1, int(step or 1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=sorted(SPLITS))
    ap.add_argument("--config", required=True, type=Path)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--seeds")
    g.add_argument("--shard")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--tag")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text())
    seeds, shard = list(SPLITS[args.split].seeds), None
    if args.seeds:
        seeds = parse_seeds(args.seeds)
    elif args.shard:
        k, n = map(int, args.shard.split("/"))
        if not 0 <= k < n:
            sys.exit(f"shard {k}/{n}: K must be in 0..N-1")
        seeds, shard = seeds[k::n], (k, n)
    print(f"{args.split}: {len(seeds)} instances, {args.workers} worker(s)", flush=True)
    try:
        out = write_batch(args.split, seeds, cfg, shard=shard, tag=args.tag, workers=args.workers,
                          allow_dirty=args.allow_dirty)
    except HardFailure as e:
        print(f"HARD FAILURE, nothing written: {e}", file=sys.stderr)
        sys.exit(2)
    m = json.loads((out / "manifest.json").read_text())
    print(f"wrote {out}\n{json.dumps(m['counts'])}\nelapsed {m['elapsed_seconds']} s")


if __name__ == "__main__":
    main()
