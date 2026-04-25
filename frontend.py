import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from datetime import datetime

from backend import TaskManager


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List Pro")
        self.root.geometry("1200x750")
        self.root.configure(bg="#2c3e50")

        self.backend = TaskManager()
        self.current_filter = "All"

        self.setup_styles()
        self.create_widgets()
        self.update_list()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Task.Treeview", font=("Segoe UI", 11), rowheight=35)
        style.configure("Task.Treeview.Heading", font=("Segoe UI", 12, "bold"))

    def create_widgets(self):
        header = tk.Label(self.root, text="📝 ToDo List Pro", font=("Segoe UI", 24, "bold"),
                          bg="#2c3e50", fg="white")
        header.pack(pady=15)

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_panel = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=10)

        right_panel = tk.Frame(main_frame, bg="#2c3e50")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ========== ЛЕВАЯ ПАНЕЛЬ ==========
        tk.Label(left_panel, text="📌 Task:", font=("Segoe UI", 13, "bold"),
                 bg="#34495e", fg="white").pack(pady=(20, 5), padx=15, anchor=tk.W)

        self.task_entry = tk.Text(left_panel, height=3, width=35, font=("Segoe UI", 11),
                                  bg="white", fg="black", relief=tk.SUNKEN, bd=2, wrap=tk.WORD)
        self.task_entry.pack(padx=15, pady=5)

        tk.Label(left_panel, text="⚡ Priority:", font=("Segoe UI", 13, "bold"),
                 bg="#34495e", fg="white").pack(pady=(15, 5), padx=15, anchor=tk.W)

        self.priority_var = tk.StringVar(value="Medium")
        for text, value in [("🔴 High", "High"), ("🟡 Medium", "Medium"), ("🟢 Low", "Low")]:
            rb = tk.Radiobutton(left_panel, text=text, variable=self.priority_var, value=value,
                                bg="#34495e", fg="white", selectcolor="#34495e", font=("Segoe UI", 11),
                                activebackground="#34495e", activeforeground="white")
            rb.pack(anchor=tk.W, padx=15, pady=3)

        tk.Label(left_panel, text="⏰ Deadline:", font=("Segoe UI", 13, "bold"),
                 bg="#34495e", fg="white").pack(pady=(15, 5), padx=15, anchor=tk.W)

        self.deadline_var = tk.StringVar(value="No deadline")
        deadlines = ["No deadline", "Today", "Tomorrow", "This week", "Next week", "Custom"]
        self.deadline_combo = ttk.Combobox(left_panel, textvariable=self.deadline_var,
                                           values=deadlines, state="readonly", width=25, font=("Segoe UI", 11))
        self.deadline_combo.pack(padx=15, pady=5)

        self.custom_date_frame = tk.Frame(left_panel, bg="#34495e")
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        date_frame = tk.Frame(self.custom_date_frame, bg="#34495e")
        date_frame.pack(pady=5)

        tk.Entry(date_frame, textvariable=self.day_var, width=5, font=("Segoe UI", 11), bg="white").pack(side=tk.LEFT,
                                                                                                         padx=2)
        tk.Label(date_frame, text="/", bg="#34495e", fg="white", font=("Segoe UI", 12)).pack(side=tk.LEFT)
        tk.Entry(date_frame, textvariable=self.month_var, width=5, font=("Segoe UI", 11), bg="white").pack(side=tk.LEFT,
                                                                                                           padx=2)
        tk.Label(date_frame, text="/", bg="#34495e", fg="white", font=("Segoe UI", 12)).pack(side=tk.LEFT)
        tk.Entry(date_frame, textvariable=self.year_var, width=7, font=("Segoe UI", 11), bg="white").pack(side=tk.LEFT,
                                                                                                          padx=2)

        self.deadline_combo.bind("<<ComboboxSelected>>", self.on_deadline_change)

        self.add_btn = tk.Button(left_panel, text="➕ Add Task", font=("Segoe UI", 13, "bold"),
                                 bg="#2ecc71", fg="white", relief=tk.RAISED, cursor="hand2",
                                 activebackground="#27ae60", activeforeground="white",
                                 command=self.add_task)
        self.add_btn.pack(pady=(25, 20), padx=15, fill=tk.X)

        # ========== ПРАВАЯ ПАНЕЛЬ ==========
        btn_frame = tk.Frame(right_panel, bg="#2c3e50")
        btn_frame.pack(pady=10, fill=tk.X)

        self.complete_btn = tk.Button(btn_frame, text="✅ Complete", font=("Segoe UI", 11, "bold"),
                                      bg="#2980b9", fg="white", relief=tk.RAISED, cursor="hand2",
                                      width=14, command=self.complete_task)
        self.complete_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_btn = tk.Button(btn_frame, text="🗑️ Delete", font=("Segoe UI", 11, "bold"),
                                    bg="#c0392b", fg="white", relief=tk.RAISED, cursor="hand2",
                                    width=14, command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_btn = tk.Button(btn_frame, text="💾 Save to File", font=("Segoe UI", 11, "bold"),
                                  bg="#27ae60", fg="white", relief=tk.RAISED, cursor="hand2",
                                  width=14, command=self.save_tasks)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.theme_btn = tk.Button(btn_frame, text="🎨 Theme", font=("Segoe UI", 11, "bold"),
                                   bg="#8e44ad", fg="white", relief=tk.RAISED, cursor="hand2",
                                   width=14, command=self.change_theme)
        self.theme_btn.pack(side=tk.LEFT, padx=5, pady=5)

        filter_frame = tk.Frame(right_panel, bg="#2c3e50")
        filter_frame.pack(pady=10, fill=tk.X)
        tk.Label(filter_frame, text="🔍 Show:", font=("Segoe UI", 11, "bold"),
                 bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=10)

        filters = [("📋 All", "All"), ("🟢 Active", "Active"), ("✅ Completed", "Completed"),
                   ("⏰ Expired", "Expired"), ("⭐ By Priority", "Priority")]
        self.filter_btns = {}
        for text, value in filters:
            btn = tk.Button(filter_frame, text=text, font=("Segoe UI", 9),
                            bg="#34495e", fg="white", relief=tk.RAISED, cursor="hand2",
                            command=lambda v=value: self.apply_filter(v))
            btn.pack(side=tk.LEFT, padx=5)
            self.filter_btns[value] = btn

        # Таблица - увеличенные колонки
        columns = ("Status", "Priority", "Task", "Deadline", "Days Left")
        self.task_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15, style="Task.Treeview")

        self.task_tree.heading("Status", text="✅ Status")
        self.task_tree.heading("Priority", text="⚡ Priority")
        self.task_tree.heading("Task", text="📌 Task")
        self.task_tree.heading("Deadline", text="⏰ Deadline")
        self.task_tree.heading("Days Left", text="📅 Days Left")

        self.task_tree.column("Status", width=100, anchor="center")
        self.task_tree.column("Priority", width=110, anchor="center")
        self.task_tree.column("Task", width=500)
        self.task_tree.column("Deadline", width=180, anchor="center")
        self.task_tree.column("Days Left", width=150, anchor="center")

        self.task_tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def on_deadline_change(self, event):
        if self.deadline_var.get() == "Custom":
            self.custom_date_frame.pack(pady=5, padx=15)
        else:
            self.custom_date_frame.pack_forget()

    def add_task(self):
        task_text = self.task_entry.get("1.0", tk.END).strip()
        if not task_text:
            messagebox.showwarning("⚠️ Error", "Enter a task!")
            return

        priority = self.priority_var.get()
        deadline_choice = self.deadline_var.get()

        if deadline_choice == "Custom":
            deadline_date = TaskManager.calculate_deadline_date(
                deadline_choice, self.day_var.get(), self.month_var.get(), self.year_var.get()
            )
            deadline_display = f"{self.day_var.get()}.{self.month_var.get()}.{self.year_var.get()}"
        else:
            deadline_date = TaskManager.calculate_deadline_date(deadline_choice)
            deadline_display = deadline_choice

        if deadline_choice != "No deadline" and deadline_date is None:
            messagebox.showwarning("⚠️ Error", "Invalid date!")
            return

        self.backend.add_task(task_text, priority, deadline_display, deadline_date)
        self.task_entry.delete("1.0", tk.END)
        self.update_list()
        messagebox.showinfo("✅ Success", "Task added!")

    def update_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = self.backend.filter_tasks(self.current_filter)

        for task in tasks:
            if task["completed"]:
                status = "✅ Done"
            else:
                status = "⬜ Pending"

            priority = task.get("priority", "Medium")
            if priority == "High":
                priority_display = "🔴 High"
            elif priority == "Medium":
                priority_display = "🟡 Medium"
            else:
                priority_display = "🟢 Low"

            deadline_date = datetime.fromisoformat(task["deadline_date"]).date() if task.get("deadline_date") else None
            deadline_status, deadline_icon, days_left = TaskManager.get_deadline_status(deadline_date)

            if not task["completed"] and deadline_date and days_left is not None and days_left < 0:
                deadline_display = f"🔴 EXPIRED! ({task['deadline']})"
                days_display = f"⚠️ +{-days_left} days overdue"
            elif not task["completed"] and deadline_date and days_left == 0:
                deadline_display = f"🟠 TODAY! ({task['deadline']})"
                days_display = "⚠️ DUE TODAY"
            else:
                deadline_display = f"🟢 {task['deadline']}"
                days_display = f"📅 {abs(days_left)} days" if deadline_date and days_left is not None else "⚪ No deadline"

            self.task_tree.insert("", tk.END, values=(
                status,
                priority_display,
                task["text"][:70],
                deadline_display,
                days_display
            ))

    def apply_filter(self, filter_type):
        self.current_filter = filter_type
        self.update_list()
        for f, btn in self.filter_btns.items():
            btn.config(bg="#34495e", fg="white")
        if filter_type in self.filter_btns:
            self.filter_btns[filter_type].config(bg="#27ae60", fg="white")

    def get_selected_task_id(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Error", "Select a task first!")
            return None

        item = selected[0]
        values = self.task_tree.item(item, "values")
        task_text = values[2]

        for task in self.backend.tasks:
            if task["text"][:70] == task_text:
                return task["id"]
        return None

    def complete_task(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            self.backend.toggle_complete(task_id)
            self.update_list()
            messagebox.showinfo("✅ Success", "Task status updated!")

    def delete_task(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            if messagebox.askyesno("🗑️ Confirm", "Delete this task?"):
                self.backend.delete_task(task_id)
                self.update_list()
                messagebox.showinfo("✅ Success", "Task deleted!")

    def save_tasks(self):
        self.backend.save_tasks()
        messagebox.showinfo("💾 Success", "Tasks saved to file!")

    def change_theme(self):
        color = colorchooser.askcolor(title="🎨 Choose theme color")[1]
        if color:
            self.root.configure(bg=color)
            for widget in self.root.winfo_children():
                self.update_bg_color(widget, color)

    def update_bg_color(self, widget, color):
        try:
            widget.configure(bg=color)
        except:
            pass
        for child in widget.winfo_children():
            self.update_bg_color(child, color)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()