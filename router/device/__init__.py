from flask import Blueprint, request
from router.device.auth import auth_bp
from middleware.device import auth_device
import modules.utils as utils
import db.domains.devices.door as door

device_bp = Blueprint('device', __name__, url_prefix='/device')
device_bp.register_blueprint(auth_bp)

@device_bp.route('/status', methods=['GET'])
@auth_device
def get_status():   
    door_status_result = door.get_status()
    if not door_status_result.success or not door_status_result.data:
        return utils.ResultDTO(code=500, message="문 상태 조회 실패", data={}).to_response()

    data = door_status_result.data
    response = {
        "door_access_level": data['status'],  # DB의 status 값 (open/restrict/close)
        "button_status_enabled": 'enable' if data['button'] else 'disable',
        "qr_status_enabled": 'enable' if data['auth_code'] else 'disable',
        "nfc_status_enabled": 'enable' if data['nfc'] else 'disable',
        "remote_open_enabled": 'disable',   # enable: 자동 출입문 열림. disable: 자동 출입문 닫힘
        "remote_open_door_by": '홍길동',    # 문 연 사람 이름. remote_open_door가 enable일 경우 사용됨
        "open_request_enabled": 'enable'    # 문 열기 요청이 가능한지 여부
    }
    
    remote_status_result = door.get_remote_status()
    if remote_status_result.success and remote_status_result.data:
        rdata = remote_status_result.data
        if rdata.get("remote_open_enabled"):
            response["remote_open_enabled"] = "enable"
            response["remote_open_door_by"] = rdata["remote_open_by_name"]
            
    return utils.ResultDTO(code=200, message="성공적으로 조회되었습니다.", data=response).to_response()

@device_bp.route('/request_open_door', methods=['POST'])
@auth_device
def request_open_door(): # 외부인 출입이 비활성화 되어있을 때 문열기를 요청하는 API. 관리자에게 카카오워크로 문열기 요청 알림 전송 후 관리자가 원격 문 열기를 시전하는 방식으로 작동
    # Request Logic
    return utils.ResultDTO(code=200, message="성공적으로 요청되었습니다.\n잠시만 기다려주세요.").to_response()