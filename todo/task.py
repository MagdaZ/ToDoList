from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Enum representing task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    """Represents a single task in the todo list."""
    def __init__(self, title, description, completed=False, deadline=None, priority=None):
        """
        Initialize a new task.

        Args:
            title (str): The title of the task.
            description (str): A short description of the task.
            completed (bool, optional): Whether the task is completed. Defaults to False.
            deadline (datetime | None, optional): Deadline for the task. Defaults to None.
            priority (Priority | None, optional): Task priority. Defaults to None.
        """
        self.title = title
        self.description = description
        self.completed = completed
        self.date_created = datetime.now()
        self.deadline = deadline
        self.priority = priority

    def __repr__(self):
        """Return  string representation of the task (for debugging)."""
        return (f"Task(title={self.title!r}, description={self.description!r}, "
                f"completed={self.completed}, "
                f"date_created={self.date_created!r}, "
                f"deadline={self.deadline!r}, "
                f"priority={self.priority!r})")

    def __str__(self):
        """Return a human-readable string representation of the task."""
        status = "[✓]" if self.completed else "[✗]"
        base = f"{status} {self.title} - {self.description} (Created: {self.date_created.strftime('%Y-%m-%d %H:%M')})"
        if self.deadline:
            base += f" (Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')})"
        priority_str = self.priority.name if self.priority else "Brak"
        base += f" (Priority: {priority_str})"
        return base

    def mark_done(self):
        """Mark the task as completed."""
        self.completed = True

    def is_done(self):
        """
        Check if the task is completed.

        Returns:
            bool: True if completed, False otherwise.
        """
        return self.completed

    def to_dict(self):
        """
        Convert the task to a dictionary (useful for serialization).

        Returns:
            dict: A dictionary representation of the task.
        """
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "date_created": self.date_created.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority.name
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Task object from a dictionary.

        Args:
            data (dict): A dictionary with task data.

        Returns:
            Task: A new Task instance.
        """
        deadline = datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None
        # check priority
        try:
            priority_str = data.get("priority", "MEDIUM")
            priority = Priority[priority_str] if priority_str in Priority.__members__ else Priority.MEDIUM
        except (KeyError, TypeError):
            priority = Priority.MEDIUM

        task = cls(
            data["title"],
            data["description"],
            data.get("completed", False),
            deadline=deadline,
            priority=priority
        )
        task.date_created = datetime.fromisoformat(data["date_created"])
        return task