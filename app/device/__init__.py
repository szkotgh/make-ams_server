from flask import Blueprint

device_bp = Blueprint('device', __name__, url_prefix='/device')

@device_bp.route('/get_status', methods=['GET'])
def get_status():
    return "OK", 200