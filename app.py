import os
from dotenv import load_dotenv
from flask import Flask
from app import app_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']

app.register_blueprint(app_bp)

if __name__ == '__main__':
    app.run(os.environ['SERVER_IP'], os.environ['SERVER_PORT'], debug=True)