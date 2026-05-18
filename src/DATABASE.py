import json
import os

class DatabaseHandler:
    def __init__(self, filepath="data/tasks.json"):
        self.filepath = filepath
        self.ensure_data_file_exists()

    def ensure_data_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def load_tasks(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self, tasks):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)