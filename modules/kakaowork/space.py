import requests
import modules.utils as utils

def space_info(app_key) -> utils.ResultDTO:
    url = "https://api.kakaowork.com/v1/spaces.info"
    try :
        result = requests.get(url, headers={"Authorization": f"Bearer {app_key}"})
        result_json = result.json()
        space_info = result_json.get("space", None)
        if not space_info:
            return utils.ResultDTO(code=400, message="스페이스 정보를 가져올 수 없습니다.", success=False)
        return utils.ResultDTO(code=200, message="스페이스 정보를 가져왔습니다.", success=True, data=space_info)
    except:
        return utils.ResultDTO(code=400, message="오류가 발생했습니다.", success=False)