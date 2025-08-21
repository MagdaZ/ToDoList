from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    def __init__(self, title, description, completed=False, deadline=None, priority=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.date_created = datetime.now()
        self.deadline = deadline
        self.priority = priority

    def __repr__(self):
        return (f"Task(title={self.title!r}, description={self.description!r}, "
                f"completed={self.completed}, "
                f"date_created={self.date_created!r}, "
                f"deadline={self.deadline!r}, "
                f"priority={self.priority!r})")

    def __str__(self):
        status = "[✓]" if self.completed else "[✗]"
        base = f"{status} {self.title} - {self.description} (Created: {self.date_created.strftime('%Y-%m-%d %H:%M')})"
        if self.deadline:
            base += f" (Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')})"
        priority_str = self.priority.name if self.priority else "Brak"
        base += f" (Priority: {priority_str})"
        return base

    def mark_done(self):
        self.completed = True

    def is_done(self):
        return self.completed

    def to_dict(self):
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