"""Build data/derived/cves.csv and build_log.json from a pinned NVD snapshot (D11).

Usage: python scripts/derive_cves.py [snapshot-date]  (default: the latest snapshot)

Every page file's SHA-256 is checked against manifest.json before anything is
parsed, so the table can only be built from the exact bytes the manifest
describes. The outputs are fully determined by the snapshot: rerunning gives
byte-identical files.
"""

import gzip
import hashlib
import json
import sys
from pathlib import Path

from ahg.cve import OUTCOMES, WINDOW, derive, write_table

ROOT = Path(__file__).resolve().parent.parent

# Provenance annotations for specific snapshots. The manifest is final raw
# data and is never edited, so facts learned about a snapshot after it was
# written are recorded here and copied into the build log.
PROVENANCE_NOTES = {
    "2026-10-21": (
        "The manifest's git_dirty_src_or_scripts flag is true only because new untracked files "
        "(scripts/derive_cves.py, src/ahg/cost.py, src/ahg/assign.py) existed under scripts/ and src/ during the fetch. "
        "The code that ran (scripts/fetch_nvd.py, src/ahg/cve.py) was byte-identical to the recorded commit bcf91c8 "
        "(empty git diff), so the snapshot's provenance is clean."
    ),
}

snapshots = ROOT / "data" / "raw" / "nvd"
snap = snapshots / sys.argv[1] if len(sys.argv) > 1 else max(p for p in snapshots.iterdir() if (p / "manifest.json").exists())
manifest_bytes = (snap / "manifest.json").read_bytes()
manifest = json.loads(manifest_bytes)

matches = []
for entry in manifest["files"]:
    raw = (snap / entry["path"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        sys.exit(f"checksum mismatch for {entry['path']}: snapshot was modified")
    resp = json.loads(gzip.decompress(raw))["response"]
    matches += [(entry["family"], entry["product"], v["cve"]) for v in resp["vulnerabilities"]]

records, counts = derive(matches)

out = ROOT / "data" / "derived"
out.mkdir(parents=True, exist_ok=True)
write_table(records, out / "cves.csv")

# Every outcome is listed for every family, so a 0 is an explicit zero, not an omission.
per_family = {fam: {o: counts[fam, o] for o in OUTCOMES} for fam in sorted({f for f, _ in counts})}
log = {
    "decision": "D11",
    "snapshot_date": manifest["snapshot_date"],
    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "fetch_git_commit": manifest["git_commit"],
    "window": [WINDOW[0].isoformat(), WINDOW[1].isoformat()],
    "rows": len(records),
    "provenance_note": PROVENANCE_NOTES.get(manifest["snapshot_date"]),
    "counts": per_family,  # family -> reason -> CVEs; "included" + one exclusion reason per (CVE, family)
}
(out / "build_log.json").write_text(json.dumps(log, indent=1, sort_keys=True) + "\n")
print(json.dumps(log, indent=1, sort_keys=True))
