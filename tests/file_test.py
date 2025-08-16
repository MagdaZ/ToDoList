import pytest
import os
from todo.user import User
from todo.todolist import ToDoList
from todo.task import Task, Priority


def test_save_and_load_from_file(tmp_path):
    # Tworzymy przykładową listę
    todo = ToDoList()
    todo.add_task(Task("A", "Pierwsze zadanie",priority=Priority.HIGH))
    todo.add_task(Task("B", "Drugie zadanie", completed =True, priority=Priority.LOW))


    file_path = "../tasks.json"     # Ścieżka do tymczasowego pliku
    todo.save_to_file(str(file_path))     # Zapis do pliku
    new_todo = ToDoList()     # Odczyt do nowej instancji
    new_todo.load_from_file(str(file_path))

    # Sprawdzamy poprawność danych
    assert len(new_todo.tasks) == 2
    assert new_todo.find_task("A").description == "Pierwsze zadanie"
    assert new_todo.find_task("B").completed is True