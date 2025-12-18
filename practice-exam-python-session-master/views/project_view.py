```python
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ProjectView(ttk.Frame):
    def __init__(self, parent, controller, task_controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.task_controller = task_controller
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        # Form
        form_frame = ttk.LabelFrame(self, text="Add Project")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date (ISO):").grid(row=1, column=0, padx=5, pady=5)
        self.start_entry = ttk.Entry(form_frame)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_entry.insert(0, datetime.now().isoformat())

        ttk.Label(form_frame, text="End Date (ISO):").grid(row=1, column=2, padx=5, pady=5)
        self.end_entry = ttk.Entry(form_frame)
        self.end_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form_frame, text="Add Project", command=self.add_project).grid(row=2, column=0, columnspan=4, pady=10)

        # Actions
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(action_frame, text="Show Project Tasks", command=self.show_project_tasks).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_projects).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Calculate Progress", command=self.show_progress).pack(side="left", padx=5)

        # Table
        columns = ("id", "name", "status", "start_date", "end_date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_project(self) -> None:
        try:
            name = self.name_entry.get()
            desc = self.desc_entry.get()
            start = datetime.fromisoformat(self.start_entry.get())
            end_val = self.end_entry.get()
            end = datetime.fromisoformat(end_val) if end_val else None
            
            self.controller.add_project(name, desc, start, end)
            self.refresh_projects()
            messagebox.showinfo("Success", "Project added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add project: {e}")

    def refresh_projects(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        projects = self.controller.get_all_projects()
        for p in projects:
            self.tree.insert("", "end", values=(p.id, p.name, p.status, p.start_date, p.end_date))

    def show_project_tasks(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a project first")
            return
        item = selected[0]
        project_id = self.tree.item(item)['values'][0]
        
        tasks = self.task_controller.get_tasks_by_project(project_id)
        
        popup = tk.Toplevel(self)
        popup.title(f"Tasks for Project {project_id}")
        
        columns = ("id", "title", "status")
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.pack(fill="both", expand=True)
        
        for t in tasks:
            tree.insert("", "end", values=(t.id, t.title, t.status))

    def show_progress(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        project_id = self.tree.item(item)['values'][0]
        try:
            progress = self.controller.get_project_progress(project_id)
            messagebox.showinfo("Progress", f"Project Progress: {progress*100:.1f}%")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calc progress: {e}")
```