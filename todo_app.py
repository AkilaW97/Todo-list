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

        # Load tasks from file (if it exists)
        self.load_tasks()

        # GUI Elements
        # Task entry and buttons (Row 0)
        self.task_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.due_date_button = tk.Button(root, text="Set Due Date", font=("Arial", 12), command=self.set_due_date)
        self.due_date_button.grid(row=0, column=2, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Task", font=("Arial", 12), command=self.add_task)
        self.add_button.grid(row=0, column=3, padx=10, pady=10)

        # Search bar and buttons (Row 1)
        self.search_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.search_button = tk.Button(root, text="Search", font=("Arial", 12), command=self.search_tasks)
        self.search_button.grid(row=1, column=2, padx=10, pady=10)

        self.clear_search_button = tk.Button(root, text="Clear Search", font=("Arial", 12), command=self.clear_search)
        self.clear_search_button.grid(row=1, column=3, padx=10, pady=10)

        # Filter options (Row 2)
        self.filter_var = tk.StringVar(value="all")
        self.filter_all = tk.Radiobutton(root, text="All", variable=self.filter_var, value="all", command=self.update_task_listbox)
        self.filter_all.grid(row=2, column=0, padx=10, pady=5)

        self.filter_completed = tk.Radiobutton(root, text="Completed", variable=self.filter_var, value="completed", command=self.update_task_listbox)
        self.filter_completed.grid(row=2, column=1, padx=10, pady=5)

        self.filter_incomplete = tk.Radiobutton(root, text="Incomplete", variable=self.filter_var, value="incomplete", command=self.update_task_listbox)
        self.filter_incomplete.grid(row=2, column=2, padx=10, pady=5)

        # Task listbox (Row 3)
        self.task_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10)
        self.task_listbox.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Action buttons (Row 4)
        self.delete_button = tk.Button(root, text="Delete Task", font=("Arial", 12), command=self.delete_task)
        self.delete_button.grid(row=4, column=0, padx=10, pady=10)

        self.complete_button = tk.Button(root, text="Mark Complete", font=("Arial", 12), command=self.mark_complete)
        self.complete_button.grid(row=4, column=1, padx=10, pady=10)

        # Store the due date for the current task
        self.due_date = None

        # Update the task listbox with loaded tasks
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
            task_data = {
                "title": task,
                "completed": False,
                "due_date": str(self.due_date) if self.due_date else None
            }
            self.tasks.append(task_data)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.due_date = None  # Reset due date after adding the task
            self.save_task()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_task_listbox()
            self.save_task()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]["completed"] = True
            self.update_task_listbox()
            self.save_task()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

    def update_task_listbox(self):
        """Update the task listbox based on the current filter and search."""
        self.task_listbox.delete(0, tk.END)
        filter_value = self.filter_var.get()
        search_query = self.search_entry.get().lower()

        for task in self.tasks:
            # Apply filter
            if filter_value == "completed" and not task["completed"]:
                continue
            if filter_value == "incomplete" and task["completed"]:
                continue

            # Apply search
            if search_query and search_query not in task["title"].lower():
                continue

            # Display the task
            status = "✓" if task["completed"] else "✗"
            due_date = f" (Due: {task['due_date']})" if task["due_date"] else ""
            self.task_listbox.insert(tk.END, f"{status} {task['title']}{due_date}")

    def search_tasks(self):
        """Filter tasks based on the search query."""
        self.update_task_listbox()

    def clear_search(self):
        """Clear the search bar and reset the task list."""
        self.search_entry.delete(0, tk.END)
        self.update_task_listbox()

    def save_task(self):
        """Save tasks to a JSON file."""
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