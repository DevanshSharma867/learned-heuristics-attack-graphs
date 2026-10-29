"""Write a measurement run into the repo with its provenance (CLAUDE.md rules 9 and 11).

Each run gets its own directory results/landscape/<name>/<UTC timestamp>-<commit>/
(or under another root, e.g. results/feasibility/)
holding raw.json (the measurements), report.md (rendered from raw.json) and
provenance.json (git commit, dirty flag, seeds, config, date, versions,
hardware). These are tracked in git, unlike results/raw/. A run directory
that already exists is never overwritten, so earlier runs stay as they were.
"""

import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANDSCAPE = ROOT / "results" / "landscape"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def hardware() -> dict:
    """CPU model, core counts and RAM (CLAUDE.md rule 9), on macOS or Linux; None where unknown.

    platform.processor() gives only "arm" on Apple silicon, so the CPU model
    comes from sysctl (macOS) or /proc/cpuinfo (Linux, e.g. the cluster).
    """
    cpu = ram = physical = None
    if sys.platform == "darwin":
        def sysctl(key):
            r = subprocess.run(["sysctl", "-n", key], capture_output=True, text=True)
            return r.stdout.strip() if r.returncode == 0 else None
        cpu, ram, physical = sysctl("machdep.cpu.brand_string"), sysctl("hw.memsize"), sysctl("hw.physicalcpu")
    elif Path("/proc/cpuinfo").exists():
        names = [line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                 if line.startswith("model name")]
        cpu = names[0] if names else None
        ram = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    return {"cpu_model": cpu, "logical_cores": os.cpu_count(),
            "physical_cores": int(physical) if physical else None,
            "ram_bytes": int(ram) if ram else None}


def library_versions() -> dict[str, str]:
    """Every distribution installed in the running environment, name -> version.

    Recording the whole environment, not a hand-kept list, means a new
    dependency (PyTorch, PyG) is stamped from its first run (CLAUDE.md rule 9).
    """
    return dict(sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions()))


def provenance(seeds: list[int], config: dict) -> dict:
    """The stamp CLAUDE.md rule 9 asks for. dirty=True means the numbers may not match the commit."""
    return {
        "date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "argv": sys.argv,
        "seeds": seeds,
        "config": config,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hardware": hardware(),
        "libraries": library_versions(),
    }


def write_run(name: str, raw: object, report_md: str, seeds: list[int], config: dict,
              root: Path | None = None) -> Path:
    """Write raw.json, report.md and provenance.json for one run; return its directory.

    root: parent of the run folders, results/landscape/ by default.
    """
    prov = provenance(seeds, config)
    stamp = prov["date_utc"].replace(":", "").replace("+0000", "Z")
    out = (root or LANDSCAPE) / name / f"{stamp}-{prov['git_commit'][:7]}"
    out.mkdir(parents=True, exist_ok=False)  # append-only: never overwrite a run (rule 11)
    (out / "raw.json").write_text(json.dumps(raw, indent=1) + "\n")
    (out / "report.md").write_text(report_md)
    (out / "provenance.json").write_text(json.dumps(prov, indent=1) + "\n")
    return out
