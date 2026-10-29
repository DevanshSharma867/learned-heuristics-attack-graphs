"""Feasibility microbenchmark: per-state inference time of untrained learned heuristics (D17 input).

Usage: python scripts/bench_inference.py [--limit N] [--devices cpu1,cpu,mps] [--no-write]

Speed only. Every model has randomly initialised weights (torch seed 0); no
training happens, and nothing here says anything about how well a learned
heuristic would guide search. It measures what one heuristic evaluation would
cost, so that D17 can ask whether a learned heuristic could win on end-to-end
time, inference included (CLAUDE.md rule 7).

Instances: every reachable D15+D16 instance at D = 3, n = 20 (seeds 0-19 of the
28 cells of that size and depth), rebuilt with make_instance exactly as the
full run built them. A*+LM-cut and A*+h_max are rerun; their expansion counts
must equal the run's (the search is deterministic), or the script aborts.

States: the first EXPANDED_CAP distinct states A*+LM-cut expands; for each, its
distinct generated successors, i.e. the states A* evaluates a heuristic on.
Per expanded node and heuristic, time is taken over all its successors:

  - h_max, LM-cut: one call per successor (src/ahg/heuristics.py).
  - mlp, gnn*: "single" = feature extraction + forward pass + .item() per
    successor; "batched" = features of all successors, one forward pass over
    the batch, then .tolist(). Feature extraction is always included.

Devices: cpu1 = CPU, torch.set_num_threads(1) (like one search worker);
cpu = CPU, torch's default thread count; mps = Apple GPU (the result is copied
back to the CPU, which synchronises).

Models. CLAUDE.md §2 fixes the inputs, not the sizes, so sizes are set here:
  - mlp: the §2 graph-level features (#facts, #actions, #held, h_sp(s), and the
    number, mean and min cost of applicable useful actions); 2 hidden layers of 64.
  - gnn64x3, gnn128x6: message passing over the fact-action graph. Fact nodes
    carry (held, is_goal), action nodes normalised cost + 7 static attributes
    (zeros here: their values do not change the time, their width does). Each
    layer passes fact -> action over preconditions, then action -> fact over add
    effects (mean aggregation); the readout uses the mean fact, mean action and
    goal-fact embeddings. Plain torch (index_add_), not PyG: the graph structure
    is built once per instance (timed as setup) and shared by every state, so a
    batch of successors is one [B, nodes, H] tensor.

Break-even (per instance, then the median over instances), from the full
D15+D16 run's recorded search times and expansion counts:
  o     = T_h0 / E_h0, the search's own overhead per expansion (UCS, trivial h);
  c*_lm = (T_lm - o E_lm) / N_lm, the largest per-state cost at which a heuristic
          with A*+LM-cut's expansion and evaluation counts would tie A*+LM-cut
          (N_lm = A*+LM-cut's heuristic evaluations, from the rerun);
  E*_hm = T_hm / (o + p), the largest expansion count at which a heuristic costing
          p per expansion would still beat A*+h_max; E*_lm likewise vs A*+LM-cut.
          p = per-state time x N_lm / E_lm for "single", the time of one batched
          call over a node's successors for "batched".
The same quantities are also computed from this script's own reruns, as a check
on the run's timings (which came from 6 parallel workers).
"""

import argparse
import importlib.util
import json
import statistics
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import torch
from torch import nn

from ahg.attack_graph import make_instance
from ahg.cve import load_table
from ahg.heuristics import hmax, hsp, lmcut
from ahg.runlog import write_run
from ahg.search import INF, astar, uniform_cost

ROOT = Path(__file__).resolve().parent.parent
RUN = Path("results/landscape/depth_coupling_sweep/full_d16/2026-10-28T142309Z-ab208e3")
D, N = 3, 20
EXPANDED_CAP = 20  # expanded states per instance whose successors are timed
TORCH_SEED = 0
COST_SCALE = 380  # largest action cost in D9 units, used to normalise costs
ACTION_DIM = 8
MLP_HIDDEN = 64
GNN_SIZES = {"gnn64x3": (64, 3), "gnn128x6": (128, 6)}
MODELS = ["mlp", *GNN_SIZES]

_spec = importlib.util.spec_from_file_location("dc", ROOT / "scripts" / "measure_depth_coupling.py")
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)
PARAMS = {v: p for _, v, p in dc.VARIANTS}


