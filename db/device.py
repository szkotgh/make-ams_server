import db
import modules.utils as utils

def get_info(device_id):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device_info = cursor.fetchone()
        conn.close()
        if not device_info:
            return utils.ResultDTO(code=404, message="Device not found", success=False)
        return utils.ResultDTO(code=200, message="Success", success=True, data=dict(device_info))
    except:
        return utils.ResultDTO(code=500, message="Fail to query", success=False)
    finally:
        if conn:
            conn.close()

def create_device(device_name):
    device_token = utils.generate_hash(16)
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (token, name) VALUES (?, ?)", (device_token, device_name))
        conn.commit()
        return utils.ResultDTO(code=201, message="Device created", success=True)
    except:
        return utils.ResultDTO(code=500, message="Fail to create device", success=False)
    finally:
        if conn:
            conn.close()

