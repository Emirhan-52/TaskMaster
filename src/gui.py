import tkinter as tk
from tkinter import messagebox

class TaskMasterGUI:
    def __init__(self, root, db_handler):
        self.root = root
        self.db = db_handler
        self.root.title("TaskMaster - To-Do List")
        self.root.geometry("500x600")
        
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        self.header_label = tk.Label(self.root, text="TaskMaster Control Panel", font=("Arial", 16, "bold"))
        self.header_label.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, font=("Arial", 12), width=45, height=18)
        self.task_listbox.pack(pady=10)

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.add_btn = tk.Button(self.btn_frame, text="Add Task", width=10, command=self.add_task_placeholder)
        self.add_btn.grid(row=0, column=0, padx=5)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.db.load_tasks()
        for task in tasks:
            status = "[✓]" if task.get("completed") else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task.get('title')}")

    def add_task_placeholder(self):
        messagebox.showinfo("TaskMaster", "CRUD operations logic will be fully implemented in April!")