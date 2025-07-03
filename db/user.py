import hashlib
import os
from db import get_db_connection

def create_user(user_id, password, user_name, group_id, join_year):
    salt = os.urandom(8).hex()
    hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()
    conn = get_db_connection()
    with conn:
        conn.execute(
            'INSERT INTO users (user_id, user_pw, user_pw_salt, user_name, group_id, join_year) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, hashed_pw, salt, user_name, group_id, join_year)
        )
    conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def verify_user(user_id, password):
    user = get_user_by_id(user_id)
    if not user:
        return False
    salt = user['user_pw_salt']
    hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_pw == user['user_pw'] 