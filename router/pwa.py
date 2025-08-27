from flask import Blueprint, send_file

pwa_bp = Blueprint('pwa', __name__)

# Manifest and Service Worker
@pwa_bp.route('/manifest.webmanifest', methods=['GET'])
def manifest():
    return send_file('static/manifest.webmanifest')
@pwa_bp.route('/sw.js', methods=['GET'])
def service_worker():
    return send_file('static/sw.js')

# Icon routes
@pwa_bp.route('/images/icon-96.png', methods=['GET'])
def icon_96(): return send_file('static/icons/icon-96.png')
@pwa_bp.route('/images/icon-120.png', methods=['GET'])
def icon_120(): return send_file('static/icons/icon-120.png')
@pwa_bp.route('/images/icon-128.png', methods=['GET'])
def icon_128(): return send_file('static/icons/icon-128.png')
@pwa_bp.route('/images/icon-144.png', methods=['GET'])
def icon_144(): return send_file('static/icons/icon-144.png')
@pwa_bp.route('/images/icon-152.png', methods=['GET'])
def icon_152(): return send_file('static/icons/icon-152.png')
@pwa_bp.route('/images/icon-180.png', methods=['GET'])
def icon_180(): return send_file('static/icons/icon-180.png')
@pwa_bp.route('/images/icon-192.png', methods=['GET'])
def icon_192(): return send_file('static/icons/icon-192.png')
@pwa_bp.route('/images/icon-384.png', methods=['GET'])
def icon_384(): return send_file('static/icons/icon-384.png')
@pwa_bp.route('/images/icon-512.png', methods=['GET'])
def icon_512(): return send_file('static/icons/icon-512.png')