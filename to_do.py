# ---------------------------
# imports
# ---------------------------

import os
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:
    tk = None
    filedialog = None


# ---------------------------
# shared maps
# ---------------------------    

PRIORITY_MAP = {
    "1": "low", "2": "medium", "3": "high",
    "low": "low", "medium": "medium", "high": "high",
}


STATUS_MAP = {
    "1": "pending", "2": "done",
    "pending": "pending", "done": "done",
}

# ---------------------------
# Helper functions for input
# ---------------------------

def get_non_empty_title():
    """Ask the user for a task title and make sure it is not empty."""
    while True:
        title = input("Enter task title: ").strip()
        if title == "":
            print("Title cannot be empty. Please try again.")
        elif "|" in title:
            print("Please do not use the '|' character in the title.")
        else:
            return title


def get_valid_date():
    """
    Ask the user for a due date in the format DD-MM-YYYY.
    The function checks if it is a real date, %d = 0-31, %m = 1-12, %Y = year in 4 digits.
    The user can leave it empty to skip the date.
    """
    while True:
        date_str = input("Enter due date (DD-MM-YYYY, or press Enter for no date): ").strip()

        if date_str == "":
            return "no date"
        
        try: 
            datetime.strptime(date_str, "%d-%m-%Y")

        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY, e.g. 31-12-2025.")
        else:
            return date_str    

       
def get_valid_priority():
    """
    Ask the user for a priority and only accept: 1=low, 2=medium, 3=high.
    """
    while True:
        choice = input("Priority (1=low, 2=medium, 3=high): ").strip().lower()
        if choice in PRIORITY_MAP:
            return PRIORITY_MAP[choice]
        else:
            print("Please enter 1, 2, 3 or low, medium, high.")


def get_valid_status():
    """
    Ask the user which status they want to view: pending or done.
    """
        
    while True:
        status = input("Show tasks with status (1=pending, 2=done): ").strip().lower()
        if status in STATUS_MAP:
            return STATUS_MAP[status]
        else:
            print("Please enter 1, 2, pending or done.")


def get_valid_task_index(tasks, action_text):
    """
    Ask the user for a task number (1..len(tasks)).
    Used when marking a task as complete or deleting a task.
    Returns the index in the list (0-based).
    """
    if len(tasks) == 0:
        print("There are no tasks.")
        return None

    while True:
        try:
            number_str = input("Enter the task number to " + action_text + ": ").strip()
            number = int(number_str)
            if 1 <= number <= len(tasks):
                return number - 1  # convert to 0-based index
            else:
                print("Please enter a number between 1 and", len(tasks))
        except ValueError:
            print("Please enter a valid integer.")


def choose_task_file():
    """
    Let the user either:
    1. Select an existing text file via file explorer
    2. Enter a new filename to create/use
    """
    while True:
        print("\n--- CHOOSE TASK FILE ---")
        print("1. Select existing file from explorer")
        print("2. Enter a new file name")
        choice = input("Choose an option (1-2): ").strip()

        if choice == "1":
            if tk is None or filedialog is None:
                print("File dialog is not available on this system.")
                continue
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the main Tk window

                print("Please choose a text file in the dialog window...")
                filename = filedialog.askopenfilename(
                    title="Select task file",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )

                root.destroy()

            except Exception as e:
                print("Could not open file dialog:", e)
                print("You can still type a filename manually (option 2).")
                continue
        
            if filename == "":
                print("No file selected. Please try again.")
                continue

            return filename
            
        elif choice == "2":
            filename = input("Enter a file name: ").strip()
            if filename == "":
                print("Filename cannot be empty.")
                continue

            # File will be automatically saved as .txt
            if not filename.lower().endswith(".txt"):
                filename += ".txt"

            if os.path.exists(filename):
                print(f"The file '{filename}' already exists.")
                use_existing = input("Use this file? (y/n): ").strip().lower()
                if use_existing == "y":
                    return filename
                else:
                    continue
            else:
                print(f"New file will be created: {filename}")
                return filename

        else:
            print("Invalid choice. Please enter 1 or 2.")
# ---------------------------
# File handling
# ---------------------------

def load_tasks_from_file(filename):
    """
    Load tasks from a text file.

    File format (one task per line):
    title|due_date|priority|status
    """
    tasks = []

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue  # skip empty lines

                parts = line.split("|")
                if len(parts) == 4:
                    title = parts[0]
                    due_date = parts[1].strip()
                    priority = parts[2].strip().lower()
                    status = parts[3].strip().lower()

                    if due_date == "" or due_date.lower() == "no date":
                        due_date = "no date"
                    else:
                        try:
                            datetime.strptime(due_date, "%d-%m-%Y")
                        except ValueError:
                            due_date = "no date"

                    if priority in PRIORITY_MAP:
                        priority = PRIORITY_MAP[priority]
                    else:
                        priority = "low"

                    if status in STATUS_MAP:
                        status = STATUS_MAP[status]
                    else:
                        status = "pending"

                    tasks.append([title, due_date, priority, status])
                else:
                    # If the line does not have exactly 4 parts, we ignore it
                    print("Warning: Ignoring invalid line in file:", line)
    except FileNotFoundError:
        # File does not exist yet -> start with empty list
        pass
    except Exception as e:
        print("Error while reading file:", e)

    return tasks


