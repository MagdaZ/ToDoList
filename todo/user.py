import os
from .todolist import ToDoList
from .task import Task, Priority

class User:
    def __init__(self, name):
        self.name = name
        self.todo_list = ToDoList()

    def get_filename(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, f"{self.name}_tasks.json")

    def save_tasks_to_file(self):
        filename = self.get_filename()
        self.todo_list.save_to_file(filename)

    def load_tasks_from_file(self):
        filename = self.get_filename()
        self.todo_list.load_from_file(filename)

    def add_task(self, title, description, deadline=None, priority=Priority.MEDIUM):
        task = Task(title, description, deadline=deadline, priority=priority)
        self.todo_list.add_task(task)

    def complete_task(self, title):
        return self.todo_list.mark_done(title)

    def remove_task(self, title):
        return self.todo_list.remove_task(title)

    def show_all_tasks(self):
        self.todo_list.show_all_tasks()

    def show_completed_tasks(self):
        self.todo_list.show_completed_tasks()

    def show_pending_tasks(self):
        self.todo_list.show_pending_tasks()

    def find_task(self, title):
        return self.todo_list.find_task(title)

    def edit_task(self, title, new_description):
        task = self.find_task(title)
        if task:
            task.description = new_description
            return True
        return False

    def count_tasks(self):
        return len(self.todo_list.tasks)

    def count_completed_tasks(self):
        return len(self.todo_list.get_completed_tasks())

    def count_pending_tasks(self):
        return len(self.todo_list.get_pending_tasks())