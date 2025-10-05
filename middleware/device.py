from flask import request
from functools import wraps
import modules.utils as utils


def auth_device(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        device_token = request.headers.get('Authorization')
        if not device_token or device_token != "Bearer DEVICE_HASH_TOKEN":
            return utils.ResultDTO(code=401, message="올바르지 않은 장치입니다.").to_response()
        return f(*args, **kwargs)
    return decorated_function