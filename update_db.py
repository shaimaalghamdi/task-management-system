import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

columns = cursor.execute("PRAGMA table_info(tasks)").fetchall()
existing_columns = [column[1] for column in columns]

if "description" not in existing_columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN description TEXT")

if "status" not in existing_columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'")

if "priority" not in existing_columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'Medium'")

if "due_date" not in existing_columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

connection.commit()
connection.close()

print("Database updated successfully!")