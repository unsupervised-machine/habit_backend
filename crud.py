from database import get_db_connection

# User CRUD
def create_user(username: str, email: str, hashed_password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()

def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_username(username: str):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    return user

def get_user_by_email(email: str):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()
    return user

def update_user(user_id: int, username: str = None, email: str = None, hashed_password: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if username is not None:
        fields.append("username = ?")
        values.append(username)
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if hashed_password is not None:
        fields.append("hashed_password = ?")
        values.append(hashed_password)
    values.append(user_id)
    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Reminders CRUD
# ----------------------------
def create_reminder(text: str, due_date: str, completed: bool, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (text, due_date, completed, user_id) VALUES (?, ?, ?, ?)",
        (text, due_date, completed, user_id)
    )
    conn.commit()
    conn.close()

def get_reminder_by_id(reminder_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders WHERE id = ?", (reminder_id,))
    reminder = cursor.fetchone()
    conn.close()
    return reminder

def get_reminders_by_user(user_id: int):
    conn = get_db_connection()
    reminders = conn.execute(
        "SELECT * FROM reminders WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return reminders

def update_reminder(reminder_id: int, text: str = None, due_date: str = None, completed: bool = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if text is not None:
        fields.append("text = ?")
        values.append(text)
    if due_date is not None:
        fields.append("due_date = ?")
        values.append(due_date)
    if completed is not None:
        fields.append("completed = ?")
        values.append(completed)
    values.append(reminder_id)
    cursor.execute(f"UPDATE reminders SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_reminder(reminder_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()

# ----------------------------
# Big Tasks CRUD
# ----------------------------
def create_big_task(title: str, description: str, completion_mode: str, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO big_tasks (title, description, completion_mode, user_id) VALUES (?, ?, ?, ?)",
        (title, description, completion_mode, user_id)
    )
    conn.commit()
    conn.close()

def get_big_task_by_id(big_task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM big_tasks WHERE id = ?", (big_task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_big_task(big_task_id: int, title: str = None, description: str = None, completion_mode: str = None, user_id: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if completion_mode is not None:
        fields.append("completion_mode = ?")
        values.append(completion_mode)
    if user_id is not None:
        fields.append("user_id = ?")
        values.append(user_id)
    values.append(big_task_id)
    cursor.execute(f"UPDATE big_tasks SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_big_task(big_task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM big_tasks WHERE id = ?", (big_task_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Sub Tasks CRUD
# ----------------------------
def create_sub_task(big_task_id: int, title: str, description: str, completion_mode: str, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sub_tasks (big_task_id, title, description, completion_mode, user_id) VALUES (?, ?, ?, ?, ?)",
        (big_task_id, title, description, completion_mode, user_id)
    )
    conn.commit()
    conn.close()

def get_sub_task_by_id(sub_task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sub_tasks WHERE id = ?", (sub_task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_sub_task(sub_task_id: int, title: str = None, description: str = None, completion_mode: str = None, user_id: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if completion_mode is not None:
        fields.append("completion_mode = ?")
        values.append(completion_mode)
    if user_id is not None:
        fields.append("user_id = ?")
        values.append(user_id)
    values.append(sub_task_id)
    cursor.execute(f"UPDATE sub_tasks SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_sub_task(sub_task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sub_tasks WHERE id = ?", (sub_task_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Daily Big Task Status CRUD
# ----------------------------
def create_daily_big_task_status(big_task_id: int, user_id: int, date: str, completion_value: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO daily_big_task_status (big_task_id, user_id, date, completion_value) VALUES (?, ?, ?, ?)",
        (big_task_id, user_id, date, completion_value)
    )
    conn.commit()
    conn.close()

def get_daily_big_task_status_by_id(status_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_big_task_status WHERE id = ?", (status_id,))
    status = cursor.fetchone()
    conn.close()
    return status

def update_daily_big_task_status(status_id: int, completion_value: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if completion_value is not None:
        cursor.execute(
            "UPDATE daily_big_task_status SET completion_value = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (completion_value, status_id)
        )
    conn.commit()
    conn.close()

def delete_daily_big_task_status(status_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_big_task_status WHERE id = ?", (status_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Daily Sub Task Status CRUD
# ----------------------------
def create_daily_sub_task_status(sub_task_id: int, user_id: int, date: str, completion_value: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO daily_sub_task_status (sub_task_id, user_id, date, completion_value) VALUES (?, ?, ?, ?)",
        (sub_task_id, user_id, date, completion_value)
    )
    conn.commit()
    conn.close()

def get_daily_sub_task_status_by_id(status_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_sub_task_status WHERE id = ?", (status_id,))
    status = cursor.fetchone()
    conn.close()
    return status

def update_daily_sub_task_status(status_id: int, completion_value: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if completion_value is not None:
        cursor.execute(
            "UPDATE daily_sub_task_status SET completion_value = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (completion_value, status_id)
        )
    conn.commit()
    conn.close()

def delete_daily_sub_task_status(status_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_sub_task_status WHERE id = ?", (status_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Big Task Attributes CRUD
# ----------------------------
def create_big_task_attribute(big_task_id: int, user_id: int, attribute_key: str, attribute_value: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO big_task_attributes (big_task_id, user_id, attribute_key, attribute_value) VALUES (?, ?, ?, ?)",
        (big_task_id, user_id, attribute_key, attribute_value)
    )
    conn.commit()
    conn.close()

def get_big_task_attribute_by_id(attribute_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM big_task_attributes WHERE id = ?", (attribute_id,))
    attribute = cursor.fetchone()
    conn.close()
    return attribute

def update_big_task_attribute(attribute_id: int, attribute_key: str = None, attribute_value: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if attribute_key is not None:
        fields.append("attribute_key = ?")
        values.append(attribute_key)
    if attribute_value is not None:
        fields.append("attribute_value = ?")
        values.append(attribute_value)
    values.append(attribute_id)
    cursor.execute(f"UPDATE big_task_attributes SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_big_task_attribute(attribute_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM big_task_attributes WHERE id = ?", (attribute_id,))
    conn.commit()
    conn.close()


# ----------------------------
# Sub Task Attributes CRUD
# ----------------------------
def create_sub_task_attribute(sub_task_id: int, user_id: int, attribute_key: str, attribute_value: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sub_task_attributes (sub_task_id, user_id, attribute_key, attribute_value) VALUES (?, ?, ?, ?)",
        (sub_task_id, user_id, attribute_key, attribute_value)
    )
    conn.commit()
    conn.close()

def get_sub_task_attribute_by_id(attribute_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sub_task_attributes WHERE id = ?", (attribute_id,))
    attribute = cursor.fetchone()
    conn.close()
    return attribute

def update_sub_task_attribute(attribute_id: int, attribute_key: str = None, attribute_value: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if attribute_key is not None:
        fields.append("attribute_key = ?")
        values.append(attribute_key)
    if attribute_value is not None:
        fields.append("attribute_value = ?")
        values.append(attribute_value)
    values.append(attribute_id)
    cursor.execute(f"UPDATE sub_task_attributes SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_sub_task_attribute(attribute_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sub_task_attributes WHERE id = ?", (attribute_id,))
    conn.commit()
    conn.close()