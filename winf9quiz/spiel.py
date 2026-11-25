"""Die eigentlichen Spielregeln. Unverändert seit 2015, nur jetzt funktionierend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

from .fragen import Frage

if TYPE_CHECKING:
    from .ui import Oberflaeche


@dataclass(eq=False)
class Spieler:
    name: str
    taste: Optional[str] = None
    punkte: int = 0


# (Spieler, abgegebene Antwort, richtig?)
Abgabe = Tuple[Spieler, str, bool]


def werte_aus(frage: Frage, spieler: Spieler, antwort: str) -> Abgabe:
    richtig = frage.ist_richtig(antwort)
    if richtig:
        spieler.punkte += 1
    return (spieler, antwort, richtig)


def variante_reihum(ui: Oberflaeche, fragen: Sequence[Frage], spieler: List[Spieler]) -> None:
    """Spielvariante 1: Jeder Spieler gibt eine Antwort ab."""
    for nr, frage in enumerate(fragen, start=1):
        ui.zeige_frage(nr, len(fragen), frage)
        abgaben = [
            werte_aus(frage, s, ui.frage_buchstabe(f"{s.name} ist an der Reihe")) for s in spieler
        ]
        ui.zeige_aufloesung(nr, len(fragen), frage, abgaben, spieler)
        if nr < len(fragen):
            ui.weiter()


def variante_buzzer(ui: Oberflaeche, fragen: Sequence[Frage], spieler: List[Spieler]) -> None:
    """Spielvariante 2: Wer zuerst seine Taste drückt, darf antworten."""
    for nr, frage in enumerate(fragen, start=1):
        ui.zeige_frage(nr, len(fragen), frage)
        abgaben: List[Abgabe] = []
        dran = ui.warte_auf_buzzer(spieler)
        if dran is not None:
            antwort = ui.frage_buchstabe(
                f"{dran.name} ist an der Reihe. Welche Antwort ist richtig?"
            )
            abgaben.append(werte_aus(frage, dran, antwort))
        ui.zeige_aufloesung(nr, len(fragen), frage, abgaben, spieler)
        if nr < len(fragen):
            ui.weiter()


def rangliste(spieler: Sequence[Spieler]) -> List[Tuple[int, Spieler]]:
    """Sortiert nach Punkten; Gleichstand teilt sich den Platz."""
    sortiert = sorted(spieler, key=lambda s: s.punkte, reverse=True)
    ergebnis: List[Tuple[int, Spieler]] = []
    for i, s in enumerate(sortiert):
        platz = ergebnis[-1][0] if ergebnis and ergebnis[-1][1].punkte == s.punkte else i + 1
        ergebnis.append((platz, s))
    return ergebnis
