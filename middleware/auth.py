from flask import session, redirect, url_for, request, flash
from functools import wraps
import db.domains.users.sessions as db_session
import db.domains.users.account as db_user
import db.domains.users.roles_admin as db_user_admin
import db.domains.users.roles_teacher as db_user_teacher
import modules.utils as utils
import db.domains.users.verify as db_user_verify

def auth_device(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        device_token = request.headers.get('Authorization')
        if not device_token or device_token != "Bearer DEVICE_HASH_TOKEN":
            return utils.ResultDTO(code=401, message="올바르지 않은 장치입니다.").to_response()
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Session
        if "session_id" not in session:
            return redirect(url_for("router.user.signin"))
        # Validate Session
        session_info = db_session.get_info(session["session_id"])
        if not session_info.success:
            session.clear()
            return redirect(url_for("router.user.signin"))
        if not session_info.data['session_info']['is_active']:
            session.clear()
            flash("만료된 세션입니다. 다시 로그인하세요.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Verify
        verify_info = db_user_verify.get_info(session_info.data['user_info']['uuid'])
        if not verify_info.success:
            session.clear()
            flash(verify_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not verify_info.data['status'] == db_user_verify.VERIFIED:
            session.clear()
            flash("인증된 상태가 아닙니다. 다시 로그인하세요.", "danger")
            return redirect(url_for("router.user.signin"))
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Session
        if "session_id" not in session:
            flash("로그인이 필요합니다.", "danger")
            return redirect(url_for("router.user.signin"))
        # Validate Session
        session_info = db_session.get_info(session["session_id"])
        if not session_info.success:
            session.clear()
            flash(session_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not session_info.data['session_info']['is_active']:
            session.clear()
            flash("만료된 세션입니다. 다시 로그인하세요.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Verify
        verify_info = db_user_verify.get_info(session_info.data['user_info']['uuid'])
        if not verify_info.success:
            session.clear()
            flash(verify_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not verify_info.data['status'] == db_user_verify.VERIFIED:
            session.clear()
            flash("인증된 상태가 아닙니다.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Admin
        if not db_user_admin.is_admin(session_info.data['user_info']['uuid']).success:
            flash("관리자 권한이 필요합니다.", "danger")
            return redirect(url_for("router.index"))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Session
        if "session_id" not in session:
            flash("로그인이 필요합니다.", "danger")
            return redirect(url_for("router.user.signin"))
        # Validate Session
        session_info = db_session.get_info(session["session_id"])
        if not session_info.success:
            session.clear()
            flash(session_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not session_info.data['session_info']['is_active']:
            session.clear()
            flash("만료된 세션입니다. 다시 로그인하세요.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Verify
        verify_info = db_user_verify.get_info(session_info.data['user_info']['uuid'])
        if not verify_info.success:
            session.clear()
            flash(verify_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not verify_info.data['status'] == db_user_verify.VERIFIED:
            session.clear()
            flash("인증된 상태가 아닙니다.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Teacher
        if not db_user_teacher.is_teacher(session_info.data['user_info']['uuid']).success:
            flash("교사 권한이 필요합니다.", "danger")
            return redirect(url_for("router.index"))
        return f(*args, **kwargs)
    return decorated_function

def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "session_id" in session:
            flash("이미 로그인되어 있습니다.", "info")
            return redirect(url_for("router.index"))
        return f(*args, **kwargs)
    return decorated_function
