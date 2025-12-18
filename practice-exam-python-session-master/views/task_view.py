import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskView(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        # Form Frame
        form_frame = ttk.LabelFrame(self, text="Add Task")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Priority (1-3):").grid(row=1, column=0, padx=5, pady=5)
        self.prio_entry = ttk.Entry(form_frame)
        self.prio_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Due Date (ISO):").grid(row=1, column=2, padx=5, pady=5)
        self.due_entry = ttk.Entry(form_frame)
        self.due_entry.grid(row=1, column=3, padx=5, pady=5)
        self.due_entry.insert(0, datetime.now().isoformat())

        ttk.Label(form_frame, text="Project ID:").grid(row=2, column=0, padx=5, pady=5)
        self.pid_entry = ttk.Entry(form_frame)
        self.pid_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Assignee ID:").grid(row=2, column=2, padx=5, pady=5)
        self.uid_entry = ttk.Entry(form_frame)
        self.uid_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Button(form_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=4, pady=10)

        # Search Frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_tasks).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Refresh", command=self.refresh_tasks).pack(side="left", padx=5)

        # Table
        columns = ("id", "title", "priority", "status", "due_date", "project_id", "assignee_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Context Menu for Status Update / Delete
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_command(label="Mark In Progress", command=lambda: self.update_status("in_progress"))
        self.context_menu.add_command(label="Mark Completed", command=lambda: self.update_status("completed"))

    def add_task(self) -> None:
        try:
            title = self.title_entry.get()
            desc = self.desc_entry.get()
            prio = int(self.prio_entry.get())
            due_date = datetime.fromisoformat(self.due_entry.get())
            pid = int(self.pid_entry.get())
            uid = int(self.uid_entry.get())
            
            self.controller.add_task(title, desc, prio, due_date, pid, uid)
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}")

    def refresh_tasks(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.controller.get_all_tasks()
        for t in tasks:
            self.tree.insert("", "end", values=(t.id, t.title, t.priority, t.status, t.due_date, t.project_id, t.assignee_id))

    def search_tasks(self) -> None:
        query = self.search_entry.get()
        tasks = self.controller.search_tasks(query)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for t in tasks:
            self.tree.insert("", "end", values=(t.id, t.title, t.priority, t.status, t.due_date, t.project_id, t.assignee_id))

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        task_id = self.tree.item(item)['values'][0]
        try:
            self.controller.delete_task(task_id)
            self.refresh_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

    def update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        task_id = self.tree.item(item)['values'][0]
        try:
            self.controller.update_task_status(task_id, status)
            self.refresh_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")