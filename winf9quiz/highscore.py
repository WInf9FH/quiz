"""Bestenliste pro Spielvariante, als JSON auf der Platte."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

PLAETZE = 5
STANDARD_PFAD = Path.home() / ".winf9-quiz" / "highscores.json"


@dataclass(frozen=True)
class Eintrag:
    name: str
    punkte: int
    von: int
    datum: str


class Highscores:
    def __init__(self, pfad: Path = STANDARD_PFAD) -> None:
        self.pfad = Path(pfad)
        self.listen: Dict[int, List[Eintrag]] = {1: [], 2: []}
        self.war_kaputt = False
        self._laden()

    def _laden(self) -> None:
        if not self.pfad.exists():
            return
        try:
            roh = json.loads(self.pfad.read_text(encoding="utf-8"))
            for variante in self.listen:
                self.listen[variante] = [Eintrag(**e) for e in roh.get(str(variante), [])]
        except (OSError, ValueError, TypeError, AttributeError):
            # Lieber neu anfangen als abstürzen.
            self.listen = {1: [], 2: []}
            self.war_kaputt = True

    def speichern(self) -> None:
        self.pfad.parent.mkdir(parents=True, exist_ok=True)
        daten = {str(v): [asdict(e) for e in liste] for v, liste in self.listen.items()}
        self.pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    def bestenliste(self, variante: int) -> List[Eintrag]:
        return list(self.listen[variante])

    def eintragen(
        self, variante: int, name: str, punkte: int, von: int, heute: Optional[date] = None
    ) -> Optional[int]:
        """Trägt ein Ergebnis ein und gibt den Platz (1-basiert) zurück, oder None."""
        if punkte <= 0:
            return None  # "Niemand, 0 Punkte" war 2015 schon Platz 1. Reicht.

        eintrag = Eintrag(name, punkte, von, (heute or date.today()).isoformat())
        liste = self.listen[variante]
        # Bei Gleichstand bleibt, wer zuerst da war.
        platz = next((i for i, e in enumerate(liste) if punkte > e.punkte), len(liste))
        if platz >= PLAETZE:
            return None
        liste.insert(platz, eintrag)
        del liste[PLAETZE:]
        return platz + 1
