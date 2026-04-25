import json
from datetime import datetime, timedelta


class TaskManager:

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, text, priority, deadline_str, deadline_date):
        task = {
            "id": len(self.tasks),
            "text": text,
            "completed": False,
            "priority": priority,
            "deadline": deadline_str,
            "deadline_date": deadline_date.isoformat() if deadline_date else None,
            "created_date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        self.tasks.append(task)
        self.sort_by_priority()
        self.save_tasks()
        return task

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def toggle_complete(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.sort_by_priority()
                self.save_tasks()
                return True
        return False

    def sort_by_priority(self):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        self.tasks.sort(key=lambda t: (
            t["completed"],
            priority_order.get(t.get("priority", "Medium"), 1),
            t.get("id", 0)
        ))

    def get_all_tasks(self):
        return self.tasks.copy()

    def get_active_tasks(self):
        return [t for t in self.tasks if not t["completed"]]

    def get_completed_tasks(self):
        return [t for t in self.tasks if t["completed"]]

    def get_expired_tasks(self):
        today = datetime.now().date()
        return [t for t in self.tasks
                if not t["completed"] and t.get("deadline_date")
                and datetime.fromisoformat(t["deadline_date"]).date() < today]

    def get_sorted_by_priority(self):
        active = self.get_active_tasks()
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        return sorted(active, key=lambda t: priority_order.get(t.get("priority", "Medium"), 1))

    def filter_tasks(self, filter_type):
        if filter_type == "All":
            return self.get_all_tasks()
        elif filter_type == "Active":
            return self.get_active_tasks()
        elif filter_type == "Completed":
            return self.get_completed_tasks()
        elif filter_type == "Expired":
            return self.get_expired_tasks()
        elif filter_type == "Priority":
            return self.get_sorted_by_priority()
        return self.get_all_tasks()

    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                for i, task in enumerate(self.tasks):
                    if "id" not in task:
                        task["id"] = i
                self.sort_by_priority()
        except FileNotFoundError:
            self.tasks = []

    @staticmethod
    def calculate_deadline_date(deadline_choice, day=None, month=None, year=None):
        today = datetime.now().date()
        if deadline_choice == "Today":
            return today
        elif deadline_choice == "Tomorrow":
            return today + timedelta(days=1)
        elif deadline_choice == "This week":
            return today + timedelta(days=7 - today.weekday())
        elif deadline_choice == "Next week":
            return today + timedelta(days=14 - today.weekday())
        elif deadline_choice == "Custom" and day and month and year:
            try:
                return datetime(int(year), int(month), int(day)).date()
            except:
                return None
        return None

    @staticmethod
    def get_deadline_status(deadline_date):
        if deadline_date is None:
            return "No deadline", "⚪", None
        today = datetime.now().date()
        days_left = (deadline_date - today).days
        if days_left < 0:
            return f"EXPIRED! (+{-days_left}d)", "🔴", days_left
        elif days_left == 0:
            return "Due TODAY!", "🟠", 0
        elif days_left <= 3:
            return f"Due in {days_left} days", "🟡", days_left
        else:
            return f"Due in {days_left} days", "🟢", days_left