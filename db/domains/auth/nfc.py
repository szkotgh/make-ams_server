import db
import modules.utils as utils
from db.domains.logs.log import insert_access_log


def get_nfc_info(nfc_value: str, pin_input: str) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM auth_nfc WHERE id = ?", (nfc_value,))
            nfc_data = cursor.fetchone()
            if not nfc_data:
                insert_access_log(user_uuid=None, method="NFC", success=False, reason="등록되지 않은 카드")
                return db.DBResultDTO(success=False, detail="등록되지 않은 NFC 카드입니다.")

            user_uuid = nfc_data['owner_uuid']
            stored_pin_hash = nfc_data['pin_hash']
            enabled = nfc_data['is_active']

            if not enabled:
                insert_access_log(user_uuid=user_uuid, method="NFC", success=False, reason="차단된 카드")
                return db.DBResultDTO(success=False, detail="차단된 카드입니다.")

            if stored_pin_hash:
                token = utils.generate_hash(16, seed=f"{user_uuid}{pin_input}")
                if token != stored_pin_hash:
                    insert_access_log(user_uuid=user_uuid, method="NFC", success=False, reason="PIN 불일치")
                    return db.DBResultDTO(success=False, detail="PIN이 올바르지 않습니다.")

            cursor.execute("SELECT name FROM users WHERE uuid = ?", (user_uuid,))
            user_name = cursor.fetchone()['name']
            insert_access_log(user_uuid=user_uuid, method="NFC", success=True, reason=None)
            return db.DBResultDTO(success=True, detail=f"{user_name}님 환영합니다.")
    except Exception as e:
        insert_access_log(user_uuid=None, method="NFC", success=False, reason=str(e))
        return db.DBResultDTO(success=False, detail=str(e))


