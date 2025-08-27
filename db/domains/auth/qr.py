import db
from db.domains.logs.log import insert_access_log
import modules.utils as utils

def generate_qr(user_uuid: str) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT created_at FROM auth_qr
                WHERE user_uuid = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (user_uuid,))
            last_qr = cursor.fetchone()
        if last_qr is not None and not utils.is_minutes_passed(last_qr['created_at'], 1):
            return db.DBResultDTO(success=False, detail="잠시 후 다시 시도하세요.")
        token = utils.generate_hash(16)
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO auth_qr (user_uuid, auth_code)
                VALUES (?, ?)
            """, (user_uuid, token))
        return db.DBResultDTO(success=True, detail="QR 코드 생성 완료", data={"value": token})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def verify_qr(qr_code: str) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM auth_qr WHERE auth_code = ?
            """, (qr_code,))
            qr_data = cursor.fetchone()
            if not qr_data:
                insert_access_log(user_uuid=None, method="QR", success=False, reason="존재하지 않는 QR 코드")
                return db.DBResultDTO(success=False, detail="존재하지 않는 QR 코드")
            qr_id = qr_data['id']
            qr_user_uuid = qr_data['user_uuid']
            use_count = qr_data['use_count']
            if utils.is_minutes_passed(qr_data['created_at'], 1):
                insert_access_log(user_uuid=qr_user_uuid, method="QR", success=False, reason="만료된 QR 코드")
                return db.DBResultDTO(success=False, detail="만료된 QR 코드")
            cursor.execute("UPDATE auth_qr SET use_count = ? WHERE id = ?", (use_count+1, qr_id,))
        insert_access_log(user_uuid=qr_user_uuid, method="QR", success=True, reason="QR 인증 성공")
        return db.DBResultDTO(success=True, detail="QR 인증 성공", data={"user_uuid": qr_user_uuid})
    except Exception as e:
        insert_access_log(user_uuid=None, method="QR", success=False, reason=str(e))
        return db.DBResultDTO(success=False, detail=str(e))


