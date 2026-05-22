from nicegui import ui

from database import create_tables, Task
from task_services import TaskService
from calendar_export import export_tasks_to_ics


# ------------------------------------------------------------
# App configuration
# ------------------------------------------------------------

APP_NAME = "SerJusJer Task Cockpit"
APP_SUBTITLE = "Small steps. Big projects."
DAILY_MISSION = "Finish one important task before adding three new ones."

PRIORITIES = ["low", "medium", "high", "urgent"]
STATUSES = ["pending", "done"]


# ------------------------------------------------------------
# Database setup
# ------------------------------------------------------------

create_tables()


# ------------------------------------------------------------
# Table configuration
# ------------------------------------------------------------

columns = [
    {"name": "id", "label": "ID", "field": "id", "sortable": True, "align": "left"},
    {"name": "title", "label": "Title", "field": "title", "sortable": True, "align": "left"},
    {"name": "due_date", "label": "Due Date", "field": "due_date", "sortable": True, "align": "left"},
    {"name": "priority", "label": "Priority", "field": "priority", "sortable": True, "align": "left"},
    {"name": "status", "label": "Status", "field": "status", "sortable": True, "align": "left"},
]


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def task_to_dict(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "due_date": task.due_date if task.due_date else "",
        "status": task.status,
        "priority": task.priority,
    }


def calculate_task_stats(tasks: list[Task]) -> dict:
    total = len(tasks)
    done = sum(1 for task in tasks if task.status == "done")
    pending = total - done
    high_priority = sum(1 for task in tasks if task.priority == "high")
    urgent_priority = sum(1 for task in tasks if task.priority == "urgent")

    completion = 0
    if total > 0:
        completion = round((done / total) * 100)

    return {
        "total": total,
        "done": done,
        "pending": pending,
        "high_priority": high_priority,
        "urgent_priority": urgent_priority,
        "completion": completion,
    }


def get_cockpit_message(stats: dict) -> str:
    if stats["total"] == 0:
        return "Your cockpit is clear. Add your first mission."
    if stats["completion"] == 100:
        return "Mission complete. Clean work."
    if stats["urgent_priority"] > 0:
        return "Urgent tasks detected. Focus mode recommended."
    if stats["high_priority"] > 0:
        return "High priority detected. Focus mode recommended."
    if stats["pending"] > stats["done"]:
        return "One task at a time. Momentum beats perfection."
    return "Good rhythm. Keep the cockpit clean."


def get_selected_task_id(task_id_input) -> int:
    if task_id_input.value is None:
        raise ValueError("Please enter a task ID first.")

    task_id = int(task_id_input.value)

    if task_id <= 0:
        raise ValueError("Task ID must be greater than zero.")

    return task_id


def get_all_tasks() -> list[Task]:
    return TaskService.sort_task_by_priority_and_due_date()


def get_visible_tasks(status_filter_value: str) -> list[Task]:
    if status_filter_value == "all":
        return get_all_tasks()

    return TaskService.filter_task_by_status(status_filter_value)


# ------------------------------------------------------------
# NiceGUI page
# ------------------------------------------------------------

