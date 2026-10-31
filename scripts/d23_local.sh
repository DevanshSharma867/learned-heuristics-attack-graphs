#!/bin/zsh
# D23 §5: the multi-seed plan on the M4 CPU, then per-seed val metrics (D21 §4 harness, val only).
# Start detached so a closed session or lost internet does not stop it:
#   nohup caffeinate -is scripts/d23_local.sh > logs/d23.log 2>&1 < /dev/null &!
# Resumable: rerun the same line after a crash or reboot; finished runs are skipped.
# Progress: tail logs/d23.log; ls results/training/d23/*/*/model.pt | wc -l   (25 runs in all).
set -u
cd "${0:A:h}/.."
source .venv/bin/activate
export PYTHONHASHSEED=0
date
python -W ignore scripts/train.py plan configs/training/d23.json || { echo "PLAN STOPPED (see the summary above)"; exit 1; }
date
python -W ignore scripts/evaluate.py --name d23-val --batches data/labels/val-677e9fe4-72e8821 \
  --manifest results/training/d23/frozen.json || { echo "VAL EVALUATION FAILED"; exit 1; }
date
echo ALL DONE
