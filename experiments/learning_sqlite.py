import sqlite3

conn = sqlite3.connect("experiments/learning.db")

cursor = conn.cursor()

cursor.execute("""
               Delete from tasks
               Where id = ?
               """, (2,))

conn.commit()

print("task updated")

conn.close()