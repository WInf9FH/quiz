"""Fragen laden und prüfen."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, List, Optional, Tuple

BUCHSTABEN: Tuple[str, ...] = ("A", "B", "C", "D")


class FragenFehler(ValueError):
    """Die Fragendatei ist kaputt."""


@dataclass(frozen=True)
class Frage:
    text: str
    antworten: Tuple[str, str, str, str]
    richtig: str

    def ist_richtig(self, antwort: str) -> bool:
        # Seit 2015 wurde hier aus einem "A" ein "B". Das Proton dankt.
        return antwort.strip().upper() == self.richtig

    @property
    def richtige_antwort(self) -> str:
        return self.antworten[BUCHSTABEN.index(self.richtig)]


def _parse_frage(roh: Any, nr: int) -> Frage:
    if not isinstance(roh, dict):
        raise FragenFehler(f"Frage {nr}: Erwartet ein Objekt, bekommen: {type(roh).__name__}")

    text = roh.get("frage")
    antworten = roh.get("antworten")
    richtig = roh.get("richtig")

    if not isinstance(text, str) or not text.strip():
        raise FragenFehler(f"Frage {nr}: 'frage' fehlt oder ist leer.")
    if (
        not isinstance(antworten, list)
        or len(antworten) != len(BUCHSTABEN)
        or not all(isinstance(a, str) and a.strip() for a in antworten)
    ):
        raise FragenFehler(f"Frage {nr}: 'antworten' muss genau vier Texte enthalten.")
    if not isinstance(richtig, str) or richtig.strip().upper() not in BUCHSTABEN:
        raise FragenFehler(f"Frage {nr}: 'richtig' muss A, B, C oder D sein.")

    return Frage(
        text=text.strip(),
        antworten=tuple(a.strip() for a in antworten),  # type: ignore[arg-type]
        richtig=richtig.strip().upper(),
    )


def parse_fragen(text: str) -> List[Frage]:
    try:
        roh = json.loads(text)
    except json.JSONDecodeError as fehler:
        raise FragenFehler(f"Kein gültiges JSON: {fehler}") from fehler

    if not isinstance(roh, list) or not roh:
        raise FragenFehler("Die Fragendatei muss eine nicht-leere Liste sein.")

    return [_parse_frage(eintrag, nr) for nr, eintrag in enumerate(roh, start=1)]


def lade_fragen(pfad: Optional[Path] = None) -> List[Frage]:
    """Lädt die eingebauten Fragen oder die aus ``pfad``."""
    if pfad is None:
        text = resources.files("winf9quiz").joinpath("data/fragen.json").read_text(encoding="utf-8")
    else:
        try:
            text = Path(pfad).read_text(encoding="utf-8")
        except OSError as fehler:
            raise FragenFehler(f"Kann {pfad} nicht lesen: {fehler}") from fehler
    return parse_fragen(text)
