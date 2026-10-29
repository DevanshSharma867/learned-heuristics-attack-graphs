# BITS HPC: how this project uses it

Cluster rules (fixed, from the cluster admins):

- **Login:** `ssh -i ~/.ssh/csisnlp_18 csisnlp_18@hpc.bits-hyderabad.ac.in`
- **Partition:** `gpu_rtx_pro_6000_6_csis_hyd`, the only one allowed. There
  is no CPU partition, so CPU-only work (label generation) is submitted there
  too.
- **Share:** a job may use at most half a card, compute and VRAM, via MPS.
- **Template:** the admins' job template is `docs/hpc/mock_job.sh`. The
  scripts here keep its gres/MPS/qos lines.
- **Docs:** https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/

## What runs where (D17 §4–§5)

| work | where | why |
|---|---|---|
| Label generation (D19) | HPC, `scripts/slurm/labels.sbatch` (job array, smallest MPS share, CPU only) | Embarrassingly parallel over instances |
| Multi-seed training | HPC, `scripts/slurm/train.sbatch` (one job per model and seed, ≤ half a card) | Several seeds share cards through MPS |
| Test-split evaluation, all timing | M4 only | One machine for every timing number; the test-access log stays in one place |

HPC runs never produce a reported time. Their batches and checkpoints record
the commit and hardware like any other run.

## Setup (once, on the login node)

```bash
git clone https://github.com/DevanshSharma867/learned-heuristics-attack-graphs.git
cd learned-heuristics-attack-graphs
git checkout <commit to run at>
uv sync --frozen
```

`data/derived/cves.csv` is tracked, so no NVD download is needed. Both
scripts refuse to run on a dirty tree.

## Labels

```bash
sbatch --array=0-23 --export=ALL,SPLIT=train,N_SHARDS=24 scripts/slurm/labels.sbatch
```

- Each array task labels the shard `seeds[k::N_SHARDS]` of the split. It
  writes its own batch,
  `data/labels/<split>-<config sha>-<commit>-s<k>of<N>/`.
- Repeat for `val` and each test split.
- Copy the batches back with
  `rsync -a csisnlp_18@hpc.bits-hyderabad.ac.in:<repo>/data/labels/ data/labels/`
  (add `-e "ssh -i ~/.ssh/csisnlp_18"`).
- The local label pilot (`results/feasibility/label_pilot/`) gives the
  expected size and CPU-hours.

## Training

```bash
for s in 0 1 2 3 4; do
  sbatch --export=ALL,MODEL=gnn64x3,SEED=$s,LABELS="<train batch dirs>,<val batch dirs>" scripts/slurm/train.sbatch
done
```

- Not runnable yet: `scripts/train.py` is D17 week 2.
- The job sets `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=50` and
  `CUDA_MPS_PINNED_DEVICE_MEM_LIMIT=0=48G`, half the card's SMs and half of
  its 96 GB, on top of the gres request.

## Open placeholders (to fill from `docs/hpc/mock_job.sh`)

1. `#SBATCH --qos=SET_ME_QOS_FROM_TEMPLATE` in both scripts.
2. The gres line: currently `--gres=mps:1` for labels and `--gres=mps:50`
   for training, the standard SLURM MPS syntax (shares out of 100 per GPU).
   Replace both with the template's form if it differs.
3. Any account, module-load or MPS-daemon lines the template has.
4. Time, memory and CPU limits (`02:00:00` / 4G / 1 CPU for labels;
   `06:00:00` / 16G / 4 CPUs for training) are guesses, to be checked
   against the cluster's limits.
