from flask import Blueprint, request, session, redirect, url_for, flash
import db.user_kakaowork
import db.session
from middleware.auth import login_required
import modules.utils as utils

link_kakaowork_bp = Blueprint('link_kakaowork', __name__, url_prefix='/link_kakaowork')

@link_kakaowork_bp.route('', methods=['POST'])
@login_required
def link_kakaowork():
    email = request.form.get('email')
    session_info = db.session.get_info(session['session_id'])
    result = db.user_kakaowork.link_kakaowork_user(session_info.data['user_info']['uuid'], email)
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
    
    return utils.ResultDTO(code=200, message="카카오워크 계정이 연결되었습니다.", success=True).to_response()

@link_kakaowork_bp.route('/check_email', methods=['POST'])
@login_required
def check_email():
    email = request.form.get('email')
    result = db.user_kakaowork.find_kakaowork_user(email)
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
    return utils.ResultDTO(code=200, message="카카오워크 계정을 찾았습니다.", data=result.data, success=True).to_response()

@link_kakaowork_bp.route('', methods=['DELETE'])
@login_required
def unlink_kakaowork():
    session_info = db.session.get_info(session['session_id'])
    result = db.user_kakaowork.unlink_kakaowork_user(session_info.data['user_info']['uuid'])
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
    
    return utils.ResultDTO(code=200, message="카카오워크 계정 연결이 해제되었습니다.", success=True).to_response()