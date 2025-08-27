import db

def get_status() -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT auth_code, button, nfc, status, remote_open, remote_open_by_uuid, created_at
                FROM door_status
                ORDER BY created_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if not row:
                return db.DBResultDTO(success=True, detail="No status", data=None)
            return db.DBResultDTO(success=True, detail="Success", data={
                "auth_code": bool(row[0]),
                "button": bool(row[1]),
                "nfc": bool(row[2]),
                "status": row[3],
                "remote_open": bool(row[4]),
                "remote_open_by_uuid": row[5],
                "created_at": row[6]
            })
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def update_status(user_uuid, updates) -> db.DBResultDTO:
    if not updates:
        return db.DBResultDTO(success=False, detail="No updates provided")
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT auth_code, button, nfc, status, remote_open, remote_open_by_uuid
                FROM door_status
                ORDER BY created_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if not row:
                return db.DBResultDTO(success=False, detail="No previous status row")
            new_row = {
                "auth_code": updates.get("auth_code", row[0]),
                "button": updates.get("button", row[1]),
                "nfc": updates.get("nfc", row[2]),
                "status": updates.get("status", row[3]),
                "remote_open": updates.get("remote_open", row[4]),
                "remote_open_by_uuid": updates.get("remote_open_by_uuid", row[5])
            }
            cursor.execute("""
                INSERT INTO door_status (auth_code, button, nfc, status, remote_open, remote_open_by_uuid)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                new_row["auth_code"], new_row["button"], new_row["nfc"], new_row["status"], new_row["remote_open"], new_row["remote_open_by_uuid"]
            ))
            return db.DBResultDTO(success=True, detail="Door status updated")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


