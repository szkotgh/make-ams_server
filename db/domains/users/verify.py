import db

PENDING = "pending"
VERIFIED = "verified"
REJECTED = "rejected"
BLOCKED = "blocked"

def get_info(user_uuid) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_verify WHERE user_uuid = ?', (user_uuid,))
            user_verify = cursor.fetchone()
            if not user_verify:
                return db.DBResultDTO(success=False, detail="인증 정보를 찾을 수 없습니다.")
            return db.DBResultDTO(success=True, detail="인증 정보를 찾았습니다.", data=dict(user_verify))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def create(user_uuid) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_verify (user_uuid, status) VALUES (?, ?)', (user_uuid, PENDING))
            return db.DBResultDTO(success=True, detail="인증 요청되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def verify(user_uuid) -> db.DBResultDTO:
    try:
        info = get_info(user_uuid)
        if not info.success:
            return info
        if info.data['status'] == VERIFIED:
            return db.DBResultDTO(success=False, detail="이미 인증된 사용자입니다.")
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user_verify SET status = ? WHERE user_uuid = ?', (VERIFIED, user_uuid))
            return db.DBResultDTO(success=True, detail="인증 처리되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def reject(user_uuid, reason) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user_verify SET status = ?, reason = ? WHERE user_uuid = ?', (REJECTED, reason, user_uuid))
            return db.DBResultDTO(success=True, detail="반려 처리되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def block(user_uuid, reason) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user_verify SET status = ?, reason = ? WHERE user_uuid = ?', (BLOCKED, reason, user_uuid))
            return db.DBResultDTO(success=True, detail="차단 처리되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


