"""Alles, was man sieht. Früher: print(). Heute: rich."""

from __future__ import annotations

from typing import Callable, List, Optional, Sequence

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .fragen import BUCHSTABEN, Frage
from .highscore import Eintrag
from .spiel import Abgabe, Spieler, rangliste
from .tasten import ENTER, lies_taste

LOGO = r"""
 ██████╗ ██╗   ██╗██╗███████╗
██╔═══██╗██║   ██║██║╚══███╔╝
██║   ██║██║   ██║██║  ███╔╝
██║▄▄ ██║██║   ██║██║ ███╔╝
╚██████╔╝╚██████╔╝██║███████╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝
"""

FARBEN = ("cyan", "magenta", "yellow", "green")
MEDAILLEN = {1: "🥇", 2: "🥈", 3: "🥉"}
MAX_SPIELER = 8


def punkte_text(n: int) -> str:
    return f"{n} Punkt" if n == 1 else f"{n} Punkte"


class Oberflaeche:
    def __init__(
        self, console: Optional[Console] = None, taste: Callable[[], str] = lies_taste
    ) -> None:
        self.console = console or Console(highlight=False)
        self._taste = taste

    # ------------------------------------------------------------------ Eingabe

    def _prompt(self, text: str) -> None:
        self.console.print(f"[bold]›[/] {text} ", end="")

    def taste(self, text: str) -> str:
        self._prompt(text)
        zeichen = self._taste()
        self.console.print("" if zeichen in ("", ENTER) else f"[bold]{zeichen}[/]")
        return zeichen

    def zeile(self, text: str) -> str:
        self._prompt(text)
        return self.console.input().strip()

    def fehler(self, text: str) -> None:
        self.console.print(f"  [red]✗ {text}[/]")

    def frage_buchstabe(self, text: str) -> str:
        while True:
            zeichen = self.taste(f"{text} [dim](A–D)[/]:").upper()
            if zeichen in BUCHSTABEN:
                return zeichen
            if zeichen:
                self.fehler("Bitte A, B, C oder D drücken.")

    def weiter(self) -> None:
        self.taste("[dim]Weiter mit beliebiger Taste …[/]")

    # ---------------------------------------------------------------- Vorspann

    def banner(self) -> None:
        self.console.clear()
        logo = Text(LOGO.strip("\n"), style="bold cyan", no_wrap=True)
        unterzeile = Text.from_markup("[dim]vom[/] [bold]WInf9-Kurs[/]  [dim]· seit 2015 ·[/]")
        self.console.print(
            Panel(
                Group(Align.center(logo), Text(), Align.center(unterzeile)),
                box=box.DOUBLE,
                border_style="cyan",
                padding=(1, 2),
            )
        )

    def waehle_variante(self) -> int:
        tabelle = Table.grid(padding=(0, 2))
        tabelle.add_row("[bold cyan]1[/]", "[bold]Reihum[/]", "Jeder Spieler gibt eine Antwort ab.")
        tabelle.add_row(
            "[bold magenta]2[/]",
            "[bold]Buzzer[/]",
            "Jeder Spieler bekommt eine Taste. Wer sie zuerst drückt,\n"
            "ist der Einzige, der die Frage beantworten darf.",
        )
        self.console.print(Panel(tabelle, title="Verfügbare Spielvarianten", border_style="dim"))
        while True:
            zeichen = self.taste("Welche möchtest du nutzen?")
            if zeichen in ("1", "2"):
                return int(zeichen)
            if zeichen:
                self.fehler("Bitte 1 oder 2 drücken.")

    def spieler_anmelden(self, mit_tasten: bool) -> List[Spieler]:
        while True:
            eingabe = self.zeile(f"Wie viele Spieler spielen mit? [dim](1–{MAX_SPIELER})[/]")
            if eingabe.isdigit() and 1 <= int(eingabe) <= MAX_SPIELER:
                anzahl = int(eingabe)
                break
            self.fehler(f"Bitte eine Zahl von 1 bis {MAX_SPIELER} eingeben.")

        spieler: List[Spieler] = []
        for i in range(1, anzahl + 1):
            farbe = FARBEN[(i - 1) % len(FARBEN)]
            while True:
                name = self.zeile(f"Name von Spieler [{farbe}]{i}[/]:")
                if not name:
                    self.fehler("Ohne Namen geht's nicht.")
                elif any(s.name.casefold() == name.casefold() for s in spieler):
                    self.fehler(f"{name} spielt schon mit.")
                else:
                    break

            taste = None
            while mit_tasten:
                taste = self.taste(f"Taste von [{farbe}]{name}[/]:")
                if not taste.strip() or not taste.isprintable():
                    self.fehler("Das ist keine gute Buzzer-Taste.")
                elif any(s.taste == taste.casefold() for s in spieler):
                    self.fehler("Die Taste ist schon vergeben.")
                else:
                    taste = taste.casefold()
                    break
            spieler.append(Spieler(name=name, taste=taste))
        return spieler

    # ----------------------------------------------------------------- Fragen

    def _fortschritt(self, nr: int, gesamt: int) -> Text:
        return Text.assemble(("●" * nr, "cyan"), ("○" * (gesamt - nr), "dim"))

    def _frage_panel(self, nr: int, gesamt: int, frage: Frage, aufgedeckt: bool) -> Group:
        kopf = Panel(
            Align.center(Text(frage.text, style="bold"), vertical="middle"),
            title=f"[bold]Frage {nr} von {gesamt}[/]",
            subtitle=self._fortschritt(nr, gesamt),
            border_style="cyan",
            box=box.HEAVY,
            padding=(1, 2),
        )

        def kasten(buchstabe: str, text: str) -> Panel:
            if not aufgedeckt:
                return Panel(f"[bold yellow]{buchstabe}[/]  {text}", border_style="blue")
            if buchstabe == frage.richtig:
                return Panel(
                    f"[bold]{buchstabe}[/]  {text}  ✓",
                    style="bold black on green",
                    border_style="green",
                )
            return Panel(f"[dim]{buchstabe}  {text}[/]", border_style="dim")

        gitter = Table.grid(expand=True, padding=(0, 1))
        gitter.add_column(ratio=1)
        gitter.add_column(ratio=1)
        kaesten = [kasten(b, t) for b, t in zip(BUCHSTABEN, frage.antworten)]
        gitter.add_row(kaesten[0], kaesten[1])
        gitter.add_row(kaesten[2], kaesten[3])
        return Group(kopf, gitter)

    def zeige_frage(self, nr: int, gesamt: int, frage: Frage) -> None:
        self.console.clear()
        self.console.print(self._frage_panel(nr, gesamt, frage, aufgedeckt=False))

    def warte_auf_buzzer(self, spieler: Sequence[Spieler]) -> Optional[Spieler]:
        nach_taste = {s.taste: s for s in spieler}
        tasten = "  ".join(f"[bold]{s.taste}[/]={s.name}" for s in spieler)
        self.console.print(f"\n[dim]{tasten}   ⏎ = weiß keiner[/]")
        zeichen = self.taste("Wenn du die Antwort weißt, drücke deine Taste!")
        while True:
            if zeichen == ENTER:
                return None
            if zeichen.casefold() in nach_taste:
                return nach_taste[zeichen.casefold()]
            zeichen = self.taste("[red]Diese Taste ist falsch.[/] Noch einmal:")

    def zeige_aufloesung(
        self,
        nr: int,
        gesamt: int,
        frage: Frage,
        abgaben: Sequence[Abgabe],
        spieler: Sequence[Spieler],
    ) -> None:
        self.console.clear()
        self.console.print(self._frage_panel(nr, gesamt, frage, aufgedeckt=True))
        self.console.print(
            f"\nDie richtige Antwort war [bold green]{frage.richtig}: {frage.richtige_antwort}[/]\n"
        )

        if not abgaben:
            self.console.print("[dim]Keiner hat sich getraut.[/]\n")

        tabelle = Table(box=box.SIMPLE_HEAD, show_edge=False, pad_edge=False)
        tabelle.add_column("Spieler")
        tabelle.add_column("Antwort", justify="center")
        tabelle.add_column("Punkte", justify="right")
        abgegeben = {id(s): (antwort, richtig) for s, antwort, richtig in abgaben}
        for s in spieler:
            if id(s) in abgegeben:
                antwort, richtig = abgegeben[id(s)]
                zelle = f"[green]{antwort} ✓[/]" if richtig else f"[red]{antwort} ✗[/]"
                punkte = f"[bold green]{s.punkte} (+1)[/]" if richtig else str(s.punkte)
            else:
                zelle, punkte = "[dim]–[/]", str(s.punkte)
            tabelle.add_row(s.name, zelle, punkte)
        self.console.print(tabelle)
        self.console.print()

    # ------------------------------------------------------------------ Ende

    def zeige_endstand(self, spieler: Sequence[Spieler], gesamt: int) -> None:
        self.console.clear()
        tabelle = Table(box=box.ROUNDED, border_style="yellow", expand=True)
        tabelle.add_column("Platz", justify="center", width=7)
        tabelle.add_column("Spieler")
        tabelle.add_column("Ergebnis", justify="right")
        tabelle.add_column("", ratio=1)
        for platz, s in rangliste(spieler):
            balken_breite = 20
            voll = round(balken_breite * s.punkte / gesamt) if gesamt else 0
            balken = Text.assemble(("█" * voll, "yellow"), ("░" * (balken_breite - voll), "dim"))
            tabelle.add_row(
                MEDAILLEN.get(platz, f"{platz}."),
                Text(s.name, style="bold" if platz == 1 else ""),
                f"{s.punkte} / {gesamt}",
                balken,
            )
        self.console.print(
            Panel(tabelle, title="[bold yellow]🏆 Endstand 🏆[/]", border_style="yellow")
        )
        for s in spieler:
            self.console.print(
                f"[bold]{s.name}[/] hat {punkte_text(s.punkte)} von {gesamt} "
                "möglichen Punkten erreicht."
            )

    def zeige_neuer_highscore(self, name: str, platz: int, variante: int) -> None:
        if platz == 1:
            self.console.print(
                f"[bold yellow]★ {name} hat damit einen neuen Highscore "
                f"für den Spielmodus {variante} erzielt! ★[/]"
            )
        else:
            self.console.print(f"[yellow]{name} landet auf Platz {platz} der Bestenliste.[/]")

    def zeige_bestenliste(self, eintraege: Sequence[Eintrag], variante: int) -> None:
        tabelle = Table(box=box.SIMPLE_HEAD, show_edge=False)
        tabelle.add_column("#", justify="right")
        tabelle.add_column("Name")
        tabelle.add_column("Punkte", justify="right")
        tabelle.add_column("Datum", style="dim")
        if not eintraege:
            tabelle.add_row("1", "[dim]Niemand[/]", "0", "")
        for i, e in enumerate(eintraege, start=1):
            tabelle.add_row(str(i), e.name, f"{e.punkte} / {e.von}", e.datum)
        self.console.print()
        self.console.print(
            Panel(tabelle, title=f"Bestenliste · Spielmodus {variante}", expand=False)
        )
