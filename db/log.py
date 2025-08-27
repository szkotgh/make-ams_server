import db

def insert_access_log(user_uuid, method, success, reason):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO log_access (user_uuid, method, success, reason) VALUES (?, ?, ?, ?)",
            (user_uuid, method, success, reason)
        )
        conn.commit()
    except Exception as e:
        fail_conn = db.get_connection()
        fail_cursor = fail_conn.cursor()
        fail_cursor.execute("""
            INSERT INTO log_access_fail (user_uuid, method, reason, original_success)
            VALUES (?, ?, ?, ?)
        """, (user_uuid, method, str(e), int(success)))
        fail_conn.commit()
    finally:
        db.close_connection(conn)


def insert_status_log(user_uuid, change_status):
    log_conn = db.get_connection()

    with log_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO log_status (user_uuid, change_status) VALUES (?, ?)",
            (user_uuid, change_status)
        )
    log_conn.commit()