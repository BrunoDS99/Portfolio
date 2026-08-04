import json
import os
from datetime import datetime


SCORE_FILE = "data/scores.json"


class ScoreManager:

    def __init__(self):
        self.scores = []
        self.load_scores()


    def load_scores(self):

        if not os.path.exists(SCORE_FILE):
            self.scores = []
            return

        with open(SCORE_FILE,"r") as file:
            self.scores = json.load(file)

    def save_score(self, wpm, accuracy, errors):

        score = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "wpm": wpm,
            "accuracy": accuracy,
            "errors": errors
        }

        self.scores.append(score)
        with open(SCORE_FILE,"w") as file:
            json.dump(
                self.scores,
                file,
                indent=4
            )


    def get_high_score(self):
        if not self.scores:
            return 0
        return max(score["wpm"]for score in self.scores)