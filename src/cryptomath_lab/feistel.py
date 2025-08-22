from __future__ import annotations
import hashlib
from typing import Tuple

def _prf_round(key: bytes, data: bytes) -> bytes:
    """Round function using SHA256(key || data) -> 16 bytes."""
    return hashlib.sha256(key + data).digest()[:16]

def _split_blocks(block: bytes) -> Tuple[bytes, bytes]:
    half = len(block)//2
    return block[:half], block[half:]

def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def feistel_encrypt_block(block: bytes, key: bytes, rounds: int = 4) -> bytes:
    """Encrypt a single even-length block with a toy Feistel network."""
    assert len(block) % 2 == 0 and len(block) > 0, "block must have even length > 0"
    L, R = _split_blocks(block)
    for r in range(rounds):
        F = _prf_round(key, R)
        L, R = R, _xor(L, F[: len(L)])
    return L + R

def feistel_decrypt_block(block: bytes, key: bytes, rounds: int = 4) -> bytes:
    """Decrypt a single even-length block with a toy Feistel network."""
    assert len(block) % 2 == 0 and len(block) > 0, "block must have even length > 0"
    L, R = _split_blocks(block)
    for r in range(rounds):
        F = _prf_round(key, L)
        L, R = _xor(R, F[: len(R)]), L
    return L + R

def feistel_encrypt(data: bytes, key: bytes, rounds: int = 4) -> bytes:
    # pad to even length with a single 0x00 if needed
    d = data if len(data) % 2 == 0 else data + b"\x00"
    return feistel_encrypt_block(d, key, rounds)

def feistel_decrypt(data: bytes, key: bytes, rounds: int = 4) -> bytes:
    pt = feistel_decrypt_block(data, key, rounds)
    # strip a possible 0x00 pad that we added
    return pt[:-1] if pt and pt[-1] == 0 else pt
