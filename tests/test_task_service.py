from datetime import date

import pytest

from task_service import TaskService


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
    tasks = []

    TaskService.add_task(tasks, "Study testing", "31-05-2026", "high")

    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Study testing"
    assert tasks[0]["due_date"] == date(2026, 5, 31)
    assert tasks[0]["priority"] == "high"
    assert tasks[0]["status"] == "pending"


def test_add_task_without_due_date_sets_due_date_to_none():
    tasks = []

    TaskService.add_task(tasks, "Study testing", "", "medium")

    assert len(tasks) == 1
    assert tasks[0]["due_date"] is None


def test_add_task_rejects_invalid_title():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.add_task(tasks, "", "31-05-2026", "high")

    assert len(tasks) == 0


def test_add_task_rejects_invalid_date():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.add_task(tasks, "Study", "2026-05-31", "high")

    assert len(tasks) == 0


def test_add_task_rejects_invalid_priority():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.add_task(tasks, "Study", "31-05-2026", "super-high")

    assert len(tasks) == 0


# ---------------------------
# List and find tests
# ---------------------------

def test_list_tasks_returns_task_list():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")
    TaskService.add_task(tasks, "Task B", "", "medium")

    result = TaskService.list_tasks(tasks)

    assert result == tasks
    assert len(result) == 2


def test_find_task_by_id_returns_correct_task():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")
    TaskService.add_task(tasks, "Task B", "", "medium")

    result = TaskService.find_task_by_id(tasks, 2)

    assert result["id"] == 2
    assert result["title"] == "Task B"


def test_find_task_by_id_raises_error_for_missing_id():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.find_task_by_id(tasks, 999)


# ---------------------------
# Edit and delete tests
# ---------------------------

def test_edit_task_updates_existing_task():
    tasks = []
    TaskService.add_task(tasks, "Old title", "01-05-2026", "low")

    TaskService.edit_task(tasks, 1, "New title", "31-05-2026", "urgent")

    assert tasks[0]["title"] == "New title"
    assert tasks[0]["due_date"] == date(2026, 5, 31)
    assert tasks[0]["priority"] == "urgent"
    assert tasks[0]["status"] == "pending"


