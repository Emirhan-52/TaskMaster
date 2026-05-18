import json
import os
from datetime import datetime

class Task:
    """
    Represents a single task in the TaskMaster application.
    """
    def __init__(self, task_id, title, description, due_date, status="pending", created_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date  # Expected format: "YYYY-MM-DD"
        self.status = status      # "pending" or "completed"
        # If no creation date is provided, use the current timestamp
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the Task object into a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "created_date": self.created_date
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Task object from a dictionary."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            status=data["status"],
            created_date=data["created_date"]
        )


class TaskManager:
    """
    Manages the collection of tasks, handles CRUD operations, 
    and controls auto-loading/auto-saving data with JSON storage.
    """
    def __init__(self, filepath="data/tasks.json"):
        self.filepath = filepath
        self.tasks = []
        self.load_tasks()  # Auto-load on startup

    def load_tasks(self):
        """Loads tasks from the local JSON file on startup."""
        if not os.path.exists(self.filepath):
            # Create directories and an empty JSON list if file doesn't exist
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            self.save_tasks()
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                # Convert primitive dictionaries back into rich Task objects
                self.tasks = [Task.from_dict(item) for item in data_list]
        except (json.JSONDecodeError, KeyError):
            # Fallback if the file is corrupted
            self.tasks = []

    def save_tasks(self):
        """Saves all tasks to the local JSON file (Auto-save trigger)."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            # Serialize Task objects into a JSON-compatible format
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def _generate_unique_id(self):
        """Generates a unique incremental ID based on existing tasks."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, title, description, due_date):
        """Creates a new task with a unique ID and auto-saves."""
        unique_id = self._generate_unique_id()
        new_task = Task(task_id=unique_id, title=title, description=description, due_date=due_date)
        self.tasks.append(new_task)
        self.save_tasks()  # Auto-save after mutation
        return new_task

    def get_all_tasks(self):
        """Returns a list of all active tasks."""
        return self.tasks

    def get_task(self, task_id):
        """Returns a specific task by its unique ID, or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        """Updates specific attributes of an existing task and auto-saves."""
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if due_date is not None:
                task.due_date = due_date
            if status is not None:
                task.status = status
            
            self.save_tasks()  # Auto-save after mutation
            return True
        return False

    def delete_task(self, task_id):
        """Deletes a task by its unique ID from the list and auto-saves."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()  # Auto-save after mutation
            return True
        return False

    def get_tasks_by_status(self, status):
        """Returns a filtered list of tasks matching the given status ('pending'/'completed')."""
        return [task for task in self.tasks if task.status.lower() == status.lower()]