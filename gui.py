from nicegui import ui

from database import create_tables
from task_services import TaskService


create_tables()


def task_tuple_to_dict(task: tuple) -> dict:
    """
    Convert a database tuple into a dictionary for the NiceGUI table.

    Expected tuple order:
    id, title, due_date, status, priority
    """
    return {
        "id": task[0],
        "title": task[1],
        "due_date": task[2] if task[2] is not None else "",
        "status": task[3],
        "priority": task[4],
    }


columns = [
    {"name": "id", "label": "ID", "field": "id", "sortable": True},
    {"name": "title", "label": "Title", "field": "title", "sortable": True},
    {"name": "due_date", "label": "Due Date", "field": "due_date", "sortable": True},
    {"name": "priority", "label": "Priority", "field": "priority", "sortable": True},
    {"name": "status", "label": "Status", "field": "status", "sortable": True},
]


@ui.page("/")
def task_page():
    ui.page_title("To-Do List")

    with ui.column().classes("w-full max-w-6xl mx-auto p-6 gap-4"):
        ui.label("To-Do List").classes("text-3xl font-bold")

        with ui.card().classes("w-full p-4"):
            ui.label("Add new task").classes("text-xl font-semibold")

            with ui.row().classes("w-full gap-4 items-end"):
                title_input = ui.input("Title").classes("w-64")
                date_input = ui.input("Due date (DD-MM-YYYY)").classes("w-48")
                priority_select = ui.select(
                    ["low", "medium", "high", "urgent"],
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
                        ui.notify("Task added successfully", type="positive")
                        refresh_table()
                    except ValueError as error:
                        ui.notify(str(error), type="negative")

                ui.button("Add task", on_click=add_task).classes("bg-blue-600 text-white")

        with ui.card().classes("w-full p-4"):
            ui.label("Manage tasks").classes("text-xl font-semibold")

            with ui.row().classes("w-full gap-4 items-end"):
                status_filter = ui.select(
                    ["all", "pending", "done"],
                    value="all",
                    label="Filter by status",
                ).classes("w-48")

                task_id_input = ui.number("Task ID", min=1, step=1).classes("w-32")

                def mark_done():
                    try:
                        task_id = int(task_id_input.value)
                        TaskService.update_task_status(task_id, "done")
                        ui.notify("Task marked as done", type="positive")
                        refresh_table()
                    except (TypeError, ValueError) as error:
                        ui.notify(str(error), type="negative")

                def mark_pending():
                    try:
                        task_id = int(task_id_input.value)
                        TaskService.update_task_status(task_id, "pending")
                        ui.notify("Task marked as pending", type="positive")
                        refresh_table()
                    except (TypeError, ValueError) as error:
                        ui.notify(str(error), type="negative")

                def delete_task():
                    try:
                        task_id = int(task_id_input.value)
                        TaskService.delete_task(task_id)
                        task_id_input.value = None
                        ui.notify("Task deleted", type="positive")
                        refresh_table()
                    except (TypeError, ValueError) as error:
                        ui.notify(str(error), type="negative")

                ui.button("Done", on_click=mark_done).classes("bg-green-600 text-white")
                ui.button("Pending", on_click=mark_pending).classes("bg-orange-500 text-white")
                ui.button("Delete", on_click=delete_task).classes("bg-red-600 text-white")

            table = ui.table(
                columns=columns,
                rows=[],
                row_key="id",
                pagination=10,
            ).classes("w-full mt-4")

            def refresh_table():
                if status_filter.value == "all":
                    tasks = TaskService.sort_task_by_priority_and_due_date()
                else:
                    tasks = TaskService.filter_task_by_status(status_filter.value)

                table.rows = [task_tuple_to_dict(task) for task in tasks]
                table.update()

            status_filter.on("update:model-value", lambda _: refresh_table())

            refresh_table()


ui.run(title="To-Do List", reload=False)