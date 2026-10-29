"""Exact cost-to-go label batches (D14, as updated by D19).

Per instance: sample states from four sources (D19 §2), label each with
A*+LM-cut (D19 §3), cross-check, then write an append-only batch under
data/labels/<batch-id>/ (D19 §4). Everything is computed in memory first, so
a cross-check failure (HardFailure) leaves nothing on disk.

Why the sources: A* evaluates h on the successors of the states it expands,
and random walks under-represent the states where classical heuristics err
(D17 §1, per-instance sign test). A learned heuristic must be accurate where
A* evaluates it, so those states are labelled as well as the walk states.
"""

import gzip
import hashlib
import json
import random
import time
from pathlib import Path

from .attack_graph import KnobInfeasible, UnreachableGoal, make_instance
from .cve import load_table
from .heuristics import hmax, lmcut
from .measure import HardFailure, check_admissible, enumerate_exact, sample_states
from .oracle import optimal_cost
from .runlog import provenance
from .search import astar
from .splits import SPLITS, cve_pool, record_test_access
from .task import Task, task_digest

ROOT = Path(__file__).resolve().parents[2]
LABELS = ROOT / "data" / "labels"
CVES = ROOT / "data" / "derived" / "cves.csv"
LABELS_FILE, FAILURES_FILE, MANIFEST = "labels.jsonl.gz", "failures.jsonl.gz", "manifest.json"
SOURCES = ("optimal_path", "walk", "expanded_lmcut", "expanded_hmax", "successor")
CONFIG_KEYS = {"walk_cap", "walks_per_sample", "successor_cap", "init_budget", "state_budget",
               "oracle_all_max_n", "oracle_states", "oracle_max_pops", "enum_cap"}


def config_sha(cfg: dict) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()


def _rng(source: str, key: str) -> random.Random:
    return random.Random(f"labels:{source}:{key}")


