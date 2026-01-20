import json
import os
import uuid
from datetime import datetime

class NotesStorage:
    def __init__(self, login: str):
        self.login = login
        self.base_path = "storage/data"
        os.makedirs(self.base_path, exist_ok=True)
        self.file_path = os.path.join(self.base_path, f"{login}.json")

    def load_notes(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("notes", [])

    def save_notes(self, notes: list[dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)

    def create_note(self, title: str, content: str) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }