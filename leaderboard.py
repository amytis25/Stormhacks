import json
import os

class Leaderboard:
    def __init__(self, filename="scores.json", max_entries=10):
        self.filename = filename
        self.max_entries = max_entries
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f)

    def add_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        # Sort scores (lower time is better)
        self.scores.sort(key=lambda x: x["score"])
        self.scores = self.scores[:self.max_entries]
        self.save_scores()

    def get_leaderboard(self):
        return self.scores

    def get_recent_score(self):
        if self.scores:
            return self.scores[-1]
        return None