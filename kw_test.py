from dotenv import load_dotenv
import os
import requests

load_dotenv()

# 유저 리스트
result = requests.get("https://api.kakaowork.com/v1/users.list", headers={"Authorization": f"Bearer {os.getenv('KW_BOT_KEY')}"})

# 유저 정보 조회
# result = requests.get("https://api.kakaowork.com/v1/users.info?user_id=10980848", headers={"Authorization": f"Bearer {os.getenv('KW_BOT_KEY')}"})

# 채팅방 생성
# data = {
#     "user_id": "10980848"
# }
# result = requests.post("https://api.kakaowork.com/v1/conversations.open", headers={"Authorization": f"Bearer {os.getenv('KW_BOT_KEY')}"}, json=data)
# ## result: {'conversation': {'allow_invite': True, 'avatar_url': None, 'id': '860811854476288', 'name': '이건희', 'type': 'dm', 'users_count': 2}, 'is_new': True, 'success': True}

# 메세지 전송
# data = {
#     "conversation_id": "860811854476288",
#     "text": "계정연동 요청\n이건희님, MAKE-AMS 계정 연동 요청이 발생했습니다. AMS ID ams1919 위 계정에 현재 카카오워크 계정을 연동하시겠습니까? 반려 승인",
#     "blocks": [
#         {
#             "type":"header",
#             "text":"계정연동 요청",
#             "style": "blue"
#         },
#         {
#             "type":"text",
#             "text":"이건희님, MAKE-AMS 계정 연동 요청이 발생했습니다.",
#             "inlines": [
#                 {
#                     "type": "styled",
#                     "text": "이건희",
#                     "bold": True
#                 },
#                 {
#                     "type": "styled",
#                     "text": "님, MAKE-AMS 계정 연동 요청이 발생했습니다.",
#                 }
#             ]
#         },
#         {
#             "type":"description",
#             "content": {
#                 "type": "text",
#                 "text": "ams1919"
#             },
#             "term": "AMS ID",
#             "accent": False
#         },
#         {
#             "type":"text",
#             "text":"위 계정과 현재 카카오워크 계정을 연동하시겠습니까?",
#         },
#         {
#             "type": "action",
#             "elements": [
#                 {
#                     "type": "button",
#                     "text": "반려",
#                     "style": "default",
#                     "action": {
#                         "type": "submit_action",
#                         "name": "account_connect",
#                         "value": "reject"
#                     }
#                 },
#                 {
#                     "type": "button",
#                     "text": "승인",
#                     "style": "primary",
#                     "action": {
#                         "type": "submit_action",
#                         "name": "account_connect",
#                         "value": "approve"
#                     }
#                 }
#             ]
#         }
#     ]
# }
# result = requests.post("https://api.kakaowork.com/v1/messages.send", headers={"Authorization": f"Bearer {os.getenv('KW_BOT_KEY')}"}, json=data)

print(result.json())