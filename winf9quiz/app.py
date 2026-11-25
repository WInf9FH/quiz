"""Einstiegspunkt: ``python -m winf9quiz`` oder ``python Quiz.py``."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import List, Optional

from rich.console import Console

from . import __version__
from .fragen import FragenFehler, lade_fragen
from .highscore import STANDARD_PFAD, Highscores
from .spiel import variante_buzzer, variante_reihum
from .ui import Oberflaeche


def argumente(argv: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="quiz", description="Das Quiz vom WInf9-Kurs.")
    parser.add_argument("--fragen", type=Path, help="eigene Fragendatei (JSON)")
    parser.add_argument("--variante", type=int, choices=(1, 2), help="Spielvariante vorwählen")
    parser.add_argument("--mischen", action="store_true", help="Fragen zufällig mischen")
    parser.add_argument(
        "--highscores",
        type=Path,
        default=STANDARD_PFAD,
        help=f"Highscore-Datei (Standard: {STANDARD_PFAD})",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None, ui: Optional[Oberflaeche] = None) -> int:
    args = argumente(argv)
    ui = ui or Oberflaeche()
    console: Console = ui.console

    try:
        fragen = lade_fragen(args.fragen)
    except FragenFehler as fehler:
        console.print(f"[red]Die Fragen konnten nicht geladen werden:[/] {fehler}")
        return 1
    if args.mischen:
        random.shuffle(fragen)

    highscores = Highscores(args.highscores)

    try:
        ui.banner()
        if highscores.war_kaputt:
            ui.fehler("Die Highscore-Datei war kaputt. Es geht von vorne los.")
        variante = args.variante or ui.waehle_variante()
        spieler = ui.spieler_anmelden(mit_tasten=variante == 2)

        if variante == 1:
            variante_reihum(ui, fragen, spieler)
        else:
            variante_buzzer(ui, fragen, spieler)

        ui.zeige_endstand(spieler, len(fragen))
        for s in spieler:
            platz = highscores.eintragen(variante, s.name, s.punkte, len(fragen))
            if platz is not None:
                ui.zeige_neuer_highscore(s.name, platz, variante)
        try:
            highscores.speichern()
        except OSError as fehler:
            ui.fehler(f"Highscores konnten nicht gespeichert werden: {fehler}")
        ui.zeige_bestenliste(highscores.bestenliste(variante), variante)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Quiz abgebrochen. Tschüss![/]")
        return 130

    return 0
