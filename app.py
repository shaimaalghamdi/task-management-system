from flask import Flask, render_template, request, redirect, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "task-management-secret-key"


def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():

    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "")
    priority_filter = request.args.get("priority", "")

    connection = get_db_connection()

    query = "SELECT * FROM tasks WHERE 1=1"
    parameters = []

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        parameters.extend([f"%{search}%", f"%{search}%"])

    if status_filter:
        query += " AND status = ?"
        parameters.append(status_filter)

    if priority_filter:
        query += " AND priority = ?"
        parameters.append(priority_filter)

    query += " ORDER BY id DESC"

    tasks = connection.execute(query, parameters).fetchall()

    total_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    pending_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'"
    ).fetchone()[0]

    in_progress_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'In Progress'"
    ).fetchone()[0]

    completed_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Completed'"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        tasks=tasks,
        search=search,
        status_filter=status_filter,
        priority_filter=priority_filter,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    status = request.form.get("status", "Pending")
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "")

    if not title:
        flash("Task title is required.")
        return redirect("/")

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO tasks
        (title, description, status, priority, due_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, description, status, priority, due_date)
    )

    connection.commit()
    connection.close()

    flash("Task added successfully.")
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    flash("Task deleted.")
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    connection = get_db_connection()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Pending")
        priority = request.form.get("priority", "Medium")
        due_date = request.form.get("due_date", "")

        if not title:
            flash("Task title is required.")
            connection.close()
            return redirect(f"/edit/{task_id}")

        connection.execute(
            """
            UPDATE tasks
            SET title = ?,
                description = ?,
                status = ?,
                priority = ?,
                due_date = ?
            WHERE id = ?
            """,
            (
                title,
                description,
                status,
                priority,
                due_date,
                task_id
            )
        )

        connection.commit()
        connection.close()

        flash("Task updated successfully.")
        return redirect("/")

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit.html",
        task=task
    )


if __name__ == "__main__":
    app.run(debug=True)