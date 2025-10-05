from flask import Blueprint, redirect, render_template, request, jsonify, session
import db.domains.users.account as db_account
import db.domains.users.guest_auth as db_guest_auth
import middleware.auth as auth
from modules import utils

guest_bp = Blueprint('guest', __name__, url_prefix='/guest')




@guest_bp.route('/qr', methods=['POST'])
@auth.admin_required
def create_guest_qr():
    qr_name = request.json.get('qr_name')
    guest_name = request.json.get('guest_name')
    effiective_date = request.json.get('effiective_date')
    expiration_date = request.json.get('expiration_date')

    if not qr_name or not guest_name or not effiective_date or not expiration_date:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()

    creator_uuid = db_account.get_info_by_session_id(session['session_id']).data['uuid']
    result = db_guest_auth.create_guest_qr(qr_name, guest_name, effiective_date, expiration_date, creator_uuid)

    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()

@guest_bp.route('/qr', methods=['DELETE'])
@auth.admin_required
def delete_guest_qr():
    qr_id = request.json.get('qr_id')

    if not qr_id:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()

    result = db_guest_auth.delete_guest_qr(qr_id)
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()

@guest_bp.route('/qr/config', methods=['POST'])
@auth.admin_required
def config_guest_qr():
    qr_id = request.json.get('qr_id')
    qr_status = request.json.get('qr_status')
    qr_name = request.json.get('qr_name')
    guest_name = request.json.get('guest_name')
    effiective_date = request.json.get('effiective_date')
    expiration_date = request.json.get('expiration_date')
    print(f"Received config_guest_qr with qr_id={qr_id}, qr_status={qr_status}, qr_name={qr_name}, guest_name={guest_name}, effiective_date={effiective_date}, expiration_date={expiration_date}")

    if not qr_id or not qr_status or not qr_name or not guest_name or not effiective_date or not expiration_date:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()

    result = db_guest_auth.config_guest_qr(qr_id, qr_status, qr_name, guest_name, effiective_date, expiration_date)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"업데이트 실패: {result.detail}", data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()





@guest_bp.route('/nfc', methods=['POST'])
@auth.admin_required
def create_guest_nfc():
    card_hash = request.json.get('card_hash')
    card_name = request.json.get('card_name')
    guest_name = request.json.get('guest_name')
    uuid = db_account.get_info_by_session_id(session['session_id']).data['uuid']

    if not card_hash or not card_name or not guest_name:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()
    
    result = db_guest_auth.create_guest_nfc(card_hash, card_name, guest_name, uuid)
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()

@guest_bp.route('/nfc', methods=['DELETE'])
@auth.admin_required
def delete_guest_nfc():
    nfc_id = request.json.get('nfc_id')

    if not nfc_id:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()
    
    result = db_guest_auth.delete_guest_nfc(nfc_id)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"삭제 실패: {result.detail}", data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()

@guest_bp.route('/nfc/config', methods=['POST'])
@auth.admin_required
def config_guest_nfc():
    nfc_id = request.json.get('nfc_id')
    r_nfc_id = request.json.get('r_nfc_id')
    nfc_hash = request.json.get('nfc_hash')
    card_name = request.json.get('card_name')
    card_status = request.json.get('card_status')
    guest_name = request.json.get('guest_name')

    if not nfc_id or not r_nfc_id or not nfc_hash or not card_name or not card_status or not guest_name:
        return utils.ResultDTO(code=400, message="누락된 파라미터가 있습니다.").to_response()

    result = db_guest_auth.config_guest_nfc(nfc_id, r_nfc_id, nfc_hash, card_name, card_status, guest_name)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"업데이트 실패: {result.detail}", data=result.data).to_response()
    return utils.ResultDTO(code=200, message=result.detail, data=result.data).to_response()