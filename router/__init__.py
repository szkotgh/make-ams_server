from flask import Blueprint, render_template, send_file
from router.user import user_bp
from router.device import device_bp

router_bp = Blueprint('router', __name__)

router_bp.register_blueprint(user_bp)
router_bp.register_blueprint(device_bp)

@router_bp.route('/')
def index():
    return render_template('index.html')

@router_bp.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')

@router_bp.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')