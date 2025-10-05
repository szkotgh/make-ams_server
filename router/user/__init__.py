from flask import Blueprint, redirect, render_template, request, flash, url_for, session, jsonify
import db.domains.users.account as db_user
import db.domains.users.sessions as db_session
import db.domains.users.roles_admin as db_user_admin
import db.domains.users.roles_teacher as db_user_teacher
import db.domains.users.class_tracking as db_user_tracking_class
import db.domains.kakaowork.user_link as db_user_kakaowork
import db.domains.users.settings as db_user_settings
import db.domains.auth.qr as db_qr
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
    session_info = db_session.get_info(session['session_id'])
    session_info_list = db_session.get_list_info(session['session_id'])
    is_admin = db_user_admin.is_admin(session_info.data['user_info']['uuid']).success
    is_teacher = db_user_teacher.is_teacher(session_info.data['user_info']['uuid']).success
    this_year_class = db_user_tracking_class.get_this_year_class(session_info.data['user_info']['uuid'])
    kakaowork_info = db_user_kakaowork.get_info(session_info.data['user_info']['uuid'])
    
    notification_settings = None
    if kakaowork_info.success:
        notification_result = db_user_settings.get_multiple_settings(
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
    session_info = db_session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    gen_qr_result = db_qr.generate_qr(user_uuid)
    if not gen_qr_result.success:
        return utils.ResultDTO(code=400, message=f"QR 코드 생성 실패: {gen_qr_result.detail}", success=False).to_response()
    
    return utils.ResultDTO(code=200, message="QR코드를 발급했습니다.", data=gen_qr_result.data['value'], success=True).to_response()

@user_bp.route('/user_list', methods=['GET'])
@auth.login_required
def user_list():
    user_list = db_user.get_all_info()
    if not user_list.success:
        return utils.ResultDTO(code=400, message=user_list.detail, success=False).to_response()
    return utils.ResultDTO(code=200, message='유저 목록을 조회했습니다.', data=user_list.data, success=True).to_response()

@user_bp.route('/create_class_info', methods=['POST'])
@auth.login_required
def create_class_info():
    session_info = db_session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db_user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return utils.ResultDTO(code=400, message='교사 계정은 학급 정보를 생성할 수 없습니다.').to_response()
    
    data = request.get_json()
    if not data: return utils.ResultDTO(code=400, message='요청 데이터가 없습니다.').to_response()
    
    grade = data.get('grade')
    _class = data.get('class')
    number = data.get('number')
    
    if not all([grade, _class, number]): return utils.ResultDTO(code=400, message='누락된 정보를 확인하십시오.').to_response()
    if not (1 <= grade <= 3):   return utils.ResultDTO(code=400, message='학년은 1~3 사이여야 합니다.').to_response()
    if not (1 <= _class <= 10): return utils.ResultDTO(code=400, message='반은 1~10 사이여야 합니다.').to_response()
    if not (1 <= number <= 30): return utils.ResultDTO(code=400, message='번호는 1~30 사이여야 합니다.').to_response()

    current_year = datetime.now().year
    
    duplicate_check = db_user_tracking_class.check_duplicate_class(current_year, grade, _class, number)
    if duplicate_check.success and duplicate_check.data:
        return utils.ResultDTO(code=400, message='같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.').to_response()
    
    result = db_user_tracking_class.create(user_uuid, current_year, grade, _class, number)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"생성에 실패했습니다: {result.detail}").to_response()

    return utils.ResultDTO(code=200, message='학급 정보가 성공적으로 생성되었습니다.', success=True).to_response()

