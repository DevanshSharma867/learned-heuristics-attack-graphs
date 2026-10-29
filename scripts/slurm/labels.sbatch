#!/bin/bash
# D19 label generation as a SLURM job array on the BITS HPC (docs/hpc.md).
# Each array task labels one strided shard of one split and writes its own
# append-only batch under data/labels/ (D19 §4). Labelling is single-threaded
# Python and never touches the GPU. The cluster has no CPU partition, so it
# runs on the GPU partition with the smallest MPS share.
#
# Submit from the repo root on the login node, at a clean commit:
#   sbatch --array=0-23 --export=ALL,SPLIT=train,N_SHARDS=24 scripts/slurm/labels.sbatch
# N_SHARDS must equal the array size; the job checks this.
#
# TEMPLATE: the gres/MPS/qos lines below must be the ones in the admins'
# docs/hpc/mock_job.sh (missing from the repo when this was written).
# Lines marked SET_ME are placeholders that SLURM will reject.
#
#SBATCH --job-name=ahg-labels
#SBATCH --partition=gpu_rtx_pro_6000_6_csis_hyd
#SBATCH --qos=SET_ME_QOS_FROM_TEMPLATE
#SBATCH --gres=mps:1
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
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=""  # CPU only
uv run --frozen python scripts/make_labels.py --split "$SPLIT" --config configs/labels/d19.json \
    --shard "${SLURM_ARRAY_TASK_ID:?}/$N_SHARDS"
