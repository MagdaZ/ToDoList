import os
import pytest
from todo.user import User
from todo.todolist import ToDoList
from todo.task import Task, Priority
from datetime import datetime
import re
from datetime import datetime, timedelta



def test_add_task(user):
    """Dodawanie taska"""
    user.add_task("Zrobić zakupy", "Kupić mleko i chleb")

    task = user.find_task("Zrobić zakupy")
    assert task is not None
    assert task.title == "Zrobić zakupy"
    assert task.description == "Kupić mleko i chleb"
    assert not task.is_done()

def test_complete_task(user):
    """Zaznaczanie taska jako zrobionego"""
    #user = User("Magda")
    user.add_task("Ćwiczenia", "15 minut jogi")
    user.complete_task("Ćwiczenia")
    task = user.find_task("Ćwiczenia")
    assert task.is_done()

def test_remove_task(user):
    """Usuwanie taska"""
    #user = User("Magda")
    user.add_task("Zadanie testowe", "Test")

    assert user.remove_task("Zadanie testowe") is True
    assert user.find_task("Zadanie testowe") is None


def test_show_all_tasks(user_with_tasks, capsys):
    """Wyświetlanie wszystkich tasków"""
    user_with_tasks.show_all_tasks()
    captured = capsys.readouterr()

    assert "Zadanie4" in captured.out
    assert "Opis zadania 4" in captured.out
    assert "Zadanie3" in captured.out
    assert "Opis zadania 3" in captured.out

    # Sprawdzenie, że data jest w formacie (YYYY-MM-DD HH:MM)
    pattern4 = (
        r"\[✗\] Zadanie4 - Opis zadania 4 "
        r"\(Utworzone: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    pattern3 = (
        r"\[✗\] Zadanie3 - Opis zadania 3 "
        r"\(Utworzone: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )

    assert re.search(pattern4, captured.out)
    assert re.search(pattern3, captured.out)

    assert user_with_tasks.count_tasks() == 2


def test_show_completed_tasks(user_with_pending_and_completed_tasks, capsys):
    """Wuświetlanie tasków zrobionych"""
    user = user_with_pending_and_completed_tasks
    user.show_completed_tasks()
    captured = capsys.readouterr()

    # Sprawdź, że w output jest zadanie A z opisem i datą
    pattern = (
        r"\[✓\] A - a "
        r"\(Utworzone: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    assert re.search(pattern, captured.out)

    # Zadanie B nie powinno być w completed, więc nie powinno się pojawić w output
    assert "- B" not in captured.out
    assert "b" not in captured.out

    assert user.count_completed_tasks() == 1


def test_show_pending_tasks(user_with_pending_and_completed_tasks, capsys):
    """Wyświtlanie tasków czekających na zrobienie"""
    user = user_with_pending_and_completed_tasks
    user.show_pending_tasks()
    captured = capsys.readouterr()

    # Zadanie A nie powinno być w pending
    assert "[✓] A - a" not in captured.out

    # Sprawdź, że w output jest zadanie B z opisem i datą
    pattern = (
        r"\[✗\] B - b "
        r"\(Utworzone: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\) "
        r"\(Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)"
    )
    assert re.search(pattern, captured.out)

    assert user.count_pending_tasks() == 1


def test_show_completed_tasks_empty(user,capsys):
    """Żaden task nie był wykonany"""
    user.show_completed_tasks()
    captured = capsys.readouterr()
    assert "Brak wykonanych zadań." in captured.out

def test_show_pending_tasks_empty(user,capsys):
    """Żaden task nie czeka na wykonanie"""
    user.show_pending_tasks()
    captured = capsys.readouterr()
    assert "Brak zadań do wykonania." in captured.out

def test_tasks_with_same_description(user):
    """Taski z takim samym opisem"""
    user.add_task("Z1", "opis")
    user.add_task("Z2", "opis")
    user.complete_task("Z1")
    assert user.count_completed_tasks() == 1
    assert user.count_pending_tasks() == 1

def test_count_completed(user_with_1_completed_and_2_pending):
    """Liczenie ile tasków jest wykonanych"""
    assert user_with_1_completed_and_2_pending.count_completed_tasks() == 1

def test_task_has_date():
    """Sprawdzanie czy data utworzenia taska jest dodana"""
    task = Task("Zadanie", "Opis")
    assert task.date_created is not None
    assert isinstance(task.date_created, datetime)

def test_task_with_deadline(user):
    """Sprawdzanie czy task ma dodany deadline"""
    deadline = datetime.now() + timedelta(days=3)
    user.add_task("Test z deadline", "Opis", deadline=deadline)
    task = user.find_task("Test z deadline")
    assert task is not None
    assert task.deadline is not None
    assert abs((task.deadline - deadline).total_seconds()) < 1  # prawie równe

def test_task_list_debug():
    """Debugowanie listy tasków"""
    todo = ToDoList()
    todo.add_task(Task("A", "Opis 1", priority=Priority.LOW))
    todo.add_task(Task("B", "Opis 2", completed=True, priority=Priority.HIGH))

    assert len(todo.tasks) == 2

def test_task_priority_set():
    """Sprawdzanie czy task ma ustawiony priorytet"""
    # Tworzymy przykładowe zadanie
    task = Task("Test", "Opis testowy", priority=Priority.HIGH)

    # Sprawdzamy, czy priorytet został ustawiony poprawnie
    assert task.priority == Priority.HIGH
    assert task.priority.name == "HIGH"

@pytest.mark.parametrize("priority", [Priority.LOW, Priority.MEDIUM, Priority.HIGH])
def test_priority_saved_and_loaded_all_levels(tmp_path, priority):
    """Sprawdzanie zadań z priorytetami"""
    # Tworzymy listę z jednym zadaniem i danym priorytetem
    todo = ToDoList()
    todo.add_task(Task("Test", "Opis", priority=priority))


    file_path = tmp_path / "tasks.json"     # Ścieżka do pliku tymczasowego
    todo.save_to_file(str(file_path))     # Zapisujemy do pliku
    new_todo = ToDoList()     # Wczytujemy z nowej instancji
    new_todo.load_from_file(str(file_path))
    loaded_task = new_todo.find_task("Test")     # Pobieramy zadanie po tytule

    assert loaded_task.priority == priority, (     # Sprawdzamy czy priorytet się zgadza
        f"Priorytet wczytanego zadania ({loaded_task.priority}) "
        f"różni się od zapisanego ({priority})"
    )

def test_priority_saved_and_loaded_multiple_tasks(tmp_path, sample_tasks):
    """Sprawdzanie tasków"""
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