@user_bp.route('/update_class_info', methods=['POST'])
@auth.login_required
def update_class_info():
    session_info = db_session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db_user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return utils.ResultDTO(code=400, message='교사 계정은 학급 정보 업데이트가 불필요합니다.').to_response()
    
    data = request.get_json()
    if not data:
        return utils.ResultDTO(code=400, message='요청 데이터가 없습니다.').to_response()
    
    grade = data.get('grade')
    _class = data.get('class')
    number = data.get('number')
    
    if not all([grade, _class, number]):
        return utils.ResultDTO(code=400, message='학년, 반, 번호를 모두 입력해주세요.').to_response()
    
    if not (1 <= grade <= 3):
        return utils.ResultDTO(code=400, message='학년은 1~3 사이의 값이어야 합니다.').to_response()
    
    if not (1 <= _class <= 10):
        return utils.ResultDTO(code=400, message='반은 1~10 사이의 값이어야 합니다.').to_response()
    
    if not (1 <= number <= 30):
        return utils.ResultDTO(code=400, message='번호는 1~30 사이의 값이어야 합니다.').to_response()
        
    year_update_check = db_user_tracking_class.check_year_update_needed(user_uuid)
    if not year_update_check.success or not year_update_check.data:
        return utils.ResultDTO(code=400, message=f'업데이트 실패: {year_update_check.detail}').to_response()
    
    if year_update_check.data.get('needs_graduation'):
        return utils.ResultDTO(code=400, message='졸업 상태로 업데이트가 필요합니다.').to_response()
    
    expected_grade = year_update_check.data.get('new_grade')
    if grade != expected_grade:
        return utils.ResultDTO(code=400, message=f'해당 계정의 올해 올바른 학년은 {expected_grade}학년입니다.').to_response()
    
    current_year = datetime.now().year
    
    duplicate_check = db_user_tracking_class.check_duplicate_class(current_year, grade, _class, number)
    if duplicate_check.success and duplicate_check.data:
        return utils.ResultDTO(code=400, message='같은 년도에 동일한 학년, 반, 번호를 가진 학생이 이미 존재합니다.').to_response()
    
    result = db_user_tracking_class.update_for_new_year(user_uuid, current_year, grade, _class, number, False)
    if not result.success:
        return utils.ResultDTO(code=400, message=f"업데이트에 실패했습니다: {result.detail}").to_response()
    
    return utils.ResultDTO(code=200, message='학급 정보가 성공적으로 업데이트되었습니다.').to_response()

@user_bp.route('/update_graduation', methods=['POST'])
@auth.login_required
def update_graduation():
    session_info = db_session.get_info(session['session_id'])
    user_uuid = session_info.data['user_info']['uuid']
    
    is_teacher = db_user_teacher.is_teacher(user_uuid).success
    if is_teacher:
        return utils.ResultDTO(code=400, message='교사 계정은 학급 정보 업데이트가 불필요합니다.').to_response()
    
    year_update_check = db_user_tracking_class.check_year_update_needed(user_uuid)
    if not year_update_check.success or not year_update_check.data:
        return utils.ResultDTO(code=400, message=f'업데이트 실패: {year_update_check.detail}').to_response()
    
    if not year_update_check.data.get('needs_graduation'):
        return utils.ResultDTO(code=400, message=f'졸업 상태로 업데이트가 불가능합니다. 학년정보를 업데이트하십시오.').to_response()
    
    current_year = datetime.now().year
    
    result = db_user_tracking_class.update_for_new_year(user_uuid, current_year, None, None, None, True)
    
    if not result.success:
        return utils.ResultDTO(code=400, message=f'업데이트에 실패했습니다: {result.detail}').to_response()
    return utils.ResultDTO(code=400, message=result.detail).to_response()

@user_bp.route('/all_logout', methods=['GET', 'POST'])
@auth.login_required
def all_logout():
    if request.method == 'POST':
        # AJAX 요청으로 모든 세션 로그아웃
        result = db_user.logout_all(session['session_id'])
        if not result.success:
            return utils.ResultDTO(code=400, message=result.detail, success=False).to_response()
        
        return utils.ResultDTO(code=200, message='모든 세션에서 로그아웃되었습니다.', success=True).to_response()
    else:
        # GET 요청으로 모든 세션 로그아웃 후 로그인 페이지로 리다이렉트
        result = db_user.logout_all(session['session_id'])
        if not result.success:
            flash(result.detail, 'danger')
            return redirect(url_for('router.user.dashboard'))

        session.clear()
        
        # 응답 생성
        response = redirect(url_for('router.user.signin'))
        
        # QR 관련 쿠키 삭제 (도메인과 경로 명시)
        response.delete_cookie('qr_code_data', path='/', domain=None)
        response.delete_cookie('qr_issue_time', path='/', domain=None)
        
        # 추가 보안을 위한 일반적인 세션 관련 쿠키들도 삭제
        response.delete_cookie('session', path='/', domain=None)
        response.delete_cookie('csrf_token', path='/', domain=None)
        response.delete_cookie('remember_token', path='/', domain=None)
        
        flash('모든 세션에서 로그아웃되었습니다.', 'success')
        return response

