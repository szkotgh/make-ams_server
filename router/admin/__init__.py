from flask import Blueprint, render_template, request, jsonify
import middleware.auth as auth
from router.admin.kw_bot_manage import kw_bot_manage_bp
import db.domains.kakaowork.bot as db_kakaowork_bot
import db.domains.users.verify
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_bp.register_blueprint(kw_bot_manage_bp)

@admin_bp.route('', methods=['GET'])
@auth.admin_required
def index():
    bot_list = db_kakaowork_bot.get_bot_list_info()
    user_rows = db.user_verify.get_all_users()  # DB에서 전체 가져오는 함수 필요
    user_list = [dict(u) for u in user_rows.data] if user_rows.success else []
    return render_template('admin/dashboard.html', bot_list=bot_list.data, user_list=user_list)

@admin_bp.route('/user-verify/update-status', methods=['POST'])
@auth.admin_required
def update_status():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    status = data.get('status')

    if status == 'verified':
        result = db.domains.users.verify.verify(user_uuid)
    elif status == 'rejected':
        result = db.domains.users.verify.reject(user_uuid, reason="관리자 거절")
    elif status == 'blocked':
        result = db.domains.users.verify.block(user_uuid, reason="관리자 차단")
    else:
        result = db.DBResultDTO(success=False, detail="잘못된 상태 값입니다.")

    return jsonify(result.__dict__)

@admin_bp.route('/update_reason', methods=['POST'])
@auth.admin_required
def update_reason():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    reason = data.get('reason', '')

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user_verify SET reason=? WHERE user_uuid=?', (reason, user_uuid))
            conn.commit()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, detail=str(e))