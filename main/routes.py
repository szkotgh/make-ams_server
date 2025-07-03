from flask import Blueprint, render_template
from . import main_bp
from utils.auth import get_current_user, login_required

@main_bp.route('/')
@login_required
def main():
    user = get_current_user()
    return render_template('main.html', user=user) 