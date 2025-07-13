from flask import Blueprint
from app.device import device_bp

app_bp = Blueprint('app', __name__)
app_bp.register_blueprint(device_bp)