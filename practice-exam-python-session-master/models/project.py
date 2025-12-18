from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"

    def update_status(self, new_status) -> bool:
        allowed_statuses = {"active", "completed", "on_hold"}
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {allowed_statuses}")
        self.status = new_status
        return True

    def get_progress(self) -> float:
        # Progress calculation requires task data which is not available in the model alone.
        # This will be handled by the controller or updated separately.
        return 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status
        }