from datetime import datetime, date
from tkinter import END
from typing import Any

from database import create_connection


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
    def add_task(title: str, date_str: str, priority: str) -> None:
        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)

        due_date_db = due_date.strftime("%Y-%m-%d") if due_date is not None else None

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tasks (title, due_date, status, priority)
        VALUES (?, ?, ?, ?)
        """, (title, due_date_db, "pending", priority))

        conn.commit()
        conn.close()
    

    @staticmethod
    def list_tasks():

        conn = create_connection()
        cursor= conn.cursor()

        cursor.execute("SELECT * FROM tasks")

        tasks = cursor.fetchall()

        conn.close()

        return tasks


    @staticmethod
    def sort_task_by_due_date():

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks ORDER BY due_date is NULL, due_date")

        tasks = cursor.fetchall()

        conn.close()
        
        return tasks
    

    @staticmethod
    def sort_task_by_priority():

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tasks 
                       ORDER BY  
                            CASE priority  
                               WHEN 'urgent' THEN 1 
                               WHEN 'high' THEN 2  
                               WHEN 'medium' THEN 3  
                               WHEN 'low' THEN 4
                                ELSE 5
                            END
                        """)        
        
        tasks = cursor.fetchall()

        conn.close()

        return tasks
        

    @staticmethod
    def sort_task_by_priority_and_due_date():

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tasks
                       ORDER BY
                            CASE priority  
                               WHEN 'urgent' THEN 1 
                               WHEN 'high' THEN 2  
                               WHEN 'medium' THEN 3  
                               WHEN 'low' THEN 4
                                ELSE 5
                            END,
                            due_date is NULL, due_date
                        """)
        
        tasks = cursor.fetchall()
        
        conn.close()

        return tasks
    

    @staticmethod
    def find_task_by_id(task_id: int):

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tasks 
                       WHERE id = ?
                       """, (task_id,))

        task = cursor.fetchone()

        conn.close()

        if task is None:
            raise ValueError(f"Task {task_id} not found")
        
        return task


    @staticmethod
    def delete_task(task_id: int):
        
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       DELETE FROM tasks
                       WHERE id = ?
                       """, (task_id,))
        
        if cursor.rowcount == 0:
            raise ValueError(f"Task {task_id} not found")
        
        conn.commit()
        
        conn.close()

        
    @staticmethod
    def edit_task(task_id: int, title: str, date_str: str, priority: str, status: str):

        title = TaskService.validate_title(title)
        due_date = TaskService.parse_due_date(date_str)
        priority = TaskService.validate_priority(priority)
        status = TaskService.validate_status(status)

        due_date_db = due_date.strftime("%Y-%m-%d") if due_date is not None else None

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE tasks
                       SET title = ?, due_date = ?, priority = ?, status = ?
                       WHERE id = ?
                       """, (title, due_date_db, priority, status, task_id))
        
        if cursor.rowcount == 0:
            raise ValueError(f"Task {task_id} not found")

        conn.commit()
        conn.close()


    @staticmethod
    def update_task_status(task_id: int, status: str):

        status = TaskService.validate_status(status)

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE tasks
                       SET status = ?
                       WHERE id = ?
                       """, (status, task_id))

        if cursor.rowcount == 0:
            raise ValueError(f"Task {task_id} not found")
        
        conn.commit()
        
        conn.close()


    @staticmethod
    def filter_task_by_status(status: str):

        status = TaskService.validate_status(status)

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tasks 
                       WHERE status = ?
                       """, (status,))
        
        tasks = cursor.fetchall()

        conn.close()

        return tasks


    @staticmethod
    def filter_done_task():

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tasks 
                       WHERE status = 'done'
                       """)
        
        tasks = cursor.fetchall()

        conn.close()

        return tasks