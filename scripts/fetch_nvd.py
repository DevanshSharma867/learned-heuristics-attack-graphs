"""Download the pinned NVD snapshot (D11) into data/raw/nvd/<snapshot-date>/.

Usage: python scripts/fetch_nvd.py [snapshot-date]  (default: today, UTC)

The script runs one CVE API 2.0 query per product in FAMILY_PRODUCTS, in
pages of PAGE_SIZE records. 2000-record pages were cut off mid-transfer
during measurement, which is why the pages are small. Requests are paced at
one per PACE seconds, because without an API key NVD allows 5 per 30 s.
Each failed request gets one delayed retry. If that also fails, the script
stops without writing a manifest.

- **Page files.** Each page is saved as a gzipped JSON envelope:
  {url, params, fetched_utc, response}. A rerun skips pages already on disk,
  so a partial snapshot can be resumed.
- **Manifest.** manifest.json is written only once every page is present
  and each product's page count matches its totalResults. A snapshot that
  has a manifest is final: raw data is append-only (CLAUDE.md §1 rule 11),
  so the script refuses to touch it.
"""

import gzip
import hashlib
import http.client
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from ahg.cve import FAMILY_PRODUCTS

API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
PAGE_SIZE = 500
PACE = 6.5
RETRY_WAIT = 35
ROOT = Path(__file__).resolve().parent.parent

snapshot = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).date().isoformat()
out = ROOT / "data" / "raw" / "nvd" / snapshot
if (out / "manifest.json").exists():
    sys.exit(f"{out}/manifest.json exists: snapshot is final, refusing to modify it")
out.mkdir(parents=True, exist_ok=True)
_last = 0.0


def request(params: dict) -> tuple[str, dict]:
    """GET one page, paced, with a single delayed retry."""
    global _last
    url = API + "?" + urllib.parse.urlencode(params, safe=":/*")
    for attempt in (1, 2):
        wait = PACE - (time.time() - _last) if attempt == 1 else RETRY_WAIT
        if wait > 0:
            time.sleep(wait)
        _last = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ahg-nvd-snapshot"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return url, json.load(r)
        except (OSError, http.client.HTTPException, json.JSONDecodeError) as e:  # OSError covers HTTPError and drops
            print(f"  attempt {attempt} failed: {url}: {e!r}", flush=True)
    sys.exit(f"giving up on {url}; rerun to resume (pages already saved are kept)")


def page_path(family: str, product: str, start: int) -> Path:
    return out / f"{family}__{product.replace(':', '__')}__{start:05d}.json.gz"


def load_page(path: Path) -> dict:
    with gzip.open(path, "rt") as f:
        return json.load(f)


for family, products in FAMILY_PRODUCTS.items():
    for product in products:
        start, total = 0, None
        while total is None or start < total:
            path = page_path(family, product, start)
            if path.exists():
                env = load_page(path)
            else:
                params = {"virtualMatchString": f"cpe:2.3:*:{product}", "resultsPerPage": PAGE_SIZE, "startIndex": start}
                url, resp = request(params)
                env = {"url": url, "params": params, "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "response": resp}
                tmp = path.with_suffix(".tmp")
                with gzip.GzipFile(tmp, "wb", mtime=0) as f:  # mtime=0: bytes depend only on content
                    f.write(json.dumps(env, sort_keys=True).encode())
                tmp.rename(path)  # never leave a half-written page under the final name
            resp = env["response"]
            total = resp["totalResults"]
            start += PAGE_SIZE
            print(f"{family:5s} {product:40s} start={resp['startIndex']:5d} got={len(resp['vulnerabilities']):4d} total={total}", flush=True)

# Every page is present: verify completeness, then write the manifest.
files = []
for family, products in FAMILY_PRODUCTS.items():
    for product in products:
        pages = sorted(out.glob(f"{family}__{product.replace(':', '__')}__*.json.gz"))
        envs = [load_page(p) for p in pages]
        got = sum(len(e["response"]["vulnerabilities"]) for e in envs)
        totals = {e["response"]["totalResults"] for e in envs}
        if len(totals) != 1 or got != totals.pop():
            sys.exit(f"{family}/{product}: {got} records across pages, totalResults {totals}; snapshot inconsistent")
        for p, e in zip(pages, envs):
            files.append({
                "path": p.name, "family": family, "product": product, "url": e["url"],
                "startIndex": e["response"]["startIndex"], "records": len(e["response"]["vulnerabilities"]),
                "totalResults": e["response"]["totalResults"], "fetched_utc": e["fetched_utc"],
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            })  # fmt: skip

commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
dirty = bool(subprocess.run(["git", "status", "--porcelain", "--", "scripts", "src"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
manifest = {
    "snapshot_date": snapshot, "api": API, "page_size": PAGE_SIZE, "pace_seconds": PACE,
    "script": "scripts/fetch_nvd.py", "git_commit": commit, "git_dirty_src_or_scripts": dirty,
    "written_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "files": files,
}  # fmt: skip
(out / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
print(f"\nmanifest: {out / 'manifest.json'}  ({len(files)} page files, git {commit[:7]}{' DIRTY' if dirty else ''})")
