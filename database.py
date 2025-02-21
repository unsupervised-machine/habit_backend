import sqlite3
import os

DATABASE = "reminders.db"

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # -------------------------
        # Users and Reminders Tables
        # -------------------------
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                due_date TEXT NOT NULL,
                completed BOOLEAN NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Big Tasks and Sub Tasks Tables (with user_id)
        # -------------------------
        c.execute('''
            CREATE TABLE big_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completion_mode TEXT NOT NULL,  -- Values: ALL, ANY, or PARTIAL
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        c.execute('''
            CREATE TABLE sub_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                big_task_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                completion_mode TEXT NOT NULL,  -- Values: FULL or PARTIAL
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (big_task_id) REFERENCES big_tasks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Daily Status Tables (with user_id)
        # -------------------------
        c.execute('''
            CREATE TABLE daily_big_task_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                big_task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                completion_value TEXT NOT NULL,  -- e.g., "True", "False", or "Partial"
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (big_task_id) REFERENCES big_tasks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        c.execute('''
            CREATE TABLE daily_sub_task_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sub_task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                completion_value TEXT NOT NULL,  -- e.g., "True", "False", or "Partial"
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Attribute Tables (with user_id)
        # -------------------------
        c.execute('''
            CREATE TABLE big_task_attributes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                big_task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                attribute_key TEXT NOT NULL,   -- e.g., "Book Name"
                attribute_value TEXT NOT NULL, -- e.g., "The Great Gatsby"
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (big_task_id) REFERENCES big_tasks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        c.execute('''
            CREATE TABLE sub_task_attributes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sub_task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                attribute_key TEXT NOT NULL,   -- e.g., "pages"
                attribute_value TEXT NOT NULL, -- e.g., "5"
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Insert Sample Data
        # -------------------------
        # Users
        c.execute('''
            INSERT INTO users (username, email, hashed_password) VALUES
            ('johndoe', 'johndoe@example.com', 'hashedpassword1'),
            ('janedoe', 'janedoe@example.com', 'hashedpassword2')
        ''')

        # Reminders
        c.execute('''
            INSERT INTO reminders (text, due_date, completed, user_id) VALUES
            ('Buy groceries', '2025-02-11 12:00:00', 0, 1),
            ('Call mom', '2025-02-11 18:00:00', 0, 2)
        ''')

        # Big Tasks (assigning tasks to users)
        c.execute('''
            INSERT INTO big_tasks (title, description, completion_mode, user_id) VALUES
            ('Reading', 'Read a book for personal growth.', 'ALL', 1),
            ('Workout', 'Complete daily exercise routine.', 'ALL', 2)
        ''')

        # Sub Tasks (ensuring the user_id matches the big task's user)
        c.execute('''
            INSERT INTO sub_tasks (big_task_id, title, description, completion_mode, user_id) VALUES
            (1, 'Read Chapter 1', 'Read the first chapter of the book.', 'FULL', 1),
            (1, 'Read Chapter 2', 'Read the second chapter of the book.', 'PARTIAL', 1),
            (2, 'Warm-up', 'Complete a 5-minute warm-up routine.', 'FULL', 2),
            (2, 'Main Workout', 'Complete the main workout session.', 'FULL', 2)
        ''')

        # Daily Big Task Status
        c.execute('''
            INSERT INTO daily_big_task_status (big_task_id, user_id, date, completion_value) VALUES
            (1, 1, '2025-02-10', 'Partial'),
            (2, 2, '2025-02-10', 'True')
        ''')

        # Daily Sub Task Status
        c.execute('''
            INSERT INTO daily_sub_task_status (sub_task_id, user_id, date, completion_value) VALUES
            (1, 1, '2025-02-10', 'True'),
            (2, 1, '2025-02-10', 'False'),
            (3, 2, '2025-02-10', 'True'),
            (4, 2, '2025-02-10', 'False')
        ''')

        # Big Task Attributes
        c.execute('''
            INSERT INTO big_task_attributes (big_task_id, user_id, attribute_key, attribute_value) VALUES
            (1, 1, 'Book Name', 'The Great Gatsby')
        ''')

        # Sub Task Attributes
        c.execute('''
            INSERT INTO sub_task_attributes (sub_task_id, user_id, attribute_key, attribute_value) VALUES
            (1, 1, 'pages', '5'),
            (2, 1, 'pages', '10')
        ''')

        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
