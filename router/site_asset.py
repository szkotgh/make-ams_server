from flask import Blueprint, send_file

site_asset_bp = Blueprint('site_asset', __name__)

@site_asset_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('static/favicon.ico')

@site_asset_bp.route('/robots.txt', methods=['GET'])
def robots():
    return send_file('static/robots.txt')