from flask import Blueprint, render_template, request, flash, redirect, url_for
import middleware.auth as auth
import modules.utils as utils
import db.domains.kakaowork.bot as db_kakaowork_bot

kw_bot_manage_bp = Blueprint('kw_bot_manage', __name__, url_prefix='/kw_bot_manage')

@kw_bot_manage_bp.route('', methods=['POST'])
@auth.admin_required
def create():
    bot_name = request.form.get('bot_name')
    bot_app_key = request.form.get('bot_app_key')
    
    result = db_kakaowork_bot.create_bot(bot_name, bot_app_key)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"생성에 실패했습니다: {result.detail}", success=False).to_response()
    
    return utils.ResultDTO(code=200, message="봇이 생성되었습니다.", success=True).to_response()

@kw_bot_manage_bp.route('/set_default', methods=['POST'])
@auth.admin_required
def set_default():
    bot_id = request.form.get('bot_id', type=int)
    result = db_kakaowork_bot.set_default_bot(bot_id)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"설정에 실패했습니다: {result.detail}", success=False).to_response()
    
    return utils.ResultDTO(code=200, message=result.detail, success=True).to_response()