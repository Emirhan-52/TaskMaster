import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from task_manager import TaskManager, Task
from edit_window import EditTaskWindow

class TaskMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster - To-Do List")
        self.root.geometry("950x650")
        self.root.minsize(950, 650)

        self.manager = TaskManager()
        self.create_styles()
        self.create_top_panel()
        self.create_left_panel()
        self.create_right_panel()
        self.create_status_bar()
        self.refresh_table()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=("Arial", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#dcdcdc")
        self.style.map("Treeview", background=[("selected", "#3498db")])

    def create_top_panel(self):
        top_frame = tk.Frame(self.root, bg="#f8f9fa", height=50)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        top_frame.pack_propagate(False)

        filter_label = tk.Label(top_frame, text="Filter:", font=("Arial", 10), bg="#f8f9fa")
        filter_label.pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="All")
        self.filter_combobox = ttk.Combobox(top_frame, textvariable=self.filter_var, values=["All", "Pending", "Completed"], state="readonly", width=12)
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top_frame, textvariable=self.search_var, font=("Arial", 10), width=30, fg="gray")
        self.search_entry.insert(0, "Search tasks...")
        self.search_entry.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_var.trace_add("write", lambda *args: self.refresh_table())

    def create_left_panel(self):
        left_frame = tk.Frame(self.root, width=350, bd=1, relief=tk.SOLID, padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        form_title = tk.Label(left_frame, text="Create New Task", font=("Arial", 12, "bold"))
        form_title.pack(anchor=tk.W, pady=(0, 15))

        tk.Label(left_frame, text="Task Title *", font=("Arial", 10)).pack(anchor=tk.W, pady=(5, 2))
        self.title_entry = tk.Entry(left_frame, font=("Arial", 10), width=35)
        self.title_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))

        tk.Label(left_frame, text="Description", font=("Arial", 10)).pack(anchor=tk.W, pady=(5, 2))
        self.desc_text = tk.Text(left_frame, font=("Arial", 10), height=5, width=35)
        self.desc_text.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))

        tk.Label(left_frame, text="Due Date (YYYY-MM-DD) *", font=("Arial", 10)).pack(anchor=tk.W, pady=(5, 2))
        self.date_entry = tk.Entry(left_frame, font=("Arial", 10), width=35)
        self.date_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        add_btn = tk.Button(left_frame, text="Add Task", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), activebackground="#27ae60", command=self.handle_add_task)
        add_btn.pack(anchor=tk.W, fill=tk.X, pady=10)

    def create_right_panel(self):
        right_frame = tk.Frame(self.root, width=550, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("id", "title", "due_date", "status")
        
        table_container = tk.Frame(right_frame)
        table_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("due_date", text="Due Date")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("title", width=220, minwidth=150, anchor=tk.W)
        self.tree.column("due_date", width=120, minwidth=100, anchor=tk.CENTER)
        self.tree.column("status", width=100, minwidth=80, anchor=tk.CENTER)

        btn_panel = tk.Frame(right_frame, pady=10)
        btn_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.complete_btn = tk.Button(btn_panel, text="Mark Complete", font=("Arial", 9), command=self.handle_mark_complete)
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = tk.Button(btn_panel, text="Edit Task", font=("Arial", 9), command=self.open_edit_window)
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_panel, text="Delete Task", font=("Arial", 9), bg="#e74c3c", fg="white", activebackground="#c0392b", command=self.handle_delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_btn = tk.Button(btn_panel, text="Refresh", font=("Arial", 9), command=self.refresh_table)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5)

    def create_status_bar(self):
        self.status_label = tk.Label(self.root, text="Pending Tasks: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9), padx=10)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def handle_add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()

        if not title or not due_date:
            messagebox.showerror("Validation Error", "Title and Due Date are required fields!")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Date format must be YYYY-MM-DD!")
            return

        self.manager.add_task(title, description, due_date)
        
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        
        self.refresh_table()
        messagebox.showinfo("Success", "Task created successfully!")

    def handle_mark_complete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a task from the list.")
            return

        task_id = int(self.tree.item(selected_item[0])['values'][0])
        if self.manager.update_task(task_id, status="Completed"):
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Task could not be updated.")

    def handle_delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a task to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?")
        if confirm:
            task_id = int(self.tree.item(selected_item[0])['values'][0])
            if self.manager.delete_task(task_id):
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Task could not be deleted.")

    def open_edit_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a task to edit.")
            return

        task_id = int(self.tree.item(selected_item[0])['values'][0])
        
        EditTaskWindow(
            parent=self.root, 
            task_id=task_id, 
            task_manager=self.manager, 
            on_success_callback=self.refresh_table
        )

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_query = self.search_var.get().strip().lower()
        if search_query == "search tasks...":
            search_query = ""

        current_filter = self.filter_var.get().lower()
        all_tasks = self.manager.get_all_tasks()
        pending_count = 0

        for task in all_tasks:
            if task.status.lower() == "pending":
                pending_count += 1

            if current_filter == "pending" and task.status.lower() != "pending":
                continue
            if current_filter == "completed" and task.status.lower() != "completed":
                continue

            if search_query and (search_query not in task.title.lower() and search_query not in task.description.lower()):
                continue

            self.tree.insert("", tk.END, values=(task.id, task.title, task.due_date, task.status.capitalize()))

        self.status_label.config(text=f"Pending Tasks: {pending_count}")

    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Search tasks...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def on_search_focus_out(self, event):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search tasks...")
            self.search_entry.config(fg="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMasterApp(root)
    root.mainloop()