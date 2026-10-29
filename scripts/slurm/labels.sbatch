#!/bin/bash
# D19 label generation on the BITS HPC as a SLURM array: one strided shard of
# one split per array task, each writing its own append-only batch under
# data/labels/ (D19 §4). CPU only: labelling is single-threaded Python, so
# each task asks for one core and never touches the GPU (D17 §5).
#
# NOT YET SUBMITTED. Before the first sbatch:
#   1. set --partition and --account below (placeholders on purpose, so an
#      accidental submit is rejected by SLURM rather than run);
#   2. on a login node: git clone the repo, check out the exact commit to
#      label at, then: uv sync --frozen;
#   3. submit, e.g. for the train split in 24 shards:
#        sbatch --array=0-23 --export=ALL,SPLIT=train,N_SHARDS=24 scripts/slurm/labels.sbatch
#      N_SHARDS must equal the array size; the job checks this.
#   4. copy data/labels/<batch-id>*/ back; the manifests carry the commit,
#      hardware and timings. HPC timings are never used as results (D17 §4).
#
#SBATCH --job-name=ahg-labels
#SBATCH --partition=SET_ME_PARTITION
#SBATCH --account=SET_ME_ACCOUNT
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --output=logs/labels-%A_%a.out
#SBATCH --error=logs/labels-%A_%a.err

set -euo pipefail
: "${SPLIT:?set SPLIT via --export}" "${N_SHARDS:?set N_SHARDS via --export}"
if [[ -n "${SLURM_ARRAY_TASK_COUNT:-}" && "$SLURM_ARRAY_TASK_COUNT" != "$N_SHARDS" ]]; then
    echo "array has $SLURM_ARRAY_TASK_COUNT tasks but N_SHARDS=$N_SHARDS" >&2
    exit 1
fi
cd "${SLURM_SUBMIT_DIR:?}"
mkdir -p logs
# A dirty tree would make the batch unreproducible from its recorded commit.
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    echo "working tree is dirty; label only at a clean commit" >&2
    exit 1
fi
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
uv run --frozen python scripts/make_labels.py --split "$SPLIT" --config configs/labels/d19.json \
    --shard "${SLURM_ARRAY_TASK_ID:?}/$N_SHARDS"
