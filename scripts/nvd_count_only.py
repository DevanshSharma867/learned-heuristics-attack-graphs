"""nvd_count.py FILE.tsv (label<TAB>query-string): NVD CVE API 2.0 count-only queries.

resultsPerPage=1 (the API's page-size parameter; 0 is tried first). Only totalResults is kept: the response
body is parsed in memory and discarded, never written. Each query is logged (label, query, time, HTTP,
totalResults, records_in_body) to data/raw/sources/2026-11-08/nvd_count_queries.jsonl. 6.5 s between
requests (the public rate the repo's fetch_nvd.py also uses)."""
import json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

LOG = Path("/Users/devanshsharma/projects/learned-heuristics-attack-graphs/data/raw/sources/2026-11-08/nvd_count_queries.jsonl")
BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0?"


def count(label, q):
    url = BASE + q + "&resultsPerPage=1"
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-w", "\n%{http_code}", url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    total = nrec = None
    try:
        d = json.loads(body)
        total, nrec = d.get("totalResults"), len(d.get("vulnerabilities", []))
    except Exception:
        pass
    rec = {"label": label, "query": url, "time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "http": code, "totalResults": total, "records_in_body_discarded": nrec}
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(code, total, label, flush=True)
    del body


if __name__ == "__main__":
    rows = [l.split("\t") for l in Path(sys.argv[1]).read_text().splitlines() if l.strip() and not l.startswith("#")]
    for i, (label, q) in enumerate(rows):
        if i:
            time.sleep(6.5)
        count(label, q)
