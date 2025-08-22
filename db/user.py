import db
import utils

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
        verify_info = is_verified(user_info['uuid'])
        if not verify_info.success:
            return db.DBResultDTO(success=False, detail="관리자 확인 후 로그인할 수 있습니다.")
        print(verify_info.data)
        if not verify_info.data['is_verified']:
            return db.DBResultDTO(success=False, detail=f"가입이 거부되었습니다. 사유: {verify_info.data['description']}")

    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)
        
    # Create Session, return session_id
    session_id = utils.generate_uuid()
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_sessions (id, user_uuid, user_agent) VALUES (?, ?, ?)', (session_id, user_info['uuid'], user_agent))
        conn.commit()
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

    return db.DBResultDTO(success=True, detail=f"{user_info['name']}님, 로그인되었습니다.", data={"session_id": session_id})

def logout(session_id) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE user_sessions SET is_active = ? WHERE id = ?', (False, session_id))
        conn.commit()
        return db.DBResultDTO(success=True, detail="로그아웃되었습니다.")
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

def is_admin(uuid) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_admin WHERE uuid = ?', (uuid,))
        result = cursor.fetchone()
        if result:
            return db.DBResultDTO(success=True, detail="성공적으로 조회했습니다.", data=dict(result))
        return db.DBResultDTO(success=False, detail="관리자 권한이 없습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def is_verified(uuid) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_verified WHERE user_uuid = ?', (uuid,))
        result = cursor.fetchone()
        if result:
            return db.DBResultDTO(success=True, detail="성공적으로 조회했습니다.", data=dict(result))
        return db.DBResultDTO(success=False, detail="사용자를 찾을 수 없습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def regi_admin(uuid) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_admin (user_uuid, is_admin) VALUES (?, ?)', (uuid, True))
        conn.commit()
        return db.DBResultDTO(success=True, detail="관리자 권한이 부여되었습니다.")
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
    now_year = utils.get_now_datetime().year

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        # Create User
        cursor.execute('''
            INSERT INTO users (uuid, id, password, salt, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (uuid, id, hashed_password, salt, name))
        conn.commit()
        # Class Tracking
        cursor.execute('''
            INSERT INTO user_class_tracking (user_uuid, year, grade, class, number)
            VALUES (?, ?, ?, ?, ?)
        ''', (uuid, now_year, grade, _class, number))
        conn.commit()
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

    return db.DBResultDTO(success=True, detail="User created successfully")

def create_teacher(id, password, name) -> db.DBResultDTO:
    uuid = utils.generate_uuid()
    salt = utils.generate_hash(16)
    hashed_password = utils.str_to_hash(password + salt)

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        # Create User
        cursor.execute('''
            INSERT INTO users (uuid, id, password, salt, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (uuid, id, hashed_password, salt, name))
        conn.commit()
        # Insert into user_teacher table
        cursor.execute('''
            INSERT INTO user_teacher (user_uuid, is_teacher)
            VALUES (?, ?)
        ''', (uuid, True))
        conn.commit()

        regi_admin(uuid) # Auto grant admin privileges

    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    
    finally:
        db.close_connection(conn)

    return db.DBResultDTO(success=True, detail="Teacher created successfully")