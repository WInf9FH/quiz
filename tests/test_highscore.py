from datetime import date

from winf9quiz.highscore import PLAETZE, Highscores

HEUTE = date(2015, 6, 15)


def test_leer_und_speichern(tmp_path):
    pfad = tmp_path / "sub" / "hs.json"
    hs = Highscores(pfad)
    assert hs.bestenliste(1) == []
    assert hs.eintragen(1, "Max", 5, 7, HEUTE) == 1
    hs.speichern()

    wieder = Highscores(pfad)
    (eintrag,) = wieder.bestenliste(1)
    assert (eintrag.name, eintrag.punkte, eintrag.von, eintrag.datum) == ("Max", 5, 7, "2015-06-15")
    assert wieder.bestenliste(2) == []


def test_reihenfolge_und_gleichstand(tmp_path):
    hs = Highscores(tmp_path / "hs.json")
    assert hs.eintragen(2, "Erster", 3, 7, HEUTE) == 1
    assert hs.eintragen(2, "Besser", 5, 7, HEUTE) == 1
    assert hs.eintragen(2, "Gleich", 5, 7, HEUTE) == 2
    assert [e.name for e in hs.bestenliste(2)] == ["Besser", "Gleich", "Erster"]


def test_null_punkte_zaehlen_nicht(tmp_path):
    assert Highscores(tmp_path / "hs.json").eintragen(1, "Niemand", 0, 7, HEUTE) is None


def test_liste_ist_begrenzt(tmp_path):
    hs = Highscores(tmp_path / "hs.json")
    for i in range(PLAETZE):
        hs.eintragen(1, f"S{i}", 7, 7, HEUTE)
    assert hs.eintragen(1, "Zu spät", 7, 7, HEUTE) is None
    assert hs.eintragen(1, "Super", 8, 8, HEUTE) == 1
    assert len(hs.bestenliste(1)) == PLAETZE


def test_kaputte_datei(tmp_path):
    pfad = tmp_path / "hs.json"
    pfad.write_text('[["Niemand", 0], ["Niemand", 0]]', encoding="utf-8")  # Highscores.txt von 2015
    hs = Highscores(pfad)
    assert hs.war_kaputt
    assert hs.bestenliste(1) == []
