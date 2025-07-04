import os
from dotenv import load_dotenv
from flask import Flask
from login.routes import login_bp
from main.routes import main_bp
from flask_wtf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']
csrf = CSRFProtect(app)

app.register_blueprint(login_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run('localhost', 47230, debug=True)