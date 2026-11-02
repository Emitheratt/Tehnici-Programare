def test_doar_ce_e_nou():
    baza = {"a", "b", "c"}
    acum = {"a", "b", "c", "d"}

    noi = acum - baza

    assert noi == {"d"}