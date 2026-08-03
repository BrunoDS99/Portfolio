import json, random
from pathlib import Path

WORDS_FILE = Path(__file__).parent / "words.json"

def load_words():
    with open(WORDS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def generate_random_words(amount=50):
    words = load_words()
    
    return " ".join(random.choice(words) for _ in range(amount))

