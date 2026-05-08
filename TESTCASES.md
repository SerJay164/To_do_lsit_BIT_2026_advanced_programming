# Test Cases – To-Do List Project

## Scope

These test cases are based on the old CLI version (`to_do.py`) and the current refactored `TaskService`.

The old CLI project stores tasks as lists:

```python
[title, due_date, priority, status]
```

The current `TaskService` stores tasks as dictionaries:

```python
{
    "id": int,
    "title": str,
    "due_date": date | None,
    "priority": str,
    "status": str
}
```

The core behaviour stays the same:

- add task
- validate title
- validate date
- validate priority
- list tasks
- edit task
- delete task
- mark task as done
- mark task as pending
- filter tasks
- sort tasks

The automated tests will be implemented separately in:

```text
tests/test_task_service.py
```

---

## Test Case Overview

| Test Case ID | Title / Description | Preconditions | Test Steps | Test Data / Input | Expected Result | Actual Result | Status | Comments |
|---|---|---|---|---|---|---|---|---|
| TC_001 | Validate valid title | None | Call `TaskService.validate_title()` | `"  Study Python  "` | Returns `"Study Python"` | Not executed yet | Open | Happy path |
| TC_002 | Reject empty title | None | Call `TaskService.validate_title()` | `"   "` | Raises `ValueError` with message `"Title cannot be empty"` | Not executed yet | Open | Edge case |
| TC_003 | Reject title with pipe character | None | Call `TaskService.validate_title()` | `"Task | invalid"` | Raises `ValueError` | Not executed yet | Open | Important because the old file format used `|` as separator |
| TC_004 | Parse valid due date | None | Call `TaskService.parse_due_date()` | `"31-05-2026"` | Returns `date(2026, 5, 31)` | Not executed yet | Open | Happy path |
| TC_005 | Empty due date is allowed | None | Call `TaskService.parse_due_date()` | `""` | Returns `None` | Not executed yet | Open | Old project used `"no date"`, current service uses `None` |
| TC_006 | Reject wrong date format | None | Call `TaskService.parse_due_date()` | `"2026-05-31"` | Raises `ValueError` with message `"Invalid date format. Please use DD-MM-YYYY"` | Not executed yet | Open | Edge case |
| TC_007 | Validate priority with uppercase input | None | Call `TaskService.validate_priority()` | `" HIGH "` | Returns `"high"` | Not executed yet | Open | Checks stripping and lowercase conversion |
| TC_008 | Validate urgent priority | None | Call `TaskService.validate_priority()` | `"urgent"` | Returns `"urgent"` | Not executed yet | Open | Current version supports `urgent` |
| TC_009 | Reject invalid priority | None | Call `TaskService.validate_priority()` | `"important"` | Raises `ValueError` | Not executed yet | Open | Edge case |
| TC_010 | Add valid task | Empty task list exists | Call `TaskService.add_task()` | title=`"Study testing"`, date=`"31-05-2026"`, priority=`"high"` | One task is added with id `1`, title `"Study testing"`, due date `31-05-2026`, priority `"high"`, status `"pending"` | Not executed yet | Open | Core feature |
| TC_011 | Add task without due date | Empty task list exists | Call `TaskService.add_task()` | title=`"Study testing"`, date=`""`, priority=`"medium"` | Task is added with `due_date = None` and status `"pending"` | Not executed yet | Open | Current replacement for old `"no date"` behaviour |
| TC_012 | Reject task with invalid title | Empty task list exists | Call `TaskService.add_task()` | title=`""`, date=`"31-05-2026"`, priority=`"high"` | Raises `ValueError`; task list remains empty | Not executed yet | Open | Validation before adding |
| TC_013 | Reject task with invalid date | Empty task list exists | Call `TaskService.add_task()` | title=`"Study"`, date=`"2026-05-31"`, priority=`"high"` | Raises `ValueError`; task list remains empty | Not executed yet | Open | Validation before adding |
| TC_014 | Reject task with invalid priority | Empty task list exists | Call `TaskService.add_task()` | title=`"Study"`, date=`"31-05-2026"`, priority=`"super-high"` | Raises `ValueError`; task list remains empty | Not executed yet | Open | Validation before adding |
| TC_015 | List tasks | Task list contains two tasks | Call `TaskService.list_tasks()` | Task list with two tasks | Returns the task list | Not executed yet | Open | Basic list behaviour |
| TC_016 | Find existing task by ID | Task list contains two tasks | Call `TaskService.find_task_by_id(tasks, 2)` | `task_id = 2` | Returns the task with id `2` | Not executed yet | Open | Core lookup |
| TC_017 | Reject missing task ID | Empty task list exists | Call `TaskService.find_task_by_id(tasks, 999)` | `task_id = 999` | Raises `ValueError` with message `"Task not found"` | Not executed yet | Open | Edge case |
| TC_018 | Edit existing task | Task list contains one task | Call `TaskService.edit_task()` | task_id=`1`, title=`"New title"`, date=`"31-05-2026"`, priority=`"urgent"` | Existing task is updated with new title, due date and priority | Not executed yet | Open | Core feature |
| TC_019 | Reject edit with invalid title | Task list contains one task | Call `TaskService.edit_task()` | task_id=`1`, title=`""`, date=`"31-05-2026"`, priority=`"high"` | Raises `ValueError`; task should not be updated | Not executed yet | Open | Edge case |
| TC_020 | Delete existing task | Task list contains one task | Call `TaskService.delete_task(tasks, 1)` | `task_id = 1` | Task list becomes empty | Not executed yet | Open | Expected to fail with current code because `delete_task()` raises an error after removing |
| TC_021 | Delete missing task | Empty task list exists | Call `TaskService.delete_task(tasks, 1)` | `task_id = 1` | Raises `ValueError` with message `"Task not found"` | Not executed yet | Open | Edge case |
| TC_022 | Mark task as done | Task list contains one pending task | Call `TaskService.mark_task_done(tasks, 1)` | `task_id = 1` | Task status becomes `"done"` | Not executed yet | Open | Expected to fail with current code because it writes key `"pending"` instead of changing `"status"` |
| TC_023 | Mark task as pending | Task list contains one done task | Call `TaskService.mark_task_pending(tasks, 1)` | `task_id = 1` | Task status becomes `"pending"` | Not executed yet | Open | Core status change |
| TC_024 | Filter pending tasks | Task list contains pending and done tasks | Call `TaskService.filter_pending_task()` | Mixed task list | Only tasks with status `"pending"` are returned | Not executed yet | Open | Core filter |
| TC_025 | Filter done tasks | Task list contains pending and done tasks | Call `TaskService.filter_done_task()` | Mixed task list | Only tasks with status `"done"` are returned | Not executed yet | Open | Core filter |
| TC_026 | Sort tasks by due date | Task list contains tasks with different dates | Call `TaskService.sort_task_by_due_date()` | Dates: `20-05-2026`, `10-05-2026`, empty date | Tasks are sorted by earliest due date first; tasks without due date are last | Not executed yet | Open | Sorting behaviour |
| TC_027 | Sort tasks by priority | Task list contains tasks with different priorities | Call `TaskService.sort_task_by_priority()` | Priorities: `low`, `urgent`, `medium`, `high` | Order is `urgent`, `high`, `medium`, `low` | Not executed yet | Open | Sorting behaviour |
| TC_028 | Sort tasks by priority and due date | Task list contains different priorities and dates | Call `TaskService.sort_task_by_priority_and_due_date()` | urgent/high/low tasks with different dates | Higher priority comes first; if priority is equal, earlier due date comes first | Not executed yet | Open | Combined sorting |
| TC_029 | ID uniqueness after delete | Three tasks exist; one task is deleted | Add three tasks, delete one, add another task | Existing IDs: `1`, `2`, `3`; delete task `2`; add new task | New task should not duplicate an existing ID | Not executed yet | Open | Current code may fail because id uses `len(task_list) + 1` |
| TC_030 | Old CLI compatibility: no due date concept | Old project used `"no date"` as text value | Compare old behaviour with new service behaviour | Old: `"no date"`; New: `None` | New service should consistently use `None` for missing due date | Not executed yet | Open | Important for migration from old CLI to new app |

