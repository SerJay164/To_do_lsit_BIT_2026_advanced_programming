# # SerJusJer Task Cockpit

A browser-based task management application developed for the **Advanced Programming** module at FHNW.

SerJusJer Task Cockpit is a modern Python web application for creating, organizing, filtering, updating, and tracking personal tasks. The project migrates a previous command-line to-do application into a structured browser-based application with a graphical user interface, server-side application logic, and persistent database storage.

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
- [Known Limitations](#known-limitations)
- [Team and Work Distribution](#team-and-work-distribution)
- [Project Management](#project-management)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

The goal of this project is to develop a browser-based task management application using Python, NiceGUI, SQLite, and SQLModel.

The application allows users to manage their daily tasks in a simple but structured way. Tasks can be created with a title, due date, priority, and status. The user can view all tasks in a clean dashboard, filter tasks by status or priority, mark tasks as done or pending, and delete tasks that are no longer needed.

The project follows the requirements of the Advanced Programming module:

- Browser-based application instead of a CLI-only application
- NiceGUI as frontend technology
- Server-side Python logic
- SQLite database for persistence
- ORM-based data access using SQLModel
- Object-oriented structure
- Automated and documented tests
- GitHub-based collaboration

---

## Problem Statement

Many students and working professionals manage tasks across different tools, notes, messages, or memory. This often leads to forgotten deadlines, unclear priorities, and inefficient planning.

The SerJusJer Task Cockpit solves this problem by providing a simple task dashboard where tasks can be collected, prioritized, tracked, and completed in one place.

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

A student opens the SerJusJer Task Cockpit in the browser before starting a study session.

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
**Precondition:** At least one task exists or the database is empty.  
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

### UC_004 – Delete Task

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

### UC_005 – Filter Tasks

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
SQLite database via SQLModel ORMTo_do_lsit_BIT_2026_advanced_programming