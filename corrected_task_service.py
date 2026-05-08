from datetime import datetime, date
from typing import Any


Task = dict[str, Any]


class TaskService:

    @staticmethod
    def validate_title(title: str) -> str:
        title = title.strip()

        if title == "":
            raise ValueError("Title cannot be empty")

        if "|" in title:
            raise ValueError("Title cannot contain '|'")

        return title

    @staticmethod
    def parse_due_date(date_str: str) -> date | None:
        date_str = date_str.strip()

        if date_str == "":
            return None

        try:
            return datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY")

    @staticmethod
    def validate_priority(priority: str) -> str:
        priority = priority.strip().lower()

        allowed = {"low", "medium", "high", "urgent"}

        if priority not in allowed:
            raise ValueError("Priority must be: low, medium, high, or urgent")

        return priority

    @staticmethod
    def validate_status(status: str) -> str:
        status = status.strip().lower()

        allowed = {"pending", "done"}

        if status not in allowed:
            raise ValueError("Status must be: pending or done")

        return status

    @staticmethod
    def get_next_id(task_list: list[Task]) -> int:
        if len(task_list) == 0:
            return 1

        return max(task["id"] for task in task_list) + 1

    @staticmethod
    def add_task(task_list: list[Task], title: str, date_str: str, priority: str) -> None:
        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)

        task = {
            "id": TaskService.get_next_id(task_list),
            "title": title,
            "due_date": due_date,
            "priority": priority,
            "status": "pending"
        }

        task_list.append(task)

    @staticmethod
    def list_tasks(task_list: list[Task]) -> list[Task]:
        return task_list.copy()

    @staticmethod
    def sort_task_by_due_date(task_list: list[Task]) -> list[Task]:
        return sorted(
            task_list,
            key=lambda task: task["due_date"] if task["due_date"] is not None else date.max
        )

    @staticmethod
    def sort_task_by_priority(task_list: list[Task]) -> list[Task]:
        priority_order = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "urgent": 4
        }

        return sorted(
            task_list,
            key=lambda task: priority_order.get(task["priority"], 0),
            reverse=True
        )

    @staticmethod
    def sort_task_by_priority_and_due_date(task_list: list[Task]) -> list[Task]:
        priority_order = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "urgent": 4
        }

        return sorted(
            task_list,
            key=lambda task: (
                -priority_order.get(task["priority"], 0),
                task["due_date"] if task["due_date"] is not None else date.max
            )
        )

    @staticmethod
    def find_task_by_id(task_list: list[Task], task_id: int) -> Task:
        for task in task_list:
            if task["id"] == task_id:
                return task

        raise ValueError("Task not found")

    @staticmethod
    def delete_task(task_list: list[Task], task_id: int) -> None:
        task = TaskService.find_task_by_id(task_list, task_id)
        task_list.remove(task)

    @staticmethod
    def edit_task(
        task_list: list[Task],
        task_id: int,
        title: str,
        date_str: str,
        priority: str
    ) -> None:
        task = TaskService.find_task_by_id(task_list, task_id)

        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)

        task["title"] = title
        task["due_date"] = due_date
        task["priority"] = priority

    @staticmethod
    def mark_task_done(task_list: list[Task], task_id: int) -> None:
        task = TaskService.find_task_by_id(task_list, task_id)
        task["status"] = "done"

    @staticmethod
    def mark_task_pending(task_list: list[Task], task_id: int) -> None:
        task = TaskService.find_task_by_id(task_list, task_id)
        task["status"] = "pending"

    @staticmethod
    def filter_pending_task(task_list: list[Task]) -> list[Task]:
        return [task for task in task_list if task["status"] == "pending"]

    @staticmethod
    def filter_done_task(task_list: list[Task]) -> list[Task]:
        return [task for task in task_list if task["status"] == "done"]