@ui.page("/")
def task_page():
    ui.page_title(APP_NAME)
    ui.query("body").classes("bg-slate-100")

    with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-5"):

        # Header
        with ui.card().classes(
            "w-full p-6 rounded-2xl shadow-xl "
            "bg-gradient-to-r from-slate-950 via-slate-800 to-slate-700 text-white"
        ):
            with ui.row().classes("w-full items-center justify-between gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label(f"🧭 {APP_NAME}").classes("text-3xl font-bold")
                    ui.label(APP_SUBTITLE).classes("text-base opacity-80")
                    ui.label(f"Today's mission: {DAILY_MISSION}").classes(
                        "text-sm mt-2 opacity-90"
                    )

                cockpit_badge = ui.label("Ready").classes(
                    "px-4 py-2 rounded-full bg-white text-slate-900 font-semibold"
                )

            with ui.grid(columns=4).classes("w-full gap-4 mt-5"):
                with ui.card().classes("p-4 bg-white/10 rounded-xl shadow-none"):
                    total_label = ui.label("0").classes("text-2xl font-bold")
                    ui.label("Total missions").classes("text-xs opacity-70")

                with ui.card().classes("p-4 bg-white/10 rounded-xl shadow-none"):
                    done_label = ui.label("0").classes("text-2xl font-bold")
                    ui.label("Completed").classes("text-xs opacity-70")

                with ui.card().classes("p-4 bg-white/10 rounded-xl shadow-none"):
                    pending_label = ui.label("0").classes("text-2xl font-bold")
                    ui.label("Open").classes("text-xs opacity-70")

                with ui.card().classes("p-4 bg-white/10 rounded-xl shadow-none"):
                    progress_label = ui.label("0%").classes("text-2xl font-bold")
                    ui.label("Progress").classes("text-xs opacity-70")

            progress_bar = ui.linear_progress(value=0).classes("w-full mt-4")

        # Add task section
        with ui.card().classes("w-full p-5 rounded-2xl shadow-md"):
            ui.label("Add a new mission").classes("text-xl font-semibold")

            with ui.row().classes("w-full gap-4 items-end"):
                title_input = ui.input("Title").classes("w-72")
                date_input = ui.input("Due date (DD-MM-YYYY)").classes("w-52")

                priority_select = ui.select(
                    PRIORITIES,
                    value="medium",
                    label="Priority",
                ).classes("w-48")

                def add_task():
                    try:
                        TaskService.add_task(
                            title_input.value,
                            date_input.value or "",
                            priority_select.value,
                        )

                        title_input.value = ""
                        date_input.value = ""
                        priority_select.value = "medium"

                        ui.notify(
                            "Mission added to the SerJusJer cockpit 🚀",
                            type="positive",
                        )

                        refresh_table()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")
                    except Exception as error:
                        ui.notify(f"Unexpected error: {error}", type="negative")

                ui.button(
                    "Add mission",
                    on_click=add_task,
                    icon="add",
                ).classes("bg-blue-600 text-white")

        # Task management section
        with ui.card().classes("w-full p-5 rounded-2xl shadow-md"):

            with ui.row().classes("w-full items-center justify-between"):
                ui.label("Mission control").classes("text-xl font-semibold")

                status_filter = ui.select(
                    ["all", "pending", "done"],
                    value="all",
                    label="Filter by status",
                ).classes("w-48")

            with ui.row().classes("w-full gap-4 items-end mt-2"):
                task_id_input = ui.number(
                    "Task ID",
                    min=1,
                    step=1,
                ).classes("w-36")

                edit_title_input = ui.input("Edit title").classes("w-72")
                edit_date_input = ui.input("Edit due date (DD-MM-YYYY)").classes("w-52")

                edit_priority_select = ui.select(
                    PRIORITIES,
                    value="medium",
                    label="Edit priority",
                ).classes("w-48")

                edit_status_select = ui.select(
                    STATUSES,
                    value="pending",
                    label="Edit status",
                ).classes("w-48")

                def edit_task():
                    try:
                        task_id = get_selected_task_id(task_id_input)

                        TaskService.edit_task(
                            task_id,
                            edit_title_input.value,
                            edit_date_input.value or "",
                            edit_priority_select.value,
                            edit_status_select.value,
                        )

                        ui.notify("Mission updated.", type="positive")
                        refresh_table()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")
                    except Exception as error:
                        ui.notify(f"Unexpected error: {error}", type="negative")

                def mark_done():
                    try:
                        task_id = get_selected_task_id(task_id_input)
                        TaskService.update_task_status(task_id, "done")

                        ui.notify("Mission marked as completed.", type="positive")
                        refresh_table()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")
                    except Exception as error:
                        ui.notify(f"Unexpected error: {error}", type="negative")

                def mark_pending():
                    try:
                        task_id = get_selected_task_id(task_id_input)
                        TaskService.update_task_status(task_id, "pending")

                        ui.notify("Mission moved back to pending.", type="positive")
                        refresh_table()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")
                    except Exception as error:
                        ui.notify(f"Unexpected error: {error}", type="negative")

                def delete_task():
                    try:
                        task_id = get_selected_task_id(task_id_input)
                        TaskService.delete_task(task_id)

                        task_id_input.value = None

                        ui.notify("Mission removed from the cockpit.", type="positive")
                        refresh_table()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")
                    except Exception as error:
                        ui.notify(f"Unexpected error: {error}", type="negative")

                def export_calendar():
                    try:
                        tasks = get_all_tasks()
                        filename = export_tasks_to_ics(tasks)

                        ui.download(filename)
                        ui.notify("Calendar file exported.", type="positive")

                    except Exception as error:
                        ui.notify(
                            f"Could not export calendar: {error}",
                            type="negative",
                        )

                ui.button(
                    "Edit",
                    on_click=edit_task,
                    icon="edit",
                ).classes("bg-purple-600 text-white")

                ui.button(
                    "Done",
                    on_click=mark_done,
                    icon="check_circle",
                ).classes("bg-green-600 text-white")

                ui.button(
                    "Pending",
                    on_click=mark_pending,
                    icon="radio_button_unchecked",
                ).classes("bg-orange-500 text-white")

                ui.button(
                    "Delete",
                    on_click=delete_task,
                    icon="delete",
                ).classes("bg-red-600 text-white")

                ui.button(
                    "Export calendar",
                    on_click=export_calendar,
                    icon="event",
                ).classes("bg-slate-700 text-white")

            table = ui.table(
                columns=columns,
                rows=[],
                row_key="id",
                pagination=10,
            ).classes("w-full mt-5")

            def refresh_table():
                try:
                    visible_tasks = get_visible_tasks(status_filter.value)
                    all_tasks = get_all_tasks()

                    table.rows = [task_to_dict(task) for task in visible_tasks]
                    table.update()

                    stats = calculate_task_stats(all_tasks)

                    total_label.set_text(str(stats["total"]))
                    done_label.set_text(str(stats["done"]))
                    pending_label.set_text(str(stats["pending"]))
                    progress_label.set_text(f'{stats["completion"]}%')
                    cockpit_badge.set_text(get_cockpit_message(stats))

                    progress_bar.value = stats["completion"] / 100
                    progress_bar.update()

                except Exception as error:
                    ui.notify(f"Could not refresh tasks: {error}", type="negative")

            status_filter.on_value_change(lambda _: refresh_table())

            refresh_table()

        # Footer
        with ui.row().classes("w-full justify-center mt-2"):
            ui.label(
                "SerJusJer Task Cockpit · Built with Python and NiceGUI"
            ).classes("text-xs text-slate-500")


# ------------------------------------------------------------
# App start
# ------------------------------------------------------------

ui.run(
    title=APP_NAME,
    reload=False,
)