from flask import Blueprint, send_file, make_response

site_asset_bp = Blueprint('site_asset', __name__)

@site_asset_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    response = make_response(send_file('static/favicon.ico'))
    return response

@site_asset_bp.route('/robots.txt', methods=['GET'])
def robots():
    response = make_response(send_file('static/robots.txt'))
    return response

@site_asset_bp.route('/static/<path:filename>', methods=['GET'])
def static_files(filename):
    response = make_response(send_file(f'static/{filename}'))
    return response