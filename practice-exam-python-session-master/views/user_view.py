import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent, controller, task_controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.task_controller = task_controller
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        # Form
        form_frame = ttk.LabelFrame(self, text="Add User")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.user_entry = ttk.Entry(form_frame)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Role:").grid(row=1, column=0, padx=5, pady=5)
        self.role_combo = ttk.Combobox(form_frame, values=["admin", "manager", "developer"])
        self.role_combo.grid(row=1, column=1, padx=5, pady=5)
        self.role_combo.current(2)

        ttk.Button(form_frame, text="Add User", command=self.add_user).grid(row=2, column=0, columnspan=4, pady=10)

        # Actions
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(action_frame, text="Show User Tasks", command=self.show_user_tasks).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_users).pack(side="left", padx=5)

        # Table
        columns = ("id", "username", "email", "role", "registered")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_user(self) -> None:
        try:
            username = self.user_entry.get()
            email = self.email_entry.get()
            role = self.role_combo.get()
            
            self.controller.add_user(username, email, role)
            self.refresh_users()
            messagebox.showinfo("Success", "User added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

    def refresh_users(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = self.controller.get_all_users()
        for u in users:
            self.tree.insert("", "end", values=(u.id, u.username, u.email, u.role, u.registration_date))

    def show_user_tasks(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a user first")
            return
        item = selected[0]
        user_id = self.tree.item(item)['values'][0]
        
        try:
            tasks = self.task_controller.get_tasks_by_user(user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get tasks: {e}")
            return
        
        popup = tk.Toplevel(self)
        popup.title(f"Tasks for User {user_id}")
        
        columns = ("id", "title", "status")
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.pack(fill="both", expand=True)
        
        for t in tasks:
            tree.insert("", "end", values=(t.id, t.title, t.status))

    def delete_selected(self) -> None:
        pass