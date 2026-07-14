import os, csv

class MorseDecoder:

    def __init__(self, decode_map, unknown_symbol="?"):
        self.decode_map = decode_map
        self.unknown_symbol = unknown_symbol

    def decode_symbol(self, symbol: str) -> str:
        """
        Convert one Morse symbol into a character.
        """
        return self.decode_map.get(symbol, self.unknown_symbol)

    def decode_word(self, word: str) -> str:
        """
        Convert a Morse word into text.
        """
        symbols = word.split(" ")

        return "".join(
            self.decode_symbol(symbol)
            for symbol in symbols
            if symbol != ""
        )

    def decode_text(self, morse: str) -> str:
        """
        Convert full Morse code into readable text.
        """
        words = morse.strip().split(" / ")

        return " ".join(
            self.decode_word(word)
            for word in words
        )