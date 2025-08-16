
import pytest
from todo.user import User
from todo.task import Task, Priority
from datetime import datetime, timedelta
from todo.todolist import ToDoList

@pytest.fixture
def user():
    return User("Magda")

@pytest.fixture
def user_with_tasks():
    user = User("Magda")
    from datetime import datetime, timedelta
    user.add_task("Zadanie4", "Opis zadania 4", deadline=datetime.now() + timedelta(days=1))
    user.add_task("Zadanie3", "Opis zadania 3", deadline=datetime.now() + timedelta(days=2))
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
        Task("Zadanie 1", "Opis 1", deadline=now + timedelta(days=1), priority=Priority.LOW),
        Task("Zadanie 2", "Opis 2", deadline=now + timedelta(days=2), priority=Priority.MEDIUM),
        Task("Zadanie 3", "Opis 3", deadline=now + timedelta(days=3), priority=Priority.HIGH)
    ]

@pytest.fixture
def todo_with_sample_tasks(sample_tasks):
    todo = ToDoList()
    for task in sample_tasks:
        todo.add_task(task)
    return todo

# Dodajemy kolumnę Description w raporcie HTML
def pytest_html_results_table_header(cells): #Funkcja modyfikuje nagłówek tabeli wyników HTML, dodając nową kolumnę "Description" jako drugą kolumnę (insert(1, ...)).
    cells.insert(1, "Description") #cells to lista nagłówków tabeli (np. "Test", "Outcome", itp.).

def pytest_html_results_table_row(report, cells): #report to obiekt TestReport, który opisuje wynik pojedynczego testu.
    desc = getattr(report, "description", "") # pobiera pole description, jeśli istnieje, inaczej zwraca pusty string
    cells.insert(1, desc) #wstawia opis testu do drugiej kolumny wiersza

# Poprawny hookwrapper dla pytest_runtest_makereport w pytest 8+
@pytest.hookimpl(hookwrapper=True) #Dekorator hookwrapper=True mówi pytest: „to generator, najpierw wykonaj standardowy hook, potem mogę dodać własną logikę”.
def pytest_runtest_makereport(item, call):
    # yield uruchamia standardową logikę pytest
    outcome = yield #w tym miejscu pytest wykonuje normalną logikę testu (setup, call, teardown) i tworzy obiekt raportu.
    report = outcome.get_result()  # to jest obiekt TestReport

    # Dodajemy docstring testu do raportu
    doc = getattr(item.function, "__doc__", "")
    report.description = doc.strip() if doc else ""