def save_tasks_to_file(tasks, filename):
    """
    Save all tasks to a text file.
    Each task becomes one line: title|due_date|priority|status
    """
    try:
        with open(filename, "w") as f:
            for task in tasks:
                if len(task) != 4:
                    continue
                title = task[0]
                due_date = task[1]
                priority = task[2]
                status = task[3]
                line = title + "|" + due_date + "|" + priority + "|" + status + "\n"
                f.write(line)
    except Exception as e:
        print("Error while saving tasks:", e)


# ---------------------------
# Task list helpers
# ---------------------------

def parse_date(date_str):
    """Convert a date string (DD-MM-YYYY) into a tuple for sorting."""
    if date_str == "no date":
        return (9999, 12, 31)  # to the end of sorting
    try:
        d = datetime.strptime(date_str, "%d-%m-%Y")
        return (d.year, d.month, d.day)
    except ValueError:
        return (9999, 12, 31)


def sort_tasks_by_due_date(tasks):
    """
    Sort the tasks list IN PLACE by due_date using a simple bubble sort
    Tasks with 'no date' are moved to the end.
    """
    n = len(tasks)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):

            date1 = tasks[j][1]
            date2 = tasks[j + 1][1]

            key1 = parse_date(date1)
            key2 = parse_date(date2)

            if key1 > key2:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]


def print_single_task(task, index):
    """
    Print one task in a nice format.
    """
    title = task[0]
    due_date = task[1]
    priority = task[2]
    status = task[3]

    if due_date == "no date":
        due_text = "no due date"
    else:
        due_text = due_date

    print(f"{index}. [{status}] ({priority}) {due_text} - {title}")


def view_all_tasks(tasks):
    """Display all tasks, sorted by due date."""
    if len(tasks) == 0:
        print("No tasks found.")
        return

    sort_tasks_by_due_date(tasks)

    print("\n--- ALL TASKS ---")
    for i, task in enumerate(tasks, start=1):
        print_single_task(task, i)


def view_tasks_by_status(tasks):
    """Display only tasks with a certain status (pending or done)."""
    if len(tasks) == 0:
        print("No tasks found.")
        return

    wanted_status = get_valid_status()

    print(f"\n--- TASKS WITH STATUS: {wanted_status} ---")
    count = 0
    for i, task in enumerate(tasks, start=1):
        if task[3] == wanted_status:
            count += 1
            print_single_task(task, i)

    if count == 0:
        print("No tasks with status:", wanted_status)


def add_task(tasks):
    """Create a new task and add it to the list."""
    print("\n--- ADD NEW TASK ---")
    title = get_non_empty_title()
    due_date = get_valid_date()
    priority = get_valid_priority()
    status = "pending"  

    tasks.append([title, due_date, priority, status])
    print("Task added successfully.")


def mark_task_complete(tasks, filename):
    """Mark a selected task as done."""
    if len(tasks) == 0:
        print("No tasks to mark as complete.")
        return

    print("\n--- MARK TASK AS COMPLETE ---")
    view_all_tasks(tasks)

    index = get_valid_task_index(tasks, "mark as complete")
    if index is None:
        return

    if tasks[index][3] == "done":
        print("This task is already marked as done.")
    else:
        tasks[index][3] = "done"
        print("Task marked as complete.")
        save_tasks_to_file(tasks, filename)  # save after change
        print("\nUpdated task list:")
        view_all_tasks(tasks)


def delete_task(tasks, filename):
    """Delete a selected task from the list."""
    if len(tasks) == 0:
        print("No tasks to delete.")
        return

    print("\n--- DELETE TASK ---")
    view_all_tasks(tasks)

    index = get_valid_task_index(tasks, "delete")
    if index is None:
        return

    print("You are about to delete this task:")
    print_single_task(tasks[index], index + 1)

    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == "y":
        tasks.pop(index)
        print("Task deleted.")
        save_tasks_to_file(tasks, filename)  # save after change
        print("\nUpdated task list:")
        view_all_tasks(tasks)
    else:
        print("Delete cancelled.")


