"""Assign CVEs to a network's services, deterministically from a seed.

Each service gets one CVE, drawn uniformly (with replacement across
services) from the CVEs of its service family.

The caller passes the CVE pool. That is how a vulnerability-shift split
will restrict which CVEs a dataset may use: by filtering the pool, without
touching this code.
"""

import random
from collections import defaultdict

from .cve import CveRecord
from .network import Network


def assign_cves(net: Network, pool: list[CveRecord], seed: int) -> dict[int, CveRecord]:
    """Map service id -> CveRecord.

    The rng is seeded on ("cves", topology family, seed), following D10's
    "family:seed" convention, so the same seed does not give correlated
    draws across topology families. The "cves" prefix keeps this stream
    separate from the topology generator's own "family:seed" stream.
    Otherwise the CVE draws would replay, and correlate with, the draws that
    built the network.

    The pool is sorted before drawing, so the result does not depend on the
    order of the input list.
    """
    rng = random.Random(f"cves:{net.meta['family']}:{seed}")
    by_family: dict[str, list[CveRecord]] = defaultdict(list)
    for r in sorted(pool):
        by_family[r.family].append(r)
    out = {}
    for s in net.services:  # id order, so the draw sequence is fixed
        candidates = by_family.get(s.family)
        if not candidates:
            raise ValueError(f"no CVEs in the pool for service family {s.family!r}")
        out[s.id] = rng.choice(candidates)
    return out
