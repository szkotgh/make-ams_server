import db
import db.user

def get_info(session_id):
    try:
        conn = db.get_connection()
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