from __future__ import annotations
import binascii
import typer
from rich import print
from .prg import prg_sha256_counter, prg_lcg
from .feistel import feistel_encrypt, feistel_decrypt
from . import randtests

app = typer.Typer(help="cryptomath-lab CLI (educational)")

@app.command()
def prg(kind: str = typer.Argument(..., help="sha256 | lcg"),
        n: int = typer.Option(32, '--n', help='number of bytes'),
        seed: str = typer.Option("seed", '--seed', help='seed (string or integer for lcg)')):
    """Generate pseudo-random bytes."""
    if kind.lower() == 'sha256':
        out = prg_sha256_counter(seed.encode(), n)
    elif kind.lower() == 'lcg':
        try:
            s = int(seed)
        except ValueError:
            raise typer.BadParameter("LCG seed must be an integer")
        out = prg_lcg(s, n)
    else:
        raise typer.BadParameter("kind must be 'sha256' or 'lcg'")
    print(binascii.hexlify(out).decode())

@app.command()
def feistel(mode: str = typer.Argument(..., help="encrypt | decrypt"),
            key: str = typer.Option("key", '--key'),
            message: str = typer.Option(..., '--message', help='hex-encoded data'),
            rounds: int = typer.Option(4, '--rounds')):
    """Encrypt/decrypt with a toy Feistel network (hex in/out)."""
    data = binascii.unhexlify(message)
    k = key.encode()
    if mode == 'encrypt':
        out = feistel_encrypt(data, k, rounds)
    elif mode == 'decrypt':
        out = feistel_decrypt(data, k, rounds)
    else:
        raise typer.BadParameter("mode must be 'encrypt' or 'decrypt'")
    print(binascii.hexlify(out).decode())

@app.command()
def test(kind: str = typer.Argument(..., help="monobit | runs | chisq"),
         hex: str = typer.Option(..., '--hex', help='hex-encoded bytes')):
    data = binascii.unhexlify(hex)
    if kind == 'monobit':
        pv = randtests.monobit_pvalue(data)
    elif kind == 'runs':
        pv = randtests.runs_test_pvalue(data)
    elif kind == 'chisq':
        pv = randtests.chisq_bytes_pvalue(data)
    else:
        raise typer.BadParameter("unknown test")
    print({"p_value": pv})
