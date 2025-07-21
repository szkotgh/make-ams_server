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

# Manifest and Service Worker
@router_bp.route('/manifest.webmanifest')
def manifest():
    return send_file('static/manifest.webmanifest')
@router_bp.route('/sw.js')
def service_worker():
    return send_file('static/sw.js')
@router_bp.route('/images/icon-192.png')
def icon_192():
    return send_file('static/images/icon-192.png')
@router_bp.route('/images/icon-512.png')
def icon_512():
    return send_file('static/images/icon-512.png')