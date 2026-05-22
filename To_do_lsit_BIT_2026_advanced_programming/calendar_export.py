from pathlib import Path
from datetime import datetime, timedelta


def export_tasks_to_ics(tasks, filename="tasks_export.ics"):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//SerJusJer Task Cockpit//EN",
    ]

    for task in tasks:
        if task.due_date is None:
            continue

        start_date = task.due_date.strftime("%Y%m%d")
        end_date = (task.due_date + timedelta(days=1)).strftime("%Y%m%d")

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:task-{task.id}@serjusjer-task-cockpit",
            f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%S')}",
            f"DTSTART;VALUE=DATE:{start_date}",
            f"DTEND;VALUE=DATE:{end_date}",
            f"SUMMARY:{task.title}",
            f"DESCRIPTION:Priority: {task.priority} | Status: {task.status}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")

    Path(filename).write_text("\n".join(lines), encoding="utf-8")

    return filename