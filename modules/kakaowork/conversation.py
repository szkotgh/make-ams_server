import os
import requests

def create_conversation(user_id):
    url = "https://api.kakaowork.com/v1/conversations.open"
    data = {
        "user_id": user_id
    }
    result = requests.post(url, headers={"Authorization": f"Bearer {os.environ['KW_APP_KEY']}"}, json=data)
    result_json = result.json()
    
    if result_json.get("success", False):
        return result_json['conversation']['id']
    return None

def send_message(conversation_id, text, blocks=None):
    url = "https://api.kakaowork.com/v1/messages.send"
    data = {
        "conversation_id": conversation_id,
        "text": text,
        "blocks": blocks or []
    }
    result = requests.post(url, headers={"Authorization": f"Bearer {os.environ['KW_APP_KEY']}"}, json=data)
    return result.json()

def send_message_link_account(conversation_id, user_name, ams_id):
    text = f"계정연동 요청\n{user_name}님, MAKE-AMS 계정 연동 요청이 발생했습니다. AMS ID {ams_id} 위 계정에 현재 카카오워크 계정을 연동하시겠습니까? 반려 승인"
    blocks = [
        {
            "type":"header",
            "text":"계정연동 요청",
            "style": "blue"
        },
        {
            "type":"text",
            "text":f"{user_name}님, MAKE-AMS 계정 연동 요청이 발생했습니다.",
            "inlines": [
                {
                    "type": "styled",
                    "text": f"{user_name}",
                    "bold": True
                },
                {
                    "type": "styled",
                    "text": "님, MAKE-AMS 계정 연동 요청이 발생했습니다.",
                }
            ]
        },
        {
            "type":"description",
            "content": {
                "type": "text",
                "text": f"{ams_id}"
            },
            "term": "AMS ID",
            "accent": False
        },
        {
            "type":"text",
            "text":"위 계정과 현재 카카오워크 계정을 연동하시겠습니까?",
        },
        {
            "type": "action",
            "elements": [
                {
                    "type": "button",
                    "text": "반려",
                    "style": "default",
                    "action": {
                        "type": "submit_action",
                        "name": "account_connect",
                        "value": "reject"
                    }
                },
                {
                    "type": "button",
                    "text": "승인",
                    "style": "primary",
                    "action": {
                        "type": "submit_action",
                        "name": "account_connect",
                        "value": "approve"
                    }
                }
            ]
        }
    ]
    return send_message(conversation_id, text, blocks)