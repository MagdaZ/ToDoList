import json
from .task import Task, Priority

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self,task):
        self.tasks.append(task)

    def find_task(self,title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def show_all_tasks(self):
        if not self.tasks:
            print("No tasks.")
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
            print(f"[{status}] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str}")

    def remove_task(self, title):
        task = self.find_task(title)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def show_completed_tasks(self):
        has_completed = False
        for task in self.tasks:
            if task.completed:
                deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
                print(f"[✓] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str}")
                has_completed = True
        if not has_completed:
            print("No tasks completed.")

    def show_pending_tasks(self):
        has_pending = False
        for task in self.tasks:
            if not task.completed:
                deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
                print(f"[✗] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str}")
                has_pending = True
        if not has_pending:
            print("No tasks to do.")

    def mark_done(self, title):
        task = self.find_task(title)
        if task:
            task.completed = True
            return True
        return False

    def save_to_file(self, file_path):
        data = [task.to_dict() for task in self.tasks]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]

    def get_tasks_sorted(self, by="deadline", reverse=False):
        if by == "title":
            return sorted(self.tasks, key=lambda t: t.title.lower(), reverse=reverse)
        elif by == "created":
            return sorted(self.tasks, key=lambda t: t.date_created, reverse=reverse)
        elif by == "deadline":
            return sorted(self.tasks, key=lambda t: t.deadline or datetime.max, reverse=reverse)
        elif by == "priority":
            return sorted(self.tasks, key=lambda t: t.priority.value, reverse=reverse)
        else:
            raise ValueError("Invalid sorting criteria, select: title, created, deadline, priority.")



