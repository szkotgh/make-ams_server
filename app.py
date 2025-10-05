import os
import atexit
import time
from dotenv import load_dotenv
from flask import Flask, make_response
from router import router_bp
import modules.utils as utils
import db.core as db_core
from db.domains.devices.door import start_scheduler

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = 31536000
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_NAME'] = 'sid'
app.config['SESSION_COOKIE_PATH'] = '/'

app.register_blueprint(router_bp)

@app.context_processor
def inject_moment():
    class Moment:
        def timestamp(self):
            return int(time.time())
    return dict(moment=Moment())

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
        start_scheduler()
        app.run(str(os.environ['HOST_IP']), int(os.environ['HOST_PORT']), debug=True)
    finally:
        cleanup_on_exit()