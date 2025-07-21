from flask import Blueprint, render_template
import modules.db.user as db_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/signup')
def signup():
    # 회원가입 처리 로직
    return render_template('user/signup.html')

@user_bp.route('/signin')
def signin():
    # 로그인 처리 로직
    return render_template('user/signin.html')