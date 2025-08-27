from flask import Blueprint, request, session
from middleware.auth import login_required
import modules.utils as utils
import db.user_settings

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('', methods=['GET'])
@login_required
def get_settings():
    try:
        session_info = db.session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        setting_keys = request.args.getlist('keys')
        
        if setting_keys:
            result = db.user_settings.get_multiple_settings(user_uuid, setting_keys)
        else:
            result = db.user_settings.get_all_settings(user_uuid)
        
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message="설정을 조회했습니다.", data=result.data, success=True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()

@settings_bp.route('', methods=['POST'])
@login_required
def set_setting():
    try:
        session_info = db.session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        data = request.get_json()
        if not data:
            return utils.ResultDTO(code=400, message="요청 데이터가 없습니다.", success=False).to_response()
        
        setting_key = data.get('key')
        setting_value = data.get('value')
        setting_type = data.get('type', 'string')
        
        if not setting_key or setting_value is None:
            return utils.ResultDTO(code=400, message="key와 value는 필수입니다.", success=False).to_response()
        
        if setting_type not in ['string', 'boolean', 'integer', 'float']:
            return utils.ResultDTO(code=400, message="잘못된 타입입니다.", success=False).to_response()
        
        result = db.user_settings.set_setting(user_uuid, setting_key, setting_value, setting_type)
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message="설정이 저장되었습니다.", success=True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()

@settings_bp.route('/batch', methods=['POST'])
@login_required
def set_multiple_settings():
    try:
        session_info = db.session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        data = request.get_json()
        if not data or not isinstance(data, list):
            return utils.ResultDTO(code=400, message="설정 배열이 필요합니다.", success=False).to_response()
        
        success_count = 0
        error_count = 0
        
        for setting in data:
            setting_key = setting.get('key')
            setting_value = setting.get('value')
            setting_type = setting.get('type', 'string')
            
            if setting_key and setting_value is not None:
                result = db.user_settings.set_setting(user_uuid, setting_key, setting_value, setting_type)
                if result.success:
                    success_count += 1
                else:
                    error_count += 1
        
        if error_count == 0:
            return utils.ResultDTO(code=200, message=f"{success_count}개 설정이 저장되었습니다.", success=True).to_response()
        else:
            return utils.ResultDTO(code=207, message=f"{success_count}개 성공, {error_count}개 실패", success=False).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()

@settings_bp.route('/<setting_key>', methods=['DELETE'])
@login_required
def delete_setting(setting_key):
    try:
        session_info = db.session.get_info(session['session_id'])
        if not session_info.success:
            return utils.ResultDTO(code=400, message="세션 정보를 가져올 수 없습니다.", success=False).to_response()
        
        user_uuid = session_info.data['user_info']['uuid']
        
        result = db.user_settings.delete_setting(user_uuid, setting_key)
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message="설정이 삭제되었습니다.", success=True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(code=500, message=f"서버 오류가 발생했습니다: {str(e)}", success=False).to_response()
