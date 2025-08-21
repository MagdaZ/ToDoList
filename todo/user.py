import os
from .todolist import ToDoList
from .task import Task, Priority

class User:
    """
    Represents a user of the to-do list system.
    """
    def __init__(self, name):
        """
        Initialize a new user with an empty to-do list.

        Args:
            name (str): The name of the user.
        """
        self.name = name
        self.todo_list = ToDoList()

    def get_filename(self):
        """
        Get the filename for saving/loading this user's tasks.

        Returns:
            str: Full path to the user's JSON file.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, f"{self.name}_tasks.json")

    def save_tasks_to_file(self):
        """Save the user's tasks to a JSON file."""
        filename = self.get_filename()
        self.todo_list.save_to_file(filename)

    def load_tasks_from_file(self):
        """Load the user's tasks from a JSON file."""
        filename = self.get_filename()
        self.todo_list.load_from_file(filename)

    def add_task(self, title, description, deadline=None, priority=Priority.MEDIUM):
        """
        Add a new task to the user's to-do list.

        Args:
            title (str): Title of the task.
            description (str): Description of the task.
            deadline (datetime, optional): Task deadline. Defaults to None.
            priority (Priority, optional): Task priority. Defaults to Priority.MEDIUM.
        """
        task = Task(title, description, deadline=deadline, priority=priority)
        self.todo_list.add_task(task)

    def complete_task(self, title):
        """
        Mark a task as completed.

        Args:
            title (str): Title of the task to complete.

        Returns:
            bool: True if the task was found and marked, False otherwise.
        """
        return self.todo_list.mark_done(title)

    def remove_task(self, title):
        """
        Remove a task from the to-do list.

        Args:
            title (str): Title of the task to remove.

        Returns:
            bool: True if the task was found and removed, False otherwise.
        """
        return self.todo_list.remove_task(title)

    def show_all_tasks(self):
        """Print all tasks to the console."""
        self.todo_list.show_all_tasks()

    def show_completed_tasks(self):
        """Print all completed tasks to the console."""
        self.todo_list.show_completed_tasks()

    def show_pending_tasks(self):
        """Print all pending tasks to the console."""
        self.todo_list.show_pending_tasks()

    def find_task(self, title):
        """
        Find a task by title.

        Args:
            title (str): Title of the task.

        Returns:
            Task | None: The task if found, else None.
        """
        return self.todo_list.find_task(title)

    def edit_task(self, title, new_description):
        """
        Edit the description of an existing task.

        Args:
            title (str): Title of the task to edit.
            new_description (str): New description text.

         Returns:
            bool: True if task was found and updated, False otherwise.
        """
        task = self.find_task(title)
        if task:
            task.description = new_description
            return True
        return False

    def count_tasks(self):
        """
        Count the total number of tasks.

        Returns:
            int: Total tasks in the user's to-do list.
        """
        return len(self.todo_list.tasks)

    def count_completed_tasks(self):
        """
        Count the number of completed tasks.

        Returns:
            int: Number of tasks marked as completed.
        """
        return len(self.todo_list.get_completed_tasks())

    def count_pending_tasks(self):
        """
        Count the number of pending tasks.

        Returns:
            int: Number of tasks not yet completed.
        """
        return len(self.todo_list.get_pending_tasks())