import sqlite3
import os
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        # Stub method calling specific creation methods to maintain compatibility
        self.create_user_table()
        self.create_project_table()
        self.create_task_table()

    def create_task_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER,
                status TEXT,
                due_date TEXT,
                project_id INTEGER,
                assignee_id INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (assignee_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def create_project_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def create_user_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT,
                registration_date TEXT
            )
        ''')
        self.conn.commit()

    # --- TASKS ---
    def add_task(self, task: Task) -> int:
        self.cursor.execute('''
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.priority, task.status, 
              task.due_date.isoformat() if task.due_date else None, 
              task.project_id, task.assignee_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_task_by_id(self, task_id) -> Task | None:
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_task(row)
        return None

    def get_all_tasks(self) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def update_task(self, task_id, **kwargs) -> bool:
        if not kwargs:
            return False
        
        # Filter supported keys just in case, though usually controller handles this
        valid_keys = {'title', 'description', 'priority', 'status', 'due_date', 'project_id', 'assignee_id'}
        updates = []
        values = []
        for k, v in kwargs.items():
            if k in valid_keys:
                updates.append(f"{k} = ?")
                # Handle datetime conversion if needed
                if k == 'due_date' and isinstance(v, datetime):
                    values.append(v.isoformat())
                else:
                    values.append(v)
        
        if not updates:
            return False
        
        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_task(self, task_id) -> bool:
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_tasks(self, query) -> list[Task]:
        search_query = f"%{query}%"
        self.cursor.execute('''
            SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ?
        ''', (search_query, search_query))
        rows = self.cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = self.cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks WHERE assignee_id = ?', (user_id,))
        rows = self.cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    # --- PROJECTS ---
    def add_project(self, project: Project) -> int:
        self.cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (project.name, project.description, 
              project.start_date.isoformat() if project.start_date else None, 
              project.end_date.isoformat() if project.end_date else None, 
              project.status))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_project_by_id(self, project_id) -> Project | None:
        self.cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_project(row)
        return None

    def get_all_projects(self) -> list[Project]:
        self.cursor.execute('SELECT * FROM projects')
        rows = self.cursor.fetchall()
        return [self._row_to_project(row) for row in rows]

    def update_project(self, project_id, **kwargs) -> bool:
        if not kwargs:
            return False
        valid_keys = {'name', 'description', 'start_date', 'end_date', 'status'}
        updates = []
        values = []
        for k, v in kwargs.items():
            if k in valid_keys:
                updates.append(f"{k} = ?")
                if k in ('start_date', 'end_date') and isinstance(v, datetime):
                    values.append(v.isoformat())
                else:
                    values.append(v)
        if not updates:
            return False
        values.append(project_id)
        
        query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_project(self, project_id) -> bool:
        self.cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- USERS ---
    def add_user(self, user: User) -> int:
        self.cursor.execute('''
            INSERT INTO users (username, email, role, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.email, user.role, 
              user.registration_date.isoformat() if user.registration_date else None))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_user(row)
        return None

    def get_all_users(self) -> list[User]:
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return [self._row_to_user(row) for row in rows]

    def update_user(self, user_id, **kwargs) -> bool:
        if not kwargs:
            return False
        valid_keys = {'username', 'email', 'role', 'registration_date'}
        updates = []
        values = []
        for k, v in kwargs.items():
            if k in valid_keys:
                updates.append(f"{k} = ?")
                if k == 'registration_date' and isinstance(v, datetime):
                    values.append(v.isoformat())
                else:
                    values.append(v)
        if not updates:
            return False
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_user(self, user_id) -> bool:
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- Helpers ---
    def _row_to_task(self, row) -> Task:
        due_date = datetime.fromisoformat(row['due_date']) if row['due_date'] else None
        task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
        task.id = row['id']
        task.status = row['status']
        return task

    def _row_to_project(self, row) -> Project:
        start_date = datetime.fromisoformat(row['start_date']) if row['start_date'] else None
        end_date = datetime.fromisoformat(row['end_date']) if row['end_date'] else None
        project = Project(row['name'], row['description'], start_date, end_date)
        project.id = row['id']
        project.status = row['status']
        return project

    def _row_to_user(self, row) -> User:
        user = User(row['username'], row['email'], row['role'])
        user.id = row['id']
        if row['registration_date']:
            user.registration_date = datetime.fromisoformat(row['registration_date'])
        return user