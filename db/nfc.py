import db
import modules.utils as utils
from db.log import insert_access_log 

def get_nfc_info(nfc_value: str, pin_input: str) -> db.DBResultDTO:
    """
    NFC 인증 정보 조회 및 PIN 검증
    nfc_value: NFC 카드 ID
    pin_input: 사용자가 입력한 PIN (없으면 PIN 검증 생략)
    """
    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        # 1. NFC 카드 조회
        cursor.execute("SELECT * FROM auth_nfc WHERE id = ?", (nfc_value,))
        nfc_data = cursor.fetchone()
        if not nfc_data:
            insert_access_log(user_uuid=None, method="NFC", success=False, reason="등록되지 않은 카드")
            print(nfc_value)
            return db.DBResultDTO(success=False, detail="등록되지 않은 NFC 카드입니다.")

        # 2. 카드 정보
        user_uuid = nfc_data['owner_uuid']
        stored_pin_hash = nfc_data['pin_hash']
        enabled = nfc_data['is_active'] 

        # 3. 카드 활성화 체크
        if not enabled:
            insert_access_log(user_uuid=user_uuid, method="NFC", success=False, reason="차단된 카드")
            return db.DBResultDTO(success=False, detail="차단된 카드입니다.")

        # 4. PIN 검증
        if stored_pin_hash:

            token = utils.generate_hash(16, seed=f"{user_uuid}{pin_input}")
            if token != stored_pin_hash:
                insert_access_log(user_uuid=user_uuid, method="NFC", success=False, reason="PIN 불일치")
                return db.DBResultDTO(success=False, detail="PIN이 올바르지 않습니다.")

        # 5. 인증 성공
        cursor.execute("SELECT name FROM users WHERE uuid = ?", (user_uuid,))
        user_name = cursor.fetchone()['name']
        insert_access_log(user_uuid=user_uuid, method="NFC", success=True, reason=None)
        return db.DBResultDTO(success=True, detail=f"{user_name}님 환영합니다.")

    except Exception as e:
        insert_access_log(user_uuid=None, method="NFC", success=False, reason=str(e))
        return db.DBResultDTO(success=False, detail=str(e))

    finally:
        db.close_connection(conn)
