import pytest
from todo.user import User
from todo.task import Task, Priority
from datetime import datetime, timedelta
from todo.todolist import ToDoList

def test_sort_by_priority_ascending(todo_with_sample_tasks):
    """Sorting by priority asc"""
    sorted_tasks = todo_with_sample_tasks.get_tasks_sorted(by="priority", reverse=False)
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value)


def test_sort_by_priority_descending(todo_with_sample_tasks):
    """Sorting by priority desc"""
    sorted_tasks = todo_with_sample_tasks.get_tasks_sorted(by="priority", reverse=True)
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value, reverse=True)


def test_sort_by_priority_then_title(todo_with_sample_tasks):
    """Sorting by priority and then by title"""""
    sorted_tasks = sorted(
        todo_with_sample_tasks.tasks,
        key=lambda t: (t.priority.value, t.title)
    )
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value)

def test_sort_by_priority_after_save_and_load(tmp_path, todo_with_sample_tasks, sample_tasks):
    """Sorting by priority after save and load"""
    file_path = tmp_path / "tasks.json"
    todo_with_sample_tasks.save_to_file(str(file_path))

    from todo.todolist import ToDoList
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    sorted_tasks = new_todo.get_tasks_sorted(by="priority", reverse=False)
    priorities = [task.priority for task in sorted_tasks]

    assert priorities == sorted(priorities, key=lambda p: p.value)

    loaded_priorities = sorted([t.priority for t in new_todo.tasks], key=lambda p: p.value)
    original_priorities = sorted([t.priority for t in sample_tasks], key=lambda p: p.value)
    assert loaded_priorities == original_priorities

def test_sort_by_date_created_after_save_and_load(tmp_path, todo_with_sample_tasks):
    """Sorting by creation date after save and load"""
    file_path = tmp_path / "tasks.json"
    todo_with_sample_tasks.save_to_file(str(file_path))

    from todo.todolist import ToDoList
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    sorted_tasks = new_todo.get_tasks_sorted(by="created", reverse=False)
    dates = [task.date_created for task in sorted_tasks]

    assert dates == sorted(dates)

    sorted_tasks_desc = new_todo.get_tasks_sorted(by="created", reverse=True)
    dates_desc = [task.date_created for task in sorted_tasks_desc]
    assert dates_desc == sorted(dates, reverse=True)

@pytest.mark.parametrize("sort_by, reverse", [
    ("title", False),
    ("title", True),
    ("created", False),
    ("created", True),
    ("deadline", False),
    ("deadline", True),
    ("priority", False),
    ("priority", True),
])
def test_sorting_after_save_and_load(tmp_path, sort_by, reverse):
    """Sorting after save and load"""
    todo = ToDoList()
    todo.add_task(Task("B task", "Description", deadline=datetime.now() + timedelta(days=1), priority=Priority.MEDIUM))
    todo.add_task(Task("A task", "Description", deadline=datetime.now() + timedelta(days=2), priority=Priority.LOW))
    todo.add_task(Task("C task", "Description", deadline=datetime.now() + timedelta(days=3), priority=Priority.HIGH,))

    file_path = tmp_path / "tasks.json"
    todo.save_to_file(str(file_path))

    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    sorted_tasks = new_todo.get_tasks_sorted(by=sort_by, reverse=reverse)

    if sort_by == "title":
        values = [task.title for task in sorted_tasks]
    elif sort_by == "created":
        values = [task.date_created for task in sorted_tasks]
    elif sort_by == "deadline":
        values = [task.deadline for task in sorted_tasks]
    elif sort_by == "priority":
        values = [task.priority.value for task in sorted_tasks]
        #expected = sorted(values, reverse=reverse)
    else:
        pytest.fail(f"Invalid sorting criteria: {sort_by}")

    expected = sorted(values, reverse=reverse)
    assert values == expected