class GNN(nn.Module):
    def __init__(self, hidden, layers):
        super().__init__()
        self.enc_f = nn.Linear(2, hidden)
        self.enc_a = nn.Linear(ACTION_DIM, hidden)
        self.up_a = nn.ModuleList(nn.Linear(2 * hidden, hidden) for _ in range(layers))
        self.up_f = nn.ModuleList(nn.Linear(2 * hidden, hidden) for _ in range(layers))
        self.head = nn.Sequential(nn.Linear(3 * hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def forward(self, fx, g):
        """fx: [B, facts, 2] per-state fact features; g: the instance's static graph."""
        b, n_f, n_a = fx.shape[0], fx.shape[1], g.act_x.shape[0]
        f = torch.relu(self.enc_f(fx))
        a = torch.relu(self.enc_a(g.act_x)).expand(b, -1, -1)
        for up_a, up_f in zip(self.up_a, self.up_f):
            # An action sees the mean of its preconditions: the AND side of the graph.
            m_a = f.new_zeros(b, n_a, f.shape[2]).index_add_(1, g.pre_dst, f[:, g.pre_src]) * g.inv_pre
            a = torch.relu(up_a(torch.cat([a, m_a], -1)))
            # A fact sees the mean of the actions that add it: the OR side.
            m_f = f.new_zeros(b, n_f, f.shape[2]).index_add_(1, g.add_dst, a[:, g.add_src]) * g.inv_add
            f = torch.relu(up_f(torch.cat([f, m_f], -1)))
        return self.head(torch.cat([f.mean(1), a.mean(1), f[:, g.goal].mean(1)], -1)).squeeze(-1)


def make_model(name):
    torch.manual_seed(TORCH_SEED)
    if name == "mlp":
        return nn.Sequential(nn.Linear(7, MLP_HIDDEN), nn.ReLU(), nn.Linear(MLP_HIDDEN, MLP_HIDDEN), nn.ReLU(),
                             nn.Linear(MLP_HIDDEN, 1))
    return GNN(*GNN_SIZES[name])


def static_graph(task, dev):
    """The state-independent part of the GNN input, built once per instance."""
    pre = [(f, i) for i, a in enumerate(task.actions) for f in a.pre]
    add = [(i, f) for i, a in enumerate(task.actions) for f in a.add]
    n_f, n_a = len(task.facts), len(task.actions)
    deg_pre, deg_add = [0] * n_a, [0] * n_f
    for _, i in pre:
        deg_pre[i] += 1
    for _, f in add:
        deg_add[f] += 1
    t = lambda xs, dt=torch.long: torch.tensor(xs, dtype=dt, device=dev)
    act_x = [[a.cost / COST_SCALE] + [0.0] * (ACTION_DIM - 1) for a in task.actions]
    return SimpleNamespace(
        pre_src=t([f for f, _ in pre]), pre_dst=t([i for _, i in pre]),
        add_src=t([i for i, _ in add]), add_dst=t([f for _, f in add]),
        inv_pre=t([[1 / max(1, d)] for d in deg_pre], torch.float32),
        inv_add=t([[1 / max(1, d)] for d in deg_add], torch.float32),
        act_x=t(act_x, torch.float32), goal=t(list(task.goal)),
        is_goal=[int(f in task.goal) for f in range(n_f)])


def mlp_row(task, s):
    """The CLAUDE.md §2 MLP features of state s; h_sp(s) is computed here, so it is timed."""
    hs = hsp(task, s)
    costs = [a.cost for a in task.actions if a.applicable(s) and a.useful(s)]
    return [len(task.facts), len(task.actions), s.bit_count(), (1e3 if hs == INF else hs / COST_SCALE),
            len(costs), statistics.fmean(costs) / COST_SCALE if costs else 0.0,
            min(costs) / COST_SCALE if costs else 0.0]


def featurizer(name, task, g, dev):
    if name == "mlp":
        return lambda states: torch.tensor([mlp_row(task, s) for s in states], dtype=torch.float32, device=dev)
    n_f = len(task.facts)
    return lambda states: torch.tensor([[[(s >> i) & 1, g.is_goal[i]] for i in range(n_f)] for s in states],
                                       dtype=torch.float32, device=dev)


def time_model(name, model, task, nodes, dev):
    t0 = time.perf_counter()
    g = static_graph(task, dev) if name != "mlp" else None
    setup = time.perf_counter() - t0
    feat = featurizer(name, task, g, dev)
    fwd = (lambda x: model(x)) if name == "mlp" else (lambda x: model(x, g))

    def single(succ):
        t_feat, t0 = 0.0, time.perf_counter()
        for s in succ:
            t = time.perf_counter()
            x = feat([s])
            t_feat += time.perf_counter() - t
            fwd(x).item()
        return time.perf_counter() - t0, t_feat

    def batched(succ):
        t0 = time.perf_counter()
        x = feat(succ)
        t_feat = time.perf_counter() - t0
        fwd(x).tolist()
        return time.perf_counter() - t0, t_feat

    with torch.inference_mode():
        single(nodes[0]["succ"][:2]), batched(nodes[0]["succ"])  # warm-up, untimed
        out = []
        for nd in nodes:
            (s_t, s_f), (b_t, b_f) = single(nd["succ"]), batched(nd["succ"])
            out.append({"single_s": s_t, "single_feat_s": s_f, "batched_s": b_t, "batched_feat_s": b_f})
    return {"setup_s": setup, "nodes": out}


def prepare(rec, pool):
    """Rebuild one instance, rerun the searches, and time h_max and LM-cut on the chosen states."""
    inst = make_instance(rec["family"], rec["seed"], N, pool, cred_levels=D, coupling=rec["rho"],
                         share_pool=rec["m"], exposed_level0=True, **PARAMS[rec["variant"]])
    task = inst.task
    where = f"{rec['cell']} seed={rec['seed']}"
    if (len(task.facts), len(task.actions)) != (rec["facts"], rec["actions"]):
        sys.exit(f"{where}: rebuilt task differs from the run's")
    trace = []
    r_lm = astar(task, lmcut, trace=trace)
    r_hm = astar(task, hmax)
    r_h0 = uniform_cost(task)
    rex = rec["init"]["expanded"]
    if (r_lm.expanded, r_hm.expanded, r_h0.expanded) != (rex["lmcut"], rex["hmax"], rex["h0"]):
        sys.exit(f"{where}: rerun expansions differ from the run's")
    nodes = []
    for s in list(dict.fromkeys(trace))[:EXPANDED_CAP]:
        succ = list(dict.fromkeys(s2 for _, s2 in task.successors(s)))
        if not succ:
            continue
        nd = {"k": len(succ), "succ": succ}
        for hname, h in (("hmax", hmax), ("lmcut", lmcut)):
            t0 = time.perf_counter()
            for s2 in succ:
                h(task, s2)
            nd[f"{hname}_s"] = time.perf_counter() - t0
        nodes.append(nd)
    eff = rec["effort"]
    return task, nodes, {
        "cell": rec["cell"], "seed": rec["seed"], "variant": rec["variant"], "rho": rec["rho"], "m": rec["m"],
        "facts": rec["facts"], "actions": rec["actions"], "plan_len": eff["plan_len_lmcut"],
        "run": {"E": dict(rex), "T": dict(eff["seconds"])},
        "rerun": {h: {"expanded": r.expanded, "evaluations": r.evaluations, "seconds": r.seconds}
                  for h, r in (("lmcut", r_lm), ("hmax", r_hm), ("h0", r_h0))}}


def med(xs):
    return statistics.median(xs) if xs else None


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None


def per_state(nodes, key):
    """Median over an instance's nodes of seconds per successor state."""
    return med([nd[key] / nd["k"] for nd in nodes])


def break_even(inst, src, costs):
    """costs: method -> (per-state s, per-expansion s or None). Returns the per-instance break-even values."""
    E = {h: inst["rerun"][h]["expanded"] for h in ("lmcut", "hmax", "h0")}
    T = ({h: inst["run"]["T"][h] for h in E} if src == "run" else {h: inst["rerun"][h]["seconds"] for h in E})
    n_lm = inst["rerun"]["lmcut"]["evaluations"]
    o = T["h0"] / E["h0"]
    out = {"o_s": o, "c_star_lm_s": (T["lmcut"] - o * E["lmcut"]) / n_lm}
    for meth, (c, p_batch) in costs.items():
        p = p_batch if p_batch is not None else c * n_lm / E["lmcut"]
        out[meth] = {"p_s": p, "E_star_hm": T["hmax"] / (o + p), "E_star_lm": T["lmcut"] / (o + p)}
    return out


def summarise(instances, devices):
    """Per-instance per-state and per-expansion costs, then break-even values from the run and the rerun."""
    for inst in instances:
        nodes = inst["nodes"]
        cost = {"hmax": (per_state(nodes, "hmax_s"), None), "lmcut": (per_state(nodes, "lmcut_s"), None)}
        for dev in devices:
            for m in MODELS:
                bn = inst["bench"][dev][m]["nodes"]
                both = [{**a, "k": nd["k"]} for a, nd in zip(bn, nodes)]
                cost[f"{m}/{dev}/single"] = (per_state(both, "single_s"), None)
                cost[f"{m}/{dev}/batched"] = (per_state(both, "batched_s"), med([b["batched_s"] for b in bn]))
                inst.setdefault("feat_share", {})[f"{m}/{dev}/single"] = med(
                    [b["single_feat_s"] / b["single_s"] for b in bn])
                inst["feat_share"][f"{m}/{dev}/batched"] = med([b["batched_feat_s"] / b["batched_s"] for b in bn])
        inst["per_state_s"] = {k: v[0] for k, v in cost.items()}
        inst["break_even"] = {src: break_even(inst, src, cost) for src in ("run", "rerun")}


def ms(x, nd=3):
    return "—" if x is None else f"{1000 * x:.{nd}f}"


def render(raw):
    inst, cfg = raw["instances"], raw["config"]
    methods = list(inst[0]["per_state_s"])
    L = [f"# {cfg['name']}", "",
         "**Speed only: untrained, randomly initialised models. Nothing here is a result about learning.**", "",
         f"Instances: the {len(inst)} reachable D15+D16 instances at D = {D}, n = {N}, from `{cfg['source_run']}`. "
         f"Rerun expansions equal the run's on every instance. States: successors of the first {EXPANDED_CAP} "
         f"distinct A*+LM-cut-expanded states per instance ({sum(len(i['nodes']) for i in inst)} expanded nodes, "
         f"{sum(nd['k'] for i in inst for nd in i['nodes'])} successor states; median "
         f"{med([nd['k'] for i in inst for nd in i['nodes']]):g} successors per node). "
         f"torch {torch.__version__}; devices {', '.join(cfg['devices'])}.", "",
         "## Per-state cost (ms)", "",
         "Median over instances of the per-instance median time per successor state, and the 90th "
         "percentile over instances. Feature extraction included; `feat.` is its median share of that time.", "",
         "| method | per state | p90 | feat. |", "|---|---|---|---|"]
    for m in methods:
        xs = [i["per_state_s"][m] for i in inst]
        fs = [i["feat_share"][m] for i in inst] if m in inst[0].get("feat_share", {}) else []
        L.append(f"| {m} | {ms(med(xs))} | {ms(pct(xs, 0.9))} | {f'{med(fs):.0%}' if fs else '—'} |")
    for src, label in (("run", f"the full run's timings (`{cfg['source_run']}`)"),
                       ("rerun", "this script's own single-process reruns (consistency check)")):
        be = [i["break_even"][src] for i in inst]
        L += ["", f"## Break-even from {label}", "",
              f"- search overhead per expansion o (UCS): median {ms(med([b['o_s'] for b in be]))} ms",
              f"- **c\\*_lm, largest per-state cost to tie A*+LM-cut at LM-cut's expansion counts: median "
              f"{ms(med([b['c_star_lm_s'] for b in be]))} ms** (p10 {ms(pct([b['c_star_lm_s'] for b in be], 0.1))}, "
              f"p90 {ms(pct([b['c_star_lm_s'] for b in be], 0.9))})",
              f"- reference medians: A*+LM-cut expands {med([i['rerun']['lmcut']['expanded'] for i in inst]):g}, "
              f"A*+h_max {med([i['rerun']['hmax']['expanded'] for i in inst]):g}; optimal plan length "
              f"{med([i['plan_len'] for i in inst]):g} (a lower bound on any A* expansion count); "
              f"A*+LM-cut evaluations per expansion "
              f"{med([i['rerun']['lmcut']['evaluations'] / i['rerun']['lmcut']['expanded'] for i in inst]):.1f}",
              f"- self-check (the cost model should reproduce the classical searches' own counts): median E\\*_hm of "
              f"h_max = {med([b['hmax']['E_star_hm'] for b in be]):.1f} vs its actual "
              f"{med([i['rerun']['hmax']['expanded'] for i in inst]):g}; median E\\*_lm of LM-cut = "
              f"{med([b['lmcut']['E_star_lm'] for b in be]):.1f} vs its actual "
              f"{med([i['rerun']['lmcut']['expanded'] for i in inst]):g}", "",
              "E\\*_hm (E\\*_lm): the largest expansion count at which a heuristic with that per-expansion cost p still "
              "beats A*+h_max (A*+LM-cut). `≥ plan` = fraction of instances where E\\*_hm ≥ optimal plan length, i.e. "
              "where even a perfect heuristic of that cost would beat A*+h_max.", "",
              "| method | p per expansion (ms) | median E\\*_hm | median E\\*_lm | E\\*_hm ≥ plan |", "|---|---|---|---|---|"]
        for m in methods:
            p = med([b[m]["p_s"] for b in be])
            ehm, elm = med([b[m]["E_star_hm"] for b in be]), med([b[m]["E_star_lm"] for b in be])
            ok = sum(b[m]["E_star_hm"] >= i["plan_len"] for b, i in zip(be, inst)) / len(inst)
            L.append(f"| {m} | {ms(p)} | {ehm:.1f} | {elm:.1f} | {ok:.0%} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, help="first N instances only (pilot)")
    ap.add_argument("--devices", default="cpu1,cpu,mps")
    ap.add_argument("--no-write", action="store_true", help="print the report instead of writing a run")
    args = ap.parse_args()
    devices = [d for d in args.devices.split(",") if d != "mps" or torch.backends.mps.is_available()]
    default_threads = torch.get_num_threads()
    recs = [r for r in json.loads((ROOT / RUN / "raw.json").read_text())["instances"]
            if r["status"] == "ok" and r["D"] == D and r["n"] == N][:args.limit]
    pool = load_table(ROOT / "data" / "derived" / "cves.csv")
    t0 = time.perf_counter()
    prepared = []
    for j, rec in enumerate(recs, 1):
        prepared.append(prepare(rec, pool))
        print(f"[prepare {j}/{len(recs)} {time.perf_counter() - t0:6.0f}s] {rec['cell']} seed={rec['seed']}", flush=True)
    for dev_name in devices:
        torch.set_num_threads(1 if dev_name == "cpu1" else default_threads)
        dev = torch.device("mps" if dev_name == "mps" else "cpu")
        for m in MODELS:
            model = make_model(m).to(dev).eval()
            for task, nodes, info in prepared:
                info.setdefault("bench", {}).setdefault(dev_name, {})[m] = time_model(m, model, task, nodes, dev)
            print(f"[{dev_name} {m} {time.perf_counter() - t0:6.0f}s]", flush=True)
    torch.set_num_threads(default_threads)
    instances = []
    for _, nodes, info in prepared:
        info["nodes"] = [{k: v for k, v in nd.items() if k != "succ"} for nd in nodes]
        instances.append(info)
    summarise(instances, devices)
    config = {"name": "inference_microbench" + ("_pilot" if args.limit else ""), "source_run": str(RUN),
              "D": D, "n": N, "exposed_level0": True, "expanded_cap": EXPANDED_CAP, "torch_seed": TORCH_SEED,
              "devices": devices, "torch_default_threads": default_threads, "models": {
                  "mlp": {"inputs": 7, "hidden": [MLP_HIDDEN, MLP_HIDDEN]},
                  **{k: {"hidden": h, "layers": l, "action_dim": ACTION_DIM} for k, (h, l) in GNN_SIZES.items()}},
              "elapsed_seconds": round(time.perf_counter() - t0, 1)}
    raw = {"config": config, "instances": instances}
    report = render(raw)
    if args.no_write:
        print(report)
        return
    path = write_run(config["name"], raw, report, sorted({i["seed"] for i in instances}), config,
                     root=ROOT / "results" / "feasibility")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
