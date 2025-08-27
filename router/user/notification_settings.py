from flask import Blueprint, request, session
from middleware.auth import login_required
import modules.utils as utils
import db.domains.users.settings as db_user_settings
import db.domains.users.sessions as db_session

notification_settings_bp = Blueprint('notification_settings', __name__, url_prefix='/notification_settings')

@notification_settings_bp.route('', methods=['GET'])
@login_required
def get():
    try:
        session_info = db_session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        result = db_user_settings.get_multiple_settings(user_uuid, ['notification_login', 'notification_door_access'])
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message="알림 설정을 조회했습니다.", data=result.data, success=True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()

@notification_settings_bp.route('/update', methods=['POST'])
@login_required
def update():
    try:
        session_info = db_session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        notification_type = request.form.get('type')
        enabled_str = request.form.get('enabled')
        
        if notification_type not in ['notification_login', 'notification_door_access']:
            return utils.ResultDTO(code=400, message="잘못된 알림 유형입니다.", success=False).to_response()
        
        if enabled_str is None:
            return utils.ResultDTO(code=400, message="enabled 값이 제공되지 않았습니다.", success=False).to_response()
        
        is_enabled = enabled_str.lower() in ['true', '1', 'yes', 'on']
        setting_key = notification_type
        
        result = db_user_settings.set_setting(user_uuid, setting_key, is_enabled, 'boolean')
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message="알림 설정이 업데이트되었습니다.", success=True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()
