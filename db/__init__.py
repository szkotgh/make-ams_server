import sqlite3

class DBResultDTO():
    def __init__(self, success: bool, detail: str, data: dict = None):
        self.success = success
        self.data = data
        self.detail = detail

def get_connection():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def close_connection(conn):
    if conn:
        conn.close()
        
def _init_db():
    conn = get_connection()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            token TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY,
            id TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        );
    ''')
    conn.executescript(f'''
        CREATE TABLE IF NOT EXISTS user_verify (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_admin (
            user_uuid TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_teacher (
            user_uuid TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_class_tracking (
            user_uuid TEXT NOT NULL,
            year INTEGER NOT NULL,
            grade INTEGER,
            class INTEGER,
            number INTEGER,
            is_graduated BOOLEAN NOT NULL DEFAULT FALSE,

            FOREIGN KEY (user_uuid) REFERENCES users (uuid),
            PRIMARY KEY (user_uuid, year)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id TEXT PRIMARY KEY,
            user_uuid TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    
    # Auth
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS auth_qr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            auth_code TEXT NOT NULL,
            use_count INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        )
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS auth_nfc (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            nfc_hash BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            regi_uuid TEXT NOT NULL,
            owner_uuid TEXT NOT NULL,
            pin_hash TEXT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (regi_uuid) REFERENCES users (uuid),
            FOREIGN KEY (owner_uuid) REFERENCES users (uuid)
        )
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS door_status (
            auth_code BOOLEAN NOT NULL,
            button BOOLEAN NOT NULL,
            nfc BOOLEAN NOT NULL,
            status TEXT NOT NULL,
            remote_open BOOLEAN NOT NULL,
            remote_open_by_uuid TEXT NOT NULL,
            remote_open_used BOOLEAN NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (auth_code) REFERENCES auth_qr (auth_code)
        )
    ''')
    
    # link to kakaowork
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS kakaowork_bot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            app_key TEXT NOT NULL UNIQUE,
            kw_space_id TEXT NOT NULL,
            is_default BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        )                
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_link_kakaowork (
            user_uuid TEXT PRIMARY KEY,
            bot_id INTEGER NOT NULL,
            kw_id TEXT NOT NULL UNIQUE,
            kw_name TEXT NOT NULL,
            kw_email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid),
            FOREIGN KEY (bot_id) REFERENCES kakaowork_bot (id)
        )
    ''')

    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            setting_key TEXT NOT NULL,
            setting_value TEXT NOT NULL,
            setting_type TEXT NOT NULL DEFAULT 'string',
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            updated_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid),
            UNIQUE(user_uuid, setting_key)
        )
    ''')

    # request open door
    # 장치에서 문 열기 요청이 발생할 경우 추가됨. 알림설정이 된 관리자에게 알림이 보내짐
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS request_open_door (
            device_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    
    # log table
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS log_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NULL,
            method TEXT NOT NULL,
            success BOOLEAN NOT NULL,
            reason TEXT,
            timestamp TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        )
    ''')
    
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS log_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            change_status TEXT NOT NULL,
            auth_code BOOLEAN NOT NULL,
            button BOOLEAN NOT NULL,
            nfc BOOLEAN NOT NULL,
            status TEXT NOT NULL,
            remote_open BOOLEAN NOT NULL,
            remote_open_by_uuid TEXT NOT NULL,
            remote_open_used BOOLEAN NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        )
    ''')
    
    conn.commit()
    close_connection(conn)

_init_db()