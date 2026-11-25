import pytest

from winf9quiz.app import main
from winf9quiz.spiel import Spieler, rangliste

from .conftest import ausgabe

# Richtige Antworten der eingebauten Fragen
ALLES_RICHTIG = list("CADBADC")


def test_rangliste_teilt_plaetze():
    a, b, c = Spieler("A", punkte=3), Spieler("B", punkte=5), Spieler("C", punkte=3)
    assert [(p, s.name) for p, s in rangliste([a, b, c])] == [(1, "B"), (2, "A"), (2, "C")]


def test_variante_reihum(ui_mit, tmp_path):
    eingaben = ["1", "2", "Anna", "Ben"]
    for nr, richtig in enumerate(ALLES_RICHTIG):
        eingaben += ["x", richtig.lower(), "B"]  # Anna: erst Unsinn, dann richtig; Ben: immer B
        if nr < len(ALLES_RICHTIG) - 1:
            eingaben.append(" ")
    ui = ui_mit(*eingaben)

    assert main(["--highscores", str(tmp_path / "hs.json")], ui=ui) == 0
    assert ui.rest.eingaben == []

    text = ausgabe(ui)
    assert "Anna hat 7 Punkte von 7 möglichen Punkten erreicht." in text
    assert "Ben hat 1 Punkt von 7 möglichen Punkten erreicht." in text
    assert "neuen Highscore für den Spielmodus 1" in text
    assert "Bitte A, B, C oder D drücken." in text


def test_variante_buzzer(ui_mit, tmp_path):
    eingaben = ["2", "Anna", "q", "Ben", "Q", "p"]  # Ben darf Annas Taste nicht nehmen
    for nr, richtig in enumerate(ALLES_RICHTIG):
        if nr == 0:
            eingaben += ["z", "P", richtig]  # falsche Taste, dann Ben (Großbuchstabe geht auch)
        elif nr == 1:
            eingaben += ["⏎"]  # weiß keiner
        else:
            eingaben += ["q", "A"]  # Anna buzzert und sagt immer A
        if nr < len(ALLES_RICHTIG) - 1:
            eingaben.append(" ")
    ui = ui_mit(*eingaben)

    assert main(["--highscores", str(tmp_path / "hs.json"), "--variante", "2"], ui=ui) == 0
    assert ui.rest.eingaben == []

    text = ausgabe(ui)
    assert "Die Taste ist schon vergeben." in text
    assert "Diese Taste ist falsch." in text
    assert "Keiner hat sich getraut." in text
    assert "Ben hat 1 Punkt von 7" in text
    assert "Anna hat 1 Punkt von 7" in text  # nur Merkel (A) aus Frage 3 bis 7


def test_abbruch(ui_mit, tmp_path):
    ui = ui_mit("1", "1", "Anna", "C")
    assert main(["--highscores", str(tmp_path / "hs.json")], ui=ui) == 130
    assert "Quiz abgebrochen" in ausgabe(ui)


def test_kaputte_fragendatei(ui_mit, tmp_path):
    datei = tmp_path / "f.json"
    datei.write_text("[]", encoding="utf-8")
    ui = ui_mit()
    assert main(["--fragen", str(datei), "--highscores", str(tmp_path / "hs.json")], ui=ui) == 1


@pytest.mark.parametrize("anzahl", ["0", "9", "zwei"])
def test_ungueltige_spielerzahl(ui_mit, tmp_path, anzahl):
    ui = ui_mit("1", anzahl)
    main(["--highscores", str(tmp_path / "hs.json")], ui=ui)
    assert "Bitte eine Zahl von 1 bis 8 eingeben." in ausgabe(ui)
