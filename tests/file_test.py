import pytest
import os
from todo.user import User
from todo.todolist import ToDoList
from todo.task import Task, Priority


def test_save_and_load_from_file(tmp_path):
    """Test save tasks and load tasks from file"""
    todo = ToDoList()
    todo.add_task(Task("A", "Description A",priority=Priority.HIGH))
    todo.add_task(Task("B", "description B", completed =True, priority=Priority.LOW))


    file_path = "../tasks.json"
    todo.save_to_file(str(file_path))
    new_todo = ToDoList()
    new_todo.load_from_file(str(file_path))

    assert len(new_todo.tasks) == 2
    assert new_todo.find_task("A").description == "Description A"
    assert new_todo.find_task("B").completed is True