import os
from datetime import datetime
from todo.user import User
from todo.task import Priority

def main():


    user_name = input("Enter your name: ").strip()
    user = User(user_name)

    filename = user.get_filename()
    if os.path.exists(filename):
        user.load_tasks_from_file()
        print(f"Tasks loaded from file {filename}")
    else:
        print("No saved tasks, starting over.")

    while True:
        print("\nMenu:")
        print("1. Add task")
        print("2. Show all tasks")
        print("3. Show completed tasks")
        print("4. Show tasks to do")
        print("5. Mark task as a completed")
        print("6. Remove task")
        print("7. Save and exit")
        print("8. Sorting")

        choice = input("Choose sorting criteria: ").strip()

        if choice == "1":
            title = input("Task title: ")
            description = input("Task description: ")
            deadline_str = input("Enter deadline deadline (format RRRR-MM-DD HH:MM) or keep empty: ")
            if deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Incorrect date format. The task will be created without a deadline.")
                    deadline = None
            else:
                deadline = None
            print("Choose priority: 1.Low  2.Medium  3.High")
            prio_choice = input("Your choice: ").strip()
            priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
            priority = priority_map.get(prio_choice, Priority.MEDIUM)
            user.add_task(title, description, deadline=deadline, priority=priority)

            print("\nTask added.")
        elif choice == "2":
            print("\nYour tasks: ")
            user.show_all_tasks()
        elif choice == "3":
            print("\nYour completed tasks: ")
            user.show_completed_tasks()
        elif choice == "4":
            print("\nYour tasks to do: ")
            user.show_pending_tasks()
        elif choice == "5":
            title = input("Enter the title of the task to mark as completed: ")
            if user.complete_task(title):
                print("Task marked as completed.")
            else:
                print("No task with this title found.")
        elif choice == "6":
            title = input("Enter the task title to remove: ")
            if user.remove_task(title):
                print("Task removed.")
            else:
                print("No task with this title found.")
        elif choice == "7":
            user.save_tasks_to_file()
            print("Task saved, Bye")
            break
        elif choice == "8":
            print("Sorting criteria: ")
            print("1. Title")
            print("2. Creation date")
            print("3. Deadline")
            print("4. Priority")
            sort_choice = input("Choose: ").strip()
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
                        f"[{status}] {task.title} - {task.description} (Created: {task.date_created.strftime('%Y-%m-%d %H:%M')}){deadline_str} [Priority: {task.priority.name}]")
            else:
                print("Invalid choice.")
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
