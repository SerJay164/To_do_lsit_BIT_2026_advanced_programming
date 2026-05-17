# SerJusJer Task Cockpit

A browser-based task management application developed for the **Advanced Programming** module at FHNW.

SerJusJer Task Cockpit is a modern Python web application for creating, organizing, filtering, updating, and tracking personal tasks. The project is based on an earlier command-line to-do application and migrates it into a structured browser-based application with a graphical user interface, server-side application logic, and persistent database storage.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Target Users](#target-users)
- [Scenario](#scenario)
- [Features](#features)
- [User Stories](#user-stories)
- [Use Cases](#use-cases)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Installation](#installation)
- [How to Run the Application](#how-to-run-the-application)
- [Testing](#testing)
- [Input Validation](#input-validation)
- [Error Handling](#error-handling)
- [Screenshots](#screenshots)
- [Wireframes](#wireframes)
- [UML Class Diagram](#uml-class-diagram)
- [Known Limitations](#known-limitations)
- [Team and Work Distribution](#team-and-work-distribution)
- [Project Management](#project-management)
- [Development Roadmap](#development-roadmap)
- [Final Presentation Preparation](#final-presentation-preparation)
- [How This Project Meets the Module Requirements](#how-this-project-meets-the-module-requirements)
- [Future Improvements](#future-improvements)
- [Authors](#authors)
- [License](#license)

---

## Project Overview

The goal of this project is to develop a browser-based task management application using Python, NiceGUI, SQLite, and SQLModel.

The application allows users to manage their daily tasks in a simple but structured way. Tasks can be created with a title, due date, priority, and status. The user can view all tasks in a clean dashboard, filter tasks by status or priority, mark tasks as done or pending, and delete tasks that are no longer needed.

The project follows the requirements of the Advanced Programming module:

- Browser-based application instead of a CLI-only application
- NiceGUI as frontend technology
- Server-side Python application logic
- SQLite database for persistent data storage
- ORM-based data access using SQLModel
- Object-oriented structure
- Automated and documented tests
- GitHub-based collaboration

---

## Problem Statement

Many students and working professionals manage tasks across different tools, notes, messages, or memory. This often leads to forgotten deadlines, unclear priorities, and inefficient planning.

SerJusJer Task Cockpit solves this problem by providing a simple task dashboard where tasks can be collected, prioritized, tracked, and completed in one place.

The application focuses on clarity and usability rather than feature overload. The user should immediately see what needs to be done, what is already completed, and which tasks are important.

---

## Target Users

The application is designed for:

- Students managing assignments, exams, and project work
- Small project teams tracking simple tasks
- Individuals who want a lightweight personal task manager
- Users who prefer a browser-based interface over command-line tools

---

## Scenario

A student opens SerJusJer Task Cockpit in the browser before starting a study session.

First, the student adds several tasks, such as preparing a presentation, writing test cases, and reviewing the project README. For each task, the student enters a title, an optional due date, and a priority.

The dashboard immediately displays all tasks. The student filters the list to show only pending tasks and focuses on the high-priority ones. After finishing a task, the student marks it as done. The application updates the task status and stores the change in the SQLite database, so the information is still available after restarting the application.

---

## Features

### Implemented Core Features

- Create new tasks
- Store tasks persistently in an SQLite database
- Display tasks in a browser-based NiceGUI interface
- Assign task priorities
- Assign task status: `pending` or `done`
- Mark tasks as completed
- Mark completed tasks as pending again
- Delete tasks
- View task statistics in a dashboard
- Filter or organize tasks by task state
- Validate user input before saving tasks

### Planned or Optional Improvements

- Edit existing tasks directly from the GUI
- Add task categories such as `School`, `Work`, or `Private`
- Add an overdue task view
- Add a search function
- Add confirmation dialogs before deleting tasks
- Add a more advanced dashboard with progress indicators
- Add user login or simple user storage

---

## User Stories

### US_001 – Add a Task

As a user, I want to create a new task with a title, due date, and priority, so that I can remember what needs to be done.

### US_002 – View All Tasks

As a user, I want to see all my tasks in one overview, so that I can understand my current workload.

### US_003 – Mark a Task as Done

As a user, I want to mark a task as done, so that I can track my progress.

### US_004 – Filter Tasks by Status

As a user, I want to filter tasks by status, so that I can focus only on pending or completed tasks.

### US_005 – Delete a Task

As a user, I want to delete tasks that are no longer relevant, so that my task list stays clean.

### US_006 – Persist Tasks

As a user, I want my tasks to be saved automatically, so that they are still available after restarting the application.

### US_007 – View Task Statistics

As a user, I want to see simple statistics about my tasks, so that I can quickly understand how many tasks are open, completed, or high priority.

---

## Use Cases

### UC_001 – Create Task

**Actor:** User  
**Precondition:** The application is running in the browser.

**Main Flow:**

1. The user enters a task title.
2. The user optionally enters a due date.
3. The user selects a priority.
4. The user clicks the button to add the task.
5. The system validates the input.
6. The system stores the task in the database.
7. The system refreshes the task list.

**Expected Result:**  
A new pending task appears in the task overview.

---

### UC_002 – View Task List

**Actor:** User  
**Precondition:** The application is running.

**Main Flow:**

1. The user opens the application.
2. The system loads all tasks from the database.
3. The system displays the tasks in the GUI.

**Expected Result:**  
The user sees all stored tasks or an empty task list.

---

### UC_003 – Complete Task

**Actor:** User  
**Precondition:** At least one pending task exists.

**Main Flow:**

1. The user selects or enters the ID of a task.
2. The user triggers the complete action.
3. The system updates the task status to `done`.
4. The system saves the change in the database.
5. The system refreshes the task overview.

**Expected Result:**  
The task is shown as completed.

---

### UC_004 – Set Task Back to Pending

**Actor:** User  
**Precondition:** At least one completed task exists.

**Main Flow:**

1. The user selects or enters the ID of a completed task.
2. The user triggers the pending action.
3. The system updates the task status to `pending`.
4. The system saves the change in the database.
5. The system refreshes the task overview.

**Expected Result:**  
The task is shown as pending again.

---

### UC_005 – Delete Task

**Actor:** User  
**Precondition:** At least one task exists.

**Main Flow:**

1. The user selects or enters the ID of a task.
2. The user triggers the delete action.
3. The system removes the task from the database.
4. The system refreshes the task list.

**Expected Result:**  
The deleted task no longer appears in the task overview.

---

### UC_006 – Filter Tasks

**Actor:** User  
**Precondition:** Tasks exist in the database.

**Main Flow:**

1. The user selects a status or priority filter.
2. The system queries or filters the available tasks.
3. The system updates the visible task list.

**Expected Result:**  
Only tasks matching the selected filter are displayed.

---

## Architecture

The application follows a layered architecture inspired by the Advanced Programming reference project.

```text
Browser / Client
    |
    v
Presentation Layer
NiceGUI pages, layout, tables, forms, buttons
    |
    v
Controller / UI Callback Layer
Receives user events and calls application services
    |
    v
Service Layer
Business logic, validation, task operations
    |
    v
Data Access Layer
DAO classes for database operations
    |
    v
Persistence Layer
SQLite database via SQLModel ORM

Presentation Layer

The presentation layer is implemented with NiceGUI. It defines what the user sees in the browser: forms, buttons, task tables, dashboard cards, and notifications.

The browser acts as a thin client. It renders the user interface, while the application logic remains on the Python server.

Application Logic Layer

The application logic is implemented in service classes. This layer validates input, applies business rules, and coordinates task-related use cases.

Examples:

Validate task title
Validate date format
Validate priority
Add a new task
Mark a task as completed
Mark a task as pending
Delete a task
Load filtered task lists
Data Access Layer

The data access layer is responsible for storing and retrieving data from the database. The goal is to keep SQLModel and database-specific code away from the GUI and business logic.

Examples:

Create task
Get all tasks
Get task by ID
Update task
Delete task
Persistence Layer

The persistence layer uses SQLite as a local database and SQLModel as the ORM. SQLModel maps Python classes to database tables and allows the application to work with Python objects instead of raw SQL strings.

Project Structure
Intended final project structure:
To_do_lsit_BIT_2026_advanced_programming/
│
├── README.md
├── requirements.txt
├── main.py
│
├── todo_app/
│   ├── __init__.py
│   ├── application.py
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── data_access/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── task_dao.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   │
│   └── ui/
│       ├── __init__.py
│       ├── task_page.py
│       └── task_controller.py
│
├── tests/
│   ├── test_task_service.py
│   ├── test_task_dao.py
│   └── test_integration_task_flow.py
│
└── docs/
    ├── TESTCASES.md
    ├── architecture.md
    ├── erd.png
    ├── uml_class_diagram.png
    ├── wireframes.png
    └── screenshots/
        ├── dashboard.png
        ├── add_task.png
        └── task_table.png

Data Model
Entity: Task

| Field      | Type            | Description                                      |
| ---------- | --------------- | ------------------------------------------------ |
| `id`       | `int`           | Unique task identifier                           |
| `title`    | `str`           | Short task description                           |
| `due_date` | `date` or `str` | Optional due date                                |
| `priority` | `str`           | Task priority: `low`, `medium`, `high`, `urgent` |
| `status`   | `str`           | Task status: `pending` or `done`                 |

ER Model

Current simplified ER model:
Task
----
id          PK
title       TEXT
due_date    TEXT / DATE
priority    TEXT
status      TEXT

Optional future extension:
Category
--------
id          PK
name        TEXT

Task
----
id          PK
title       TEXT
due_date    TEXT / DATE
priority    TEXT
status      TEXT
category_id FK -> Category.id

Technology Stack
| Technology | Purpose                                           |
| ---------- | ------------------------------------------------- |
| Python     | Main programming language                         |
| NiceGUI    | Browser-based user interface                      |
| SQLite     | Local persistent database                         |
| SQLModel   | ORM for mapping Python classes to database tables |
| SQLAlchemy | Database engine used by SQLModel                  |
| Pydantic   | Data validation support through SQLModel          |
| pytest     | Automated testing framework                       |
| GitHub     | Version control and team collaboration            |

Design Patterns
Layered Architecture

The project separates responsibilities into presentation, application logic, data access, and persistence. This improves maintainability and makes it easier to test individual parts of the system.

Model-View-Controller Inspired Structure

The project uses an MVC-inspired structure:

View: NiceGUI page components
Controller: UI callbacks and event handlers
Model: Task entity and database-backed domain objects
Service: Application-specific business logic

This keeps the GUI from becoming responsible for business rules.

Data Access Object

The DAO pattern is used to separate database access from business logic. The service layer should not need to know how SQLModel queries are written internally.

Facade

The database setup can be treated as a small facade. A central database module provides simple functions for engine creation, table creation, and session handling.

Installation
1. Clone the Repository
git clone https://github.com/SerJay164/To_do_lsit_BIT_2026_advanced_programming.git
cd To_do_lsit_BIT_2026_advanced_programming

2. Create a Virtual Environment
Windows:
python -m venv .venv
macOS / Linux:
.venv\Scripts\activate
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

How to Run the Application
WELCHER BEFEHL FUNKTIONIERT BEI UNS -> ZU PRÜFEN
...

Testing

The project includes automated and documented tests. The target test mix follows the Advanced Programming expectations:
| Test Type         | Number | Purpose                                                              |
| ----------------- | -----: | -------------------------------------------------------------------- |
| Unit Tests        |      6 | Test isolated service methods and validation logic                   |
| Database Tests    |      3 | Test database persistence and DAO behavior                           |
| Integration Tests |      3 | Test complete task flows across UI, service, and database boundaries |
| Total             |     12 | Required project test coverage target                                |

Run All Tests
pytest

Run Tests Verbosely
pytest -v

Planned Test Cases
| ID     | Test Type   | Description                                     |
| ------ | ----------- | ----------------------------------------------- |
| TC_001 | Unit        | Valid task title is accepted                    |
| TC_002 | Unit        | Empty task title raises a validation error      |
| TC_003 | Unit        | Invalid priority raises a validation error      |
| TC_004 | Unit        | Valid due date is parsed correctly              |
| TC_005 | Unit        | Invalid due date raises a validation error      |
| TC_006 | Unit        | New task is created with status `pending`       |
| TC_007 | DB          | Task is saved to SQLite database                |
| TC_008 | DB          | Existing task can be loaded by ID               |
| TC_009 | DB          | Deleted task is removed from database           |
| TC_010 | Integration | User creates task and sees it in the task list  |
| TC_011 | Integration | User marks task as done and status is persisted |
| TC_012 | Integration | User deletes task and list updates correctly    |

Detailed manual and automated test cases are documented in:
TESTCASES.md

or after moving documentation into the docs folder:
docs/TESTCASES.md

!!! ANZUPASSEN: Hier nur den Pfad stehen lassen, der bei uns wirklich existiert. Wenn am Ende TESTCASES.md direkt im Hauptordner liegt, dann docs/TESTCASES.md löschen.

Input Validation

The application validates user input before storing data.

Title Validation

Rules:

Title must not be empty
Title should not contain invalid separator characters
Title should be stripped of unnecessary whitespace
Date Validation

Rules:

Empty due date is allowed
Valid date format: DD-MM-YYYY
Invalid dates are rejected
Priority Validation

Allowed values:
low
medium
high
urgent

ACHTUNG!! Wenn "urgent" in unserer GUI nicht funktioniert, dann entweder in der GUI ergänzen oder hier löschen. Wichtig: README, GUI, Service und Tests müssen übereinstimmen!!!

Status Validation

Allowed values:
pending
done

Error Handling

The application aims to fail gracefully instead of crashing.

Examples:

Invalid user input is rejected with a clear message
Missing or invalid task IDs are handled safely
Database operations are handled through controlled service or DAO methods
User feedback is shown through NiceGUI notifications

Screenshots
NOCH EINZUFÜGEN

Dashboard
...
Add Task Form
...
Task Table
...

Wireframes
NOCH EINZUFÜGEN: aus Figma, draw.io, Excalidraw oder PowerPoint exportieren. Es soll zeigen, wie unsere App geplant ist.

The planned screen layout is documented in:
docs/wireframes.png

Main screens:
1. Dashboard overview
2. Add task form
3. Task table
4. Task action section
5. Optional edit dialog

UML Class Diagram
NOCH EINZUFÜGEN

The UML class diagram is documented in:
docs/uml_class_diagram.png

Main classes:

Task
TaskService
TaskDAO
Database
TaskController
TaskPage

Known Limitations

Current known limitations:
- The current version focuses on a single-user local task manager.
- Authentication is not implemented.
- Multi-user task separation is not implemented.
- Task categories are optional and may be added later.
- Advanced recurring tasks are not supported.
- The edit function may still require final GUI integration.
- The project structure may still need final refactoring into packages.
NOCH ANZUPASSEN -> NICHTS ALS FERTIG DARSTELLEN, WAS NOCH NICHT WIRKLICH FUNKTIONIERT

Team and Work Distribution
| Team Member      | Main Responsibilities                            | GitHub Evidence                |
| ---------------- | ------------------------------------------------ | ------------------------------ |
| [Justin Vogler]  | GUI, testing, documentation, README         | Commits, branch, pull requests |
| [Jeremy Heer]    | Database, SQLModel, presentation            | Commits, branch, pull requests |
| [Seraph Schobin] | Service logic, testing, user interaction    | Commits, branch, pull requests |

The team uses GitHub commits, branches, issues, and pull requests to document contributions.

Project Management

The project is organized through GitHub.

Branch Strategy
| Branch                 | Purpose                                |
| ---------------------- | -------------------------------------- |
| `main`                 | Stable version for final submission    |
| `sql-database`         | Database and NiceGUI implementation    |
| `feature/task-service` | Service logic and test development     |
| `gui`                  | GUI development and layout experiments |
| `experiments`          | Learning and technical experiments     |

Before final submission, the stable implementation should be merged into main.

GitHub Issues

Issues are used for:

Feature planning
Bug tracking
Documentation tasks
Test case tracking
Refactoring tasks

Example issues: SCHAUEN OB DAS SO IST!

Implement DAO layer
Refactor GUI into UI package
Fix pytest imports
Add edit task dialog
Write final README
Add ERD and UML diagrams
Prepare final presentation

Development Roadmap
CHECK COMPLETETED, ALLES WIRKLICH UMGESETZT AM ENDE?

Completed
- Initial CLI-based to-do application
- Migration concept to browser-based app
- NiceGUI user interface prototype
- SQLite database integration
- SQLModel-based task entity
- Basic task service logic
- Initial test case planning

In Progress
- Refactoring into layered architecture
- Improving test coverage
- Finalizing README documentation
- Adding diagrams and screenshots
- Merging stable branch into main

Planned
- Edit task dialog
- Category support
- Better dashboard statistics
- Overdue task view
- Search functionality
- Improved error handling
- Final presentation and live demo preparation
- Final Presentation Preparation

The final presentation will cover:

1. Justification of the chosen topic
2. Project goals and core features
3. Architecture and design decisions
4. Database and ORM implementation
5. Testing strategy and test results
6. Team collaboration and work distribution
7. Live demo of the application
8. Challenges and lessons learned

presentation split:
| Part                           | Responsible Person |
| ------------------------------ | ------------------ |
| Topic and problem statement    | [Jeremy]           |
| Architecture and database      | [Seraphin]         |
| GUI and live demo              | [Justin]           |
| Testing and project management | [Seraphin]         |

How This Project Meets the Module Requirements
| Requirement                 | Implementation                                |
| --------------------------- | --------------------------------------------- |
| Browser-based app           | Implemented with NiceGUI                      |
| Frontend                    | NiceGUI UI components rendered in the browser |
| Backend / application logic | Python service layer                          |
| Database                    | SQLite                                        |
| ORM                         | SQLModel                                      |
| Object orientation          | Task entity, service classes, DAO classes     |
| Testing                     | pytest-based unit, DB, and integration tests  |
| Documentation               | README, TESTCASES, diagrams, screenshots      |
| GitHub collaboration        | Branches, commits, issues, pull requests      |

Future Improvements

Possible future extensions:

User login and user-specific task lists
Task categories and tags
Recurring tasks
Calendar view
Export tasks to CSV or PDF
Dark mode / theme switch
Deployment with Docker
GitHub Actions for automated test execution

Authors / SerJusJer Team:
Justin Vogler
Jeremy Heer
Seraphin Schobin

FHNW
BSc Business Information Technology
Advanced Programming
Spring Semester 2026

License
This project was created for educational purposes as part of the Advanced Programming module at FHNW.