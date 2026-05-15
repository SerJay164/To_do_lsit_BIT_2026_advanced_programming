from datetime import datetime, date
from sqlmodel import Session, select, col

from database import engine, Task


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
    def add_task(title: str, date_str: str, priority: str) -> None:
        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)

        due_date_db = due_date.strftime(
            "%Y-%m-%d") if due_date is not None else None

        task = Task(title=title, due_date=due_date_db,
                    status="pending", priority=priority)

        with Session(engine) as session:
            session.add(task)
            session.commit()

    @staticmethod
    def list_tasks() -> list[Task]:
        with Session(engine) as session:
            return session.exec(select(Task)).all()

    @staticmethod
    def sort_task_by_due_date() -> list[Task]:
        with Session(engine) as session:
            statement = select(Task).order_by(
                col(Task.due_date).is_(None), Task.due_date)
            return session.exec(statement).all()

    @staticmethod
    def sort_task_by_priority() -> list[Task]:
        priority_order = {"urgent": 1, "high": 2, "medium": 3, "low": 4}

        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 5))

    @staticmethod
    def sort_task_by_priority_and_due_date() -> list[Task]:
        priority_order = {"urgent": 1, "high": 2, "medium": 3, "low": 4}

        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            return sorted(
                tasks,
                key=lambda t: (
                    priority_order.get(t.priority, 5),
                    (t.due_date is None, t.due_date)
                )
            )

    @staticmethod
    def find_task_by_id(task_id: int) -> Task:
        with Session(engine) as session:
            task = session.get(Task, task_id)

            if task is None:
                raise ValueError(f"Task {task_id} not found")

            return task

    @staticmethod
    def delete_task(task_id: int) -> None:
        with Session(engine) as session:
            task = session.get(Task, task_id)

            if task is None:
                raise ValueError(f"Task {task_id} not found")

            session.delete(task)
            session.commit()

    @staticmethod
    def edit_task(task_id: int, title: str, date_str: str, priority: str, status: str) -> None:
        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)
        status = TaskService.validate_status(status)

        due_date_db = due_date.strftime(
            "%Y-%m-%d") if due_date is not None else None

        with Session(engine) as session:
            task = session.get(Task, task_id)

            if task is None:
                raise ValueError(f"Task {task_id} not found")

            task.title = title
            task.due_date = due_date_db
            task.priority = priority
            task.status = status

            session.add(task)
            session.commit()

    @staticmethod
    def update_task_status(task_id: int, status: str) -> None:
        status = TaskService.validate_status(status)

        with Session(engine) as session:
            task = session.get(Task, task_id)

            if task is None:
                raise ValueError(f"Task {task_id} not found")

            task.status = status

            session.add(task)
            session.commit()

    @staticmethod
    def filter_task_by_status(status: str) -> list[Task]:
        status = TaskService.validate_status(status)

        with Session(engine) as session:
            statement = select(Task).where(Task.status == status)
            return session.exec(statement).all()

    @staticmethod
    def filter_done_task() -> list[Task]:
        with Session(engine) as session:
            statement = select(Task).where(Task.status == "done")
            return session.exec(statement).all()
