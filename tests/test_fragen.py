import json

import pytest

from winf9quiz.fragen import BUCHSTABEN, Frage, FragenFehler, lade_fragen, parse_fragen


def test_eingebaute_fragen_sind_die_originale():
    fragen = lade_fragen()
    assert len(fragen) == 7
    assert fragen[0].text == "Wie heißt die Hauptstadt von Deutschland?"
    assert fragen[0].richtige_antwort == "Berlin"
    assert all(f.richtig in BUCHSTABEN for f in fragen)


@pytest.mark.parametrize("eingabe", ["A", "a", " a ", "A\n"])
def test_a_ist_a(eingabe):
    """Regressionstest für convertUpperCase() von 2015, wo aus "A" ein "B" wurde."""
    proton = Frage("Welches Teilchen ist positiv?", ("Proton", "Neutron", "Elektron", "Anion"), "A")
    assert proton.ist_richtig(eingabe)
    assert not proton.ist_richtig("B")


@pytest.mark.parametrize("eingabe", ["", "E", "AB", "1"])
def test_unsinn_ist_falsch(eingabe):
    assert not Frage("?", ("a", "b", "c", "d"), "A").ist_richtig(eingabe)


@pytest.mark.parametrize(
    "roh",
    [
        "kein json",
        "[]",
        "{}",
        json.dumps([{"frage": "x", "antworten": ["a", "b", "c"], "richtig": "A"}]),
        json.dumps([{"frage": "x", "antworten": ["a", "b", "c", "d"], "richtig": "E"}]),
        json.dumps([{"frage": "", "antworten": ["a", "b", "c", "d"], "richtig": "A"}]),
        json.dumps([["Frage?\n", ["A: a", "B: b", "C: c", "D: d\n"], "A"]]),  # Format von 2015
    ],
)
def test_kaputte_fragen_werden_erkannt(roh):
    with pytest.raises(FragenFehler):
        parse_fragen(roh)


def test_eigene_fragendatei(tmp_path):
    datei = tmp_path / "fragen.json"
    frage = {"frage": " Ja? ", "antworten": ["ja", "nein", "vielleicht", "42"], "richtig": "d"}
    datei.write_text(json.dumps([frage]), encoding="utf-8")
    (geladen,) = lade_fragen(datei)
    assert geladen.text == "Ja?"
    assert geladen.richtig == "D"
    assert geladen.richtige_antwort == "42"


def test_fehlende_datei(tmp_path):
    with pytest.raises(FragenFehler):
        lade_fragen(tmp_path / "gibtsnicht.json")
