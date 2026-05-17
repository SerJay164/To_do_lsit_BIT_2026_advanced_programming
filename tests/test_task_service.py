import pytest
from sqlmodel import SQLModel, create_engine

import task_services
from database import Task
from task_services import TaskService


@pytest.fixture()
def test_engine(monkeypatch, tmp_path):
    db_file = tmp_path / "test_tasks.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False)

    SQLModel.metadata.create_all(engine)

    monkeypatch.setattr(task_services, "engine", engine)

    yield engine

    SQLModel.metadata.drop_all(engine)


# ------------------------------------------------------------
# 6 UNIT TESTS
# ------------------------------------------------------------

def test_unit_validate_title_removes_spaces():
    result = TaskService.validate_title("  Study Python  ")

    assert result == "Study Python"


def test_unit_validate_title_rejects_empty_title():
    with pytest.raises(ValueError):
        TaskService.validate_title("   ")


def test_unit_parse_due_date_accepts_valid_date():
    result = TaskService.parse_due_date("24-05-2026")

    assert str(result) == "2026-05-24"


def test_unit_parse_due_date_rejects_invalid_format():
    with pytest.raises(ValueError):
        TaskService.parse_due_date("2026-05-24")


def test_unit_validate_priority_accepts_urgent():
    result = TaskService.validate_priority("URGENT")

    assert result == "urgent"


def test_unit_validate_status_rejects_invalid_status():
    with pytest.raises(ValueError):
        TaskService.validate_status("in progress")


# ------------------------------------------------------------
# 3 DATABASE TESTS
# ------------------------------------------------------------

def test_db_add_task_persists_task(test_engine):
    TaskService.add_task("Write report", "24-05-2026", "high")

    tasks = TaskService.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Write report"
    assert str(tasks[0].due_date) == "2026-05-24"
    assert tasks[0].priority == "high"
    assert tasks[0].status == "pending"


def test_db_edit_task_updates_existing_task(test_engine):
    TaskService.add_task("Old title", "24-05-2026", "low")
    task = TaskService.list_tasks()[0]

    TaskService.edit_task(
        task.id,
        "New title",
        "25-05-2026",
        "urgent",
        "done",
    )

    updated_task = TaskService.find_task_by_id(task.id)

    assert updated_task.title == "New title"
    assert str(updated_task.due_date) == "2026-05-25"
    assert updated_task.priority == "urgent"
    assert updated_task.status == "done"


def test_db_delete_task_removes_task(test_engine):
    TaskService.add_task("Delete me", "24-05-2026", "medium")
    task = TaskService.list_tasks()[0]

    TaskService.delete_task(task.id)

    assert TaskService.list_tasks() == []