
from collections import Counter
from arsenal.aparare.detector import suspecti


# Testul 1 - Verifica daca pragul functioneaza
def test_pragul_taie():

    c = Counter({"a": 13, "b": 2})

    assert suspecti(c, 10) == [("a", 13)]


# Testul 2 - Verifica daca pragul invalid genereaza eroare
def test_prag_invalid():

    import pytest

    with pytest.raises(ValueError):
        suspecti({}, 0)
