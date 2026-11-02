"""The D23 §2 statistics: nested bootstrap, Wilcoxon signed-rank, Holm correction, rank-biserial effect size.

Pure Python plus torch (the only numeric dependency of the project), so no new package is pinned. Every
function is deterministic: bootstrap resamples come from a torch.Generator seeded by a string key.

Conventions (fixed by D23 §2 and D24 §6):
- Ratios are analysed as logs. The point estimate is exp(mean of log ratios over instances and seeds).
- Nested bootstrap: each resample draws instances with replacement, then, within each drawn instance,
  seeds with replacement from that model's seeds. A plain instance bootstrap is the special case of one seed.
- Wilcoxon signed-rank, two-sided, on per-instance paired differences d_i; zero differences are dropped
  (Wilcoxon's original treatment, scipy's default "wilcox"). Exact null distribution when n <= 50 and the
  |d| have no ties; otherwise the normal approximation with tie correction and continuity correction
  (scipy's defaults, so values can be checked against it).
- Effect size: matched-pairs rank-biserial r = (W+ - W-) / (W+ + W-), on the same nonzero pairs; r > 0 means
  the differences are mostly positive.
"""

import hashlib
import math

import torch

BOOTSTRAP = 10_000


def _generator(key: str) -> torch.Generator:
    return torch.Generator().manual_seed(int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "big") >> 1)


def nested_bootstrap(logs: list[list[float]], key: str, n: int = BOOTSTRAP) -> list[float] | None:
    """Geometric mean and 95% percentile CI of exp(logs), logs[instance][seed] (NaN = missing, ignored).

    Instances are the outer unit and seeds the inner one (D23 §2); with one seed per instance this is the
    instance bootstrap of evaluate._geo_ci, but with a different random stream.
    """
    if not logs:
        return None
    x = torch.tensor(logs, dtype=torch.float64)  # [I, S]
    if torch.isnan(x).all():
        return None
    I, S = x.shape
    g = _generator(key)
    ii = torch.randint(I, (n, I), generator=g)
    ss = torch.randint(S, (n, I, S), generator=g)
    draws = x[ii[..., None], ss]  # [n, I, S]
    means = torch.nanmean(draws.reshape(n, -1), dim=1).sort().values
    lo, hi = means[int(0.025 * n)], means[int(0.975 * n) - 1]
    return [math.exp(float(torch.nanmean(x))), math.exp(float(lo)), math.exp(float(hi))]


def _ranks(values: list[float]) -> list[float]:
    """Ranks 1..n of values, ties given their average rank."""
    order = sorted(range(len(values)), key=lambda k: values[k])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def _exact_two_sided(w_plus: float, n: int) -> float:
    """P(W+ as extreme as observed) under H0, no ties: W+ is the sum of a random subset of 1..n."""
    counts = [1] + [0] * (n * (n + 1) // 2)
    for k in range(1, n + 1):
        for t in range(len(counts) - 1, k - 1, -1):
            counts[t] += counts[t - k]
    total = 2 ** n
    lo = min(w_plus, n * (n + 1) / 2 - w_plus)
    p = 2 * sum(counts[t] for t in range(int(math.floor(lo)) + 1)) / total
    return min(1.0, p)


def wilcoxon(d: list[float]) -> dict:
    """Two-sided Wilcoxon signed-rank test of median(d) = 0, plus the matched-pairs rank-biserial r."""
    nz = [x for x in d if x != 0]
    n = len(nz)
    out = {"n": len(d), "n_nonzero": n, "zeros": len(d) - n}
    if n == 0:
        return {**out, "w_plus": 0.0, "w_minus": 0.0, "p": 1.0, "method": "none", "rank_biserial": 0.0}
    r = _ranks([abs(x) for x in nz])
    w_plus = sum(rk for rk, x in zip(r, nz) if x > 0)
    w_minus = sum(rk for rk, x in zip(r, nz) if x < 0)
    ties = len(set(abs(x) for x in nz)) < n
    if n <= 50 and not ties:
        p, method = _exact_two_sided(w_plus, n), "exact"
    else:
        mean = n * (n + 1) / 4
        tie_term = 0.0
        for v in set(abs(x) for x in nz):
            t = sum(abs(x) == v for x in nz)
            tie_term += t ** 3 - t
        sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24 - tie_term / 48)
        z = (abs(w_plus - mean) - 0.5) / sd if sd > 0 else 0.0
        p, method = min(1.0, math.erfc(max(z, 0.0) / math.sqrt(2))), "normal"
    return {**out, "w_plus": w_plus, "w_minus": w_minus, "p": p, "method": method,
            "rank_biserial": (w_plus - w_minus) / (w_plus + w_minus)}


def holm(p: list[float]) -> list[float]:
    """Holm step-down adjusted p-values, in the input order (family-wise error control)."""
    m = len(p)
    order = sorted(range(m), key=lambda k: p[k])
    adj, running = [0.0] * m, 0.0
    for rank, k in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[k]))
        adj[k] = running
    return adj


BEATS, LOSES, NO_DIFFERENCE = "beats", "loses", "no difference shown"


def verdict(ci: list[float], p_holm: float, threshold: float = 0.90, alpha: float = 0.01) -> str:
    """D17 §2 / D23 §2: beats if ratio <= 0.90, CI upper < 1 and Holm p < 0.01; loses if ratio >= 1/0.90,
    CI lower > 1 and Holm p < 0.01; otherwise no difference shown."""
    est, lo, hi = ci
    if p_holm < alpha and est <= threshold and hi < 1:
        return BEATS
    if p_holm < alpha and est >= 1 / threshold and lo > 1:
        return LOSES
    return NO_DIFFERENCE
