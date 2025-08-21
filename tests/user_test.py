import os
import pytest
from todo.user import User
from todo.todolist import ToDoList
from todo.task import Task, Priority
from datetime import datetime
import re
from datetime import datetime, timedelta



def test_add_task(user):
    """Add task"""
    user.add_task("Shopping", "Buy bread and milk")

    task = user.find_task("Shopping")
    assert task is not None
    assert task.title == "Shopping"
    assert task.description == "Buy bread and milk"
    assert not task.is_done()

def test_complete_task(user):
    """Mark task as a completed"""
    user.add_task("Training", "Yoga 15 min")
    user.complete_task("Training")
    task = user.find_task("Training")
    assert task.is_done()

def test_remove_task(user):
    """Remove task"""
    user.add_task("Cooking", "Dinner")

    assert user.remove_task("Cooking") is True
    assert user.find_task("Cooking") is None


def test_show_all_tasks(user_with_tasks, capsys):
    """Show all tasks"""
    user_with_tasks.show_all_tasks()
    captured = capsys.readouterr()

    assert "Task1" in captured.out
    assert "Task1 description" in captured.out
    assert "Task2" in captured.out
    assert "Task2 description" in captured.out


    pattern4 = (
        r"\[✗\] Task1 - Task1 description "
        r"\(Created: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    pattern3 = (
        r"\[✗\] Task2 - Task2 description "
        r"\(Created: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )

    assert re.search(pattern4, captured.out)
    assert re.search(pattern3, captured.out)

    assert user_with_tasks.count_tasks() == 2


def test_show_completed_tasks(user_with_pending_and_completed_tasks, capsys):
    """Show completed tasks"""
    user = user_with_pending_and_completed_tasks
    user.show_completed_tasks()
    captured = capsys.readouterr()

    pattern = (
        r"\[✓\] A - a "
        r"\(Created: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    assert re.search(pattern, captured.out)

    assert "- B" not in captured.out
    assert "b" not in captured.out

    assert user.count_completed_tasks() == 1


def test_show_pending_tasks(user_with_pending_and_completed_tasks, capsys):
    """Show pending tasks"""
    user = user_with_pending_and_completed_tasks
    user.show_pending_tasks()
    captured = capsys.readouterr()

    assert "[✓] A - a" not in captured.out

    pattern = (
        r"\[✗\] B - b "
        r"\(Created: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    assert re.search(pattern, captured.out)

    assert user.count_pending_tasks() == 1


def test_show_completed_tasks_empty(user,capsys):
    """No tasks completed"""
    user.show_completed_tasks()
    captured = capsys.readouterr()
    assert "No tasks completed." in captured.out

def test_show_pending_tasks_empty(user,capsys):
    """No pending tasks"""
    user.show_pending_tasks()
    captured = capsys.readouterr()
    assert "No tasks to do." in captured.out

def test_tasks_with_same_description(user):
    """Tasks with the same description"""
    user.add_task("Task1", "Description")
    user.add_task("Task2", "Description")
    user.complete_task("Task1")
    assert user.count_completed_tasks() == 1
    assert user.count_pending_tasks() == 1

def test_count_completed(user_with_1_completed_and_2_pending):
    """How many tasks is completed"""
    assert user_with_1_completed_and_2_pending.count_completed_tasks() == 1

def test_task_has_date():
    """Checking if the task creation date is added"""
    task = Task("Task", "Description")
    assert task.date_created is not None
    assert isinstance(task.date_created, datetime)

def test_task_with_deadline(user):
    """Checking if the task has deadline"""
    deadline = datetime.now() + timedelta(days=3)
    user.add_task("Task with deadline", "Description", deadline=deadline)
    task = user.find_task("Task with deadline")
    assert task is not None
    assert task.deadline is not None
    assert abs((task.deadline - deadline).total_seconds()) < 1  # prawie równe

def test_task_list_debug():
    """Task list debug"""
    todo = ToDoList()
    todo.add_task(Task("A", "Description 1", priority=Priority.LOW))
    todo.add_task(Task("B", "Description 2", completed=True, priority=Priority.HIGH))

    assert len(todo.tasks) == 2

def test_task_priority_set():
    """Checking if the task has priority"""
    task = Task("Task", "Description", priority=Priority.HIGH)

    assert task.priority == Priority.HIGH
    assert task.priority.name == "HIGH"

@pytest.mark.parametrize("priority", [Priority.LOW, Priority.MEDIUM, Priority.HIGH])
def test_priority_saved_and_loaded_all_levels(tmp_path, priority):
    """Checking tasks with priorities"""

    todo = ToDoList()
    todo.add_task(Task("Task", "Description", priority=priority))


    file_path = tmp_path / "tasks.json"
    todo.save_to_file(str(file_path))
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))
    loaded_task = new_todo.find_task("Task")

    assert loaded_task.priority == priority, (
        f"Loaded task priority ({loaded_task.priority}) "
        f"different from the one written down ({priority})"
    )

def test_priority_saved_and_loaded_multiple_tasks(tmp_path, sample_tasks):
    """Checking tasks"""
    todo = ToDoList()
    for task in sample_tasks:
        todo.add_task(task)

    file_path = tmp_path / "tasks.json"
    todo.save_to_file(str(file_path))

    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    for original_task in sample_tasks:
        loaded_task = new_todo.find_task(original_task.title)
        assert loaded_task is not None
        assert loaded_task.priority == original_task.priority