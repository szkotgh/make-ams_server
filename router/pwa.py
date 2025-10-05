from flask import Blueprint, send_file, make_response

pwa_bp = Blueprint('pwa', __name__)

# Manifest and Service Worker
@pwa_bp.route('/manifest.webmanifest', methods=['GET'])
def manifest():
    response = make_response(send_file('static/manifest.webmanifest'))
    return response

@pwa_bp.route('/sw.js', methods=['GET'])
def service_worker():
    response = make_response(send_file('static/sw.js'))
    return response

# Icon routes
@pwa_bp.route('/images/icon-96.png', methods=['GET'])
def icon_96(): 
    response = make_response(send_file('static/icons/icon-96.png'))
    return response

@pwa_bp.route('/images/icon-120.png', methods=['GET'])
def icon_120(): 
    response = make_response(send_file('static/icons/icon-120.png'))
    return response

@pwa_bp.route('/images/icon-128.png', methods=['GET'])
def icon_128(): 
    response = make_response(send_file('static/icons/icon-128.png'))
    return response

@pwa_bp.route('/images/icon-144.png', methods=['GET'])
def icon_144(): 
    response = make_response(send_file('static/icons/icon-144.png'))
    return response

@pwa_bp.route('/images/icon-152.png', methods=['GET'])
def icon_152(): 
    response = make_response(send_file('static/icons/icon-152.png'))
    return response

@pwa_bp.route('/images/icon-180.png', methods=['GET'])
def icon_180(): 
    response = make_response(send_file('static/icons/icon-180.png'))
    return response

@pwa_bp.route('/images/icon-192.png', methods=['GET'])
def icon_192(): 
    response = make_response(send_file('static/icons/icon-192.png'))
    return response

@pwa_bp.route('/images/icon-384.png', methods=['GET'])
def icon_384(): 
    response = make_response(send_file('static/icons/icon-384.png'))
    return response

@pwa_bp.route('/images/icon-512.png', methods=['GET'])
def icon_512(): 
    response = make_response(send_file('static/icons/icon-512.png'))
    return response