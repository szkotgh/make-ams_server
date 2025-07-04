from flask import request, redirect, url_for, g
import jwt
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')

def get_current_user():
    if hasattr(g, 'user'):
        return g.user
    token = request.cookies.get('token')
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        g.user = payload
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function 