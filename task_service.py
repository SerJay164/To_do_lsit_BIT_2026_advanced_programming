from datetime import datetime, date


class TaskService:

    @staticmethod
    def validate_title(title: str) -> str:
        title = title.strip()
        
        if title == "":
            raise ValueError("Title cannot be empty")
        
        if "|" in title:
            raise ValueError("Title cannot contain '|' ")
        
        return title


    @staticmethod
    def parse_due_date(date_str: str) -> date | None:
        date_str = date_str.strip()

        if date_str == "":
            return None
                
        try:
            return datetime.strptime(date_str, "%d-%m-%Y") .date()

        
        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY")

    @staticmethod
    def validate_priority(priority: str) -> str:
        priority = priority.strip().lower()

        allowed = {"low", "medium", "high", "urgent"}
        if priority not in allowed:
            raise ValueError("Priority must be: low, medium, high, or urgent")
        
        return priority
    

    def add_task(task_list: list, title: str, date_str: str, priority: str) -> None:

        title = TaskService.validate_title(title)

        due_date = TaskService.parse_due_date(date_str)

        priority = TaskService.validate_priority(priority)

        task = {
            "title": title,
            "due_date": due_date,
            "priority": priority,
            "status": "pending"
        }
        
        task_list.append(task)


    def list_tasks(task_list: list) -> list:
        return task_list
    
    
    def sort_task_by_due_date(task_list) -> list:
        return sorted(
            task_list,
            key=lambda task: task["due_date"] if task["due_date"] is not None else date.max
            )


    def sort_task_by_priority(task_list) -> list:
        priority_order = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
        
        return sorted(
            task_list,
            key=lambda task: priority_order.get(task["priority"], 0),
            reverse=True
        )