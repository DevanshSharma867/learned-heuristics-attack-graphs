"""fetch.py --batch FILE.tsv (name<TAB>url[<TAB>accept]): curl with its default user-agent into
data/raw/sources/2026-11-08/<name>; append {name,url,date_utc,http,bytes,sha256,content_type} to fetch_log.jsonl;
write a whitespace-normalised text copy of HTML pages to the scratchpad txt/ folder."""
import hashlib, html, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/devanshsharma/projects/learned-heuristics-attack-graphs")
OUT = ROOT / "data/raw/sources/2026-11-08"
TXT = Path("/private/tmp/claude-501/-Users-devanshsharma-projects-learned-heuristics-attack-graphs/8a74ae48-88c2-4e7d-8a01-0207a1b3f49a/scratchpad/txt")


def fetch(name, url, accept=None):
    dest = OUT / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sS", "-L", "--max-time", "180", "-o", str(dest), "-w", "%{http_code} %{content_type}", url]
    if accept:
        cmd[1:1] = ["-H", f"Accept: {accept}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    code, _, ctype = r.stdout.partition(" ")
    data = dest.read_bytes() if dest.exists() else b""
    rec = {"name": name, "url": url, "date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "http": code if r.returncode == 0 else f"{code} curl-exit-{r.returncode}: {r.stderr.strip()[:80]}",
           "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest() if data else None, "content_type": ctype}
    with (OUT / "fetch_log.jsonl").open("a") as f:
        f.write(json.dumps(rec) + "\n")
    if data and "html" in ctype:
        t = data.decode("utf-8", "replace")
        t = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", t)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        (TXT / (Path(name).name + ".txt")).write_text(re.sub(r"\s+", " ", t))
    print(rec["http"], rec["bytes"], name, ctype)


if __name__ == "__main__":
    for line in Path(sys.argv[2]).read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            p = line.split("\t")
            fetch(p[0], p[1], p[2] if len(p) > 2 else None)
