from flask import Blueprint, request, render_template, redirect, url_for, make_response
from db.user import create_user, verify_user, get_user_by_id
import jwt
import datetime
from flask_wtf import CSRFProtect
from utils.auth import get_current_user, login_required

from . import login_bp

SECRET_KEY = 'your_secret_key'

@login_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user_name = request.form['user_name']
        group_id = request.form['group_id']
        join_year = request.form['join_year']
        create_user(user_id, password, user_name, group_id, join_year)
        return redirect(url_for('login.login'))
    return render_template('signin.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if verify_user(user_id, password):
            user = get_user_by_id(user_id)
            payload = {
                'user_id': user['user_id'],
                'user_name': user['user_name'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            resp = make_response(redirect(url_for('main.main')))
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template('login.html', error='로그인 실패')
    return render_template('login.html') 