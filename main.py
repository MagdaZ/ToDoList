
from todo.user import User
from todo.task import Priority
import os
from datetime import datetime



if __name__ == "__main__":
    user_name = input("Enter your name: ").strip()
    user = User(user_name)
    #user = User("zosia")
    filename = user.get_filename()
    if os.path.exists(filename):
        user.load_tasks_from_file()
        user.show_completed_tasks()
        user.show_pending_tasks()
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    deadline_str = input("Enter deadline (format RRRR-MM-DD HH:MM) or keep empty: ")
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

    user.save_tasks_to_file()