def short_cut_menu(tasks, filename):
    """
    After showing tasks, give the user shortcuts:
    1. Mark a task as complete
    2. Delete a task
    3. Return to main menu
    """
    while True:
        if len(tasks) == 0:
            print("There are no tasks")
            return
        
        print("\nWhat do you want to do?")
        print("1. Mark a task as complete")
        print("2. Delete a task")
        print("3. Return to main menu")

        short_cut = input("Choose an option (1-3): ").strip()

        if short_cut == "1":
            index = get_valid_task_index(tasks, "mark as complete")
            if index is None:
                print("No tasks available.")
                continue  

            if tasks[index][3] == "done":
                print("This task is already marked as done.")
                continue  

            # If we get here, the task is NOT done → mark it complete
            tasks[index][3] = "done"
            print("Task marked as complete.")
            save_tasks_to_file(tasks, filename)  # save after change
            print("\nUpdated task list:")
            view_all_tasks(tasks)

            continue    

        elif short_cut == "2":
            index = get_valid_task_index(tasks, "delete")
            if index is None:
                print("No tasks available.")
                continue  

            print("You are about to delete this task:")
            print_single_task(tasks[index], index + 1)

            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                tasks.pop(index)
                print("Task deleted.")
                save_tasks_to_file(tasks, filename)  # save after change
                print("\nUpdated task list:")
                view_all_tasks(tasks)
            else:
                print("Delete cancelled.")

            continue  
        
        elif short_cut == "3":
            return  # Go back to the view / main
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


def edit_task(tasks):
    """Edit an existing task (title, due date, priority, status)."""
    if len(tasks) == 0:
        print("No tasks to edit.")
        return

    print("\n--- EDIT TASK ---")
    view_all_tasks(tasks)

    index = get_valid_task_index(tasks, "edit")
    if index is None:
        return

    task = tasks[index]
    print("\nCurrent values:")
    print_single_task(task, index + 1)
    print("Press Enter to keep the current value.\n")

    # --- Edit title ---
    while True:
        new_title = input(f"New title (current: {task[0]}), Enter = keep: ").strip()
        if new_title == "":
            break  # keep old title
        elif "|" in new_title:
            print("Please do not use the '|' character in the title.")
        else:
            task[0] = new_title
            break

    # --- Edit due date ---
    while True:
        current_due = "no due date" if task[1] == "no date" else task[1]
        new_date = input(
            f"New due date (DD-MM-YYYY, current: {current_due}, Enter = keep, 'none' = no date): "
        ).strip()

        if new_date == "":
            break  # keep old date
        if new_date.lower() == "none":
            task[1] = "no date"
            break

        try:
            datetime.strptime(new_date, "%d-%m-%Y")
            task[1] = new_date
            break
        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY, e.g. 31-12-2025.")

    # --- Edit priority ---
    
    while True:
        new_prio = input(
            f"New priority (1=low, 2=medium, 3=high, current: {task[2]}, Enter = keep): "
        ).strip().lower()

        if new_prio == "":
            break  # keep old
        if new_prio in PRIORITY_MAP:
            task[2] = PRIORITY_MAP[new_prio]
            break
        else:
            print("Please enter 1, 2, 3 or low/medium/high.")

    # --- Edit status ---
   
    while True:
        new_status = input(
            f"New status (1=pending, 2=done, current: {task[3]}, Enter = keep): "
        ).strip().lower()

        if new_status == "":
            break  # keep status
        if new_status in STATUS_MAP:
            task[3] = STATUS_MAP[new_status]
            break
        else:
            print("Please enter 1, 2, pending or done.")

    print("\nTask updated:")
    print_single_task(task, index + 1)

# ---------------------------
# Menu and main program
# ---------------------------

def show_menu():
    """Print the main menu."""
    print("\n--- TO-DO LIST MANAGER ---")
    print("1. Add new task")
    print("2. View all tasks (sorted by due date)")
    print("3. View tasks by status (pending/done)")
    print("4. Mark task as complete")
    print("5. Edit task")
    print("6. Delete task")
    print("7. Exit")


def main():
    #ask the user to choose or create a task file
    filename = choose_task_file()

    # Load existing tasks from file (if file exists)
    tasks = load_tasks_from_file(filename)

    print("Welcome to the To-Do List Manager!")

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_task(tasks)
            save_tasks_to_file(tasks, filename)  
        elif choice == "2":
            view_all_tasks(tasks)
            short_cut_menu(tasks, filename)  
        elif choice == "3":
            view_tasks_by_status(tasks)
            short_cut_menu(tasks, filename)  
        elif choice == "4":
            mark_task_complete(tasks, filename)
        elif choice == "5":
            edit_task(tasks)
            save_tasks_to_file(tasks, filename)
        elif choice == "6":
            delete_task(tasks, filename)
        elif choice == "7":
            print("Goodbye!")
            # Save once more before exiting (optional, but safe)
            save_tasks_to_file(tasks, filename)
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
