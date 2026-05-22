from pathlib import Path

import task_services
from sqlmodel import SQLModel, create_engine

import pytest

from calendar_export import export_tasks_to_ics
from task_services import TaskService


@pytest.fixture()
def test_engine(monkeypatch, tmp_path):
    db_file = tmp_path / "test_calendar.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False)

    SQLModel.metadata.create_all(engine)

    monkeypatch.setattr(task_services, "engine", engine)

    yield engine

    SQLModel.metadata.drop_all(engine)


# ------------------------------------------------------------
# 3 INTEGRATION TESTS
# ------------------------------------------------------------

def test_integration_export_creates_ics_file(test_engine, tmp_path):
    TaskService.add_task("Prepare presentation", "24-05-2026", "high")

    tasks = TaskService.list_tasks()
    filename = tmp_path / "tasks_export.ics"

    result = export_tasks_to_ics(tasks, filename)

    assert Path(result).exists()


def test_integration_export_contains_task_information(test_engine, tmp_path):
    TaskService.add_task("Prepare presentation", "24-05-2026", "high")

    tasks = TaskService.list_tasks()
    filename = tmp_path / "tasks_export.ics"

    export_tasks_to_ics(tasks, filename)

    content = filename.read_text(encoding="utf-8")

    assert "BEGIN:VCALENDAR" in content
    assert "BEGIN:VEVENT" in content
    assert "SUMMARY:Prepare presentation" in content
    assert "DTSTART;VALUE=DATE:20260524" in content
    assert "Priority: high" in content
    assert "Status: pending" in content
    assert "END:VEVENT" in content
    assert "END:VCALENDAR" in content


def test_integration_export_skips_task_without_due_date(test_engine, tmp_path):
    TaskService.add_task("Task without date", "", "medium")

    tasks = TaskService.list_tasks()
    filename = tmp_path / "tasks_export.ics"

    export_tasks_to_ics(tasks, filename)

    content = filename.read_text(encoding="utf-8")

    assert "Task without date" not in content
    assert "BEGIN:VEVENT" not in content
    assert "BEGIN:VCALENDAR" in content
    assert "END:VCALENDAR" in content