---

## Known Issues Found During Test Planning

### Issue 1: `delete_task()` raises an error after successful deletion

Current code:

```python
@staticmethod
def delete_task(task_list: list, task_id: int) -> None:
    task = TaskService.find_task_by_id(task_list, task_id)
    task_list.remove(task)
        
    raise ValueError("Task not found")
```

Problem:

The task is removed, but afterwards `ValueError("Task not found")` is always raised.

Expected correction:

```python
@staticmethod
def delete_task(task_list: list, task_id: int) -> None:
    task = TaskService.find_task_by_id(task_list, task_id)
    task_list.remove(task)
```

Affected test cases:

- TC_020
- TC_021

---

### Issue 2: `mark_task_done()` changes the wrong dictionary key

Current code:

```python
@staticmethod
def mark_task_done(task_list: list, task_id: int) -> None:
    task = TaskService.find_task_by_id(task_list, task_id)
    task["pending"] = "done"
```

Problem:

This creates a new key called `"pending"` instead of changing the existing `"status"` field.

Expected correction:

```python
@staticmethod
def mark_task_done(task_list: list, task_id: int) -> None:
    task = TaskService.find_task_by_id(task_list, task_id)
    task["status"] = "done"
```

Affected test cases:

- TC_022
- TC_024
- TC_025

---

### Issue 3: Task IDs can become duplicated after deleting tasks

Current code:

```python
"id": len(task_list) + 1
```

Problem:

If a task is deleted and a new task is added afterwards, the new task can receive an ID that already exists.

Example:

```text
Existing tasks:
ID 1
ID 2
ID 3

Delete ID 2

Remaining tasks:
ID 1
ID 3

Add new task:
len(task_list) + 1 = 3

Result:
ID 1
ID 3
ID 3
```

Expected correction:

```python
@staticmethod
def get_next_id(task_list: list) -> int:
    if not task_list:
        return 1
    return max(task["id"] for task in task_list) + 1
```

Then use it in `add_task()`:

```python
"id": TaskService.get_next_id(task_list),
```

Affected test cases:

- TC_010
- TC_029

---

## Test Execution Plan

The documented test cases will later be implemented as automated tests with `pytest`.

Planned test file:

```text
tests/test_task_service.py
```

Planned command to run all tests:

```bash
python -m pytest -v
```

Planned command to run only the TaskService tests:

```bash
python -m pytest tests/test_task_service.py -v
```

---

## Test Status Legend

| Status | Meaning |
|---|---|
| Open | Test case has been defined but not executed yet |
| Pass | Test was executed and the actual result matched the expected result |
| Fail | Test was executed and the actual result did not match the expected result |
| Blocked | Test cannot be executed because another feature or bug fix is missing |

---

## Notes

These test cases are written before the full ORM, SQLite and NiceGUI migration.  
They focus on the current business logic in `TaskService`.

Later, additional test cases should be added for:

- ORM entities
- SQLite database persistence
- DAO / repository layer
- NiceGUI forms
- NiceGUI buttons and navigation
- end-to-end demo workflow