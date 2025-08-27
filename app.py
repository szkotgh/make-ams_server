import os
import atexit
from dotenv import load_dotenv
from flask import Flask, send_file, jsonify
from router import router_bp
import modules.utils as utils
import db.core as db_core

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# 세션 보안 설정
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

app.register_blueprint(router_bp)

@app.errorhandler(404)
def page_not_found(e):
    return utils.ResultDTO(404, 'not found').to_response()

@app.errorhandler(405)
def method_not_allowed(e):
    return utils.ResultDTO(405, 'method not allowed').to_response()


def cleanup_on_exit():
    try:
        db_core.cleanup_connections()
        print("Database connections cleaned up successfully.")
    except Exception as e:
        print(f"Error during database cleanup: {e}")

atexit.register(cleanup_on_exit)

if __name__ == '__main__':
    try:
        app.run(os.environ['SERVER_IP'], os.environ['SERVER_PORT'], debug=True)
    finally:
        cleanup_on_exit()