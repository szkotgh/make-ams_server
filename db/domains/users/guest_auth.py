from bdb import effective
import db
import modules.utils as utils

def auth_guest_qr(auth_hash: str) -> db.DBResultDTO:
    auth_result = get_guest_qr_by_auth_hash(auth_hash)
    if not auth_result.success:
        return auth_result
    if auth_result.data['qr_status'] != 'active':
        return db.DBResultDTO(success=False, detail="QR 상태가 올바르지 않습니다.")
    
    now_datetime = utils.get_current_datetime()
    if now_datetime < utils.str_to_datetime(auth_result.data['effective_date']):
        return db.DBResultDTO(success=False, detail="아직 사용할 수 없습니다.")
    if now_datetime > utils.str_to_datetime(auth_result.data['expiration_date']):
        return db.DBResultDTO(success=False, detail="만료된 QR코드입니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE guest_auth_qr SET use_count = ? WHERE auth_hash = ?", (auth_result.data['use_count']+1, auth_hash,))
            conn.commit()
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")
    
    return db.DBResultDTO(success=True, detail="QR 인증 성공", data=auth_result.data)

def auth_guest_nfc(nfc_hash: str) -> db.DBResultDTO:
    auth_result = get_guest_nfc_by_nfc_hash(nfc_hash)
    if not auth_result.success:
        return auth_result
    if auth_result.data['card_status'] != 'active':
        return db.DBResultDTO(success=False, detail="NFC 상태가 올바르지 않습니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE guest_auth_nfc SET use_count = ? WHERE nfc_hash = ?", (auth_result.data['use_count']+1, nfc_hash,))
            conn.commit()
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")
    
    return db.DBResultDTO(success=True, detail="NFC 인증 성공", data=auth_result.data)

def get_guest_qr_by_auth_hash(auth_hash: str) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM guest_auth_qr WHERE auth_hash = ?", (auth_hash,))
            row = cursor.fetchone()
            return db.DBResultDTO(success=True, detail="조회 성공", data=row)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")

def get_guest_nfc_by_nfc_hash(nfc_hash: str) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM guest_auth_nfc WHERE nfc_hash = ?", (nfc_hash,))
            row = cursor.fetchone()
            return db.DBResultDTO(success=True, detail="조회 성공", data=row)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")

def get_guest_nfc(limit=100) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM guest_auth_nfc ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            cards = [dict(row) for row in rows] if rows else []
        return db.DBResultDTO(success=True, detail="조회 성공", data=cards)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"조회 실패: {e}")

def get_guest_qr(limit=100) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM guest_auth_qr ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            cards = [dict(row) for row in rows] if rows else []
        return db.DBResultDTO(success=True, detail="조회 성공", data=cards)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"조회 실패: {e}")
    
    
