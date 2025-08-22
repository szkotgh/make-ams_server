from flask import Blueprint, request
import utils

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/button', methods=['POST'])
def button_auth():
    # Device Auth
    device_token = request.headers.get('Authorization')
    if not device_token or device_token != "Bearer DEVICE_HASH_TOKEN":
        return utils.ResultDTO(code=401, message="올바르지 않은 장치입니다.").to_response()

    # Auth Logic
    auth_possible = False
    
    if auth_possible:
        return utils.ResultDTO(code=200, message="메이크에 오신 것을 환영합니다.", success=True).to_response()
    else:
        return utils.ResultDTO(code=403, message="출입이 거부되었습니다.").to_response()

@auth_bp.route('/qr', methods=['POST'])
def qr_auth():
    # Device Auth
    device_token = request.headers.get('Authorization')
    if not device_token or device_token != "Bearer DEVICE_HASH_TOKEN":
        return utils.ResultDTO(code=401, message="올바르지 않은 장치입니다.").to_response()
    
    # Auth Logic
    qr_value = request.json.get('value', None)
    
    if not qr_value:
        return utils.ResultDTO(code=400, message="필수 파라미터가 누락되었습니다.").to_response()

    user_name = None

    if qr_value == "GMLASD12".lower():
        user_name = "관리자"

    if not user_name:
        return utils.ResultDTO(code=404, message="알 수 없는 QR 코드입니다.").to_response()

    return utils.ResultDTO(code=200, message=f"{user_name}님 환영합니다.", success=True).to_response()

@auth_bp.route('/nfc', methods=['POST'])
def nfc_auth():
    # Device Auth
    device_token = request.headers.get('Authorization')
    if not device_token or device_token != "Bearer DEVICE_HASH_TOKEN":
        return utils.ResultDTO(code=401, message="올바르지 않은 장치입니다.").to_response()
    
    # Auth Logic
    nfc_value = request.json.get('value', None)

    if not nfc_value:
        return utils.ResultDTO(code=400, message="필수 파라미터가 누락되었습니다.").to_response()
    
    user_name = None
    user_nfc_pin = None
    enabled = True
    
    if nfc_value == "0497e436bc2a81":
        user_name = "관리자"
        user_nfc_pin = "1234"
    if nfc_value == "0491b736bc2a81":
        user_name = "관리자2"
        user_nfc_pin = None # 핀 설정을 안한 사용자
    if nfc_value == "0491b736bc2a82":
        user_name = "홍길동"
        user_nfc_pin = "5678"
        enabled = False
        
    if not user_name:
        return utils.ResultDTO(code=404, message="알 수 없는 카드입니다.").to_response()

    if not enabled:
        return utils.ResultDTO(code=403, message="차단된 카드입니다.").to_response()

    return utils.ResultDTO(code=200, message=f"{user_name}님 환영합니다.", data={
        "user_nfc_pin": user_nfc_pin
    }).to_response()