from flask import Blueprint, request
from middleware.auth import auth_device
import db
from db.nfc import get_nfc_info
from db.qr import verify_qr
from db.log import insert_access_log
import modules.utils as utils

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/button', methods=['POST'])
@auth_device
def button_auth():
    # Auth Logic
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT button FROM door_status")
        row = cursor.fetchone()
        auth_possible = bool(row[0])
    finally:
        db.close_connection(conn)
        
    if auth_possible:
        insert_access_log(method="BUTTON", success=True)
        return utils.ResultDTO(code=200, message="메이크에 오신 것을 환영합니다.", success=True).to_response()
    else:
        insert_access_log(method="BUTTON", success=False, reason="출입 거부")
        return utils.ResultDTO(code=403, message="출입이 거부되었습니다.").to_response()

@auth_bp.route('/qr', methods=['POST'])
@auth_device
def qr_auth():
    qr_value = request.json.get('value')
    print(qr_value)
    
    if not qr_value:
        return utils.ResultDTO(code=400, message="필수 파라미터가 누락되었습니다.").to_response()

    # DB 기반 인증
    verifu_result = verify_qr(qr_value)
    print(verifu_result.success)
    
    if not verifu_result.success:
        return utils.ResultDTO(code=404, message="알 수 없는 QR 코드이거나\n만료/사용된 코드입니다.").to_response()

    # 인증 성공
    return utils.ResultDTO(code=200, message="QR 인증 성공").to_response()

@auth_bp.route('/nfc', methods=['POST'])
@auth_device
def nfc_auth():
    nfc_value = request.json.get('value')
    pin_input = request.json.get('pin')

    if not nfc_value:
        return utils.ResultDTO(code=400, message="NFC 카드 ID가 필요합니다.").to_response()

    # DB 기반 인증
    nfc_result = get_nfc_info(nfc_value, pin_input)

    if not nfc_result.success:
        # 실패 사유에 맞게 HTTP 코드 지정
        detail = nfc_result.detail
        if "등록되지 않은" in detail:
            code = 404
        elif "차단된 카드" in detail:
            code = 403
        elif "PIN" in detail:
            code = 401
        else:
            code = 400
        return utils.ResultDTO(code=code, message=detail).to_response()

    # 인증 성공
    return utils.ResultDTO(
        code=200,
        message=nfc_result.detail
    ).to_response()
    
    '''
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
        '''