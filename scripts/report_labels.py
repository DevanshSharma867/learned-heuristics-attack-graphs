"""Summarise label batches and project the full label-set size and compute (D19 pilot).

Usage: python scripts/report_labels.py NAME BATCH_DIR [BATCH_DIR ...] [--no-write]

Reads only the batches' manifest.json and label files, and writes a run to
results/feasibility/<NAME>/ (raw.json.gz, report.md, provenance.json). It
reports, per batch:
  - states per labelled instance, by source (a state with several sources counts in each);
  - the h* distribution in effort units (D9: 38 stored units per unit), overall and by source;
  - time per instance and per state (search + cross-checks; workers as recorded);
  - disk size.
The projection scales the pilot's per-instance means to each split's seed count,
for splits drawn from the same distribution as the pilot (train, val, test_id,
test_vuln, test_vuln_cost). test_size (n = 30) and test_structure (hub_and_spoke)
are outside the pilot's distribution and are not projected.
"""

import argparse
import gzip
import json
import statistics
from pathlib import Path

from ahg.cost import SCALE
from ahg.labels import SOURCES
from ahg.runlog import write_run
from ahg.splits import SPLITS

ROOT = Path(__file__).resolve().parent.parent
PROJECTED = ("train", "val", "test_id", "test_vuln", "test_vuln_cost")
QUANTILES = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)


def quantiles(xs):
    xs = sorted(xs)
    return [xs[min(len(xs) - 1, int(q * len(xs)))] for q in QUANTILES] if xs else None


def summarise(batch_dir: Path) -> dict:
    m = json.loads((batch_dir / "manifest.json").read_text())
    rows = [json.loads(line) for line in gzip.decompress((batch_dir / "labels.jsonl.gz").read_bytes()).splitlines()]
    st = [r["stats"] for r in m["instances"] if r["stats"] is not None]
    per_inst = {src: [s["by_source"][src] for s in st] for src in SOURCES}
    h_units = lambda keep: [r["h"] / SCALE for r in rows if keep(r)]
    return {
        "batch_id": m["batch_id"], "split": m["split"], "workers": m["workers"], "git_commit":
            m["provenance"]["git_commit"], "git_dirty": m["provenance"]["git_dirty"],
        "instances": len(m["instances"]), "labelled": len(st), "failures": m["counts"]["failures"],
        "states": len(rows), "goal_states": m["counts"]["goal_states"],
        "states_per_instance": {"mean": statistics.mean(s["states"] for s in st),
                                "median": statistics.median(s["states"] for s in st),
                                "max": max(s["states"] for s in st)},
        "by_source_mean": {src: statistics.mean(v) for src, v in per_inst.items()},
        "successors_before_cap_median": statistics.median(s["successors_before_cap"] for s in st),
        "successor_capped": sum(s["successors_before_cap"] > m["config"]["successor_cap"] for s in st),
        "hstar_quantiles": quantiles(h_units(lambda r: True)),
        "hstar_quantiles_by_source": {src: quantiles(h_units(lambda r, src=src: src in r["src"])) for src in SOURCES},
        "seconds_per_instance": {"mean": statistics.mean(s["seconds"] for s in st),
                                 "median": statistics.median(s["seconds"] for s in st),
                                 "max": max(s["seconds"] for s in st)},
        "seconds_per_state": {"label_mean": sum(s["label_seconds"] for s in st) / len(rows),
                              "check_mean": sum(s["check_seconds"] for s in st) / len(rows),
                              "total_mean": sum(s["seconds"] for s in st) / len(rows),
                              "median_of_instances": statistics.median(s["seconds"] / s["states"] for s in st)},
        "oracle": {"checked": sum(s["oracle_checked"] for s in st), "skipped": sum(s["oracle_skipped"] for s in st),
                   "enumerated_instances": sum(s["enumerated"] for s in st)},
        "init_expanded_median": {h: statistics.median(s["init_expanded"][h] for s in st) for h in ("lmcut", "hmax")},
        "disk_bytes": sum(f.stat().st_size for f in batch_dir.iterdir()),
        "label_file_bytes": (batch_dir / "labels.jsonl.gz").stat().st_size,
        "elapsed_seconds": m["elapsed_seconds"],
    }


