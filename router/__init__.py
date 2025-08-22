from flask import Blueprint, render_template, session
from router.user import user_bp
from router.device import device_bp
from router.admin import admin_bp
import middleware.auth as auth
import db.user
import db.session

router_bp = Blueprint('router', __name__)

router_bp.register_blueprint(user_bp)
router_bp.register_blueprint(device_bp)
router_bp.register_blueprint(admin_bp)

@router_bp.route('/', methods=['GET'])
@auth.login_required
def index():
    user_session_info = db.session.get_info(session['session_id'])
    is_admin = db.user.is_admin(user_session_info.data['user_info']['uuid']).success

    return render_template('index.html', is_admin=is_admin)

