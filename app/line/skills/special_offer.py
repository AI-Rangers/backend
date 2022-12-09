from linebot.models import *
from linebot.models.template import *
from linebot.models.actions import *
from ..models.message_request import MessageRequest
from . import add_skill


@add_skill('/special_offer')
def get(message_request: MessageRequest):
    
    buttons_template_message = TemplateSendMessage(
        alt_text='是否要開始玩遊戲拿優惠?',
        template=ButtonsTemplate(
            title='您確定要開始嗎?',
            text='請點選開始',
            actions=[
                PostbackAction(
                    label='開始',
                    data='#GO'
                )
            ]
        )
    )
    
    return [
        buttons_template_message
    ]
