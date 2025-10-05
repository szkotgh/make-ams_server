import db
import modules.utils as utils

def get_info(device_id) -> db.DBResultDTO:
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
            device_info = cursor.fetchone()
            if not device_info:
                return db.DBResultDTO(success=False, detail="Device not found")
            return db.DBResultDTO(success=True, detail="Success", data=dict(device_info))
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))

def create_device(device_name) -> db.DBResultDTO:
    device_token = utils.generate_hash(16)
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO devices (token, name) VALUES (?, ?)", (device_token, device_name))
            return db.DBResultDTO(success=True, detail="Device created", data={"token": device_token})
    except Exception as e:
        return db.DBResultDTO(success=False, detail=str(e))


