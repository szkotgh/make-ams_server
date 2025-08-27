import db
import modules.utils as utils
import modules.kakaowork.send_message as kakaowork_send_message
import db.domains.kakaowork.bot as kakaowork_bot

def login(id, password, user_agent) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user_info = cursor.fetchone()
        if not user_info:
            return db.DBResultDTO(success=False, detail="아이디 또는 비밀번호를 확인하십시오.")
        if not utils.check_password(password, user_info['password'], user_info['salt']):
            return db.DBResultDTO(success=False, detail="아이디 또는 비밀번호를 확인하십시오.")
        verify_info = db.user_verify.get_info(user_info['uuid'])
        if not verify_info.success:
            return verify_info
        if not verify_info.data['status'] == db.user_verify.VERIFIED:
            if verify_info.data['status'] == db.user_verify.PENDING:
                return db.DBResultDTO(success=False, detail="관리자 승인 후 로그인할 수 있습니다.")
            elif verify_info.data['status'] == db.user_verify.REJECTED:
                return db.DBResultDTO(success=False, detail=f"가입이 거부되었습니다. 사유: {verify_info.data['reason']}")
            elif verify_info.data['status'] == db.user_verify.BLOCKED:
                return db.DBResultDTO(success=False, detail=f"차단된 계정입니다. 사유: {verify_info.data['reason']}")
            else:
                return db.DBResultDTO(success=False, detail="인증된 상태가 아닙니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

    create_session = db.session.create(user_info['uuid'], user_agent)
    if not create_session.success:
        return db.DBResultDTO(success=False, detail=create_session.detail)

    notification_login_setting = db.user_settings.get_setting(user_info['uuid'], 'notification_login', True)
    if notification_login_setting.success and notification_login_setting.data:
        try:
            bot_info = kakaowork_bot.get_default_bot_info()
            if not bot_info.success:
                raise Exception(bot_info.detail)
            user_kakaowork_info = db.user_kakaowork.get_info(user_info['uuid'])
            if not user_kakaowork_info.success:
                raise Exception(user_kakaowork_info.detail)
            session_info = db.session.get_info(create_session.data)
            kakaowork_send_message.send_login_notification(
                app_key=bot_info.data['app_key'],
                kw_id=user_kakaowork_info.data['kw_id'],
                user_name=session_info.data['user_info']['name'],
                user_id=session_info.data['user_info']['id'],
            )
        except Exception:
            pass

    return db.DBResultDTO(success=True, detail=f"{user_info['name']}님, 로그인되었습니다.", data={"session_id": create_session.data})


def logout(session_id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        check_session = db.session.is_active_session(session_id)
        if not check_session.success:
            return check_session
        cursor.execute('UPDATE user_sessions SET is_active = ? WHERE id = ?', (False, session_id))
        conn.commit()
        return db.DBResultDTO(success=True, detail="로그아웃되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)


def logout_all(session_id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        check_session = db.session.is_active_session(session_id)
        if not check_session.success:
            return check_session
        cursor.execute('SELECT * FROM user_sessions WHERE id = ?', (session_id,))
        session_info = cursor.fetchone()
        cursor.execute('UPDATE user_sessions SET is_active = False WHERE user_uuid = ?', (session_info['user_uuid'],))
        conn.commit()
        return db.DBResultDTO(success=True, detail="모든 세션에서 로그아웃되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)


def get_info(uuid) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE uuid = ?', (uuid,))
        user = cursor.fetchone()
        if user:
            return db.DBResultDTO(success=True, detail="User found", data=dict(user))
        return db.DBResultDTO(success=False, detail="User not found")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)


def get_all_info() -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return db.DBResultDTO(success=True, detail="Users found", data=dict(users))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)


def get_info_by_id(id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = cursor.fetchone()
        if user:
            return db.DBResultDTO(success=True, detail="User found", data=dict(user))
        return db.DBResultDTO(success=False, detail="User not found")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)


def create(id, password, name, grade, _class, number) -> db.DBResultDTO:
    uuid = utils.generate_uuid()
    salt = utils.generate_hash(16)
    hashed_password = utils.str_to_hash(password + salt)
    now_year = utils.get_current_datetime().year

    check_id = get_info_by_id(id)
    if check_id.success:
        return db.DBResultDTO(success=False, detail="이미 사용중인 아이디입니다.")

    # 중복 학년, 반, 번호 체크 (세 항목이 모두 동시에 겹치는 경우만 차단)
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as count FROM user_class_tracking 
                WHERE year = ? AND grade = ? AND class = ? AND number = ?
            ''', (now_year, grade, _class, number))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                return db.DBResultDTO(success=False, detail="같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"중복 체크 중 오류가 발생했습니다: {str(e)}")

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            
            # 사용자 계정 생성
            cursor.execute('''
                INSERT INTO users (uuid, id, password, salt, name)
                VALUES (?, ?, ?, ?, ?)
            ''', (uuid, id, hashed_password, salt, name))
            
            # 학급 정보 생성 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_class_tracking (user_uuid, year, grade, class, number, is_graduated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (uuid, now_year, grade, _class, number, False))
            
            # 인증 정보 생성 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_verify (user_uuid, status, reason)
                VALUES (?, ?, ?)
            ''', (uuid, 'pending', None))
            
            # 설정 생성 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_settings (user_uuid, setting_key, setting_value, setting_type)
                VALUES (?, ?, ?, ?)
            ''', (uuid, 'first_login', 'true', 'boolean'))
            
            # 모든 작업이 성공하면 자동으로 커밋됨 (with 문에서)
            
        return db.DBResultDTO(success=True, detail="User created successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


def create_teacher(id, password, name) -> db.DBResultDTO:
    uuid = utils.generate_uuid()
    salt = utils.generate_hash(16)
    hashed_password = utils.str_to_hash(password + salt)

    check_id = get_info_by_id(id)
    if check_id.success:
        return db.DBResultDTO(success=False, detail="이미 사용중인 아이디입니다.")

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            
            # 사용자 계정 생성
            cursor.execute('''
                INSERT INTO users (uuid, id, password, salt, name)
                VALUES (?, ?, ?, ?, ?)
            ''', (uuid, id, hashed_password, salt, name))
            
            # 교사 역할 등록 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_teacher (user_uuid)
                VALUES (?)
            ''', (uuid,))
            
            # 인증 정보 생성 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_verify (user_uuid, status, reason)
                VALUES (?, ?, ?)
            ''', (uuid, 'pending', None))
            
            # 설정 생성 (직접 SQL 실행)
            cursor.execute('''
                INSERT INTO user_settings (user_uuid, setting_key, setting_value, setting_type)
                VALUES (?, ?, ?, ?)
            ''', (uuid, 'first_login', 'true', 'boolean'))
            
            # 모든 작업이 성공하면 자동으로 커밋됨 (with 문에서)
            
        return db.DBResultDTO(success=True, detail="Teacher created successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


