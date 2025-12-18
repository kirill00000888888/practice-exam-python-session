from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "pending"
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        allowed_statuses = {"pending", "in_progress", "completed"}
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {allowed_statuses}")
        self.status = new_status
        return True

    def is_overdue(self) -> bool:
        if self.status == "completed":
            return False
        return self.due_date < datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project_id": self.project_id,
            "assignee_id": self.assignee_id
        }