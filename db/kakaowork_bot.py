import db
import modules.kakaowork.bot as kakaowork_bot
import modules.kakaowork.space as kakaowork_space

def create_bot(name, app_key) -> db.DBResultDTO:
    # test app key
    bot_info = kakaowork_bot.bot_info(app_key)
    if not bot_info.success:
        return db.DBResultDTO(success=False, detail=bot_info.message)
    space_info = kakaowork_space.space_info(app_key)
    if not space_info.success:
        return db.DBResultDTO(success=False, detail=space_info.message)
    print(bot_info.data, space_info.data)

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO kakaowork_bot (name, app_key, kw_space_id) VALUES (?, ?, ?)', (name, app_key, space_info.data['id']))
        conn.commit()
        return db.DBResultDTO(success=True, detail="카카오워크 봇이 생성되었습니다.", data={"bot_info": bot_info.data, "space_info": space_info.data})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_bot_info(bot_id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kakaowork_bot WHERE id = ?', (bot_id,))
        bot_info = cursor.fetchone()
        return db.DBResultDTO(success=True, detail="카카오워크 봇 정보를 조회했습니다.", data=dict(bot_info))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_default_bot_info() -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kakaowork_bot WHERE is_default = TRUE')
        bot_info = cursor.fetchone()
        if not bot_info:
            return db.DBResultDTO(success=False, detail="기본 카카오워크 봇이 설정되지 않았습니다. 관리자에게 문의하세요.")
        return db.DBResultDTO(success=True, detail="기본 카카오워크 봇 정보를 조회했습니다.", data=dict(bot_info))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_bot_list_info() -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kakaowork_bot')
        bot_list = cursor.fetchall()
        bot_list = [dict(bot) for bot in bot_list]
        bot_list.reverse()
        return db.DBResultDTO(success=True, detail="카카오워크 봇 목록을 조회했습니다.", data=bot_list)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)
        
def set_default_bot(bot_id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE kakaowork_bot SET is_default = FALSE WHERE is_default = TRUE')
        cursor.execute('UPDATE kakaowork_bot SET is_default = TRUE WHERE id = ?', (bot_id,))
        conn.commit()
        return db.DBResultDTO(success=True, detail="해당 카카오워크 봇이 기본 봇으로 설정되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)