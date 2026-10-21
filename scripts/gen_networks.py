"""Generate one network per topology family, print a summary, save the JSON.

Usage: python scripts/gen_networks.py [out_dir] [n_hosts] [seed]
out_dir defaults to a temp directory; the JSON is for inspection, not committed.
"""

import sys
import tempfile
from pathlib import Path

from ahg.network import INTERNET, structure_stats
from ahg.topology import GENERATORS

out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else Path(tempfile.gettempdir()) / "ahg_networks")
n_hosts = int(sys.argv[2]) if len(sys.argv) > 2 else 8
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
out_dir.mkdir(parents=True, exist_ok=True)

for family, gen in GENERATORS.items():
    net = gen(seed, n_hosts)
    path = out_dir / f"{family}_n{n_hosts}_s{seed}.json"
    path.write_text(net.to_json())
    name = {h.id: h.name for h in net.hosts}
    svc = {s.id: s for s in net.services}
    print(f"=== {family}  seed={seed}  params={net.meta['params']}")
    print("    stats:", structure_stats(net))
    for h in net.hosts:
        fams = ",".join(s.family for s in net.services if s.host == h.id) or "-"
        reaches = sorted({f"{name[svc[r.service].host]}:{svc[r.service].family}" for r in net.reach if r.src == h.id})
        trusts = [name[t.dst] for t in net.trust if t.src == h.id]
        line = f"    {h.name:10s} services=[{fams}]"
        line += f"\n        reaches: {', '.join(reaches) or '-'}"
        if h.id != INTERNET:
            line += f"\n        control gives login on: {', '.join(trusts) or '-'}"
        print(line)
    print(f"    saved {path}\n")
