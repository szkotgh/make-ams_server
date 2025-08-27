import requests
from dataclasses import dataclass
from db import DBResultDTO

@dataclass
class KWUserDTO:
    id: str
    space_id: str
    name: str
    nickname: str
    avatar_url: str
    department: str
    identifications: str
    position: str
    responsibility: str
    status: str
    
    def to_dict(self):
        return {key: getattr(self, key) for key in self.__dataclass_fields__.keys()}

def get_users(app_key):
    url = "https://api.kakaowork.com/v1/users.list"
    params = {
        "limit": 100, # Max Query Limit
        "status_in": "activated"
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {app_key}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = KWUserDTO.__init__.__code__.co_varnames[1:KWUserDTO.__init__.__code__.co_argcount]
        users = []
        for user in result_json.get("users", []):
            filtered_user = {key: user.get(key, None) for key in dto_keys}
            users.append(KWUserDTO(**filtered_user))
        return DBResultDTO(success=True, detail="카카오워크 유저 목록을 조회했습니다.", data=users)
    return DBResultDTO(success=False, detail="카카오워크 유저 목록을 조회할 수 없습니다.")

def find_user_by_id(app_key, id):
    url = "https://api.kakaowork.com/v1/users.info"
    params = {
        "user_id": id
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {app_key}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = KWUserDTO.__init__.__code__.co_varnames[1:KWUserDTO.__init__.__code__.co_argcount]
        user = result_json.get("user", {})
        filtered_user = {key: user.get(key, None) for key in dto_keys}
        return DBResultDTO(success=True, detail="카카오워크 유저 정보를 조회했습니다.", data=KWUserDTO(**filtered_user))
    return DBResultDTO(success=False, detail="카카오워크 유저 정보를 조회할 수 없습니다.")

def find_user_by_email(app_key, email):
    url = "https://api.kakaowork.com/v1/users.find_by_email"
    params = {
        "email": email
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {app_key}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = KWUserDTO.__init__.__code__.co_varnames[1:KWUserDTO.__init__.__code__.co_argcount]
        user = result_json.get("user", {})
        filtered_user = {key: user.get(key, None) for key in dto_keys}
        return DBResultDTO(success=True, detail="카카오워크 유저 정보를 조회했습니다.", data=KWUserDTO(**filtered_user))
    print(result_json)
    return DBResultDTO(success=False, detail="카카오워크 유저 정보를 조회할 수 없습니다.")

