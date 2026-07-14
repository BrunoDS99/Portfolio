import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # File paths
    MORSE_CSV_PATH = BASE_DIR / "data" / "morse.csv"

    # Morse formatting rules
    LETTER_SEPARATOR = " "
    WORD_SEPARATOR = " / "
    UNKNOWN_SYMBOL = "?"

    # Behavior settings
    STRICT_MODE = False