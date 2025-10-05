from flask import Blueprint, request, render_template
import db.domains.users.guest_auth as guest_auth

guest_bp = Blueprint('guest', __name__, url_prefix='/guest')

@guest_bp.route('/qr')
def qr():
    code_value = request.args.get('code')
    guest_qr_info = guest_auth.get_guest_qr()

    correct_guest_qr_info = next((qr for qr in guest_qr_info.data if qr['qr_id'] == code_value), None)

    return render_template('guest/qr.html', code_value=code_value, guest_qr_info=guest_qr_info, correct_guest_qr_info=correct_guest_qr_info)