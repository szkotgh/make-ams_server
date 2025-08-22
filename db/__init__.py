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
        CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY,
            id TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_verified (
            user_uuid TEXT PRIMARY KEY,
            is_verified BOOLEAN NOT NULL DEFAULT FALSE,
            description TEXT,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_admin (
            user_uuid TEXT PRIMARY KEY,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
            
            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        );
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS user_teacher (
            user_uuid TEXT PRIMARY KEY,
            is_teacher BOOLEAN NOT NULL DEFAULT FALSE,
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
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS auth_qr (
            id TEXT PRIMARY KEY,
            user_uuid TEXT NOT NULL,
            qr_code TEXT NOT NULL,
            is_used BOOLEAN NOT NULL DEFAULT FALSE,
            expiration_date TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours +1 minutes')),
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

            FOREIGN KEY (user_uuid) REFERENCES users (uuid)
        )
    ''')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS door_status (
            qr_code BOOLEAN NOT NULL,
            button BOOLEAN NOT NULL,
            nfc BOOLEAN NOT NULL,
            is_used BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
        )
    ''')
    conn.commit()
    close_connection(conn)

_init_db()