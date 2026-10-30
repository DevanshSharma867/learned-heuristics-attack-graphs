#!/bin/bash
# One training run (one model, one seed) on the BITS HPC (docs/hpc.md), using
# at most half an RTX Pro 6000, compute and VRAM, through MPS (cluster rule).
# Several seeds can share a card through MPS, each within its half-card limit.
#
# Submit one job per (model, seed), from the repo root at a clean commit. SET holds
# scripts/train.py overrides of configs/training/d21.json, space-separated:
#   for s in 0 1 2 3 4; do
#     sbatch --export=ALL,SEED=$s,SET="kind=gnn hidden=128 layers=3 lr=0.001 loss=asym" \
#         scripts/slurm/train.sbatch
#   done
# CUDA training is not bitwise reproducible (scatter-add order), unlike CPU; seeds
# still fix initialisation and data order.
# HPC runs report losses, validation metrics and checkpoints only. Test splits
# and timing stay on the M4 (D17 §4, §5).
#
# TEMPLATE: the gres/MPS/qos lines below must be the ones in the admins'
# docs/hpc/mock_job.sh (missing from the repo when this was written).
# Lines marked SET_ME are placeholders that SLURM will reject.
#
#SBATCH --job-name=ahg-train
#SBATCH --partition=gpu_rtx_pro_6000_6_csis_hyd
#SBATCH --qos=SET_ME_QOS_FROM_TEMPLATE
#SBATCH --gres=mps:50
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=06:00:00
#SBATCH --output=logs/train-%j.out
#SBATCH --error=logs/train-%j.err

set -euo pipefail
: "${SEED:?set SEED via --export}" "${SET:?set SET via --export}"
cd "${SLURM_SUBMIT_DIR:?}"
mkdir -p logs
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    echo "working tree is dirty; train only at a clean commit" >&2
    exit 1
fi
# Half a card: MPS caps this client's SM share and its pinned device memory.
# The RTX Pro 6000 has 96 GB, so half is 48G.
export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=50
export CUDA_MPS_PINNED_DEVICE_MEM_LIMIT="0=48G"
export PYTHONHASHSEED=0 OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
args=(--set "seed=$SEED" --set device=cuda)
for kv in $SET; do args+=(--set "$kv"); done
uv run --frozen python scripts/train.py run "${args[@]}"
