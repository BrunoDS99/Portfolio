from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_PATH = BASE_DIR / "data" / "projects.json"


def load_projects():
    with open(PROJECTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)