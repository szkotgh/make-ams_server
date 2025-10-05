-- AMS Server Database Schema

-- Device Management
CREATE TABLE IF NOT EXISTS terminals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    name TEXT NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_heartbeat TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    updated_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

-- User Account
CREATE TABLE IF NOT EXISTS users (
    uuid TEXT PRIMARY KEY,
    id TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

-- User Verification Status
CREATE TABLE IF NOT EXISTS user_verify (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- Admin Role
CREATE TABLE IF NOT EXISTS user_admin (
    user_uuid TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- Teacher Role
CREATE TABLE IF NOT EXISTS user_teacher (
    user_uuid TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- Class Tracking
CREATE TABLE IF NOT EXISTS user_class_tracking (
    user_uuid TEXT NOT NULL,
    year INTEGER NOT NULL,
    grade INTEGER CHECK (grade >= 1 AND grade <= 3),
    class INTEGER CHECK (class >= 1 AND class <= 10),
    number INTEGER CHECK (number >= 1 AND number <= 30),
    is_graduated BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_uuid) REFERENCES users (uuid),
    PRIMARY KEY (user_uuid, year),
    UNIQUE(year, grade, class, number)
);

-- User Sessions
CREATE TABLE IF NOT EXISTS user_sessions (
    id TEXT PRIMARY KEY,
    user_uuid TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- QR Authentication
CREATE TABLE IF NOT EXISTS auth_qr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    auth_code TEXT NOT NULL,
    use_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);

-- NFC Card Management
CREATE TABLE IF NOT EXISTS auth_nfc (
    id TEXT PRIMARY KEY,  -- 카드 식별용
    name TEXT NOT NULL,                    -- 별칭
    nfc_hash TEXT NOT NULL,                -- 카드 식별용 해시
    pin_hash TEXT NULL,                    -- PIN 인증용 해시 (없을 수도 있음. 소유 유저가 원할 경우 설정하는 거임)
    pin_salt TEXT NULL,                    -- PIN 해시용 솔트
    status TEXT NOT NULL DEFAULT 'active',                  -- 카드 상태: active, lost, stolen, disabled
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

-- NFC Card Owner Management
CREATE TABLE IF NOT EXISTS auth_nfc_owner (
    nfc_id TEXT PRIMARY KEY NOT NULL, -- 카드 주인은 한 명만 가능
    owner_uuid TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (nfc_id) REFERENCES auth_nfc (id),
    FOREIGN KEY (owner_uuid) REFERENCES users (uuid)
);

-- Guest NFC Card Management
CREATE TABLE IF NOT EXISTS guest_auth_nfc (
    nfc_id TEXT PRIMARY KEY,
    nfc_hash TEXT NOT NULL UNIQUE,
    card_name TEXT NOT NULL,
    card_status TEXT NOT NULL DEFAULT 'active', -- active, disabled, lost, stolen, blocked
    use_count INTEGER NOT NULL DEFAULT 0,
    guest_name TEXT NOT NULL,
    creator_uuid TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    
    FOREIGN KEY (creator_uuid) REFERENCES users (uuid)
);

-- Guest QR Code Management
CREATE TABLE IF NOT EXISTS guest_auth_qr (
    qr_id TEXT PRIMARY KEY NOT NULL,
    auth_hash TEXT NOT NULL UNIQUE,
    qr_name TEXT NOT NULL,
    qr_status TEXT NOT NULL DEFAULT 'active', -- active, disabled
    use_count INTEGER NOT NULL DEFAULT 0,
    guest_name TEXT NOT NULL,
    creator_uuid TEXT NOT NULL,
    effective_date TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),

    FOREIGN KEY (creator_uuid) REFERENCES users (uuid)
);

-- Door Status
CREATE TABLE IF NOT EXISTS door_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auth_code BOOLEAN NOT NULL,
    button BOOLEAN NOT NULL,
    nfc BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    remote_change_by_uuid TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

CREATE TABLE IF NOT EXISTS door_remote (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remote_open_by_uuid TEXT NOT NULL,
    remote_open_used BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);


-- KakaoWork Bot
CREATE TABLE IF NOT EXISTS kakaowork_bot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    app_key TEXT NOT NULL UNIQUE,
    kw_space_id TEXT NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

-- KakaoWork User Link
CREATE TABLE IF NOT EXISTS user_link_kakaowork (
    user_uuid TEXT PRIMARY KEY,
    bot_id INTEGER NOT NULL,
    kw_id TEXT NOT NULL UNIQUE,
    kw_name TEXT NOT NULL,
    kw_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid),
    FOREIGN KEY (bot_id) REFERENCES kakaowork_bot (id)
);

-- User Settings
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
);

-- Door Open Request
CREATE TABLE IF NOT EXISTS request_open_door (
    device_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (device_id) REFERENCES terminals (id)
);

-- Access Log
CREATE TABLE IF NOT EXISTS log_access (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NULL,
    method TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);

-- Status Change Log
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
);