def project(batches: list[dict]) -> dict:
    """Pooled pilot rates -> projected totals for the in-distribution splits."""
    inst = sum(b["instances"] for b in batches)
    lab = sum(b["labelled"] for b in batches)
    states = sum(b["states"] for b in batches)
    sec = sum(b["seconds_per_instance"]["mean"] * b["labelled"] for b in batches)
    byte = sum(b["label_file_bytes"] for b in batches)
    rate = {"labelled_fraction": lab / inst, "states_per_labelled": states / lab, "seconds_per_labelled": sec / lab,
            "label_bytes_per_state": byte / states}
    out = {"rates": rate, "splits": {}}
    for name in PROJECTED:
        n = len(SPLITS[name].seeds)
        k = n * rate["labelled_fraction"]
        out["splits"][name] = {"seeds": n, "labelled": k, "states": k * rate["states_per_labelled"],
                               "cpu_hours": k * rate["seconds_per_labelled"] / 3600,
                               "label_mb": k * rate["states_per_labelled"] * rate["label_bytes_per_state"] / 1e6}
    out["total"] = {key: sum(s[key] for s in out["splits"].values()) for key in ("labelled", "states", "cpu_hours",
                                                                                 "label_mb")}
    return out


def render(raw) -> str:
    L = [f"# {raw['config']['name']}", "", "D19 label pilot. Feasibility and sizing only; no model is trained.", ""]
    for b in raw["batches"]:
        sp, q = b["states_per_instance"], b["hstar_quantiles"]
        L += [f"## {b['batch_id']} ({b['split']}; {b['workers']} worker(s); commit {b['git_commit'][:7]}"
              f"{', DIRTY' if b['git_dirty'] else ''})", "",
              f"- instances: {b['instances']}, labelled {b['labelled']}; failures {b['failures'] or 'none'}",
              f"- states: {b['states']} ({b['goal_states']} goal states); per labelled instance mean "
              f"{sp['mean']:.1f}, median {sp['median']:g}, max {sp['max']}",
              "- mean states per instance by source (a state counts once per source): "
              + ", ".join(f"{s} {v:.1f}" for s, v in b["by_source_mean"].items()),
              f"- successors before the cap: median {b['successors_before_cap_median']:g}; "
              f"capped on {b['successor_capped']} instances",
              f"- init expansions, median: LM-cut {b['init_expanded_median']['lmcut']:g}, "
              f"h_max {b['init_expanded_median']['hmax']:g}",
              f"- oracle: {b['oracle']['checked']} states checked, {b['oracle']['skipped']} over its pop budget; "
              f"enumeration on {b['oracle']['enumerated_instances']} instances", "",
              "h\\* in effort units (quantiles " + ", ".join(f"{x:g}" for x in QUANTILES) + "):", "",
              "| states | " + " | ".join(f"q{x:g}" for x in QUANTILES) + " |",
              "|---|" + "---|" * len(QUANTILES),
              "| all | " + " | ".join(f"{x:.2f}" for x in q) + " |"]
        for src, qs in b["hstar_quantiles_by_source"].items():
            L.append(f"| {src} | " + (" | ".join(f"{x:.2f}" for x in qs) if qs else "—") + " |")
        t, ts = b["seconds_per_instance"], b["seconds_per_state"]
        L += ["", f"- time per instance (s): mean {t['mean']:.2f}, median {t['median']:.2f}, max {t['max']:.2f}",
              f"- time per state (s): {ts['total_mean']:.4f} mean (search {ts['label_mean']:.4f}, "
              f"cross-checks {ts['check_mean']:.4f}); per-instance median {ts['median_of_instances']:.4f}",
              f"- disk: {b['disk_bytes'] / 1e3:.1f} kB ({b['label_file_bytes'] / 1e3:.1f} kB labels); "
              f"elapsed {b['elapsed_seconds']} s", ""]
    p = raw["projection"]
    r = p["rates"]
    L += ["## Projection (pooled pilot rates)", "",
          f"Labelled fraction {r['labelled_fraction']:.3f}; {r['states_per_labelled']:.1f} states and "
          f"{r['seconds_per_labelled']:.2f} s per labelled instance; {r['label_bytes_per_state']:.1f} bytes per label "
          "(gzip).", "", "| split | seeds | labelled (exp.) | states | CPU-hours | labels MB |", "|---|---|---|---|---|---|"]
    for name, s in list(p["splits"].items()) + [("total", {"seeds": "", **p["total"]})]:
        L.append(f"| {name} | {s['seeds']} | {s['labelled']:.0f} | {s['states']:,.0f} | {s['cpu_hours']:.2f} "
                 f"| {s['label_mb']:.2f} |")
    L += ["", "test_size (n = 30) and test_structure (hub_and_spoke) are outside the pilot distribution and are "
          "not projected here."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("batches", nargs="+", type=Path)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    batches = [summarise(d) for d in args.batches]
    config = {"name": args.name, "batches": [str(d) for d in args.batches], "projected_splits": list(PROJECTED)}
    raw = {"config": config, "batches": batches, "projection": project(batches)}
    if args.no_write:
        print(render(raw))
        return
    print(render(raw))
    print("wrote", write_run(args.name, raw, render(raw), [], config, root=ROOT / "results" / "feasibility"))


if __name__ == "__main__":
    main()
