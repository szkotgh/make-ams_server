from flask import Blueprint, request
from middleware.auth import auth_device
import db
import db.domains.auth.nfc as db_nfc
import db.domains.auth.qr as db_qr
import db.domains.logs.log as db_log
import db.domains.devices.door as db_door
import modules.utils as utils

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/button', methods=['POST'])
@auth_device
def button_auth():
    try:
        status_res = db_door.get_status()
        auth_possible = False
        if status_res.success and status_res.data is not None:
            auth_possible = bool(status_res.data.get('button', False))
    except Exception:
        auth_possible = False

    if auth_possible:
        db_log.insert_access_log(method="BUTTON", success=True, user_uuid=None, reason=None)
        return utils.ResultDTO(code=200, message="메이크에 오신 것을 환영합니다.", success=True).to_response()
    else:
        db_log.insert_access_log(method="BUTTON", success=False, user_uuid=None, reason="출입 거부")
        return utils.ResultDTO(code=403, message="출입이 거부되었습니다.").to_response()

@auth_bp.route('/qr', methods=['POST'])
@auth_device
def qr_auth():
    qr_value = request.json.get('value')
    if not qr_value:
        return utils.ResultDTO(code=400, message="필수 파라미터가 누락되었습니다.").to_response()

    verifu_result = db_qr.verify_qr(qr_value)
    if not verifu_result.success:
        return utils.ResultDTO(code=404, message="알 수 없는 QR 코드이거나\n만료/사용된 코드입니다.").to_response()

    return utils.ResultDTO(code=200, message="QR 인증 성공").to_response()

@auth_bp.route('/nfc', methods=['POST'])
@auth_device
def nfc_auth():
    nfc_value = request.json.get('value')
    pin_input = request.json.get('pin')

    if not nfc_value:
        return utils.ResultDTO(code=400, message="NFC 카드 ID가 필요합니다.").to_response()

    nfc_result = db_nfc.get_nfc_info(nfc_value, pin_input)

    if not nfc_result.success:
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