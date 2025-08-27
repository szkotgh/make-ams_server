import db

def get_setting(user_uuid, setting_key, default_value=None):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT setting_value, setting_type FROM user_settings WHERE user_uuid = ? AND setting_key = ?', (user_uuid, setting_key))
        result = cursor.fetchone()
        
        if not result:
            return default_value
        
        value = result['setting_value']
        value_type = result['setting_type']
        
        if value_type == 'boolean':
            return value.lower() in ['true', '1', 'yes', 'on']
        elif value_type == 'integer':
            return int(value)
        elif value_type == 'float':
            return float(value)
        else:
            return value
            
    except Exception as e:
        return default_value
    finally:
        db.close_connection(conn)

def set_setting(user_uuid, setting_key, setting_value, setting_type='string'):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if setting_type == 'boolean':
            value_str = str(setting_value).lower()
        else:
            value_str = str(setting_value)
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_settings (user_uuid, setting_key, setting_value, setting_type, updated_at) 
            VALUES (?, ?, ?, ?, DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        ''', (user_uuid, setting_key, value_str, setting_type))
        
        conn.commit()
        return db.DBResultDTO(success=True, detail="설정이 저장되었습니다.")
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_multiple_settings(user_uuid, setting_keys):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in setting_keys])
        cursor.execute(f'SELECT setting_key, setting_value, setting_type FROM user_settings WHERE user_uuid = ? AND setting_key IN ({placeholders})', (user_uuid, *setting_keys))
        results = cursor.fetchall()
        
        settings = {}
        for result in results:
            key = result['setting_key']
            value = result['setting_value']
            value_type = result['setting_type']
            
            if value_type == 'boolean':
                settings[key] = value.lower() in ['true', '1', 'yes', 'on']
            elif value_type == 'integer':
                settings[key] = int(value)
            elif value_type == 'float':
                settings[key] = float(value)
            else:
                settings[key] = value
        
        return db.DBResultDTO(success=True, detail="설정을 조회했습니다.", data=settings)
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def delete_setting(user_uuid, setting_key):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_settings WHERE user_uuid = ? AND setting_key = ?', (user_uuid, setting_key))
        conn.commit()
        
        if cursor.rowcount == 0:
            return db.DBResultDTO(success=False, detail="설정을 찾을 수 없습니다.")
        
        return db.DBResultDTO(success=True, detail="설정이 삭제되었습니다.")
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)

def get_all_settings(user_uuid):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT setting_key, setting_value, setting_type FROM user_settings WHERE user_uuid = ?', (user_uuid,))
        results = cursor.fetchall()
        
        settings = {}
        for result in results:
            key = result['setting_key']
            value = result['setting_value']
            value_type = result['setting_type']
            
            if value_type == 'boolean':
                settings[key] = value.lower() in ['true', '1', 'yes', 'on']
            elif value_type == 'integer':
                settings[key] = int(value)
            elif value_type == 'float':
                settings[key] = float(value)
            else:
                settings[key] = value
        
        return db.DBResultDTO(success=True, detail="모든 설정을 조회했습니다.", data=settings)
        
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))
    finally:
        db.close_connection(conn)
