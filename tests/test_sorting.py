import pytest
from todo.user import User
from todo.task import Task, Priority
from datetime import datetime, timedelta
from todo.todolist import ToDoList

def test_sort_by_priority_ascending(todo_with_sample_tasks):
    sorted_tasks = todo_with_sample_tasks.get_tasks_sorted(by="priority", reverse=False)
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value)


def test_sort_by_priority_descending(todo_with_sample_tasks):
    sorted_tasks = todo_with_sample_tasks.get_tasks_sorted(by="priority", reverse=True)
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value, reverse=True)


def test_sort_by_priority_then_title(todo_with_sample_tasks):
    # dodatkowy test – sortujemy po priorytecie, a w ramach tego samego priorytetu po tytule
    sorted_tasks = sorted(
        todo_with_sample_tasks.tasks,
        key=lambda t: (t.priority.value, t.title)
    )
    priorities = [task.priority for task in sorted_tasks]
    assert priorities == sorted(priorities, key=lambda p: p.value)

def test_sort_by_priority_after_save_and_load(tmp_path, todo_with_sample_tasks, sample_tasks):
    # 1. Zapisujemy listę zadań do pliku
    file_path = tmp_path / "tasks.json"
    todo_with_sample_tasks.save_to_file(str(file_path))

    # 2. Wczytujemy listę zadań do nowej instancji
    from todo.todolist import ToDoList
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    # 3. Sortujemy po priorytecie rosnąco
    sorted_tasks = new_todo.get_tasks_sorted(by="priority", reverse=False)
    priorities = [task.priority for task in sorted_tasks]

    # 4. Sprawdzamy, czy kolejność priorytetów jest poprawna
    assert priorities == sorted(priorities, key=lambda p: p.value)

    # 5. Dodatkowe sprawdzenie: czy priorytety po odczycie są takie same jak w oryginale
    loaded_priorities = sorted([t.priority for t in new_todo.tasks], key=lambda p: p.value)
    original_priorities = sorted([t.priority for t in sample_tasks], key=lambda p: p.value)
    assert loaded_priorities == original_priorities

def test_sort_by_date_created_after_save_and_load(tmp_path, todo_with_sample_tasks):
    # 1. Zapisujemy listę zadań do pliku
    file_path = tmp_path / "tasks.json"
    todo_with_sample_tasks.save_to_file(str(file_path))

    # 2. Wczytujemy listę do nowej instancji
    from todo.todolist import ToDoList
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    # 3. Sortujemy po dacie utworzenia rosnąco
    sorted_tasks = new_todo.get_tasks_sorted(by="created", reverse=False)
    dates = [task.date_created for task in sorted_tasks]

    # 4. Sprawdzamy, czy daty są posortowane rosnąco
    assert dates == sorted(dates)

    # 5. Sortowanie malejące – kontrola odwrotności
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
    # Przygotowanie listy zadań
    todo = ToDoList()
    todo.add_task(Task("B zadanie", "Opis", deadline=datetime.now() + timedelta(days=1), priority=Priority.MEDIUM))
    todo.add_task(Task("A zadanie", "Opis", deadline=datetime.now() + timedelta(days=2), priority=Priority.LOW))
    todo.add_task(Task("C zadanie", "Opis", deadline=datetime.now() + timedelta(days=3), priority=Priority.HIGH,))

    # Zapis do pliku
    file_path = tmp_path / "tasks.json"
    todo.save_to_file(str(file_path))

    # Wczytanie do nowej instancji
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    # Sortowanie
    sorted_tasks = new_todo.get_tasks_sorted(by=sort_by, reverse=reverse)

    # Pobranie wartości klucza do porównania
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
        pytest.fail(f"Nieznany klucz sortowania: {sort_by}")

    # Sprawdzenie porządku sortowania
    expected = sorted(values, reverse=reverse)
    assert values == expected