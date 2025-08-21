import json
from .task import Task, Priority

class ToDoList:
    """A class for managing a collection of tasks."""
    def __init__(self):
        """Initialize an empty to-do list."""
        self.tasks = []

    def add_task(self,task):
        """
        Add a task to the list.

        Args:
            task (Task): The task to be added.
        """
        self.tasks.append(task)

    def find_task(self,title):
        """
        Find a task by its title.

        Args:
            title (str): The title of the task to find.

        Returns:
            Task | None: The task if found, otherwise None.
        """
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_completed_tasks(self):
        """
        Get all completed tasks.

        Returns:
            list[Task]: A list of tasks marked as completed.
        """
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self):
        """
        Get all pending (not completed) tasks.

        Returns:
            list[Task]: A list of tasks not yet completed.
        """
        return [task for task in self.tasks if not task.completed]

    def show_all_tasks(self):
        """
        Print all tasks to the console.

        If no tasks exist, prints "No tasks.".
        """
        if not self.tasks:
            print("No tasks.")
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
            print(f"[{status}] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str} Priority: {task.priority.name}")

    def remove_task(self, title):
        """
        Remove a task by its title.

        Args:
            title (str): The title of the task to remove.

        Returns:
            bool: True if the task was removed, False if not found.
        """
        task = self.find_task(title)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def show_completed_tasks(self):
        """
        Print all completed tasks to the console.

        If none are completed, prints "No tasks completed.".
        """
        has_completed = False
        for task in self.tasks:
            if task.completed:
                deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
                priority_str = task.priority.name if task.priority else ""
                print(f"[✓] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str} Priority: {priority_str}")
                has_completed = True
        if not has_completed:
            print("No tasks completed.")

    def show_pending_tasks(self):
        """
        Print all pending (not completed) tasks to the console.

        If none are pending, prints "No tasks to do.".
        """
        has_pending = False
        for task in self.tasks:
            if not task.completed:
                deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
                priority_str = task.priority.name if task.priority else ""
                print(f"[✗] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str} Priority: {priority_str}")
                has_pending = True
        if not has_pending:
            print("No tasks to do.")

    def mark_done(self, title):
        """
        Mark a task as completed.

        Args:
            title (str): The title of the task to mark.

        Returns:
            bool: True if the task was marked as done, False if not found.
        """
        task = self.find_task(title)
        if task:
            task.completed = True
            return True
        return False

    def save_to_file(self, file_path):
        """
        Save all tasks to a JSON file.

        Args:
            file_path (str): Path to the file where tasks will be saved.
        """
        data = [task.to_dict() for task in self.tasks]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, file_path):
        """
        Load tasks from a JSON file.

        Args:
            file_path (str): Path to the file to load tasks from.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]

    def get_tasks_sorted(self, by="deadline", reverse=False):
        """
        Get tasks sorted by a specific attribute.

        Args:
            by (str): Sorting criteria. Options: "title", "created", "deadline", "priority". Defaults to "deadline".
            reverse (bool): If True, sorts in descending order. Defaults to False.

        Returns:
            list[Task]: A list of sorted tasks.

        Raises:
            ValueError: If the sorting criteria is invalid.
        """
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



