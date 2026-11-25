from __future__ import annotations

import io
from typing import Iterable

import pytest
from rich.console import Console

from winf9quiz.tasten import ENTER
from winf9quiz.ui import Oberflaeche


class Skript:
    """Spielt einem Spiel Tastendrücke und Zeilen vor."""

    def __init__(self, eingaben: Iterable[str]) -> None:
        self.eingaben = list(eingaben)

    def naechste(self) -> str:
        if not self.eingaben:
            raise EOFError
        return self.eingaben.pop(0)


@pytest.fixture
def ui_mit():
    def bauen(*eingaben: str) -> Oberflaeche:
        skript = Skript(ENTER if e == "⏎" else e for e in eingaben)
        console = Console(file=io.StringIO(), width=100, force_terminal=False, color_system=None)
        console.input = lambda *a, **k: skript.naechste()  # type: ignore[method-assign]
        ui = Oberflaeche(console=console, taste=skript.naechste)
        ui.rest = skript  # type: ignore[attr-defined]
        return ui

    return bauen


def ausgabe(ui: Oberflaeche) -> str:
    return ui.console.file.getvalue()  # type: ignore[attr-defined]
