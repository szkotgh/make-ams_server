from flask import Blueprint, render_template, session
import middleware.auth as auth
from router.user import user_bp
from router.device import device_bp
from router.admin import admin_bp
from router.pwa import pwa_bp
from router.site_asset import site_asset_bp
import db.session
import db.user_admin
import db.user_teacher
import db.user_settings
import db.user_tracking_class

router_bp = Blueprint('router', __name__)

router_bp.register_blueprint(user_bp)
router_bp.register_blueprint(device_bp)
router_bp.register_blueprint(admin_bp)
router_bp.register_blueprint(pwa_bp)
router_bp.register_blueprint(site_asset_bp)

@router_bp.route('/', methods=['GET'])
@auth.login_required
def index():
    session_info = db.session.get_info(session['session_id'])
    is_admin = db.user_admin.is_admin(session_info.data['user_info']['uuid']).success
    is_teacher = db.user_teacher.is_teacher(session_info.data['user_info']['uuid']).success
    
    first_login = db.user_settings.get_setting(session_info.data['user_info']['uuid'], 'first_login', True)
    if first_login:
        db.user_settings.set_setting(session_info.data['user_info']['uuid'], 'first_login', False, 'boolean')
    
    year_update_needed = None
    if not is_teacher:
        year_update_check = db.user_tracking_class.check_year_update_needed(session_info.data['user_info']['uuid'])
        if year_update_check.success:
            year_update_needed = year_update_check.data
        
        if not year_update_needed:
            force_update_check = db.user_tracking_class.force_update_for_missing_year(session_info.data['user_info']['uuid'])
            if force_update_check.success:
                year_update_needed = force_update_check.data
    
    return render_template('index.html', 
                         is_admin=is_admin, 
                         is_teacher=is_teacher, 
                         is_first_login=first_login,
                         year_update_needed=year_update_needed,
                         current_user=session_info.data['user_info'])

