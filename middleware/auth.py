from flask import session, redirect, url_for, request, flash
from functools import wraps
import db.session
import db.user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Session
        if "session_id" not in session:
            flash("로그인이 필요합니다.", "danger")
            return redirect(url_for("router.user.signin"))
        # Validate Session
        session_info = db.session.get_info(session["session_id"])
        if not session_info.success:
            session.clear()
            flash(session_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not session_info.data['session_info']['is_active']:
            session.clear()
            flash("만료된 세션입니다. 다시 로그인하세요.", "danger")
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
        session_info = db.session.get_info(session["session_id"])
        if not session_info.success:
            session.clear()
            flash(session_info.detail, "danger")
            return redirect(url_for("router.user.signin"))
        if not session_info.data['session_info']['is_active']:
            session.clear()
            flash("만료된 세션입니다. 다시 로그인하세요.", "danger")
            return redirect(url_for("router.user.signin"))
        # Check Admin
        if not db.user.is_admin(session_info.data['user_info']['uuid']).success:
            flash("관리자 권한이 필요합니다.", "danger")
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
