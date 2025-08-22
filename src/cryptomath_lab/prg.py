from __future__ import annotations
import hashlib
from typing import Iterator

def prg_sha256_counter(seed: bytes, nbytes: int) -> bytes:
    """SHA256-based counter PRG (educational).
    Expands (seed, counter) -> SHA256(seed || counter).
    """
    out = bytearray()
    counter = 0
    while len(out) < nbytes:
        h = hashlib.sha256(seed + counter.to_bytes(8, 'big')).digest()
        out.extend(h)
        counter += 1
    return bytes(out[:nbytes])

def prg_lcg(seed: int, nbytes: int) -> bytes:
    """Simple 32-bit LCG -> bytes (educational, not secure).
    X_{k+1} = (a X_k + c) mod m, then pack outputs into bytes.
    """
    a = 1664525
    c = 1013904223
    m = 2**32
    x = seed % m
    out = bytearray()
    while len(out) < nbytes:
        x = (a * x + c) % m
        out.extend(x.to_bytes(4, 'big'))
    return bytes(out[:nbytes])

def bytes_from_iter(it: Iterator[int]) -> bytes:
    return bytes(bytearray(it))
