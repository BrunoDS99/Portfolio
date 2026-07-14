import csv, os
from config import Config

class MorseMapping:
    def __init__(self, path: str = Config.MORSE_CSV_PATH):
        self.path = path
        self.encode_map = {}
        self.decode_map = {}
        self.load_morse_csv()
        
    def load_morse_csv(self):
        with open(self.path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                char = (row.get("char") or "").strip()
                morse = (row.get("morse") or "").strip()

                if not char or not morse:
                    continue

                self.encode_map[char] = morse
                self.decode_map[morse] = char

    def get_encode_map(self):
        return self.encode_map

    def get_decode_map(self):
        return self.decode_map