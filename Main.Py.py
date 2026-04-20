import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List")
        self.root.geometry("600x500")
        self.tasks = []

        # UI elements
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.add_btn = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=5)

        columns = ("Status", "Task", "Date")
        self.task_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.task_tree.heading("Status", text="[X]")
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Date", text="Date")

        self.task_tree.column("Status", width=50)
        self.task_tree.column("Task", width=350)
        self.task_tree.column("Date", width=150)

        self.task_tree.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.complete_btn = tk.Button(btn_frame, text="Complete", command=self.complete_task)
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(btn_frame, text="Save", command=self.save_tasks)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "text": task_text,
                "completed": False,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            self.tasks.append(task)
            self.update_list()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Error", "Enter a task!")

    def update_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        for task in self.tasks:
            status = "[OK]" if task["completed"] else "[ ]"
            self.task_tree.insert("", tk.END, values=(status, task["text"], task["date"]))

    def complete_task(self):
        selected = self.task_tree.selection()
        if selected:
            index = self.task_tree.index(selected[0])
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.update_list()
            self.save_tasks()

    def delete_task(self):
        selected = self.task_tree.selection()
        if selected:
            index = self.task_tree.index(selected[0])
            del self.tasks[index]
            self.update_list()
            self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                self.update_list()
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()