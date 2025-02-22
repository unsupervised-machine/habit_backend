import os
import sqlite3
from datetime import datetime

DATABASE = 'database.db'

def init_db():
    # Only initialize if the database file doesn't exist
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # -------------------------
        # Users Table
        # -------------------------
        c.execute('''
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                notifications_enabled INTEGER NOT NULL DEFAULT 1,
                stripe_customer_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        # -------------------------
        # Payments Table
        # -------------------------
        c.execute('''
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                stripe_charge_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                payment_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Habits Table
        # -------------------------
        c.execute('''
            CREATE TABLE habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Sub-Habits Table
        # -------------------------
        c.execute('''
            CREATE TABLE sub_habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')

        # -------------------------
        # Habit Completions Table
        # -------------------------
        c.execute('''
            CREATE TABLE habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                completed INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')

        # -------------------------
        # Sub-Habit Completions Table
        # -------------------------
        c.execute('''
            CREATE TABLE sub_habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sub_habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                completed INTEGER NOT NULL,
                user_id TEXT,
                FOREIGN KEY(sub_habit_id) REFERENCES sub_habits(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # -------------------------
        # Insert Sample Data
        # -------------------------
        # Using a fixed sample timestamp for demonstration
        timestamp = datetime.utcnow().isoformat() + "Z"
        sample_user_id = "123e4567-e89b-12d3-a456-426614174000"

        # Users
        c.execute('''
            INSERT INTO users (id, email, name, password_hash, notifications_enabled, stripe_customer_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sample_user_id, "user@example.com", "John Doe", "hashedpassword", 1, "cus_sample", timestamp, timestamp))

        # Payments
        c.execute('''
            INSERT INTO payments (user_id, stripe_charge_id, amount, currency, payment_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sample_user_id, "ch_sample", 9.99, "USD", "paid", timestamp, timestamp))

        # Habits
        c.execute('''
            INSERT INTO habits (user_id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (sample_user_id, "Drink Water", "Drink 8 glasses of water", timestamp, timestamp))
        habit_id = c.lastrowid

        # Sub-Habits
        c.execute('''
            INSERT INTO sub_habits (habit_id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (habit_id, "Morning Water", "Drink a glass of water in the morning", timestamp, timestamp))
        sub_habit_id = c.lastrowid

        # Habit Completions
        c.execute('''
            INSERT INTO habit_completions (user_id, habit_id, date, completed)
            VALUES (?, ?, ?, ?)
        ''', (sample_user_id, habit_id, "2025-02-21", 1))

        # Sub-Habit Completions
        c.execute('''
            INSERT INTO sub_habit_completions (sub_habit_id, date, completed, user_id)
            VALUES (?, ?, ?, ?)
        ''', (sub_habit_id, "2025-02-21", 1, sample_user_id))

        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