def test_edit_task_rejects_invalid_title():
    tasks = []
    TaskService.add_task(tasks, "Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(tasks, 1, "", "31-05-2026", "high")

    assert tasks[0]["title"] == "Old title"


def test_edit_task_rejects_invalid_date():
    tasks = []
    TaskService.add_task(tasks, "Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(tasks, 1, "New title", "2026-05-31", "high")

    assert tasks[0]["title"] == "Old title"
    assert tasks[0]["due_date"] == date(2026, 5, 1)
    assert tasks[0]["priority"] == "low"


def test_edit_task_rejects_invalid_priority():
    tasks = []
    TaskService.add_task(tasks, "Old title", "01-05-2026", "low")

    with pytest.raises(ValueError):
        TaskService.edit_task(tasks, 1, "New title", "31-05-2026", "invalid")

    assert tasks[0]["title"] == "Old title"
    assert tasks[0]["priority"] == "low"


def test_delete_task_removes_existing_task():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")

    TaskService.delete_task(tasks, 1)

    assert len(tasks) == 0


def test_delete_task_raises_error_for_missing_task():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.delete_task(tasks, 1)


# ---------------------------
# Status tests
# ---------------------------

def test_mark_task_done_changes_status_to_done():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")

    TaskService.mark_task_done(tasks, 1)

    assert tasks[0]["status"] == "done"


def test_mark_task_pending_changes_status_to_pending():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")

    # Set status manually because mark_task_done currently has a known bug.
    tasks[0]["status"] = "done"

    TaskService.mark_task_pending(tasks, 1)

    assert tasks[0]["status"] == "pending"


def test_mark_task_done_raises_error_for_missing_task():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.mark_task_done(tasks, 1)


def test_mark_task_pending_raises_error_for_missing_task():
    tasks = []

    with pytest.raises(ValueError):
        TaskService.mark_task_pending(tasks, 1)


# ---------------------------
# Filter tests
# ---------------------------

def test_filter_pending_task_returns_only_pending_tasks():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")
    TaskService.add_task(tasks, "Task B", "", "medium")

    # Set status manually because mark_task_done currently has a known bug.
    tasks[1]["status"] = "done"

    result = TaskService.filter_pending_task(tasks)

    assert len(result) == 1
    assert result[0]["title"] == "Task A"
    assert result[0]["status"] == "pending"


def test_filter_done_task_returns_only_done_tasks():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")
    TaskService.add_task(tasks, "Task B", "", "medium")

    # Set status manually because mark_task_done currently has a known bug.
    tasks[1]["status"] = "done"

    result = TaskService.filter_done_task(tasks)

    assert len(result) == 1
    assert result[0]["title"] == "Task B"
    assert result[0]["status"] == "done"


def test_filter_pending_task_returns_empty_list_if_no_pending_tasks():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")
    tasks[0]["status"] = "done"

    result = TaskService.filter_pending_task(tasks)

    assert result == []


def test_filter_done_task_returns_empty_list_if_no_done_tasks():
    tasks = []
    TaskService.add_task(tasks, "Task A", "", "low")

    result = TaskService.filter_done_task(tasks)

    assert result == []


# ---------------------------
# Sorting tests
# ---------------------------

def test_sort_task_by_due_date_sorts_earliest_date_first_and_none_last():
    tasks = []
    TaskService.add_task(tasks, "No date", "", "low")
    TaskService.add_task(tasks, "Later", "20-05-2026", "low")
    TaskService.add_task(tasks, "Earlier", "10-05-2026", "low")

    result = TaskService.sort_task_by_due_date(tasks)

    assert result[0]["title"] == "Earlier"
    assert result[1]["title"] == "Later"
    assert result[2]["title"] == "No date"


def test_sort_task_by_priority_sorts_urgent_first():
    tasks = []
    TaskService.add_task(tasks, "Low task", "", "low")
    TaskService.add_task(tasks, "Urgent task", "", "urgent")
    TaskService.add_task(tasks, "Medium task", "", "medium")
    TaskService.add_task(tasks, "High task", "", "high")

    result = TaskService.sort_task_by_priority(tasks)

    assert result[0]["priority"] == "urgent"
    assert result[1]["priority"] == "high"
    assert result[2]["priority"] == "medium"
    assert result[3]["priority"] == "low"


def test_sort_task_by_priority_and_due_date_sorts_priority_first_then_due_date():
    tasks = []
    TaskService.add_task(tasks, "High later", "20-05-2026", "high")
    TaskService.add_task(tasks, "Urgent later", "30-05-2026", "urgent")
    TaskService.add_task(tasks, "Urgent earlier", "10-05-2026", "urgent")
    TaskService.add_task(tasks, "Low earlier", "01-05-2026", "low")

    result = TaskService.sort_task_by_priority_and_due_date(tasks)

    assert result[0]["title"] == "Urgent earlier"
    assert result[1]["title"] == "Urgent later"
    assert result[2]["title"] == "High later"
    assert result[3]["title"] == "Low earlier"


# ---------------------------
# Known design issue test
# ---------------------------

def test_add_task_should_not_create_duplicate_ids_after_delete():
    tasks = []
    TaskService.add_task(tasks, "Task 1", "", "low")
    TaskService.add_task(tasks, "Task 2", "", "low")
    TaskService.add_task(tasks, "Task 3", "", "low")

    # Delete task with ID 2 manually to avoid depending on the current delete_task bug.
    task_to_delete = TaskService.find_task_by_id(tasks, 2)
    tasks.remove(task_to_delete)

    TaskService.add_task(tasks, "Task 4", "", "low")

    ids = [task["id"] for task in tasks]

    assert len(ids) == len(set(ids))