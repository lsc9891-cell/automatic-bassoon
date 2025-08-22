from __future__ import annotations
from typing import Dict, Tuple
from math import erfc, sqrt

def monobit_pvalue(bits: bytes) -> float:
    """Monobit test (NIST SP800-22 style p-value).
    Convert bytes -> bit string, count ones vs zeros.
    """
    n = len(bits) * 8
    if n == 0:
        return 0.0
    s = 0
    for b in bits:
        for i in range(8):
            s += 1 if ((b >> i) & 1) else -1
    sobs = abs(s) / sqrt(n)
    return erfc(sobs / sqrt(2))

def runs_test_pvalue(bits: bytes) -> float:
    """Runs test p-value (simplified)."""
    n = len(bits) * 8
    if n < 100:
        return 0.0  # too small, return 0 to indicate 'not enough data'
    # proportion of ones
    ones = 0
    for b in bits:
        ones += bin(b).count("1")
    pi = ones / n
    if abs(pi - 0.5) >= 0.25:
        return 0.0  # fails precondition
    # count runs
    bitstr = ''.join(f'{b:08b}' for b in bits)
    Vn = 1 + sum(bitstr[i] != bitstr[i-1] for i in range(1, len(bitstr)))
    statistic = abs(Vn - 2 * n * pi * (1 - pi)) / (2 * sqrt(2 * n) * pi * (1 - pi))
    # two-sided normal approximation
    from math import erf
    return 1 - erf(statistic)

def chisq_bytes_pvalue(bits: bytes) -> float:
    """Chi-square test on byte frequencies (256 bins)."""
    n = len(bits)
    if n == 0:
        return 0.0
    from math import exp
    expected = n / 256
    counts = [0]*256
    for b in bits:
        counts[b] += 1
    chi = sum((c - expected)**2 / expected for c in counts if expected > 0)
    # Approximate p-value via survival function of chi-square with 255 dof
    # Using Wilson-Hilferty approximation
    k = 255.0
    z = ((chi / k)**(1/3) - (1 - 2/(9*k))) / sqrt(2/(9*k))
    # survival function ~ 1 - Phi(z)
    from math import erf
    return 0.5 * (1 - erf(z / sqrt(2)))
