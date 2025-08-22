from flask import Blueprint, redirect, render_template, request, flash, url_for, session
import db.user
import middleware.auth as auth

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET'])
@auth.login_required
def dashboard():
    user_session_info = db.session.get_info(session['session_id'])
    return render_template('user/dashboard.html', user_info=user_session_info.data['user_info'])

@user_bp.route('/generate_qr', methods=['GET'])
@auth.login_required
def generate_qr():
    user_session_info = db.session.get_info(session['session_id'])
    return render_template('user/generate_qr.html', user_info=user_session_info.data['user_info'])

@user_bp.route('/logout', methods=['GET'])
@auth.login_required
def logout():
    session_id = session.get('session_id')
    if not session_id:
        flash("로그아웃에 실패했습니다.", 'danger')
        return redirect(url_for('router.index'))

    result = db.user.logout(session_id)
    if not result.success:
        flash(result.detail, 'danger')
        return redirect(url_for('router.index'))

    session.pop('session_id', None)
    flash(result.detail, 'success')
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

        # Save session_id in session
        flash(result.detail, 'success')
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
        
        flash('회원가입되었습니다.', 'success')
        return redirect(url_for('router.user.signin'))

    return render_template('user/signup.html')