def label_instance(task: Task, key: str, n_hosts: int, cfg: dict) -> dict:
    """Sample and label one instance. key names its rng streams ("<variant>:<n>:<seed>").

    Returns {"rows": [[state, h*, sources], ...] sorted by state, "failures": [...], "stats": {...}}.
    Raises HardFailure on any cross-check mismatch.
    """
    t0 = time.perf_counter()
    tr_lm, tr_hm = [], []
    r_lm = astar(task, lmcut, max_expansions=cfg["init_budget"], trace=tr_lm)
    r_hm = astar(task, hmax, max_expansions=cfg["init_budget"], trace=tr_hm)
    if r_lm.budget_hit:
        return {"rows": [], "failures": [{"kind": "init_budget", "expanded": r_lm.expanded}], "stats": None}
    if not r_lm.solved:
        # make_instance guarantees a reachable goal (UnreachableGoal otherwise), so this is a bug.
        raise HardFailure("goal unreachable from the initial state of a generated instance")
    if r_hm.solved and r_hm.cost != r_lm.cost:
        raise HardFailure(f"A*+h_max {r_hm.cost} != A*+LM-cut {r_lm.cost} from the initial state")

    sources: dict[int, set[str]] = {}

    def add(states, source):
        for s in states:
            sources.setdefault(s, set()).add(source)

    # 1. The optimal path, labelled from the suffix costs of the one plan.
    known, s, rest = {}, task.init, r_lm.cost
    path = [s]
    for ai in r_lm.plan:
        known[s] = rest
        s, rest = s | task.actions[ai].add_mask, rest - task.actions[ai].cost
        path.append(s)
    known[s] = 0
    add(path, "optimal_path")
    # 2. Random-walk states (D14 §2).
    walk, _ = sample_states(task, _rng("walk", key), cfg["walk_cap"], cfg["walks_per_sample"])
    add(walk, "walk")
    # 3. States the two A* searches expanded, and 4. their generated successors.
    expanded = list(dict.fromkeys(tr_lm + tr_hm))
    add(dict.fromkeys(tr_lm), "expanded_lmcut")
    add(dict.fromkeys(tr_hm), "expanded_hmax")
    succ = sorted({s2 for s in expanded for _, s2 in task.successors(s)})
    if len(succ) > cfg["successor_cap"]:
        succ = sorted(_rng("successor", key).sample(succ, cfg["successor_cap"]))
    add(succ, "successor")

    # Label every state: A*+LM-cut from it, unless a known optimal plan suffix already gives h*.
    rows, failures, label_expansions = [], [], 0
    t_label = time.perf_counter()
    for s in sorted(sources):
        if s not in known:
            r = astar(task, lmcut, start=s, max_expansions=cfg["state_budget"])
            label_expansions += r.expanded
            if r.budget_hit:
                failures.append({"kind": "label_budget", "state": hex(s), "sources": sorted(sources[s])})
                continue
            st, rest = s, r.cost
            for ai in r.plan:  # every state on this optimal plan gets its suffix cost
                known.setdefault(st, rest)
                st, rest = st | task.actions[ai].add_mask, rest - task.actions[ai].cost
            known.setdefault(st, 0)
        rows.append([s, known[s], sorted(sources[s])])
    label_s = time.perf_counter() - t_label

    # Cross-checks (D19 §3); any mismatch aborts the whole batch.
    t_check = time.perf_counter()
    for s, h, _ in rows:
        check_admissible(task, s, h)
    exact = enumerate_exact(task, cfg["enum_cap"])
    if exact is not None:
        for s, h, _ in rows:
            if exact[s] != h:
                raise HardFailure(f"enumeration h*={exact[s]} != label {h} at {s:#x}")
    if n_hosts <= cfg["oracle_all_max_n"]:
        to_check = rows
    else:
        to_check = sorted(_rng("oracle", key).sample(rows, min(cfg["oracle_states"], len(rows))))
    oracle_checked = oracle_skipped = 0
    for s, h, _ in to_check:
        o = optimal_cost(task, s, max_pops=cfg["oracle_max_pops"])
        if o is None:
            oracle_skipped += 1  # recorded as not checked, never as agreement
        elif o != h:
            raise HardFailure(f"oracle {o} != label {h} at {s:#x}")
        else:
            oracle_checked += 1

    by_source = {src: sum(src in r[2] for r in rows) for src in SOURCES}
    stats = {"states": len(rows), "by_source": by_source, "goal_states": sum(r[1] == 0 for r in rows),
             "successors_before_cap": len({s2 for s in expanded for _, s2 in task.successors(s)}),
             "init_expanded": {"lmcut": r_lm.expanded, "hmax": r_hm.expanded}, "hmax_budget_hit": r_hm.budget_hit,
             "hstar_init": r_lm.cost, "plan_len": len(r_lm.plan), "label_expansions": label_expansions,
             "label_seconds": round(label_s, 4), "check_seconds": round(time.perf_counter() - t_check, 4),
             "enumerated": exact is not None, "oracle_checked": oracle_checked, "oracle_skipped": oracle_skipped,
             "seconds": round(time.perf_counter() - t0, 4)}
    return {"rows": rows, "failures": failures, "stats": stats}


def label_seed(split_name: str, seed: int, cfg: dict, pool: list) -> dict:
    """Build and label the instance a split seed stands for. Generation failures are records (rule 10)."""
    spec = SPLITS[split_name].instance_spec(seed)
    try:
        inst = make_instance(spec["family"], seed, spec["n"], pool, cred_levels=spec["D"], coupling=spec["rho"],
                             share_pool=spec["m"], exposed_level0=spec["exposed_level0"], **spec["params"])
    except (UnreachableGoal, KnobInfeasible) as e:
        kind = "unreachable" if isinstance(e, UnreachableGoal) else "generation_failure"
        return {"spec": spec, "task_digest": None, "rows": [], "failures": [{"kind": kind, "reason": str(e)}],
                "stats": None}
    key = f"{spec['variant']}:{spec['n']}:{seed}"
    try:
        out = label_instance(inst.task, key, spec["n"], cfg)
    except HardFailure as e:
        raise HardFailure(f"{split_name} seed {seed} ({key}): {e}") from None
    return {"spec": spec, "task_digest": task_digest(inst.task), "facts": len(inst.task.facts),
            "actions": len(inst.task.actions), **out}


def _gz_lines(records) -> bytes:
    return gzip.compress("".join(json.dumps(r, sort_keys=True) + "\n" for r in records).encode(), mtime=0)


