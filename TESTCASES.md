# Test Cases – SerJusJer Task Cockpit

## Overview

This document describes the 12 main test cases for the SerJusJer Task Cockpit project.

The project testing follows the required structure:

- 6 unit tests
- 3 database tests
- 3 integration tests

---

## Test Case TC_001

| Field | Details |
|---|---|
| Test case ID | TC_001 |
| Test case title/description | Validate that spaces are removed from a task title |
| Preconditions | TaskService is available |
| Test steps | 1. Call `validate_title("  Study Python  ")` |
| Test data/input | `"  Study Python  "` |
| Expected result | Returned title is `"Study Python"` |
| Actual result | Returned title is `"Study Python"` |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_002

| Field | Details |
|---|---|
| Test case ID | TC_002 |
| Test case title/description | Reject empty task title |
| Preconditions | TaskService is available |
| Test steps | 1. Call `validate_title("   ")` |
| Test data/input | Empty title with spaces |
| Expected result | `ValueError` is raised |
| Actual result | `ValueError` is raised |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_003

| Field | Details |
|---|---|
| Test case ID | TC_003 |
| Test case title/description | Accept valid due date |
| Preconditions | TaskService is available |
| Test steps | 1. Call `parse_due_date("24-05-2026")` |
| Test data/input | `"24-05-2026"` |
| Expected result | Date is parsed as `2026-05-24` |
| Actual result | Date is parsed as `2026-05-24` |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_004

| Field | Details |
|---|---|
| Test case ID | TC_004 |
| Test case title/description | Reject invalid date format |
| Preconditions | TaskService is available |
| Test steps | 1. Call `parse_due_date("2026-05-24")` |
| Test data/input | `"2026-05-24"` |
| Expected result | `ValueError` is raised |
| Actual result | `ValueError` is raised |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_005

| Field | Details |
|---|---|
| Test case ID | TC_005 |
| Test case title/description | Accept urgent priority |
| Preconditions | TaskService is available |
| Test steps | 1. Call `validate_priority("URGENT")` |
| Test data/input | `"URGENT"` |
| Expected result | Returned priority is `"urgent"` |
| Actual result | Returned priority is `"urgent"` |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_006

| Field | Details |
|---|---|
| Test case ID | TC_006 |
| Test case title/description | Reject invalid task status |
| Preconditions | TaskService is available |
| Test steps | 1. Call `validate_status("in progress")` |
| Test data/input | `"in progress"` |
| Expected result | `ValueError` is raised |
| Actual result | `ValueError` is raised |
| Status | Pass |
| Comments | Unit test |

---

## Test Case TC_007

| Field | Details |
|---|---|
| Test case ID | TC_007 |
| Test case title/description | Add task and persist it in database |
| Preconditions | Test database is empty |
| Test steps | 1. Add task through `TaskService.add_task()` 2. Read tasks with `list_tasks()` |
| Test data/input | Title: `Write report`, date: `24-05-2026`, priority: `high` |
| Expected result | One task is stored with status `pending` |
| Actual result | One task is stored with status `pending` |
| Status | Pass |
| Comments | Database test |

---

## Test Case TC_008

| Field | Details |
|---|---|
| Test case ID | TC_008 |
| Test case title/description | Edit existing task in database |
| Preconditions | Test database contains one task |
| Test steps | 1. Add task 2. Edit task 3. Read updated task |
| Test data/input | New title: `New title`, date: `25-05-2026`, priority: `urgent`, status: `done` |
| Expected result | Task fields are updated correctly |
| Actual result | Task fields are updated correctly |
| Status | Pass |
| Comments | Database test |

---

## Test Case TC_009

| Field | Details |
|---|---|
| Test case ID | TC_009 |
| Test case title/description | Delete task from database |
| Preconditions | Test database contains one task |
| Test steps | 1. Add task 2. Delete task 3. Read all tasks |
| Test data/input | Task title: `Delete me` |
| Expected result | Task list is empty |
| Actual result | Task list is empty |
| Status | Pass |
| Comments | Database test |

---

## Test Case TC_010

| Field | Details |
|---|---|
| Test case ID | TC_010 |
| Test case title/description | Export tasks to calendar file |
| Preconditions | Test database contains one task with due date |
| Test steps | 1. Add task 2. Export tasks to `.ics` file |
| Test data/input | Title: `Prepare presentation`, date: `24-05-2026`, priority: `high` |
| Expected result | `.ics` file is created |
| Actual result | `.ics` file is created |
| Status | Pass |
| Comments | Integration test |

---

## Test Case TC_011

| Field | Details |
|---|---|
| Test case ID | TC_011 |
| Test case title/description | Calendar export contains task information |
| Preconditions | Test database contains one task with due date |
| Test steps | 1. Add task 2. Export calendar file 3. Read file content |
| Test data/input | Title: `Prepare presentation`, date: `24-05-2026`, priority: `high` |
| Expected result | Calendar file contains title, date, priority and status |
| Actual result | Calendar file contains title, date, priority and status |
| Status | Pass |
| Comments | Integration test |

---

## Test Case TC_012

| Field | Details |
|---|---|
| Test case ID | TC_012 |
| Test case title/description | Calendar export skips tasks without due date |
| Preconditions | Test database contains one task without due date |
| Test steps | 1. Add task without date 2. Export calendar file 3. Read file content |
| Test data/input | Title: `Task without date`, date: empty, priority: `medium` |
| Expected result | Task is not exported as calendar event |
| Actual result | Task is not exported as calendar event |
| Status | Pass |
| Comments | Integration test |