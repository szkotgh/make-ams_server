from flask import Blueprint, render_template
import middleware.auth as auth
from router.admin.kw_bot_manage import kw_bot_manage_bp
import db.domains.kakaowork.bot as db_kakaowork_bot

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_bp.register_blueprint(kw_bot_manage_bp)

@admin_bp.route('', methods=['GET'])
@auth.admin_required
def index():
    bot_list = db_kakaowork_bot.get_bot_list_info()
    return render_template('admin/dashboard.html', bot_list=bot_list.data)


'''
전체 유저관리(비밀번호 변경, 유저비활)
문 상태 변경
가입 승인
'''