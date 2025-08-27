from flask import Blueprint, redirect, render_template, request, flash, url_for, session, jsonify
import db.user
import db.session
import db.user_admin
import db.user_teacher
import db.user_tracking_class
import db.user_kakaowork
import db.user_settings
import db.qr
import middleware.auth as auth
import router.user.link_kakaowork as link_kakaowork
import router.user.notification_settings as notification_settings
import router.user.settings as settings
import modules.utils as utils
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.register_blueprint(link_kakaowork.link_kakaowork_bp)
user_bp.register_blueprint(notification_settings.notification_settings_bp)
user_bp.register_blueprint(settings.settings_bp)

@user_bp.route('/dashboard', methods=['GET'])
@auth.login_required
def dashboard():
    session_info = db.session.get_info(session['session_id'])
    session_info_list = db.session.get_list_info(session['session_id'])
    is_admin = db.user_admin.is_admin(session_info.data['user_info']['uuid']).success
    is_teacher = db.user_teacher.is_teacher(session_info.data['user_info']['uuid']).success
    this_year_class = db.user_tracking_class.get_this_year_class(session_info.data['user_info']['uuid'])
    kakaowork_info = db.user_kakaowork.get_info(session_info.data['user_info']['uuid'])
    
    notification_settings = None
    if kakaowork_info.success:
        notification_result = db.user_settings.get_multiple_settings(
            session_info.data['user_info']['uuid'], 
            ['notification_login', 'notification_door_access']
        )
        if notification_result.success:
            notification_settings = notification_result.data

    return render_template('user/dashboard.html',
                                user_info=session_info.data['user_info'],
                                session_info=session_info.data['session_info'],
                                session_list_info=session_info_list.data['session_list_info'],
                                is_admin=is_admin,
                                is_teacher=is_teacher,
                                this_year_class=this_year_class.data,
                                kakaowork_info=kakaowork_info.data,
                                notification_settings=notification_settings
                           )

@user_bp.route('/qr_code', methods=['POST'])
@auth.login_required
def qr_code():
    session_info = db.session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    gen_qr_result = db.qr.generate_qr(user_uuid)
    if not gen_qr_result.success:
        return utils.ResultDTO(code=400, message=f"QR 코드 생성 실패: {gen_qr_result.detail}", success=False).to_response()
    
    return utils.ResultDTO(code=200, message="QR코드를 발급했습니다.", data=gen_qr_result.data['value'], success=True).to_response()

@user_bp.route('/user_list', methods=['GET'])
@auth.login_required
def user_list():
    user_list = db.user.get_all_info()
    if not user_list.success:
        return utils.ResultDTO(code=400, message=user_list.detail, success=False).to_response()
    return utils.ResultDTO(code=200, message='유저 목록을 조회했습니다.', data=user_list.data, success=True).to_response()

@user_bp.route('/create_class_info', methods=['POST'])
@auth.login_required
def create_class_info():
    session_info = db.session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db.user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return jsonify({'success': False, 'detail': '교사 계정은 학급 정보를 생성할 수 없습니다.'})
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'detail': '요청 데이터가 없습니다.'})
    
    grade = data.get('grade')
    _class = data.get('class')
    number = data.get('number')
    
    if not all([grade, _class, number]):
        return jsonify({'success': False, 'detail': '학년, 반, 번호를 모두 입력해주세요.'})
    
    if not (1 <= grade <= 3):
        return jsonify({'success': False, 'detail': '학년은 1~3 사이의 값이어야 합니다.'})
    
    if not (1 <= _class <= 10):
        return jsonify({'success': False, 'detail': '반은 1~10 사이의 값이어야 합니다.'})
    
    if not (1 <= number <= 30):
        return jsonify({'success': False, 'detail': '번호는 1~30 사이의 값이어야 합니다.'})
    
    current_year = datetime.now().year
    
    duplicate_check = db.user_tracking_class.check_duplicate_class(current_year, grade, _class, number)
    if duplicate_check.success and duplicate_check.data:
        return jsonify({'success': False, 'detail': '같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.'})
    
    result = db.user_tracking_class.create(user_uuid, current_year, grade, _class, number)
    
    if result.success:
        return jsonify({'success': True, 'detail': '학급 정보가 성공적으로 생성되었습니다.'})
    else:
        return jsonify({'success': False, 'detail': result.detail})

@user_bp.route('/update_class_info', methods=['POST'])
@auth.login_required
def update_class_info():
    session_info = db.session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db.user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return jsonify({'success': False, 'detail': '교사 계정은 학급 정보를 업데이트할 수 없습니다.'})
    
    already_updated = db.user_tracking_class.is_already_updated_this_year(user_uuid)
    if already_updated.success and already_updated.data:
        return jsonify({'success': False, 'detail': '올해 이미 학급 정보를 업데이트했습니다.'})
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'detail': '요청 데이터가 없습니다.'})
    
    grade = data.get('grade')
    _class = data.get('class')
    number = data.get('number')
    
    if not all([grade, _class, number]):
        return jsonify({'success': False, 'detail': '학년, 반, 번호를 모두 입력해주세요.'})
    
    if not (1 <= grade <= 3):
        return jsonify({'success': False, 'detail': '학년은 1~3 사이의 값이어야 합니다.'})
    
    if not (1 <= _class <= 10):
        return jsonify({'success': False, 'detail': '반은 1~10 사이의 값이어야 합니다.'})
    
    if not (1 <= number <= 30):
        return jsonify({'success': False, 'detail': '번호는 1~30 사이의 값이어야 합니다.'})
    
    year_update_check = db.user_tracking_class.check_year_update_needed(user_uuid)
    if not year_update_check.success or not year_update_check.data:
        return jsonify({'success': False, 'detail': '학급 정보 업데이트가 필요하지 않습니다.'})
    
    if year_update_check.data.get('needs_graduation'):
        return jsonify({'success': False, 'detail': '졸업 상태 업데이트가 필요한 계정입니다.'})
    
    expected_grade = year_update_check.data.get('new_grade')
    if grade != expected_grade:
        return jsonify({'success': False, 'detail': f'올바른 학년은 {expected_grade}학년입니다.'})
    
    current_year = datetime.now().year
    
    duplicate_check = db.user_tracking_class.check_duplicate_class(current_year, grade, _class, number)
    if duplicate_check.success and duplicate_check.data:
        return jsonify({'success': False, 'detail': '같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.'})
    
    result = db.user_tracking_class.update_for_new_year(
        user_uuid, current_year, grade, _class, number, False
    )
    
    if result.success:
        return jsonify({'success': True, 'detail': '학급 정보가 성공적으로 업데이트되었습니다.'})
    else:
        return jsonify({'success': False, 'detail': result.detail})

