import db
from log import insert_status_log

def get_status() -> dict:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT auth_code, button, nfc, status, remote_open, remote_open_by_uuid, created_at
            FROM door_status
        """)
        row = cursor.fetchone()
        if not row:
            return {}
        return {
            "auth_code": bool(row[0]),
            "button": bool(row[1]),
            "nfc": bool(row[2]),
            "status": row[3],
            "remote_open": bool(row[4]),
            "remote_open_by_uuid": row[5],
            "created_at": row[6]
        }
    finally:
        db.close_connection(conn)


def update_status(user_uuid, change_status):
    if not updates:
        return False

    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        # 가장 최근 상태 가져오기
        cursor.execute("""
            SELECT auth_code, button, nfc, status, remote_open, remote_open_by_uuid
            FROM door_status
            ORDER BY created_at DESC
        """)
        row = cursor.fetchone()
        if not row:
            # 행이 반드시 존재한다고 가정하므로 여기서는 False 반환
            return False

        # 이전 값 기반으로 새 행 생성, 전달된 값만 덮어쓰기
        new_row = {
            "auth_code": updates.get("auth_code", row[0]),
            "button": updates.get("button", row[1]),
            "nfc": updates.get("nfc", row[2]),
            "status": updates.get("status", row[3]),
            "remote_open": updates.get("remote_open", row[4]),
            "remote_open_by_uuid": updates.get("remote_open_by_uuid", row[5])
        }

        # 새 행 삽입
        cursor.execute("""
            INSERT INTO door_status (auth_code, button, nfc, status, remote_open, remote_open_by_uuid)
            VALUES (?, ?, ?, ?, ?, ?)
        """, tuple(new_row[col] for col in ["auth_code", "button", "nfc", "status", "remote_open", "remote_open_by_uuid"]))
        conn.commit()

        return True

    finally:
        db.close_connection(conn)