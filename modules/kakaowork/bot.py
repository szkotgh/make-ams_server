import requests
import modules.utils as utils

def bot_info(app_key) -> utils.ResultDTO:
    url = "https://api.kakaowork.com/v1/bots.info"
    try :
        result = requests.get(url, headers={"Authorization": f"Bearer {app_key}"})
        result_json = result.json()
        success = result_json.get("success", False)
        bot_info = result_json.get("info", None)
        if not success or not bot_info:
            return utils.ResultDTO(code=400, message="봇 정보를 가져올 수 없습니다.", success=False)
        return utils.ResultDTO(code=200, message="봇 정보를 가져왔습니다.", success=True, data=bot_info)
    except:
        return utils.ResultDTO(code=400, message="봇 정보를 가져올 수 없습니다.", success=False)