def create_guest_nfc(card_hash: str, card_name: str, guest_name: str, creator_uuid: str) -> db.DBResultDTO:
    card_id = utils.generate_hash(16)
    nfc_hash = card_hash
    if len(nfc_hash) > 64: return db.DBResultDTO(success=False, detail="생성 실패: NFC 해시가 너무 깁니다.")
    card_name = card_name
    if len(card_name) > 20: return db.DBResultDTO(success=False, detail="생성 실패: 카드 이름이 너무 깁니다.")
    guest_name = guest_name
    if len(guest_name) > 10: return db.DBResultDTO(success=False, detail="생성 실패: 게스트 이름이 너무 깁니다.")
    creator_uuid = creator_uuid
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO guest_auth_nfc (nfc_id, nfc_hash, card_name, guest_name, creator_uuid) VALUES (?, ?, ?, ?, ?)", (card_id, nfc_hash, card_name, guest_name, creator_uuid))
            conn.commit()
        return db.DBResultDTO(success=True, detail="게스트 NFC가 성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"생성 실패: {e}")

def create_guest_qr(qr_name: str, guest_name: str, effiective_date: str, expiration_date: str, creator_uuid: str) -> db.DBResultDTO:
    qr_id = utils.genetare_alnum_hash(8)
    auth_hash = utils.generate_hash(32)
    if len(qr_name) > 20: return db.DBResultDTO(success=False, detail="QR 이름이 너무 깁니다.")
    if len(guest_name) > 10: return db.DBResultDTO(success=False, detail="게스트 이름이 너무 깁니다.")
    creator_uuid = creator_uuid
    if not utils.is_valid_date(effiective_date).success: return db.DBResultDTO(success=False, detail=f"발효일 검증 실패: {utils.is_valid_date(effiective_date).detail}")
    if not utils.is_valid_date(expiration_date).success: return db.DBResultDTO(success=False, detail=f"만료일 검증 실패: {utils.is_valid_date(expiration_date).detail}")
    
    if utils.str_to_datetime(effiective_date) >= utils.str_to_datetime(expiration_date):
        return db.DBResultDTO(success=False, detail="발효일은 만료일보다 이전이어야 합니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO guest_auth_qr (qr_id, auth_hash, qr_name, guest_name, creator_uuid, effective_date, expiration_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (qr_id, auth_hash, qr_name, guest_name, creator_uuid, effiective_date, expiration_date))
            conn.commit()
        return db.DBResultDTO(success=True, detail="게스트 QR이 성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"생성 실패: {e}")
    

def config_guest_nfc(nfc_id: str, r_nfc_id: str, nfc_hash: str, card_name: str, card_status: str, guest_name: str) -> db.DBResultDTO:
    if not nfc_id: return db.DBResultDTO(success=False, detail="NFC ID는 필수입니다.")
    if not r_nfc_id: return db.DBResultDTO(success=False, detail="변경된 NFC ID는 필수입니다.")
    if len(nfc_hash) > 64: return db.DBResultDTO(success=False, detail="NFC 해시가 너무 깁니다.")
    if len(card_name) > 20: return db.DBResultDTO(success=False, detail="카드 이름이 너무 깁니다.")
    if not utils.is_valid_nfc_card_status(card_status).success: return db.DBResultDTO(success=False, detail=utils.is_valid_nfc_card_status(card_status).detail)
    if len(guest_name) > 10: return db.DBResultDTO(success=False, detail="게스트 이름이 너무 깁니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE guest_auth_nfc SET nfc_id = ?, nfc_hash = ?, card_name = ?, card_status = ?, guest_name = ? WHERE nfc_id = ?", (r_nfc_id, nfc_hash, card_name, card_status, guest_name, nfc_id))
            conn.commit()
        return db.DBResultDTO(success=True, detail="업데이트 되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"업데이트 실패: {e}")

def config_guest_qr(qr_id: str, qr_status: str, qr_name: str, guest_name: str, effiective_date: str, expiration_date: str) -> db.DBResultDTO:
    if not qr_id: return db.DBResultDTO(success=False, detail="QR ID는 필수입니다.")
    if not utils.is_valid_qr_status(qr_status).success: return db.DBResultDTO(success=False, detail=utils.is_valid_qr_status(qr_status).detail)
    if not len(qr_name) <= 20: return db.DBResultDTO(success=False, detail="QR 이름이 너무 깁니다.")
    if not len(guest_name) <= 10: return db.DBResultDTO(success=False, detail="게스트 이름이 너무 깁니다.")
    if not utils.is_valid_date(effiective_date).success: return db.DBResultDTO(success=False, detail=f"발효일 검증 실패: {utils.is_valid_date(effiective_date).detail}")
    if not utils.is_valid_date(expiration_date).success: return db.DBResultDTO(success=False, detail=f"만료일 검증 실패: {utils.is_valid_date(expiration_date).detail}")

    if utils.str_to_datetime(effiective_date) >= utils.str_to_datetime(expiration_date):
        return db.DBResultDTO(success=False, detail="발효일은 만료일보다 이전이어야 합니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE guest_auth_qr SET qr_status = ?, qr_name = ?, guest_name = ?, effective_date = ?, expiration_date = ? WHERE qr_id = ?", (qr_status, qr_name, guest_name, effiective_date, expiration_date, qr_id))
            conn.commit()
        return db.DBResultDTO(success=True, detail="업데이트 되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")
    

def delete_guest_nfc(nfc_id: str) -> db.DBResultDTO:
    if not nfc_id: return db.DBResultDTO(success=False, detail="NFC ID는 필수입니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM guest_auth_nfc WHERE nfc_id = ?", (nfc_id,))
            conn.commit()
        return db.DBResultDTO(success=True, detail="성공적으로 삭제했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")

def delete_guest_qr(qr_id: str) -> db.DBResultDTO:
    if not qr_id: return db.DBResultDTO(success=False, detail="QR ID는 필수입니다.")
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM guest_auth_qr WHERE qr_id = ?", (qr_id,))
            conn.commit()
        return db.DBResultDTO(success=True, detail="성공적으로 삭제했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"{e}")