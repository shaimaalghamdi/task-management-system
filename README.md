# Task Management System

A web-based task management system built with Python and Flask.

## Features

- Add new tasks
- Edit existing tasks
- Delete tasks
- Search tasks
- Filter tasks by status
- Filter tasks by priority
- Set task priorities
- Set due dates
- Detect overdue tasks automatically
- Display tasks due today
- Dashboard with task statistics
- Input validation
- User feedback messages

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2

## Database

The project uses SQLite to store task information.

Each task contains:

- Task ID
- Title
- Description
- Status
- Priority
- Due Date
- Creation Date

## Project Structure

```text
Python web project/
│
├── app.py
├── init_db.py
├── update_db.py
├── database.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   └── edit.html
│
├── static/
│   └── style.css
│
└── venv/