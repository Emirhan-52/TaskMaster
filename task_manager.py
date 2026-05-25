import json
import os
import shutil
from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, due_date, status="pending", created_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status.lower()
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
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
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            status=data["status"],
            created_date=data["created_date"]
        )

class TaskManager:
    def __init__(self):
        # Uygulamanın çalıştığı yer neresi olursa olsun, ana proje klasöründeki /data klasörünü bulur.
        current_dir = os.path.dirname(os.path.abspath(__file__))  # src klasörü
        project_root = os.path.dirname(current_dir)  # TaskMaster ana klasörü
        
        self.filepath = os.path.join(project_root, "data", "tasks.json")
        self.backup_dir = os.path.join(project_root, "data", "backups")
        
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            if not os.path.exists(self.filepath):
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
                self.save_tasks()
                return
            
            with open(self.filepath, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data_list]
        except Exception:
            self.tasks = []

    def save_tasks(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=4)
            self._create_backup()
        except Exception as e:
            print(f"Save Error: {e}")

    def _create_backup(self):
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"tasks_backup_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            shutil.copy2(self.filepath, backup_path)
            
            # Son 5 yedeği tut, eskileri sil
            backups = sorted(
                [os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.startswith("tasks_backup_")],
                key=os.path.getmtime
            )
            while len(backups) > 5:
                os.remove(backups.pop(0))
        except Exception:
            pass

    def _generate_unique_id(self):
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, title, description, due_date):
        unique_id = self._generate_unique_id()
        new_task = Task(task_id=unique_id, title=title, description=description, due_date=due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def get_all_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if due_date is not None:
                task.due_date = due_date
            if status is not None:
                task.status = status.lower()
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status.lower() == status.lower()]