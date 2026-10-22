"""Write a measurement run into the repo with its provenance (CLAUDE.md rules 9 and 11).

Each run gets its own directory results/landscape/<name>/<UTC timestamp>-<commit>/
holding raw.json (the measurements), report.md (rendered from raw.json) and
provenance.json (git commit, dirty flag, seeds, config, date, versions,
hardware). These are tracked in git, unlike results/raw/. A run directory
that already exists is never overwritten, so earlier runs stay as they were.
"""

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANDSCAPE = ROOT / "results" / "landscape"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def provenance(seeds: list[int], config: dict) -> dict:
    """The stamp CLAUDE.md rule 9 asks for. dirty=True means the numbers may not match the commit.

    The package has no runtime dependencies yet, so the Python version is the
    only version recorded. TODO: once PyTorch (and PyG) become dependencies,
    add their versions here.
    """
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
    }


def write_run(name: str, raw: object, report_md: str, seeds: list[int], config: dict) -> Path:
    """Write raw.json, report.md and provenance.json for one run; return its directory."""
    prov = provenance(seeds, config)
    stamp = prov["date_utc"].replace(":", "").replace("+0000", "Z")
    out = LANDSCAPE / name / f"{stamp}-{prov['git_commit'][:7]}"
    out.mkdir(parents=True, exist_ok=False)  # append-only: never overwrite a run (rule 11)
    (out / "raw.json").write_text(json.dumps(raw, indent=1) + "\n")
    (out / "report.md").write_text(report_md)
    (out / "provenance.json").write_text(json.dumps(prov, indent=1) + "\n")
    return out
