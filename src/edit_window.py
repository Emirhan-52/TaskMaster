import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Securing the module search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

class EditTaskWindow:
    def __init__(self, parent, task_id, task_manager, on_success_callback=None):
        """
        Initializes the Edit Task popup window.
        
        :param parent: The parent Tkinter window (main application window)
        :param task_id: The unique ID of the task to be edited
        :param task_manager: The active TaskManager instance handling the data
        :param on_success_callback: A function to run (like refresh_table) after a successful save
        """
        self.parent = parent
        self.task_id = task_id
        self.manager = task_manager
        self.on_success_callback = on_success_callback

        # Fetch the existing task details
        self.task = self.manager.get_task(self.task_id)
        if not self.task:
            messagebox.showerror("Error", f"Task with ID #{self.task_id} not found.")
            return

        # Configure the Toplevel Window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Edit Task")
        self.window.geometry("400x440")  # Slightly expanded height to comfortably fit the Status combobox
        self.window.resizable(False, False)
        self.window.grab_set()  # Freeze parent window inputs while this modal is active

        self.create_widgets()
        self.prefill_data()

    def create_widgets(self):
        """Creates form fields, labels, and action buttons."""
        
        # Form Header
        header_label = tk.Label(self.window, text=f"Updating Task #{self.task_id}", font=("Arial", 12, "bold"))
        header_label.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Task Title Field
        tk.Label(self.window, text="Task Title *", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(5, 2))
        self.title_entry = tk.Entry(self.window, font=("Arial", 10), width=45)
        self.title_entry.pack(padx=20, pady=(0, 10))

        # Description Field
        tk.Label(self.window, text="Description", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(5, 2))
        self.desc_text = tk.Text(self.window, font=("Arial", 10), height=5, width=45)
        self.desc_text.pack(padx=20, pady=(0, 10))

        # Due Date Field
        tk.Label(self.window, text="Due Date (YYYY-MM-DD) *", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(5, 2))
        self.date_entry = tk.Entry(self.window, font=("Arial", 10), width=45)
        self.date_entry.pack(padx=20, pady=(0, 10))

        # Status Combobox Field
        tk.Label(self.window, text="Status *", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(5, 2))
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(self.window, textvariable=self.status_var, values=["Pending", "Completed"], state="readonly", width=42)
        self.status_combobox.pack(padx=20, pady=(0, 20))

        # Buttons Panel Frame
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        # Cancel Button
        cancel_btn = tk.Button(btn_frame, text="Cancel", font=("Arial", 10), width=12, command=self.window.destroy)
        cancel_btn.pack(side=tk.LEFT)

        # Save Changes Button
        save_btn = tk.Button(btn_frame, text="Save Changes", font=("Arial", 10, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", width=15, command=self.handle_save)
        save_btn.pack(side=tk.RIGHT)

    def prefill_data(self):
        """Pre-populates the fields with the current task registry metrics."""
        self.title_entry.insert(0, self.task.title)
        self.desc_text.insert("1.0", self.task.description)
        self.date_entry.insert(0, self.task.due_date)
        
        # Ensure proper casing matches combobox selection values
        current_status = self.task.status.capitalize() if self.task.status else "Pending"
        self.status_combobox.set(current_status)

    def handle_save(self):
        """Validates entry values and updates the database record."""
        new_title = self.title_entry.get().strip()
        new_desc = self.desc_text.get("1.0", tk.END).strip()
        new_date = self.date_entry.get().strip()
        new_status = self.status_var.get()

        # Input Validation
        if not new_title or not new_date:
            messagebox.showerror("Validation Error", "Title and Due Date cannot be empty!", parent=self.window)
            return

        # Syntax Date Format Validation
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Date format must be YYYY-MM-DD!", parent=self.window)
            return

        # Commit changes to the task manager (Triggers Auto-save inside manager layer)
        success = self.manager.update_task(
            task_id=self.task_id, 
            title=new_title, 
            description=new_desc, 
            due_date=new_date, 
            status=new_status
        )

        if success:
            if self.on_success_callback:
                self.on_success_callback()  # Trigger UI reload on the main view grid
            self.window.destroy()
            messagebox.showinfo("Success", "Task updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update the task in local storage.", parent=self.window)