@user_bp.route('/update_graduation', methods=['POST'])
@auth.login_required
def update_graduation():
    session_info = db.session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db.user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return jsonify({'success': False, 'detail': '교사 계정은 졸업 상태를 업데이트할 수 없습니다.'})
    
    already_updated = db.user_tracking_class.is_already_updated_this_year(user_uuid)
    if already_updated.success and already_updated.data:
        return jsonify({'success': False, 'detail': '올해 이미 졸업 상태를 업데이트했습니다.'})
    
    year_update_check = db.user_tracking_class.check_year_update_needed(user_uuid)
    if not year_update_check.success or not year_update_check.data:
        return jsonify({'success': False, 'detail': '졸업 상태 업데이트가 필요하지 않습니다.'})
    
    if not year_update_check.data.get('needs_graduation'):
        return jsonify({'success': False, 'detail': '졸업 상태 업데이트가 필요하지 않습니다.'})
    
    current_year = datetime.now().year
    
    result = db.user_tracking_class.update_for_new_year(
        user_uuid, current_year, None, None, None, True
    )
    
    if result.success:
        return jsonify({'success': True, 'detail': '졸업 상태가 성공적으로 업데이트되었습니다.'})
    else:
        return jsonify({'success': False, 'detail': result.detail})

@user_bp.route('/all_logout', methods=['GET'])
@auth.login_required
def all_logout():
    result = db.user.logout_all(session['session_id'])
    if not result.success:
        flash(result.detail, 'danger')
        return redirect(url_for('router.user.dashboard'))

    return redirect(url_for('router.user.signin'))

@user_bp.route('/remote_logout', methods=['POST'])
@auth.login_required
def remote_logout():
    session_index = request.form.get('index', type=int)
    session_list_info = db.session.get_list_info(session['session_id'])
    if not session_list_info.data:
        return utils.ResultDTO(code=400, message='세션 정보를 찾을 수 없습니다.', success=False).to_response()
    
    if 0 > session_index or session_index >= len(session_list_info.data['session_list_info']):
        return utils.ResultDTO(code=400, message='세션 인덱스가 범위를 벗어났습니다.', success=False).to_response()
    
    target_session = session_list_info.data['session_list_info'][session_index]
    if not target_session:
        return utils.ResultDTO(code=400, message='세션 정보를 찾을 수 없습니다.', success=False).to_response()

    result = db.user.logout(target_session['id'])
    if not result.success:
        return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()

    return utils.ResultDTO(code=200, message='세션을 성공적으로 로그아웃했습니다.', success=True).to_response()

@user_bp.route('/logout', methods=['GET', 'POST'])
@auth.login_required
def logout():
    if request.method == 'GET':
        session_id = session.get('session_id')
    else:
        session_id = request.args.get('session_id', type=str)
    result = db.user.logout(session_id)
    if not result.success:
        flash(result.detail, 'danger')
        return redirect(url_for('router.index'))

    session.pop('session_id', None)
    return redirect(url_for('router.user.signin'))

@user_bp.route('/signin', methods=['GET', 'POST'])
@auth.not_login_required
def signin():
    if request.method == 'POST':
        id = request.form.get('id', type=str)
        password = request.form.get('password', type=str)
        user_agent = request.headers.get('User-Agent', 'Unknown', type=str)
        result = db.user.login(id, password, user_agent)
        if not result.success:
            flash(result.detail, 'danger')
            return render_template('user/signin.html')

        session['session_id'] = result.data['session_id']
        return redirect(url_for('router.index'))

    return render_template('user/signin.html')

@user_bp.route('/signup', methods=['GET', 'POST'])
@auth.not_login_required
def signup():
    if request.method == 'POST':
        # Teacher Signup
        if request.form.get('role') == 'teacher':
            result = db.user.create_teacher(
                id=request.form.get('id', type=str),
                password=request.form.get('password', type=str),
                name=request.form.get('name', type=str)
            )
            if not result.success:
                flash(result.detail, 'danger')
                return render_template('user/signup.html')
        
        # Normal Signup
        else:
            result = db.user.create(
                id=request.form.get('id', type=str),
                password=request.form.get('password', type=str),
                name=request.form.get('name', type=str),
                grade=request.form.get('grade', type=int),
                _class=request.form.get('class', type=int),
                number=request.form.get('number', type=int)
            )
            if not result.success:
                flash(result.detail, 'danger')
                return render_template('user/signup.html')
        
        flash('가입 요청되었습니다. 관리자 승인 후 로그인 가능합니다.', 'success')
        return redirect(url_for('router.user.signin'))

    return render_template('user/signup.html')
