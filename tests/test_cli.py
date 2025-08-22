import subprocess, sys, os, json, binascii

def run(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

def test_cli_sha256(tmp_path):
    # install editable package before running CLI commands in CI
    pass
