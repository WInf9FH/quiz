# Für Nostalgiker: `python Quiz.py` funktioniert wie 2015. Nur ohne Absturz.
import sys

try:
    from winf9quiz.app import main
except ImportError as fehler:
    sys.exit(f"{fehler}\n\nErst installieren:  pip install -e .")

sys.exit(main())
