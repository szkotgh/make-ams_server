import db
from flask import session
import schedule
import time
import threading


def get_status() -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT auth_code, button, nfc, status, remote_change_by_uuid, created_at
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
                "remote_change_by_uuid": row[4],
                "created_at": row[5]
            })
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def update_door_status(user_uuid, updates) -> db.DBResultDTO:
    if not user_uuid:
        return db.DBResultDTO(success=False, detail="User UUID is required")

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT auth_code, button, nfc, status, remote_change_by_uuid, created_at
                FROM door_status
                ORDER BY created_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()

            if not row:
                return db.DBResultDTO(success=False, detail="No previous status row")

            # row에서 직전 상태 불러오기
            new_row = {
                "auth_code": updates.get("auth_code", row[0]),
                "button": updates.get("button", row[1]),
                "nfc": updates.get("nfc", row[2]),
                "status": updates.get("status", row[3]),
                "remote_change_by_uuid": user_uuid  # 항상 현재 요청자의 UUID로 기록
            }

            cursor.execute("""
                INSERT INTO door_status (auth_code, button, nfc, status, remote_change_by_uuid)
                VALUES (?, ?, ?, ?, ?)
            """, (
                new_row["auth_code"],
                new_row["button"],
                new_row["nfc"],
                new_row["status"],
                new_row["remote_change_by_uuid"]
            ))

            return db.DBResultDTO(success=True, detail="Door status updated")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))

def remote_open(user_uuid) -> db.DBResultDTO:
    if not user_uuid:
        return db.DBResultDTO(success=False, detail="User UUID is required")

    try:
        with db.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO door_remote (remote_open_by_uuid, remote_open_used)
                VALUES (?, ?)
            """, (user_uuid, False))

            return db.DBResultDTO(success=True, detail="Remote open recorded")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))

def get_remote_status() -> db.DBResultDTO:
    """
    최신 원격 열기 상태 반환
    DB에는 UUID 기록, 이름까지 포함해서 반환
    """
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT remote_open_by_uuid, remote_open_used, created_at
                FROM door_remote
                ORDER BY created_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()

            if not row:
                return db.DBResultDTO(success=True, detail="No remote open", data=None)

            enabled = not bool(row[1])

            if not row[1]:
                cursor.execute("""
                    UPDATE door_remote
                    SET remote_open_used = 1
                    WHERE created_at = ?
                """, (row[2],))
                conn.commit()

            # UUID → 이름 조회 (users 테이블)
            cursor.execute("SELECT * FROM users WHERE uuid = ?", (row[0],))
            user_row = cursor.fetchone()
            name = user_row[4] if user_row else "알 수 없음"

            return db.DBResultDTO(success=True, detail="Success", data={
                "remote_open_by_uuid": row[0],
                "remote_open_by_name": name,
                "remote_open_enabled": enabled,
                "created_at": row[2]
            })
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    
def current_user_uuid():
    user_info = session.get('user_info')
    if user_info and 'uuid' in user_info:
        return user_info['uuid']
    return None

def time_midnight():
    """매일 밤 12시에 잠금 상태로 변경"""
    update_door_status("system", {
        "status": "close",
        "auth_code": False,
        "button": False,
        "nfc": False
    })

def time_7am():
    try:
        result = update_door_status("system", {
            "status": "restrict",
            "auth_code": True,
            "button": False,
            "nfc": True
        })
        print("[Scheduler] time_7am 실행됨:", result.detail)
    except Exception as e:
        print(f"[Scheduler] time_7am 예외 발생: {e}")


def time_mon_wed():
    """월~수 오후 3시 30분 오픈 상태 (버튼 포함)"""
    update_door_status("system", {
        "status": "open",
        "auth_code": True,
        "button": True,  
        "nfc": True
    })

def time_thu_fri():
    """목~금 오후 4시 40분 오픈 상태 (버튼 포함)"""
    update_door_status("system", {
        "status": "open",
        "auth_code": True,
        "button": True,
        "nfc": True
    })

def run_schedule():
    """스케줄러 실행 (별도 쓰레드에서 동작)"""
    schedule.every().day.at("00:00").do(time_midnight)
    schedule.every().day.at("07:00").do(time_7am)

    schedule.every().monday.at("15:30").do(time_mon_wed)
    schedule.every().tuesday.at("15:30").do(time_mon_wed)
    schedule.every().wednesday.at("15:30").do(time_mon_wed)

    schedule.every().thursday.at("16:40").do(time_thu_fri)
    schedule.every().friday.at("16:40").do(time_thu_fri)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    t = threading.Thread(target=run_schedule, daemon=True)
    t.start()