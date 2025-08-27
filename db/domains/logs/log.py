import db

def insert_access_log(user_uuid=None, method=None, success=None, reason=None, **kwargs) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO log_access (user_uuid, method, success, reason) VALUES (?, ?, ?, ?)",
                (user_uuid, method, success, reason)
            )
            return db.DBResultDTO(success=True, detail="logged")
    except Exception as e:
        try:
            with db.connect() as fail_conn:
                fail_cursor = fail_conn.cursor()
                fail_cursor.execute("""
                    INSERT INTO log_access_fail (user_uuid, method, reason, original_success)
                    VALUES (?, ?, ?, ?)
                """, (user_uuid, method, str(e), int(success) if success is not None else None))
        except Exception as e2:
            return db.DBResultDTO(success=False, detail=str(e2))
        return db.DBResultDTO(success=False, detail=str(e))


def insert_status_log(user_uuid, change_status) -> db.DBResultDTO:
    try:
        with db.connect() as log_conn:
            cursor = log_conn.cursor()
            cursor.execute(
                "INSERT INTO log_status (user_uuid, change_status) VALUES (?, ?)",
                (user_uuid, change_status)
            )
            return db.DBResultDTO(success=True, detail="status logged")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


