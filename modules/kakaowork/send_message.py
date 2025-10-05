from modules import utils
from modules.kakaowork.conversation import send_message

def send_login_notification(app_key, kw_id, user_name, user_id) -> utils.ResultDTO:
    text = f"[로그인] {user_name}님, 방금 AMS에 로그인하였습니다."
    blocks = [
        {
            "type":"header",
            "text":"로그인 알림",
            "style": "blue"
        },
        {
            "type":"text",
            "text":f"{user_name}님, AMS에 로그인하였습니다.",
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{user_id}"
            },
            "term": "AMS ID",
            "accent": False
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{utils.get_current_datetime_str()}"
            },
            "term": "로그인 시간",
            "accent": False
        }
    ]
    
    result = send_message(app_key, kw_id, text, blocks)
    if not result.success:
        return result
    return utils.ResultDTO(code=200, message="메시지를 전송했습니다.", success=True)

def send_link_kakaowork_notification(app_key, kw_id, user_name, user_id) -> utils.ResultDTO:
    text = f"[계정 연동] {user_name}님, 카카오워크 계정과 연동이 완료되었습니다."
    blocks = [
        {
            "type":"header",
            "text":"계정 연동",
            "style": "blue"
        },
        {
            "type":"text",
            "text":f"{user_name}님, AMS 계정과 카카오워크\n계정 연동이 완료되었습니다.",
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{user_id}"
            },
            "term": "AMS ID",
            "accent": False
        }
    ]

    result = send_message(app_key, kw_id, text, blocks)
    if not result.success:
        return result
    return utils.ResultDTO(code=200, message="메시지를 전송했습니다.", success=True)

def send_unlink_kakaowork_notification(app_key, kw_id, user_name, user_id) -> utils.ResultDTO:
    text = f"[계정 연동 해제] {user_name}님, AMS 계정과 카카오워크 계정 연동이 해제되었습니다."
    blocks = [
        {
            "type":"header",
            "text":"카카오워크 계정 연동 해제 알림",
            "style": "yellow"
        },
        {
            "type":"text",
            "text":f"{user_name}님, AMS 계정과 카카오워크 계정 연동이 해제되었습니다.",
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{user_id}"
            },
            "term": "AMS ID",
            "accent": False
        }
    ]

    result = send_message(app_key, kw_id, text, blocks)
    if not result.success:
        return result
    return utils.ResultDTO(code=200, message="메시지를 전송했습니다.", success=True)

def send_door_access_notification(app_key, kw_id, user_name, method) -> utils.ResultDTO:
    text = f"출입 알림\n{user_name}님, {method} 인증을 통해 정상적으로 출입했습니다."
    blocks = [
        {
            "type":"header",
            "text":"출입 알림",
            "style": "green"
        },
        {
            "type":"text",
            "text":f"{user_name}님, 메이크에 출입했습니다.",
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{method}"
            },
            "term": "인증 방법",
            "accent": False
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{utils.get_current_datetime_str()}"
            },
            "term": "출입 시간",
            "accent": False
        }
    ]

    result = send_message(app_key, kw_id, text, blocks)
    if not result.success:
        return result
    return utils.ResultDTO(code=200, message="메시지를 전송했습니다.", success=True)