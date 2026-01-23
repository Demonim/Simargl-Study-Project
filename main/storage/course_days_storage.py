import json
import os

class CourseDaysStorage:
    def __init__(self, login):
        self.path = f"storage/course_days_{login}.json"

    def load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)