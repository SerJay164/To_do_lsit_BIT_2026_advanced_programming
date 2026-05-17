from datetime import date

import pytest

from task_services import TaskService

from sqlmodel import Session, delete
from database import engine, Task


@pytest.fixture(autouse=True)
def clean_database():
    with Session(engine) as session:
        session.exec(delete(Task))
        session.commit()


# ---------------------------
# Validation tests
# ---------------------------

def test_validate_title_accepts_valid_title():
    # Arrange
    title = "  Study Python  "

    # Act
    result = TaskService.validate_title(title)

    # Assert
    assert result == "Study Python"


def test_validate_title_rejects_empty_title():
    with pytest.raises(ValueError):
        TaskService.validate_title("   ")


def test_validate_title_rejects_pipe_character():
    with pytest.raises(ValueError):
        TaskService.validate_title("Task | invalid")


def test_parse_due_date_accepts_valid_date():
    result = TaskService.parse_due_date("31-05-2026")

    assert result == date(2026, 5, 31)


def test_parse_due_date_returns_none_for_empty_input():
    result = TaskService.parse_due_date("")

    assert result is None


def test_parse_due_date_rejects_wrong_format():
    with pytest.raises(ValueError):
        TaskService.parse_due_date("2026-05-31")


def test_validate_priority_accepts_valid_priority_and_normalizes_it():
    result = TaskService.validate_priority(" HIGH ")

    assert result == "high"


def test_validate_priority_accepts_urgent():
    result = TaskService.validate_priority("urgent")

    assert result == "urgent"


def test_validate_priority_rejects_invalid_priority():
    with pytest.raises(ValueError):
        TaskService.validate_priority("important")


# ---------------------------
# Task creation tests
# ---------------------------

def test_add_task_adds_valid_task():    

    TaskService.add_task("Task","", "low")
    tasks = TaskService.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Task"
    assert tasks[0].due_date is None
    assert tasks[0].priority == "low"
    assert tasks[0].status == "pending"

def test_add_task_without_due_date_sets_due_date_to_none():
    
    TaskService.add_task("Study testing", "", "medium")

    tasks = TaskService.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].due_date is None  


def test_add_task_rejects_invalid_title():
    
    with pytest.raises(ValueError):
        TaskService.add_task("", "31-05-2026", "high")

    assert len(TaskService.list_tasks()) == 0


def test_add_task_rejects_invalid_date():
    
    with pytest.raises(ValueError):
        TaskService.add_task("Study", "2026-05-31", "high")

    assert len(TaskService.list_tasks()) == 0


def test_add_task_rejects_invalid_priority():
    
    with pytest.raises(ValueError):
        TaskService.add_task("Study", "31-05-2026", "super-high")

    assert len(TaskService.list_tasks()) == 0


# ---------------------------
# List and find tests
# ---------------------------

def test_list_tasks_returns_task_list():
    TaskService.add_task("Task A", "", "low")
    TaskService.add_task("Task B", "", "medium")

    result = TaskService.list_tasks()

    assert result == TaskService.list_tasks()
    assert len(result) == 2


def test_find_task_by_id_returns_correct_task():
    TaskService.add_task("Task A", "", "low")
    TaskService.add_task("Task B", "", "medium")

    result = TaskService.find_task_by_id(2)

    assert result.id == 2
    assert result.title == "Task B"


def test_find_task_by_id_raises_error_for_missing_id():
    
    with pytest.raises(ValueError):
        TaskService.find_task_by_id(999)


# ---------------------------
# Edit and delete tests
# ---------------------------

def test_edit_task_updates_existing_task():
    TaskService.add_task("Old title", "01-05-2026", "low")

    TaskService.edit_task(
    1,
    "New title",
    "31-05-2026",
    "urgent",
    "pending"
)

    tasks = TaskService.list_tasks()[0]
    assert tasks.title == "New title"
    assert tasks.due_date == date(2026, 5, 31)
    assert tasks.priority == "urgent"
    assert tasks.status == "pending"


