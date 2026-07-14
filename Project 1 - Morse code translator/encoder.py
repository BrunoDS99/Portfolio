import os, csv
from config import Config

class MorseEncoder:

    def __init__(self, encode_map, unknown_symbol="?"):
        self.encode_map = encode_map
        self.unknown_symbol = unknown_symbol

    def encode_char(self, char: str) -> str:
        """
        Encode a single character into Morse.
        """
        return self.encode_map.get(char.upper(), self.unknown_symbol)

    def encode_word(self, word: str) -> str:
        """
        Encode a single word into Morse.
        """
        return " ".join(
            self.encode_char(char)
            for char in word
        )

    def encode_text(self, text: str) -> str:
        """
        Encode full text into Morse code.
        """
        words = text.strip().split()

        morse_words = [
            self.encode_word(word)
            for word in words
        ]

        return " / ".join(morse_words)