import re
from linebot import LineBotApi
from linebot.models import TextMessage, TextSendMessage
from . import config
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

    # Text message
    if isinstance(event.message, TextMessage):

        func = get_message(msg_request)
        line_bot_api.reply_message(event.reply_token, func)

        # Get user sent message
        # user_message = event.message.text

        # Reply with same message
        # messages = TextSendMessage(text=user_message)
        # line_bot_api.reply_message(reply_token=reply_token, messages=messages)
