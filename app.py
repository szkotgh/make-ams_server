import os
from dotenv import load_dotenv
from flask import Flask, send_file
from router import router_bp
import modules.utils as utils

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.register_blueprint(router_bp)

# Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return utils.ResultDTO(404, 'Page not found').to_response()

@app.errorhandler(405)
def method_not_allowed(e):
    return utils.ResultDTO(405, 'Method not allowed').to_response()

if __name__ == '__main__':
    app.run(os.environ['SERVER_IP'], os.environ['SERVER_PORT'], debug=True)