def write_batch(split_name: str, seeds: list[int], cfg: dict, root: Path | None = None,
                shard: tuple[int, int] | None = None, tag: str | None = None, workers: int = 1,
                allow_dirty: bool = False, test_log: Path | None = None) -> Path:
    """Label the instances of `seeds` (all in one split) and write one batch; return its directory.

    shard: (k, K) for the k-th of K SLURM array shards; tag: e.g. "pilot". Both only name the batch.
    workers: instances labelled in parallel (results are kept in seed order, so
    the files do not depend on it; per-state timings do).
    """
    if set(cfg) != CONFIG_KEYS:
        raise ValueError(f"label config keys {sorted(cfg)} != {sorted(CONFIG_KEYS)}")
    split = SPLITS[split_name]
    members = set(split.seeds)
    bad = [s for s in seeds if s not in members]
    if bad:
        raise ValueError(f"seeds {bad[:10]} are not in split {split_name} ({split.ranges})")
    prov = provenance(list(seeds), cfg)
    if prov["git_dirty"] and not allow_dirty:
        raise RuntimeError("working tree is dirty: commit first, or pass allow_dirty for a throwaway batch")
    sha = config_sha(cfg)
    batch_id = (f"{split_name}-{sha[:8]}-{prov['git_commit'][:7]}" + (f"-s{shard[0]}of{shard[1]}" if shard else "")
                + (f"-{tag}" if tag else ""))
    out = (root or LABELS) / batch_id
    if out.exists():
        raise FileExistsError(f"{out} exists; label batches are append-only")
    if split.is_test:
        # Generating a test batch reads no model and no labels; it is still logged (D19 §1).
        record_test_access(batch_id, split_name, "label generation", prov["git_commit"], log=test_log)

    full_pool = load_table(CVES)
    pool = cve_pool(full_pool, split.pool)
    t0 = time.perf_counter()
    if workers > 1:
        from multiprocessing import Pool
        with Pool(workers) as p:
            results = p.starmap(label_seed, [(split_name, s, cfg, pool) for s in seeds])
    else:
        results = [label_seed(split_name, s, cfg, pool) for s in seeds]

    rows, failures = [], []
    for i, res in enumerate(results):
        rows += [{"i": i, "s": hex(s), "h": h, "src": src} for s, h, src in res["rows"]]
        failures += [{"i": i, **f} for f in res["failures"]]
    labels_gz, failures_gz = _gz_lines(rows), _gz_lines(failures)
    manifest = {
        "batch_id": batch_id, "split": split_name, "shard": shard, "tag": tag, "config": cfg, "config_sha256": sha,
        "content_sha256": hashlib.sha256(labels_gz + failures_gz).hexdigest(),
        "cves_csv_sha256": hashlib.sha256(CVES.read_bytes()).hexdigest(), "cve_pool": split.pool,
        "cve_pool_size": len(pool), "decisions": ["D14", "D17", "D19"],
        "solver": "A*+LM-cut (src/ahg/search.py, src/ahg/heuristics.py)",
        "cross_checks": ["oracle UCS (src/ahg/oracle.py)", "enumeration (measure.enumerate_exact)",
                         "h_max, LM-cut <= h*", "A*+h_max = A*+LM-cut from the initial state"],
        "rng_streams": {s: f"labels:{s}:<variant>:<n>:<seed>" for s in ("walk", "successor", "oracle")},
        "instances": [{k: r.get(k) for k in ("spec", "task_digest", "facts", "actions", "stats")} for r in results],
        "counts": {"instances": len(results), "labelled_instances": sum(r["stats"] is not None for r in results),
                   "states": len(rows), "goal_states": sum(r["h"] == 0 for r in rows),
                   "failures": {k: sum(f["kind"] == k for f in failures) for k in sorted({f["kind"] for f in failures})},
                   "by_source": {src: sum(src in r["src"] for r in rows) for src in SOURCES}},
        "elapsed_seconds": round(time.perf_counter() - t0, 1), "workers": workers, "provenance": prov,
    }
    out.mkdir(parents=True)
    (out / LABELS_FILE).write_bytes(labels_gz)
    (out / FAILURES_FILE).write_bytes(failures_gz)
    (out / MANIFEST).write_text(json.dumps(manifest, indent=1) + "\n")
    return out
