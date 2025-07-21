import os
import requests
from dataclasses import dataclass

@dataclass
class UserDTO:
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

def get_users() -> list[UserDTO]:
    url = "https://api.kakaowork.com/v1/users.list"
    params = {
        "limit": 100,
        "status_in": "activated"
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {os.environ['KW_APP_KEY']}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = UserDTO.__init__.__code__.co_varnames[1:UserDTO.__init__.__code__.co_argcount]
        users = []
        for user in result_json.get("users", []):
            filtered_user = {key: user.get(key, None) for key in dto_keys}
            users.append(UserDTO(**filtered_user))
        return users
    return []

def get_user(id) -> UserDTO | None:
    url = "https://api.kakaowork.com/v1/users.info"
    params = {
        "user_id": id
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {os.environ['KW_APP_KEY']}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = UserDTO.__init__.__code__.co_varnames[1:UserDTO.__init__.__code__.co_argcount]
        user = result_json.get("user", {})
        filtered_user = {key: user.get(key, None) for key in dto_keys}
        return UserDTO(**filtered_user)
    return None

def find_user_by_email(email) -> UserDTO | None:
    url = "https://api.kakaowork.com/v1/users.find_by_email"
    params = {
        "email": email
    }
    result = requests.get(url, params=params, headers={"Authorization": f"Bearer {os.environ['KW_APP_KEY']}"})
    result_json = result.json()
    
    if result_json.get("success", False):
        dto_keys = UserDTO.__init__.__code__.co_varnames[1:UserDTO.__init__.__code__.co_argcount]
        user = result_json.get("user", {})
        filtered_user = {key: user.get(key, None) for key in dto_keys}
        filtered_user["identifications"] = {"email": email}
        return UserDTO(**filtered_user)
    return None

