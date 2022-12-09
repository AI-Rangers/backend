from typing import Text
from linebot.models import TextSendMessage
from ..models.message_request import MessageRequest
from ..skills import add_skill

# 重複使用者說的話
@add_skill('{not_match}')
def get(message_request: MessageRequest):
    return [
        TextSendMessage(text=f'{message_request.message}')
    ]
