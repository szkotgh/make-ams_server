import db
import db.user

def is_admin(user_uuid) -> db.DBResultDTO:
    user_info = db.user.get_info(user_uuid)
    if not user_info.success:
        return user_info
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_admin WHERE user_uuid = ?', (user_uuid,))
        user_data = cursor.fetchone()
        if not user_data:
            return db.DBResultDTO(success=False, detail="User not found")

        return db.DBResultDTO(success=True, detail="User is admin")
    except:
        return db.DBResultDTO(success=False, detail="Error occurred while checking admin status")
    finally:
        db.close_connection(conn)

def register(user_uuid) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_admin (user_uuid) VALUES (?)', (user_uuid,))
        conn.commit()
        return db.DBResultDTO(success=True, detail="Admin registered successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)