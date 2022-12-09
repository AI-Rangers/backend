import re
from linebot import LineBotApi
from linebot.models import TextMessage, TextSendMessage
from . import config, database
from .models.message_request import MessageRequest
from .skills import *
from .skills import skills

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

# 比對訊息
def get_message(request: MessageRequest):
    for pattern, skill in skills.items():
        if re.match(pattern, request.intent):
            return skill(request)
    request.intent = '{not_match}'
    return skills['{not_match}'](request)

# def handle_message(event) -> None:
def handle_message(event):
    """Event - User sent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    msg_request = MessageRequest()
    msg_request.intent = event.message.text
    msg_request.message = event.message.text
    msg_request.user_id = event.source.user_id

    # reply_token = event.reply_token

    # 處理當前使用者對話場景
    current_intent = log_user(msg_request.user_id)
    if current_intent != '':
        msg_request.intent = f'{current_intent} {msg_request.message}'

    # Text message
    if isinstance(event.message, TextMessage):

        func = get_message(msg_request)
        line_bot_api.reply_message(event.reply_token, func)

        # Get user sent message
        # user_message = event.message.text

        # Reply with same message
        # messages = TextSendMessage(text=user_message)
        # line_bot_api.reply_message(reply_token=reply_token, messages=messages)

def log_user(user_id):
    print("log_user 處理當前使用者對話場景")
    print(user_id)
    # 使用者資訊儲存到 DB
    # database.add_city()
    # database.get_member()

    exists_member = database.exists_member(user_id)
    profile = line_bot_api.get_profile(user_id)

    print('len(exists_member)', len(exists_member))
 
    if len(exists_member) == 0 :
        create = {
            u'PartitionKey': 'users',
            u'RowKey': user_id,
            u'DisplayName': profile.display_name,
            u'CurrentIntent': '',
            u'money': 0
        }
        database.update_member(create)
        return ''
    else:
        intent = ''
        if exists_member.get(u'CurrentIntent') is not None:
            intent = exists_member[u'CurrentIntent']
        update = {
            u'PartitionKey': 'users',
            u'RowKey': user_id,
            u'DisplayName': profile.display_name,
            u'CurrentIntent': intent,
            u'money': exists_member.get(u'money')
        }
        database.update_member(update)
        return intent
