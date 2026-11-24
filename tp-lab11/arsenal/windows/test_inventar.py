
from arsenal.windows.inventar import (
    Proces,
    Eveniment,
    Inventar,
    incarca_procese,
    incarca_evenimente
)


# Test 1 - Verifica identificarea unui proces suspect
def test_proces_suspect():
    p = Proces(
        3120,
        "update.exe",
        "ana",
        "C:\\Users\\ana\\AppData\\Local\\Temp\\update.exe"
    )
    assert p.e_suspect() is True


# Test 2 - Verifica un proces normal
def test_proces_normal():
    p = Proces(
        1340,
        "explorer.exe",
        "ana",
        "C:\\Windows\\explorer.exe"
    )
    assert p.e_suspect() is False


# Test 3 - Verifica identificarea unui eveniment suspect
def test_eveniment_suspect():
    e = Eveniment(
        4625,
        "warning",
        "Security",
        "administrator",
        "An account failed to log on"
    )
    assert e.e_suspect() is True


# Test 4 - Verifica incarcarea datelor si numararea suspectilor
def test_inventar():
    p = incarca_procese("arsenal/windows/start/procese.json")
    e = incarca_evenimente("arsenal/windows/start/evenimente.json")

    inventar = Inventar(p, e)

    assert len(p) == 7
    assert len(e) == 8
    assert inventar.numara_suspecte() == {
        "procese": 2,
        "evenimente": 5
    }
