import db

def is_admin(user_uuid) -> db.DBResultDTO:
    user_info = db.user.get_info(user_uuid)
    if not user_info.success:
        return user_info

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_admin WHERE user_uuid = ?', (user_uuid,))
            user_data = cursor.fetchone()
            if not user_data:
                return db.DBResultDTO(success=False, detail="User not found")

            return db.DBResultDTO(success=True, detail="User is admin")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def register(user_uuid) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_admin (user_uuid) VALUES (?)', (user_uuid,))
            return db.DBResultDTO(success=True, detail="Admin registered successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


