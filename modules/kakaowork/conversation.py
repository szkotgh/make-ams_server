import os
import requests
import modules.utils as utils

def create_conversation(app_key, user_id) -> utils.ResultDTO:
    url = "https://api.kakaowork.com/v1/conversations.open"
    data = {
        "user_id": user_id
    }
    result = requests.post(url, headers={"Authorization": f"Bearer {app_key}"}, json=data)
    result_json = result.json()
    
    if result_json.get("success", False):
        return result_json['conversation']['id']
    return None

def send_message(app_key, kw_id, text, blocks=None) -> utils.ResultDTO:
    conversation_id = create_conversation(app_key, kw_id)
    if not conversation_id:
        return utils.ResultDTO(code=400, message="카카오워크 대화방을 생성할 수 없습니다.", success=False)
    
    url = "https://api.kakaowork.com/v1/messages.send"
    data = {
        "conversation_id": conversation_id,
        "text": text,
        "blocks": blocks or []
    }
    result = requests.post(url, headers={"Authorization": f"Bearer {app_key}"}, json=data)
    if result.status_code != 200:
        return utils.ResultDTO(code=400, message="메시지 전송에 실패했습니다.", success=False)
    return utils.ResultDTO(code=200, message="메시지를 전송했습니다.", success=True)

