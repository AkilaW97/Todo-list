import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import os
from datetime import datetime

# To-Do List Application
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = []
        self.filename = "task.json"

        #Load task from file (if it exists)
        self.load_tasks()

        # GUI Elements
        self.task_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.due_date_button = tk.Button(root, text="Set Due Date", font=("Arial", 12), command=self.set_due_date)
        self.due_date_button.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Task", font=("Arial", 12), command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, font=("Arial", 12), width=40, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", font=("Arial", 12), command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.complete_button = tk.Button(root, text="Mark Complete", font=("Arial", 12), command=self.mark_complete)
        self.complete_button.grid(row=2, column=1, padx=10, pady=10)

        #Update the task listbox with loaded tasks
        self.update_task_listbox()

    def set_due_date(self):
        """Prompt the user to enter a due date."""
        due_date_str = simpledialog.askstring("Due date", "Enter due date (YYYY-MM-DD):")
        if due_date_str:
            try:
                self.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                messagebox.showinfo("Due Date", f"Due date set to {self.due_date}")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({"title": task, "completed": False})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]["completed"] = True
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            self.task_listbox.insert(tk.END, f"{status} {task['title']}")

    def save_task(self):
        """Save task to a JSON file"""
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        """Load tasks from a JSON file (if it exists)."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()