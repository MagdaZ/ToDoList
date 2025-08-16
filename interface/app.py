import os
from datetime import datetime
from todo.user import User
from todo.task import Priority

def main():


    user_name = input("Podaj swoje imię: ").strip()
    user = User(user_name)

    filename = user.get_filename()
    if os.path.exists(filename):
        user.load_tasks_from_file()
        print(f"Wczytano zadania z pliku {filename}")
    else:
        print("Brak zapisanych zadań, zaczynamy od nowa.")

    while True:
        print("\nMenu:")
        print("1. Dodaj zadanie")
        print("2. Pokaż wszystkie zadania")
        print("3. Pokaż wykonane zadania")
        print("4. Pokaż do zrobienia zadania")
        print("5. Oznacz zadanie jako wykonane")
        print("6. Usuń zadanie")
        print("7. Zapisz i wyjdź")
        print("8. Sortuj")

        choice = input("Wybierz opcj sortowania: ").strip()

        if choice == "1":
            title = input("Tytuł zadania: ")
            description = input("Opis zadania: ")
            deadline_str = input("Podaj deadline (format RRRR-MM-DD HH:MM) lub zostaw puste: ")
            if deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Niepoprawny format daty. Zadanie zostanie utworzone bez deadline’u.")
                    deadline = None
            else:
                deadline = None
            print("Wybierz priorytet: 1.Low  2.Medium  3.High")
            prio_choice = input("Twój wybór: ").strip()
            priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
            priority = priority_map.get(prio_choice, Priority.MEDIUM)
            user.add_task(title, description, deadline=deadline, priority=priority)

            print("\nDodano zadanie.")
        elif choice == "2":
            print("\nTwoje zadania: ")
            user.show_all_tasks()
        elif choice == "3":
            print("\nTwoje zadania wykonane: ")
            user.show_completed_tasks()
        elif choice == "4":
            print("\nTwoje zadania do wykonania: ")
            user.show_pending_tasks()
        elif choice == "5":
            title = input("Podaj tytuł zadania do oznaczenia jako wykonane: ")
            if user.complete_task(title):
                print("Zadanie oznaczone jako wykonane.")
            else:
                print("Nie znaleziono zadania o takim tytule.")
        elif choice == "6":
            title = input("Podaj tytuł zadania do usunięcia: ")
            if user.remove_task(title):
                print("Zadanie usunięte.")
            else:
                print("Nie znaleziono zadania o takim tytule.")
        elif choice == "7":
            user.save_tasks_to_file()
            print("Zapisano zadania. Do widzenia!")
            break
        elif choice == "8":
            print("Sortuj według: ")
            print("1. Tytuł")
            print("2. Data utworzenia")
            print("3. Deadline")
            print("4. Priorytet")
            sort_choice = input("Wybierz: ").strip()
            sort_map = {
                "1":"title",
                "2":"created",
                "3":"deadline",
                "4":"priority"
            }
            if sort_choice in sort_map:
                sorted_tasks = user.todo_list.get_tasks_sorted(by=sort_map[sort_choice])
                for task in sorted_tasks:
                    status = "✓" if task.completed else "✗"
                    deadline_str = f" (Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')})" if task.deadline else ""
                    print(
                        f"[{status}] {task.title} - {task.description} (Utworzone: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str} [Priority: {task.priority.name}]")
            else:
                print("Nieprawidłowy wybór.")
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")


if __name__ == "__main__":
    main()
