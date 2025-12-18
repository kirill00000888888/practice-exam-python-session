# How to Run the Task Management System

## Requirements
- Python 3.8+
- pip installed

## Install dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Database initialization

The SQLite database (`database/tasks.db`) will be created automatically on first run.
Tables are created in `main.py`.

## Run the application

```bash
python main.py
```

A Tkinter window will open with:
* Tasks tab
* Projects tab
* Users tab

## Run tests

```bash
pytest
```

Tests use a temporary database, so the main DB file is not affected.
