from arsenal.forensics import desfa


def test_base64():
    strat, rezultat = desfa("U2FsdXQ=")

    assert strat == "base64"
    assert rezultat == b"Salut"


def test_hex():
    strat, rezultat = desfa("48656c6c6f")

    assert strat == "hex"
    assert rezultat == b"Hello"


def test_url():
    strat, rezultat = desfa("%2Fetc%2Fpasswd")

    assert strat == "url"
    assert rezultat == b"/etc/passwd"