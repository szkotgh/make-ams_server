import db
import modules.utils as utils
import db.session
import db.user_tracking_class
import db.user_teacher
import db.user_verify
import db.user_settings
import modules.kakaowork.send_message as kakaowork_send_message
import db.kakaowork_bot as kakaowork_bot

def login(id, password, user_agent) -> db.DBResultDTO:
    # Check user id, password
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user_info = cursor.fetchone()
        if not user_info:
            return db.DBResultDTO(success=False, detail="아이디 또는 비밀번호를 확인하십시오.")
        # Check password
        if not utils.check_password(password, user_info['password'], user_info['salt']):
            return db.DBResultDTO(success=False, detail="아이디 또는 비밀번호를 확인하십시오.")
        # Check account is verified
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
        
    # Create Session, return session_id
    create_session = db.session.create(user_info['uuid'], user_agent)
    if not create_session.success:
        return utils.ResultDTO(code=400, message=create_session.detail, success=False)

    # send login notification
    notification_login_setting = db.user_settings.get_setting(user_info['uuid'], 'notification_login', True)
    if notification_login_setting:
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
        except Exception as e:
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
    id = id
    salt = utils.generate_hash(16)
    hashed_password = utils.str_to_hash(password + salt)
    name = name
    now_year = utils.get_current_datetime().year

    check_id = get_info_by_id(id)
    print(check_id.detail)
    if check_id.success:
        return db.DBResultDTO(success=False, detail="이미 사용중인 아이디입니다.")
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (uuid, id, password, salt, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (uuid, id, hashed_password, salt, name))
        conn.commit()
        
        create_class_tracking = db.user_tracking_class.create(uuid, now_year, grade, _class, number)
        if not create_class_tracking.success:
            return create_class_tracking
        
        create_verify = db.user_verify.create(uuid)
        if not create_verify.success:
            return create_verify
        
        db.user_settings.set_setting(uuid, 'first_login', True, 'boolean')
        
        return db.DBResultDTO(success=True, detail="User created successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def create_teacher(id, password, name) -> db.DBResultDTO:
    uuid = utils.generate_uuid()
    salt = utils.generate_hash(16)
    hashed_password = utils.str_to_hash(password + salt)

    check_id = get_info_by_id(id)
    if check_id.success:
        return db.DBResultDTO(success=False, detail="이미 사용중인 아이디입니다.")

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (uuid, id, password, salt, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (uuid, id, hashed_password, salt, name))
        conn.commit()
        
        register_teacher = db.user_teacher.register(uuid)
        if not register_teacher.success:
            return register_teacher
        
        create_verify = db.user_verify.create(uuid)
        if not create_verify.success:
            return create_verify

        db.user_settings.set_setting(uuid, 'first_login', True, 'boolean')

    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    
    finally:
        db.close_connection(conn)

    return db.DBResultDTO(success=True, detail="Teacher created successfully")