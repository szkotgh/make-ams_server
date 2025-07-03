from flask import Flask
from login.routes import login_bp
from main.routes import main_bp
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

app.register_blueprint(login_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run('localhost', 47230, debug=True)