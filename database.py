import sqlite3

DB_NAME = "to_do.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()