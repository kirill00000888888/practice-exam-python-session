from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController
from views.main_window import MainWindow
import os

def main():
    # Database path relative to main.py
    db_path = os.path.join(os.path.dirname(__file__), "database", "tasks.db")
    db = DatabaseManager(db_path)
    
    # Create tables
    db.create_user_table()
    db.create_project_table()
    db.create_task_table()

    # Initialize Controllers
    task_ctrl = TaskController(db)
    proj_ctrl = ProjectController(db)
    user_ctrl = UserController(db)

    # Launch GUI
    app = MainWindow(task_ctrl, proj_ctrl, user_ctrl)
    app.run()
    
    # Cleanup on exit
    db.close()

if __name__ == "__main__":
    main()
