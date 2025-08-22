from flask import Blueprint
import middleware.auth as auth

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('', methods=['GET'])
@auth.admin_required
def index():
    return "Hello", 200