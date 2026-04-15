from datetime import datetime


class TaskService:

    def validate_title(title: str) -> str:
        title = title.strip()
        
        if title == "":
            raise ValueError("Title cannot be empty")
        
        if "|" in title:
            raise ValueError("Title cannot contain '|' ")
        
        return title


    def parse_due_date(date_str: str) -> date | None:
        date_str = date_str.strip()

        if date == "":
            return None
                
        try:
            return datetime.strptime(date_str, "%d-%m-%Y") .date()

        
        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY")
        
        

        
