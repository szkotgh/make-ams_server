from flask import Blueprint, request
from router.device.auth import auth_bp
from middleware.auth import auth_device
import modules.utils as utils

device_bp = Blueprint('device', __name__, url_prefix='/device')
device_bp.register_blueprint(auth_bp)

@device_bp.route('/status', methods=['GET'])
@auth_device
def get_status():
    response = {
        'door_access_level': 'open',       # open: 열림, restrict: 외부인 출입 제한, close: 관리자만 출입 가능
        "button_status_enabled": 'enable',  # enable: 해당 인증 활성화. disable: 해당 인증 비활성화
        "qr_status_enabled": 'enable',      # enable: 해당 인증 활성화. disable: 해당 인증 비활성화
        "nfc_status_enabled": 'enable',     # enable: 해당 인증 활성화. disable: 해당 인증 비활성화
        "remote_open_enabled": 'disable',   # enable: 자동 출입문 열림. disable: 자동 출입문 닫힘
        "remote_open_door_by": '홍길동',    # 문 연 사람 이름. remote_open_door가 enable일 경우 사용됨
        "open_request_enabled": 'enable'    # 문 열기 요청이 가능한지 여부
    }
    
    return utils.ResultDTO(code=200, message="성공적으로 조회되었습니다.", data=response).to_response()

@device_bp.route('/request_open_door', methods=['POST'])
@auth_device
def request_open_door(): # 외부인 출입이 비활성화 되어있을 때 문열기를 요청하는 API. 관리자에게 카카오워크로 문열기 요청 알림 전송 후 관리자가 원격 문 열기를 시전하는 방식으로 작동
    # Request Logic
    return utils.ResultDTO(code=200, message="성공적으로 요청되었습니다.\n잠시만 기다려주세요.").to_response()