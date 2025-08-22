import os
from dotenv import load_dotenv
from flask import Flask, send_file
from router import router_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.register_blueprint(router_bp)

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')

@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')

# Manifest and Service Worker
@app.route('/manifest.webmanifest')
def manifest():
    return send_file('static/manifest.webmanifest')
@app.route('/sw.js')
def service_worker():
    return send_file('static/sw.js')
@app.route('/images/icon-192.png')
def icon_192():
    return send_file('static/images/icon-192.png')
@app.route('/images/icon-512.png')
def icon_512():
    return send_file('static/images/icon-512.png')

if __name__ == '__main__':
    app.run(os.environ['SERVER_IP'], os.environ['SERVER_PORT'], debug=True)