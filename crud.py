import uuid
from datetime import datetime
from database import get_db_connection

# -------------------------
# Users CRUD Functions
# -------------------------
def create_user(email, password_hash, notifications_enabled=1, stripe_customer_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    cur.execute('''
        INSERT INTO users (id, email, name,password_hash, notifications_enabled, stripe_customer_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, email, password_hash, notifications_enabled, stripe_customer_id, timestamp, timestamp))
    conn.commit()
    conn.close()
    return user_id

def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cur.fetchone()
    conn.close()
    return user

def update_user(user_id, email=None, password_hash=None, notifications_enabled=None, stripe_customer_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    # Get the existing user record
    user = get_user_by_id(user_id)
    if not user:
        conn.close()
        return None
    new_email = email if email is not None else user["email"]
    new_password_hash = password_hash if password_hash is not None else user["password_hash"]
    new_notifications_enabled = notifications_enabled if notifications_enabled is not None else user["notifications_enabled"]
    new_stripe_customer_id = stripe_customer_id if stripe_customer_id is not None else user["stripe_customer_id"]

    cur.execute('''
        UPDATE users
        SET email = ?, password_hash = ?, notifications_enabled = ?, stripe_customer_id = ?, updated_at = ?
        WHERE id = ?
    ''', (new_email, new_password_hash, new_notifications_enabled, new_stripe_customer_id, timestamp, user_id))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id)

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True

# -------------------------
# Payments CRUD Functions
# -------------------------
def create_payment(user_id, stripe_charge_id, amount, currency, payment_status):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    cur.execute('''
        INSERT INTO payments (user_id, stripe_charge_id, amount, currency, payment_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, stripe_charge_id, amount, currency, payment_status, timestamp, timestamp))
    conn.commit()
    payment_id = cur.lastrowid
    conn.close()
    return payment_id

def get_payment_by_id(payment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
    payment = cur.fetchone()
    conn.close()
    return payment

def update_payment(payment_id, stripe_charge_id=None, amount=None, currency=None, payment_status=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    payment = get_payment_by_id(payment_id)
    if not payment:
        conn.close()
        return None
    new_stripe_charge_id = stripe_charge_id if stripe_charge_id is not None else payment["stripe_charge_id"]
    new_amount = amount if amount is not None else payment["amount"]
    new_currency = currency if currency is not None else payment["currency"]
    new_payment_status = payment_status if payment_status is not None else payment["payment_status"]

    cur.execute('''
        UPDATE payments
        SET stripe_charge_id = ?, amount = ?, currency = ?, payment_status = ?, updated_at = ?
        WHERE id = ?
    ''', (new_stripe_charge_id, new_amount, new_currency, new_payment_status, timestamp, payment_id))
    conn.commit()
    conn.close()
    return get_payment_by_id(payment_id)

def delete_payment(payment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM payments WHERE id = ?', (payment_id,))
    conn.commit()
    conn.close()
    return True

# -------------------------
# Habits CRUD Functions
# -------------------------
def create_habit(user_id, name, description=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    cur.execute('''
        INSERT INTO habits (user_id, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, name, description, timestamp, timestamp))
    conn.commit()
    habit_id = cur.lastrowid
    conn.close()
    return habit_id

def get_habit_by_id(habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
    habit = cur.fetchone()
    conn.close()
    return habit

def update_habit(habit_id, name=None, description=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    habit = get_habit_by_id(habit_id)
    if not habit:
        conn.close()
        return None
    new_name = name if name is not None else habit["name"]
    new_description = description if description is not None else habit["description"]

    cur.execute('''
        UPDATE habits
        SET name = ?, description = ?, updated_at = ?
        WHERE id = ?
    ''', (new_name, new_description, timestamp, habit_id))
    conn.commit()
    conn.close()
    return get_habit_by_id(habit_id)

def delete_habit(habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()
    return True

# -------------------------
# Sub-Habits CRUD Functions
# -------------------------
def create_sub_habit(habit_id, name, description=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    cur.execute('''
        INSERT INTO sub_habits (habit_id, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (habit_id, name, description, timestamp, timestamp))
    conn.commit()
    sub_habit_id = cur.lastrowid
    conn.close()
    return sub_habit_id

def get_sub_habit_by_id(sub_habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sub_habits WHERE id = ?', (sub_habit_id,))
    sub_habit = cur.fetchone()
    conn.close()
    return sub_habit

def update_sub_habit(sub_habit_id, name=None, description=None):
    conn = get_db_connection()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    sub_habit = get_sub_habit_by_id(sub_habit_id)
    if not sub_habit:
        conn.close()
        return None
    new_name = name if name is not None else sub_habit["name"]
    new_description = description if description is not None else sub_habit["description"]

    cur.execute('''
        UPDATE sub_habits
        SET name = ?, description = ?, updated_at = ?
        WHERE id = ?
    ''', (new_name, new_description, timestamp, sub_habit_id))
    conn.commit()
    conn.close()
    return get_sub_habit_by_id(sub_habit_id)

def delete_sub_habit(sub_habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM sub_habits WHERE id = ?', (sub_habit_id,))
    conn.commit()
    conn.close()
    return True

# -------------------------
# Habit Completions CRUD Functions
# -------------------------
def create_habit_completion(user_id, habit_id, date_str, completed):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO habit_completions (user_id, habit_id, date, completed)
        VALUES (?, ?, ?, ?)
    ''', (user_id, habit_id, date_str, 1 if completed else 0))
    conn.commit()
    completion_id = cur.lastrowid
    conn.close()
    return completion_id

def get_habit_completion_by_id(completion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit_completions WHERE id = ?', (completion_id,))
    record = cur.fetchone()
    conn.close()
    return record

def update_habit_completion(completion_id, completed):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE habit_completions
        SET completed = ?
        WHERE id = ?
    ''', (1 if completed else 0, completion_id))
    conn.commit()
    conn.close()
    return get_habit_completion_by_id(completion_id)

def delete_habit_completion(completion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habit_completions WHERE id = ?', (completion_id,))
    conn.commit()
    conn.close()
    return True

# -------------------------
# Sub-Habit Completions CRUD Functions
# -------------------------
def create_sub_habit_completion(sub_habit_id, date_str, completed, user_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO sub_habit_completions (sub_habit_id, date, completed, user_id)
        VALUES (?, ?, ?, ?)
    ''', (sub_habit_id, date_str, 1 if completed else 0, user_id))
    conn.commit()
    completion_id = cur.lastrowid
    conn.close()
    return completion_id

def get_sub_habit_completion_by_id(completion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sub_habit_completions WHERE id = ?', (completion_id,))
    record = cur.fetchone()
    conn.close()
    return record

def update_sub_habit_completion(completion_id, completed):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE sub_habit_completions
        SET completed = ?
        WHERE id = ?
    ''', (1 if completed else 0, completion_id))
    conn.commit()
    conn.close()
    return get_sub_habit_completion_by_id(completion_id)

def delete_sub_habit_completion(completion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM sub_habit_completions WHERE id = ?', (completion_id,))
    conn.commit()
    conn.close()
    return True
