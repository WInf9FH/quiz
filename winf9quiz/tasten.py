"""Eine einzelne Taste lesen, ohne dass jemand Enter drücken muss.

2015 hieß es "drücke deine Taste!" und dann musste man doch Enter drücken.
"""

from __future__ import annotations

import os
import sys

ENTER = "\n"


def _lies_zeile() -> str:
    zeile = sys.stdin.readline()
    if not zeile:
        raise EOFError
    zeile = zeile.strip()
    return zeile[0] if zeile else ENTER


def _lies_windows() -> str:
    import msvcrt

    zeichen = msvcrt.getwch()
    if zeichen in ("\x00", "\xe0"):  # Pfeiltasten & Co.
        msvcrt.getwch()
        return ""
    return zeichen


def _lies_unix() -> str:
    import termios
    import tty

    fd = sys.stdin.fileno()
    alt = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        roh = os.read(fd, 8)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, alt)
    if roh.startswith(b"\x1b"):  # Escape-Sequenzen ignorieren
        return ""
    return roh.decode("utf-8", errors="ignore")[:1]


def lies_taste() -> str:
    """Gibt das gedrückte Zeichen zurück, ``ENTER`` für Enter, "" für Unlesbares."""
    if not sys.stdin.isatty():
        return _lies_zeile()

    zeichen = _lies_windows() if os.name == "nt" else _lies_unix()
    if zeichen == "\x03":
        raise KeyboardInterrupt
    if zeichen in ("\x04", "\x1a"):
        raise EOFError
    if zeichen in ("\r", "\n"):
        return ENTER
    return zeichen
