import db
import db.user
import db.session
from datetime import datetime

def get_this_year_class(user_uuid) -> db.DBResultDTO:
    now_year = datetime.now().year

    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, now_year))
        class_info = cursor.fetchone()

        if class_info:
            return db.DBResultDTO(success=True, detail="Class found", data=dict(class_info))
        return db.DBResultDTO(success=False, detail="Class not found", data=None)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_last_year_class(user_uuid) -> db.DBResultDTO:
    """작년 학급 정보를 가져옵니다."""
    now_year = datetime.now().year
    last_year = now_year - 1

    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, last_year))
        class_info = cursor.fetchone()

        if class_info:
            return db.DBResultDTO(success=True, detail="Last year class found", data=dict(class_info))
        return db.DBResultDTO(success=False, detail="Last year class not found", data=None)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def check_duplicate_class(year, grade, _class, number, exclude_uuid=None) -> db.DBResultDTO:
    """같은 년도에 동일한 학년, 반, 번호를 가진 학생이 있는지 확인합니다."""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if exclude_uuid:
            cursor.execute('''
                SELECT COUNT(*) as count FROM user_class_tracking 
                WHERE year = ? AND grade = ? AND class = ? AND number = ? AND user_uuid != ?
            ''', (year, grade, _class, number, exclude_uuid))
        else:
            cursor.execute('''
                SELECT COUNT(*) as count FROM user_class_tracking 
                WHERE year = ? AND grade = ? AND class = ? AND number = ?
            ''', (year, grade, _class, number))
        
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            return db.DBResultDTO(success=True, detail="Duplicate class found", data=True)
        return db.DBResultDTO(success=True, detail="No duplicate class", data=False)
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def check_year_update_needed(user_uuid) -> db.DBResultDTO:
    """현재 년도에 학급 정보 업데이트가 필요한지 확인합니다."""
    now_year = datetime.now().year
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        # 현재 년도 정보 확인
        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, now_year))
        current_year_info = cursor.fetchone()
        
        if current_year_info:
            return db.DBResultDTO(success=False, detail="Already updated this year", data=None)
        
        # 작년 정보 확인
        last_year = now_year - 1
        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, last_year))
        last_year_info = cursor.fetchone()
        
        if last_year_info:
            last_grade = last_year_info['grade']
            last_is_graduated = last_year_info['is_graduated']
            
            # 3학년이었거나 이미 졸업한 경우
            if last_grade == 3 or last_is_graduated:
                return db.DBResultDTO(success=True, detail="Graduation update needed", data={
                    'last_grade': last_grade,
                    'last_is_graduated': last_is_graduated,
                    'needs_graduation': True
                })
            else:
                # 학년 자동 증가
                new_grade = last_grade + 1
                return db.DBResultDTO(success=True, detail="Grade update needed", data={
                    'last_grade': last_grade,
                    'new_grade': new_grade,
                    'needs_graduation': False
                })
        
        return db.DBResultDTO(success=False, detail="No previous year data", data=None)
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def force_update_for_missing_year(user_uuid) -> db.DBResultDTO:
    """학년 정보가 없는 경우 강제로 업데이트를 요구합니다."""
    now_year = datetime.now().year
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 현재 년도 정보 확인
        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, now_year))
        current_year_info = cursor.fetchone()
        
        if current_year_info:
            return db.DBResultDTO(success=False, detail="Already has current year data", data=None)
        
        # 작년 정보 확인
        last_year = now_year - 1
        cursor.execute('SELECT * FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, last_year))
        last_year_info = cursor.fetchone()
        
        if last_year_info:
            last_grade = last_year_info['grade']
            last_is_graduated = last_year_info['is_graduated']
            
            # 3학년이었거나 이미 졸업한 경우
            if last_grade == 3 or last_is_graduated:
                return db.DBResultDTO(success=True, detail="Force graduation update needed", data={
                    'last_grade': last_grade,
                    'last_is_graduated': last_is_graduated,
                    'needs_graduation': True,
                    'force_update': True
                })
            else:
                # 학년 자동 증가
                new_grade = last_grade + 1
                return db.DBResultDTO(success=True, detail="Force grade update needed", data={
                    'last_grade': last_grade,
                    'new_grade': new_grade,
                    'needs_graduation': False,
                    'force_update': True
                })
        
        # 아무 정보도 없는 경우 (신규 사용자)
        return db.DBResultDTO(success=True, detail="New user needs class info", data={
            'new_user': True,
            'force_update': True
        })
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def create(user_uuid, year, grade, _class, number) -> db.DBResultDTO:
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 이미 해당 년도에 등록된 정보가 있는지 확인
        cursor.execute('SELECT COUNT(*) as count FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, year))
        existing = cursor.fetchone()
        
        if existing and existing['count'] > 0:
            return db.DBResultDTO(success=False, detail="이미 해당 년도에 등록된 학급 정보가 있습니다.")
        
        # 중복 학급 정보 확인
        duplicate_check = check_duplicate_class(year, grade, _class, number)
        if duplicate_check.success and duplicate_check.data:
            return db.DBResultDTO(success=False, detail="같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.")
        
        cursor.execute('INSERT INTO user_class_tracking (user_uuid, year, grade, class, number) VALUES (?, ?, ?, ?, ?)', (user_uuid, year, grade, _class, number))
        conn.commit()
        return db.DBResultDTO(success=True, detail="Class tracking created successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def update_for_new_year(user_uuid, year, grade=None, _class=None, number=None, is_graduated=False) -> db.DBResultDTO:
    """새로운 년도에 대한 학급 정보를 업데이트합니다."""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if is_graduated:
            cursor.execute('''
                INSERT INTO user_class_tracking (user_uuid, year, grade, class, number, is_graduated) 
                VALUES (?, ?, NULL, NULL, NULL, TRUE)
            ''', (user_uuid, year))
        else:
            # 중복 학급 정보 확인
            duplicate_check = check_duplicate_class(year, grade, _class, number)
            if duplicate_check.success and duplicate_check.data:
                return db.DBResultDTO(success=False, detail="같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.")
            
            cursor.execute('''
                INSERT INTO user_class_tracking (user_uuid, year, grade, class, number, is_graduated) 
                VALUES (?, ?, ?, ?, ?, FALSE)
            ''', (user_uuid, year, grade, _class, number))
        
        conn.commit()
        return db.DBResultDTO(success=True, detail="New year class tracking updated successfully")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def is_already_updated_this_year(user_uuid) -> db.DBResultDTO:
    """올해 이미 업데이트했는지 확인합니다."""
    now_year = datetime.now().year
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as count FROM user_class_tracking WHERE user_uuid = ? AND year = ?', (user_uuid, now_year))
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            return db.DBResultDTO(success=True, detail="Already updated this year", data=True)
        return db.DBResultDTO(success=True, detail="Not updated this year", data=False)
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)