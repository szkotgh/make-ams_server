import sqlite3

def get_db_connection():
    conn = sqlite3.connect('./db/main.db')
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    if conn:
        conn.close()

def init_db():
    conn = get_db_connection()
    with conn:
        conn.executescript('''
            -- 유저 정보 테이블
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(16) PRIMARY KEY,                        -- 유저 로그인 ID
                user_pw VARCHAR(256) NOT NULL,                          -- 유저 비밀번호(암호화된 값)
                user_pw_salt VARCHAR(16) NOT NULL,                      -- 유저 비밀번호 솔트값
                user_name VARCHAR(10) NOT NULL,                         -- 유저 이름(정확인 실제 이름)
                is_activated BOOLEAN NOT NULL DEFAULT 0,                -- 유저 활성화 여부(0: 비활성화, 1: 활성화. 회원가입 후 관리자가 승인해야 계정 로그인 가능)
                is_admin BOOLEAN NOT NULL DEFAULT 0,                    -- 관리자 여부
                group_id INT NOT NULL,                                  -- 그룹 ID(디자인? 정보보안? AI/SW?)
                join_year INT NOT NULL,                                 -- 입학년도(학년계산용)
                kakaowork_id VARCHAR(32) DEFAULT NULL,                  -- 카카오워크 ID(카카오워크 연동 시 사용)
                create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 유저 정보 생성 시각
                update_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 마지막 유저 정보 수정 시각
                
                FOREIGN KEY (group_id) REFERENCES groups(group_id)
            );
            
            -- 동아리 그룹 정보 테이블
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 그룹 ID(ID)
                group_name VARCHAR(16) NOT NULL,         -- 그룹 이름(MAKE@AI/SW)
                display_name VARCHAR(16) NOT NULL,       -- 그룹 표시 이름(MAKE@AI/SW)
                part_possible BOOLEAN NOT NULL DEFAULT 0 -- 참여 가능 여부
            );
            
            -- 하드웨어 장치에 있는 버튼(게스트 접근, True일 시 버튼만 누르면 문이 열림)을 통한 인증을 위한 테이블
            CREATE TABLE IF NOT EXISTS auth_button (
                is_activated BOOLEAN NOT NULL DEFAULT 0 -- 버튼 인증 활성화 여부
            );

            -- NFC 인증을 위한 테이블
            CREATE TABLE IF NOT EXISTS auth_nfc (
                nfc_id VARCHAR(8) PRIMARY KEY,                          -- NFC ID(NFC 객체의 ID. 실제 NFC 카드와는 관련없는 값)
                user_id VARCHAR(16) NULL,                               -- 유저 ID(NULL일 경우 미등록 카드(카드 주인이 없는 상태))
                nfc_name VARCHAR(16) NOT NULL,                          -- NFC 이름(소유 유저가 마음대로 식별용 설정. 예: 내 NFC 카드)
                auth_value VARCHAR(64) NOT NULL,                        -- NFC 인증 값(예: k120fnja9t4a)
                is_activated BOOLEAN NOT NULL DEFAULT 0,                -- NFC 활성화 여부
                is_lost BOOLEAN NOT NULL DEFAULT 0,                     -- NFC 분실 여부(1일 경우 활성화 되어 있어도 인증 불가)
                create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- NFC 인증 생성 시각
                update_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 마지막 NFC 인증 시각
                
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            
            -- QR 코드 인증을 위한 테이블(QR인증을 요청할 때마다 QR 생성)
            CREATE TABLE IF NOT EXISTS auth_qr (
                auth_token VARCHAR(64) PRIMARY KEY,                     -- QR 인증 토큰
                user_id VARCHAR(16) NOT NULL,                           -- 유저 ID
                is_used BOOLEAN NOT NULL DEFAULT 0,                     -- QR 인증 사용 여부
                expires_at TIMESTAMP NOT NULL,                          -- QR 인증 만료 시각(기본 1분)
                create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- QR 인증 생성 시각
                update_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 마지막 QR 인증 시각

                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            
            CREATE TABLE IF NOT EXISTS auth_qr_guest (
                auth_token VARCHAR(64) PRIMARY KEY,                     -- 게스트 인증 QR 토큰
                guest_name VARCHAR(32) NOT NULL,                        -- 게스트 이름
                guest_info TEXT DEFAULT NULL,                           -- 게스트 정보(예: 전화번호, 이메일 등)
                host_user_id VARCHAR(16) NOT NULL,                      -- 게스트 QR을 만든 관리자 유저 ID
                start_at TIMESTAMP NOT NULL,                            -- 사용 시작 시각
                expires_at TIMESTAMP NOT NULL,                          -- 사용 종료 시각
                create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 생성 시각
                update_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 마지막 QR 인증 시각

                FOREIGN KEY (host_user_id) REFERENCES users(user_id)
            );
            
            CREATE TABLE IF NOT EXISTS auth_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,               -- 로그 ID
                user_id VARCHAR(16) NULL,                               -- 유저 ID(NULL일 경우 게스트)
                auth_type VARCHAR(16) NOT NULL,                         -- 인증 방식 (button, qr, qr_guest, nfc)
                is_success BOOLEAN NOT NULL DEFAULT 0,                  -- 인증 성공 여부
                create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 인증 시각

                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            
            -- 실제 하드웨어 장치 실시간 상태 저장 테이블(1대만 운영 예정이지만, 혹시나 추후 더 늘어날 수도 있음.)
            CREATE TABLE IF NOT EXISTS device (
                auth_token VARCHAR(32) PRIMARY KEY,        -- 장치 인증 토큰(장치가 서버에 요청할 때 Bearer 토큰으로 사용)
                button_enabled BOOLEAN NOT NULL DEFAULT 0, -- 장치 버튼 인증 활성화 여부
                nfc_enabled BOOLEAN NOT NULL DEFAULT 0,    -- 장치 NFC 인증 활성화 여부
                qr_enabled BOOLEAN NOT NULL DEFAULT 0      -- 장치 QR 인증 활성화 여부
                -- door_remote_open BOOLEAN NOT NULL DEFAULT 0 이거는 서버 메모리에서 관리하는 것으로 변경. status를 장치가 한번 get하게 되면 door_remote_open는 다시 0으로 바뀜. 관리자만 사용 가능한 기능이며 1로 설정해서 장치가 get할 때 1로 바뀌면 문이 열림.
            );

        ''')
    close_db_connection(conn)
    

init_db()