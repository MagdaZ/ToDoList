
import pytest
from todo.user import User
from todo.task import Task, Priority
from datetime import datetime, timedelta
from todo.todolist import ToDoList
from py.xml import html

@pytest.fixture
def user():
    return User("Magda")

@pytest.fixture
def user_with_tasks():
    user = User("Magda")
    from datetime import datetime, timedelta
    user.add_task("Task1", "Task1 description", deadline=datetime.now() + timedelta(days=1))
    user.add_task("Task2", "Task2 description", deadline=datetime.now() + timedelta(days=2))
    return user

@pytest.fixture
def user_with_pending_and_completed_tasks():
    user = User("testuser")
    now = datetime.now()
    task1 = Task("A", "a", completed=True, deadline=now + timedelta(days=1))
    task2 = Task("B", "b", completed=False, deadline=now + timedelta(days=2))
    user.todo_list.tasks = [task1, task2]
    return user

@pytest.fixture
def user_with_1_completed_and_2_pending():
    user = User("Magda")
    user.add_task("A", "a")
    user.add_task("B", "b")
    user.add_task("C", "c")
    user.complete_task("A")
    return user

@pytest.fixture
def sample_tasks():
    now = datetime.now()
    return [
        Task("Task 1", "Description 1", deadline=now + timedelta(days=1), priority=Priority.LOW),
        Task("Task 2", "Description 2", deadline=now + timedelta(days=2), priority=Priority.MEDIUM),
        Task("Task 3", "Description 3", deadline=now + timedelta(days=3), priority=Priority.HIGH)
    ]

@pytest.fixture
def todo_with_sample_tasks(sample_tasks):
    todo = ToDoList()
    for task in sample_tasks:
        todo.add_task(task)
    return todo

# New column with description in the HTML report
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Description"))

def pytest_html_results_table_row(report, cells):
    desc = getattr(report, "description", "")
    cells.insert(1, html.td(desc))

#  hookwrapper
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    doc = getattr(item.function, "__doc__", "")
    report.description = doc.strip() if doc else ""