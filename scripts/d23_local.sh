#!/bin/zsh
# D23 (amendments 1, 2): the multi-seed plan on the M4 CPU at 1 torch thread per run, then per-seed val metrics
# (D21 §4 harness, val only). Phases: gate runs (4 in parallel) -> gate check -> the rest (3 workers)
# -> finalize (summary, frozen.json) -> val evaluation.
# Start detached so a closed session or lost internet does not stop it:
#   nohup caffeinate -is scripts/d23_local.sh >> logs/d23.log 2>&1 < /dev/null &!
# Resumable: rerun the same line after a crash or reboot; finished runs are skipped.
# Progress: tail logs/d23.log; ls results/training/d23t1*/*/*/model.pt | wc -l   (27 runs: 25 + 2 gate copies).
set -u
cd "${0:A:h}/.."
source .venv/bin/activate
export PYTHONHASHSEED=0
P=configs/training/d23.json

phase() {  # phase NAME N: N workers in parallel, each logging to logs/d23-NAME-wK.log; fails if any worker fails
  local pids=() k st=0
  for k in $(seq 0 $(($2 - 1))); do
    python -W ignore scripts/train.py plan $P --phase $1 --worker $k --workers $2 >> logs/d23-$1-w$k.log 2>&1 &
    pids+=($!)
  done
  for k in $pids; do wait $k || st=1; done
  return $st
}

date; echo "phase gate"
phase gate 4 || { echo "GATE RUNS FAILED (logs/d23-gate-w*.log)"; exit 1; }
date; echo "gate check"
python -W ignore scripts/train.py gate $P || { echo "GATE FAILED: nothing else trains"; exit 1; }
date; echo "phase rest"
phase rest 3 || echo "SOME RUNS FAILED (logs/d23-rest-w*.log); finalize lists them"
date; echo "finalize"
python -W ignore scripts/train.py finalize $P || { echo "PLAN INCOMPLETE"; exit 1; }
python -W ignore scripts/evaluate.py --name d23-val --batches data/labels/val-677e9fe4-72e8821 \
  --manifest results/training/d23t1/frozen.json || { echo "VAL EVALUATION FAILED"; exit 1; }
date
echo ALL DONE
