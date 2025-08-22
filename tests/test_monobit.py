from cryptomath_lab.randtests import monobit_pvalue

def test_monobit_trivial():
    assert monobit_pvalue(b"\x00"*8) < 0.05  # very biased

def test_monobit_randomish():
    # a mixed pattern that shouldn't be insanely biased
    pv = monobit_pvalue(bytes(range(255)))  # remove one byte so it's not perfectly balanced
    assert 0.0001 < pv < 0.9999
