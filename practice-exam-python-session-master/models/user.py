from datetime import datetime
import re

class User:
    def __init__(self, username, email, role) -> None:
        if role not in {"admin", "manager", "developer"}:
            raise ValueError(f"Invalid role: {role}")
        self.id = None
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        # Simple regex for email validation
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def update_info(self, username=None, email=None, role=None) -> None:
        if username:
            self.username = username
        if email:
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format")
            self.email = email
        if role:
            if role not in {"admin", "manager", "developer"}:
                raise ValueError(f"Invalid role: {role}")
            self.role = role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None
        }