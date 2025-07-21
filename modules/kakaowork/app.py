import time
from dotenv import load_dotenv
import user as kw_user
import conversation as kw_conversation

load_dotenv()

for index, user in enumerate(kw_user.get_users()):
    print(index, f"ID: {user.id}, Space ID: {user.space_id} Name: {user.name}, {user.department} | {user.responsibility}, url: {user.avatar_url}, identi: {user.identifications}")
print()

user_class = kw_user.find_user_by_email("me@szk.kr")
if not user_class:
    print("User not found")
else:
    print(f"User ID: {user_class.id}, Name: {user_class.name}, Department: {user_class.department}, Responsibility: {user_class.responsibility}, Status: {user_class.status}, identi: {user_class.identifications}")

    conversation_id = kw_conversation.create_conversation(user_class.id)
    print(kw_conversation.send_message_link_account(conversation_id, user_class.name, user_class.identifications['email']))