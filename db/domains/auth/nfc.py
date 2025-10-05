import db
import modules.utils as utils
from db.domains.logs.log import insert_access_log



def add_card(name, owner_uuid, status="active"):
    card_id = str(utils.generate_hash(16))
    nfc_hash = str(utils.generate_hash(16))
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO auth_nfc (id, name, nfc_hash, status) VALUES (?, ?, ?, ?)",
                (card_id, name, nfc_hash, status)
            )
            if owner_uuid:
                cursor.execute(
                    "INSERT INTO auth_nfc_owner (nfc_id, owner_uuid) VALUES (?, ?)",
                    (card_id, owner_uuid)
                )
            conn.commit()
        return db.DBResultDTO(success=True, detail="카드 추가 완료", data={"id": card_id})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))

def get_all_cards():
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM auth_nfc")
            rows = cursor.fetchall()
            cards = [dict(row) for row in rows]
        return db.DBResultDTO(success=True, data=cards)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"NFC 카드 목록 조회 실패: {e}")
    
def update_card(card_id, name=None, owner_uuid=None, status=None):
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            fields = []
            values = []

            if name is not None:
                fields.append("name=?")
                values.append(name)
            if owner_uuid is not None:
                fields.append("owner_uuid=?")
                values.append(owner_uuid)
            if status is not None:
                fields.append("status=?")
                values.append(status)

            if not fields:
                return db.DBResultDTO(success=False, detail="수정할 항목이 없습니다.")

            values.append(card_id)
            cursor.execute(f"UPDATE auth_nfc SET {', '.join(fields)} WHERE id=?", values)
            conn.commit()
        return db.DBResultDTO(success=True, detail="수정 완료")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))

def delete_card(card_id):
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM auth_nfc WHERE id=?", (card_id,))
            conn.commit()
        return db.DBResultDTO(success=True, detail="카드가 삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"카드 삭제 실패: {e}")
    
    
def add_owner(nfc_id, owner_uuid):
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO auth_nfc_owner (nfc_id, owner_uuid, created_at) VALUES (?, ?, datetime('now'))",
                (nfc_id, owner_uuid)
            )
            conn.commit()
        return db.DBResultDTO(success=True, detail="카드 소유자 등록 완료")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"소유자 등록 실패: {e}")

def update_owner(nfc_id, owner_uuid):
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE auth_nfc_owner SET owner_uuid=? WHERE nfc_id=?",
                (owner_uuid, nfc_id)
            )
            conn.commit()
        return db.DBResultDTO(success=True, detail="카드 소유자 수정 완료")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"소유자 수정 실패: {e}")

def delete_owner(nfc_id):
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM auth_nfc_owner WHERE nfc_id=?", (nfc_id,))
            conn.commit()
        return db.DBResultDTO(success=True, detail="카드 소유자 삭제 완료")
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"소유자 삭제 실패: {e}")

def get_all_cards_with_owner():
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                c.name AS 별칭, 
                c.status AS 상태, 
                o.owner_uuid AS 소유자, 
                c.created_at AS 등록일,
                '관리' AS 관리  -- 여기서는 관리용 버튼/링크 표시용
            FROM auth_nfc c
            LEFT JOIN auth_nfc_owner o ON c.id = o.nfc_id;
            """)
            rows = cursor.fetchall()
            cards = [dict(r) for r in rows]
        return db.DBResultDTO(success=True, data=cards)
    except Exception as e:
        return db.DBResultDTO(success=False, detail=f"NFC 카드+소유자 조회 실패: {e}")
