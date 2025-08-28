import db
import modules.utils as utils

def is_active_session(session_id) -> db.DBResultDTO:
    try:
        session_info = get_info(session_id)
        if not session_info.success:
            return session_info
        if not session_info.data['session_info']['is_active']:
            return db.DBResultDTO(success=False, detail="비활성화된 세션입니다.")
        return db.DBResultDTO(success=True, detail="활성화된 세션입니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def get_info(session_id) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_sessions WHERE id = ?', (session_id,))
            session_data = cursor.fetchone()
            if not session_data:
                return db.DBResultDTO(success=False, detail="올바르지 않은 세션입니다.")
            user_info = db.user.get_info(session_data['user_uuid'])
            if not user_info.success:
                return db.DBResultDTO(success=False, detail=user_info.detail)
            return db.DBResultDTO(success=True, detail="성공적으로 조회했습니다.", data={'session_info': dict(session_data), 'user_info': dict(user_info.data)})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def get_list_info(session_id) -> db.DBResultDTO:
    try:
        session_info = get_info(session_id)
        if not session_info.success:
            return session_info
        user_info = db.user.get_info(session_info.data['session_info']['user_uuid'])
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_sessions WHERE user_uuid = ? AND is_active = True', (user_info.data['uuid'],))
            session_data = cursor.fetchall()
            session_data_list = [dict(row) for row in session_data]
            session_data_list.reverse()
            return db.DBResultDTO(success=True, detail="성공적으로 조회했습니다.", data={'session_list_info': session_data_list})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def create(user_uuid, user_agent) -> db.DBResultDTO:
    session_id = utils.generate_uuid()
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_sessions (id, user_uuid, user_agent) VALUES (?, ?, ?)', (session_id, user_uuid, user_agent))
            return db.DBResultDTO(success=True, detail="세션이 생성되었습니다.", data=session_id)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


