import db
import db.domains.kakaowork.bot as kakaowork_bot
import modules.kakaowork.user as kakaowork_user
import modules.kakaowork.send_message as kakaowork_send_message

def get_info(user_uuid) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_link_kakaowork WHERE user_uuid = ?', (user_uuid,))
            user_kakaowork_info = cursor.fetchone()
            if not user_kakaowork_info:
                return db.DBResultDTO(success=False, detail="연결된 카카오워크 계정이 없습니다.")
            return db.DBResultDTO(success=True, detail="연결된 카카오워크 계정 정보를 조회했습니다.", data=dict(user_kakaowork_info))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def find_kakaowork_user(email) -> db.DBResultDTO:
    default_bot_info = kakaowork_bot.get_default_bot_info()
    if not default_bot_info.success:
        return default_bot_info
    kakaowork_user_info = kakaowork_user.find_user_by_email(default_bot_info.data['app_key'], email)
    if not kakaowork_user_info.success:
        return kakaowork_user_info
    kakaowork_user_info.data = kakaowork_user_info.data.to_dict()
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_link_kakaowork WHERE kw_id = ?', (kakaowork_user_info.data['id'],))
            user_kakaowork_info = cursor.fetchone()
            if user_kakaowork_info:
                return db.DBResultDTO(success=False, detail="해당 이메일은 이미 카카오워크 계정과 연결되어 있습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    return db.DBResultDTO(success=True, detail="카카오워크 계정을 찾았습니다.", data=kakaowork_user_info.data)


def link_kakaowork_user(user_uuid, email) -> db.DBResultDTO:
    user_kakaowork_info = get_info(user_uuid)
    if user_kakaowork_info.success:
        return db.DBResultDTO(success=False, detail="이미 카카오워크와 연결되어 있습니다.")
    default_bot_info = kakaowork_bot.get_default_bot_info()
    if not default_bot_info.success:
        return default_bot_info
    kakaowork_user_info = find_kakaowork_user(email)
    if not kakaowork_user_info.success:
        return kakaowork_user_info
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_link_kakaowork (user_uuid, bot_id, kw_id, kw_name, kw_email) VALUES (?, ?, ?, ?, ?)', (user_uuid, default_bot_info.data['id'], kakaowork_user_info.data['id'], kakaowork_user_info.data['name'], email))
            db.user_settings.set_setting(user_uuid, 'notification_login', True, 'boolean')
            db.user_settings.set_setting(user_uuid, 'notification_door_access', True, 'boolean')
            user_info = db.user.get_info(user_uuid)
            notification_result = kakaowork_send_message.send_link_kakaowork_notification(
                app_key=default_bot_info.data['app_key'],
                kw_id=kakaowork_user_info.data['id'],
                user_name=user_info.data['name'],
                user_id=user_info.data['id'],
            )
            if not notification_result.success:
                print(notification_result.detail)
            return db.DBResultDTO(success=True, detail="카카오워크 계정을 연결했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def unlink_kakaowork_user(user_uuid) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_link_kakaowork WHERE user_uuid = ?', (user_uuid,))
            user_kakaowork_info = cursor.fetchone()
            if not user_kakaowork_info:
                return db.DBResultDTO(success=False, detail="연결된 카카오워크 계정이 없습니다.")
            kw_id = user_kakaowork_info['kw_id']
            cursor.execute('DELETE FROM user_link_kakaowork WHERE user_uuid = ?', (user_uuid,))
            user_info = db.user.get_info(user_uuid)
            default_bot_info = kakaowork_bot.get_default_bot_info()
            if not default_bot_info.success:
                return default_bot_info
            notification_result = kakaowork_send_message.send_unlink_kakaowork_notification(
                app_key=default_bot_info.data['app_key'],
                kw_id=kw_id,
                user_name=user_info.data['name'],
                user_id=user_info.data['id'],
            )
            if not notification_result.success:
                print(notification_result.detail)
            return db.DBResultDTO(success=True, detail="카카오워크 계정 연결이 해제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