@user_bp.route('/remote_logout', methods=['POST'])
@auth.login_required
def remote_logout():
    session_index = request.get_json().get('index')
    session_list_info = db_session.get_list_info(session['session_id'])
    if not session_list_info.data:
        return utils.ResultDTO(code=400, message='세션 정보를 찾을 수 없습니다.', success=False).to_response()
    
    if 0 > session_index or session_index >= len(session_list_info.data['session_list_info']):
        return utils.ResultDTO(code=400, message='세션 인덱스가 범위를 벗어났습니다.', success=False).to_response()
    
    target_session = session_list_info.data['session_list_info'][session_index]
    if not target_session:
        return utils.ResultDTO(code=400, message='세션 정보를 찾을 수 없습니다.', success=False).to_response()

    result = db_user.logout(target_session['id'])
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
    result = db_user.logout(session_id)
    if not result.success:
        flash(result.detail, 'danger')
        return redirect(url_for('router.index'))

    session.clear()
    
    response = redirect(url_for('router.user.signin'))
    
    response.delete_cookie('qr_code_data', path='/', domain=None)
    response.delete_cookie('qr_issue_time', path='/', domain=None)
    
    response.delete_cookie('session', path='/', domain=None)
    response.delete_cookie('csrf_token', path='/', domain=None)
    response.delete_cookie('remember_token', path='/', domain=None)
    
    flash('로그아웃되었습니다.', 'success')
    return response

@user_bp.route('/signin', methods=['GET', 'POST'])
@auth.not_login_required
def signin():
    if request.method == 'POST':
        id = request.form.get('id', type=str)
        password = request.form.get('password', type=str)
        user_agent = request.headers.get('User-Agent', 'Unknown', type=str)
        result = db_user.login(id, password, user_agent)
        if not result.success:
            flash(result.detail, 'danger')
            return render_template('user/signin.html')

        session['session_id'] = result.data['session_id']
        return redirect(url_for('router.index'))

    if request.cookies.get('skip_welcome', default=False, type=bool) == False:
        return render_template('welcome.html')
    return render_template('user/signin.html')

@user_bp.route('/signup', methods=['GET', 'POST'])
@auth.not_login_required
def signup():
    if request.method == 'POST':
        # Teacher Signup
        if request.form.get('role') == 'teacher':
            result = db_user.create_teacher(
                id=request.form.get('id', type=str),
                password=request.form.get('password', type=str),
                name=request.form.get('name', type=str)
            )
            if not result.success:
                flash(result.detail, 'danger')
                return render_template('user/signup.html')
        
        # Normal Signup
        else:
            # 클라이언트 측 유효성 검사 강화
            grade = request.form.get('grade', type=int)
            _class = request.form.get('class', type=int)
            number = request.form.get('number', type=int)
            
            # 학년, 반, 번호 유효성 검사
            if not grade or not _class or not number:
                flash('학년, 반, 번호를 모두 입력해주세요.', 'danger')
                return render_template('user/signup.html')
            
            if not (1 <= grade <= 3):
                flash('학년은 1~3 사이의 값이어야 합니다.', 'danger')
                return render_template('user/signup.html')
            
            if not (1 <= _class <= 10):
                flash('반은 1~10 사이의 값이어야 합니다.', 'danger')
                return render_template('user/signup.html')
            
            if not (1 <= number <= 30):
                flash('번호는 1~30 사이의 값이어야 합니다.', 'danger')
                return render_template('user/signup.html')
            
            result = db_user.create(
                id=request.form.get('id', type=str),
                password=request.form.get('password', type=str),
                name=request.form.get('name', type=str),
                grade=grade,
                _class=_class,
                number=number
            )
            if not result.success:
                flash(result.detail, 'danger')
                return render_template('user/signup.html')
        
        flash('가입 요청되었습니다. 관리자 승인 후 로그인 가능합니다.', 'success')
        return redirect(url_for('router.user.signin'))

    return render_template('user/signup.html')
