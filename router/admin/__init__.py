from flask import Blueprint, render_template, request, jsonify, session
import middleware.auth as auth
from router.admin.kw_bot_manage import kw_bot_manage_bp
import db.domains.kakaowork.bot as db_kakaowork_bot
import db.domains.users.verify
import db.domains.users.sessions as db_session
import db.domains.devices.door as db_door
import db.domains.auth.nfc as db_nfc
from router.admin.guest import guest_bp
import os
import db.domains.auth.nfc as db_nfc
import db.domains.users.guest_auth as db_guest_auth

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_bp.register_blueprint(kw_bot_manage_bp)
admin_bp.register_blueprint(guest_bp)

@admin_bp.route('', methods=['GET'])
@auth.admin_required
def index():
    bot_list = db_kakaowork_bot.get_bot_list_info()
    user_rows = db.user_verify.get_all_users()
    user_list = [dict(u) for u in user_rows.data] if user_rows.success else []
    door_status_result = db_door.get_status()
    door_status = door_status_result.data if door_status_result.success else None
    session_info = db_session.get_info(session['session_id'])
    current_user_uuid = session_info.data['user_info']['uuid'] if session_info.success else ''
    guest_nfc_list = db_guest_auth.get_guest_nfc()
    guest_qr_list = db_guest_auth.get_guest_qr()

    return render_template('admin/dashboard.html', 
                            bot_list = bot_list.data, 
                            user_list = user_list, 
                            door_status = door_status,
                            current_user_uuid=current_user_uuid,
                            guest_nfc_list=guest_nfc_list,
                            guest_qr_list=guest_qr_list,
                            host_domain=os.environ['HOST_DOMAIN']
           )

@admin_bp.route('/user-verify/update-status', methods=['POST'])
@auth.admin_required
def update_status():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    status = data.get('status')

    if status == 'verified':
        result = db.domains.users.verify.verify(user_uuid)
    elif status == 'rejected':
        result = db.domains.users.verify.reject(user_uuid, reason="관리자 거절")
    elif status == 'blocked':
        result = db.domains.users.verify.block(user_uuid, reason="관리자 차단")
    else:
        result = db.DBResultDTO(success=False, detail="잘못된 상태 값입니다.")

    return jsonify(result.__dict__)

@admin_bp.route('/update_reason', methods=['POST'])
@auth.admin_required
def update_reason():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    reason = data.get('reason', '')

    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user_verify SET reason=? WHERE user_uuid=?', (reason, user_uuid))
            conn.commit()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, detail=str(e))
    
@admin_bp.route('/door/update', methods=['POST'])
@auth.admin_required
def update_door():
    session['session_id']
    
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    if not user_uuid:
        return jsonify({"success": False, "detail": "로그인 정보가 없습니다."})
    
    result = db_door.update_door_status(user_uuid, data)
    return jsonify({"success": result.success, "detail": result.detail})

@admin_bp.route('/check-session')
def check_session():
    user_info = session.get('user_info')
    if user_info:
        return f"user_info 있음: {user_info}"
    else:
        return "user_info 없음"
    
    
@admin_bp.route('/door/remote-open', methods=['POST'])
@auth.admin_required
def remote_open_door():
    try:
        session_info = db_session.get_info(session['session_id'])
        user_uuid = session_info.data['user_info']['uuid']

        # door.py 함수 호출
        result = db_door.remote_open(user_uuid)
        if not result.success:
            return jsonify({"code": 500, "data": None, "message": result.detail or "문 열기 실패"})

        return jsonify({"code": 200, "data": None, "message": "원격 열기 요청이 기록됨"})
    except Exception as e:
        return jsonify({"code": 500, "data": None, "message": f"서버 오류: {str(e)}"})
    
# ------------------------------
# NFC 카드 관리
# ------------------------------

@admin_bp.route("/nfc")
@auth.admin_required
def nfc_card_management():
    # 모든 유저 가져오기
    users_result = db.domains.users.verify.get_all_users()
    active_users = []
    if users_result.success:
        # 실제 소유주로 지정 가능한 상태만 필터링
        active_users = [
            {
                "uuid": u["user_uuid"],
                "student_id": f"{u['grade']}{u['class']:02}{u['number']:02}",
                "name": u["user_name"]
            }
            for u in users_result.data
            if u["status"] == "verified"  # 필요하면 조건 조정
        ]

    nfc_cards_result = db_nfc.get_all_cards()
    nfc_cards = nfc_cards_result.data if nfc_cards_result.success else []
    print(active_users)

    return render_template(
        "admin/dashboard.html",
        nfc_cards=nfc_cards,
        active_users=active_users,
        user_list=users_result.data  # 인증 관리 탭에서 사용
    )

@admin_bp.route("/nfc/add", methods=["POST"])
@auth.admin_required
def add_nfc_card():
    data = request.json
    result = db_nfc.add_card(
        name=data["name"],
        owner_uuid=data.get("owner_uuid"),
        status=data["status"]
    )
    return jsonify(result.__dict__)


# NFC 카드 수정
@admin_bp.route('/nfc/update', methods=['POST'])
@auth.admin_required
def update_nfc_card():
    data = request.get_json()
    card_id = data.get('id')
    name = data.get('name')
    owner_uuid = data.get('owner_uuid') or None
    status = data.get('status')

    if not card_id:
        return jsonify({"success": False, "message": "카드 ID가 필요합니다."}), 400

    # auth_nfc 테이블 업데이트
    result = db_nfc.update_card(card_id, name=name, status=status)
    if not result.success:
        return jsonify({"success": False, "message": result.detail})

    # owner 정보 업데이트
    if owner_uuid is not None:
        owner_result = db_nfc.update_owner(card_id, owner_uuid)
        if not owner_result.success:
            return jsonify({"success": False, "message": owner_result.detail})

    return jsonify({"success": True, "message": "카드 수정 완료"})


# NFC 카드 삭제
@admin_bp.route('/nfc/delete', methods=['POST'])
@auth.admin_required
def delete_nfc_card():
    data = request.get_json()
    card_id = data.get('id')

    if not card_id:
        return jsonify({"success": False, "message": "카드 ID가 필요합니다."}), 400

    # auth_nfc_owner 삭제
    owner_result = db_nfc.delete_owner(card_id)
    # auth_nfc 삭제
    card_result = db_nfc.delete_card(card_id)

    success = owner_result.success and card_result.success
    detail = card_result.detail or owner_result.detail

    return jsonify({"success": success, "message": detail or "카드 삭제 완료"})


# NFC 카드 목록 조회
@admin_bp.route('/nfc/list', methods=['GET'])
@auth.admin_required
def list_guest_nfc():
    result = db_nfc.get_all_cards_with_owner()
    print(result)
    return jsonify({
        "code": 200 if result.success else 500,
        "data": result.data if result.success else None,
        "message": result.detail
    })