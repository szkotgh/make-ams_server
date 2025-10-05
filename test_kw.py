import modules.kakaowork.send_message as kakaowork_send_message

app_key = "87d4fca2.bd7624ded45a4b38a2aadcca72ec732f"
kw_id = "10980848"

print(kakaowork_send_message.send_login_notification(app_key, kw_id, "이건희", "gi6791991").success)