from .core import DBResultDTO, get_connection, close_connection, connect, init_db

# Import all domain modules for backward compatibility
from .domains.users import account as user
from .domains.users import verify as user_verify
from .domains.users import sessions as session
from .domains.users import settings as user_settings
from .domains.users import roles_admin as user_admin
from .domains.users import roles_teacher as user_teacher
from .domains.users import class_tracking as user_tracking_class

from .domains.auth import qr
from .domains.auth import nfc

from .domains.kakaowork import bot as kakaowork_bot
from .domains.kakaowork import user_link as user_kakaowork

from .domains.devices import devices as device
from .domains.devices import door

from .domains.logs import log

# 앱 시작 시 한 번만 초기화되도록 유지
init_db()