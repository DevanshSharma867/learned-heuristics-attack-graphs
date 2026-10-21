"""D9: the exact integer encoding of the frozen cost model.

The model is c(a) = 1 + 9·(1 − x_a), with x_a = (k − 1)/38 and k = round(10·E),
where E is the NVD Primary CVSS v3.x exploitability sub-score. Costs are
stored in units of 1/38 effort unit:

    C = 38·c = 389 − 9k,  so C ∈ [38, 380] ↔ c ∈ [1, 10].

Integers keep search and LM-cut comparisons exact (D9).
"""

SCALE = 38  # stored cost units per effort unit
K_MIN, K_MAX = 1, 39  # E ∈ [0.1, 3.9] on NVD's one-decimal grid


def exploitability_k(e: float) -> int:
    """k = round(10·E), checked to be on the one-decimal grid.

    It must be round(), not int(). 10·E is not exact in floating point, and
    int() truncates a value like 31.999999999999996 down to 31.
    """
    k = round(10 * e)
    if abs(10 * e - k) >= 1e-9:
        raise ValueError(f"exploitability {e!r} is not on NVD's 0.1 grid")
    if not K_MIN <= k <= K_MAX:
        raise ValueError(f"exploitability {e!r} outside the CVSS v3 range [0.1, 3.9]")
    return k


def cost_units(e: float) -> int:
    """Integer action cost C = 389 − 9k for exploitability sub-score E."""
    return 389 - 9 * exploitability_k(e)