def test_edit_task_rejects_invalid_title():
    TaskService.add_task("Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(1, "", "31-05-2026", "high", "pending")

    task = TaskService.list_tasks()[0]

    assert task.title == "Old title"


def test_edit_task_rejects_invalid_date():
    TaskService.add_task("Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(
    1,
    "New title",
    "2026-05-31",
    "urgent",
    "pending"
)

    tasks = TaskService.list_tasks()[0]

    assert tasks.title == "Old title"
    assert tasks.due_date == date(2026, 5, 1)
    assert tasks.priority == "low"


def test_edit_task_rejects_invalid_priority():
    TaskService.add_task("Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(
    1,
    "New title",
    "31-05-2026",
    "invalid",
    "pending"
)

    tasks = TaskService.list_tasks()[0]

    assert tasks.title == "Old title"
    assert tasks.priority == "low"


def test_delete_task_removes_existing_task():
    TaskService.add_task("Task A", "", "low")

    TaskService.delete_task(1)

    assert len(TaskService.list_tasks()) == 0


def test_delete_task_raises_error_for_missing_task():
    
    with pytest.raises(ValueError):
        TaskService.delete_task(1)


# ---------------------------
# Status tests
# ---------------------------

def test_update_task_status_updates_status():
    TaskService.add_task("Task A", "", "low")

    TaskService.update_task_status(1, "done")

    tasks = TaskService.list_tasks()[0]

    assert tasks.status == "done"


def test_update_task_status_raises_error_for_missing_task():
    
    with pytest.raises(ValueError):
        TaskService.update_task_status(1, "done")


def test_update_task_status_raises_error_for_invalid_status():
    
    with pytest.raises(ValueError):
        TaskService.update_task_status(1, "invalid")
        TaskService.update_task_status(1, "pending")
        


# ---------------------------
# Filter tests
# ---------------------------

def test_filter_pending_task_returns_only_pending_tasks():
    TaskService.add_task("Task A", "", "low")
    TaskService.add_task("Task B", "", "medium")

    TaskService.update_task_status(2, "done")

    result = TaskService.filter_pending_task()

    assert len(result) == 1
    assert result[0].title == "Task A"
    assert result[0].status == "pending"


def test_filter_done_task_returns_only_done_tasks():
    TaskService.add_task("Task A", "", "low")
    TaskService.add_task("Task B", "", "medium")

    TaskService.update_task_status(2, "done")

    result = TaskService.filter_done_task()

    assert len(result) == 1
    assert result[0].title == "Task B"
    assert result[0].status == "done"

def test_filter_pending_task_returns_empty_list_if_no_pending_tasks():
    TaskService.add_task("Task A", "", "low")
    TaskService.update_task_status(1, "done")

    result = TaskService.filter_pending_task()

    assert result == []


def test_filter_done_task_returns_empty_list_if_no_done_tasks():
    TaskService.add_task("Task A", "", "low")
    TaskService.list_tasks()[0].status = "pending"
    result = TaskService.filter_done_task()

    assert result == []


# ---------------------------
# Sorting tests
# ---------------------------

def test_sort_task_by_due_date_sorts_earliest_date_first_and_none_last():
    TaskService.add_task("No date", "", "low")
    TaskService.add_task("Later", "20-05-2026", "low")
    TaskService.add_task("Earlier", "10-05-2026", "low")

    result = TaskService.sort_task_by_due_date()

    assert result[0].title == "Earlier"
    assert result[1].title == "Later"
    assert result[2].title == "No date"


def test_sort_task_by_priority_sorts_urgent_first():
    TaskService.add_task("Low task", "", "low")
    TaskService.add_task("Urgent task", "", "urgent")
    TaskService.add_task("Medium task", "", "medium")
    TaskService.add_task("High task", "", "high")

    result = TaskService.sort_task_by_priority()

    assert result[0].priority == "urgent"
    assert result[1].priority == "high"
    assert result[2].priority == "medium"
    assert result[3].priority == "low"


def test_sort_task_by_priority_and_due_date_sorts_priority_first_then_due_date():
    TaskService.add_task("High later", "20-05-2026", "high")
    TaskService.add_task("Urgent later", "30-05-2026", "urgent")
    TaskService.add_task("Urgent earlier", "10-05-2026", "urgent")
    TaskService.add_task("Low earlier", "01-05-2026", "low")

    result = TaskService.sort_task_by_priority_and_due_date()

    assert result[0].title == "Urgent earlier"
    assert result[1].title == "Urgent later"
    assert result[2].title == "High later"
    assert result[3].title == "Low earlier"

