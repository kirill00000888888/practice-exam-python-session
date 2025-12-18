import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView

class MainWindow:
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        self.root = tk.Tk()
        self.root.title("Task Management System")
        self.root.geometry("800x600")

        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Initialize Views
        self.task_view = TaskView(self.notebook, self.task_controller)
        self.project_view = ProjectView(self.notebook, self.project_controller, self.task_controller)
        self.user_view = UserView(self.notebook, self.user_controller, self.task_controller)

        # Add tabs
        self.notebook.add(self.task_view, text="Tasks")
        self.notebook.add(self.project_view, text="Projects")
        self.notebook.add(self.user_view, text="Users")

    def run(self):
        self.root.mainloop()

