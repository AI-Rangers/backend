from typing import Text
from linebot.models import TemplateSendMessage
from linebot.models.template import ButtonsTemplate
from linebot.models.actions import CameraAction, CameraRollAction
from ..models.message_request import MessageRequest
from ..skills import add_skill

@add_skill('@style_photo')
def get(message_request: MessageRequest):
    camara = TemplateSendMessage(
            alt_text='Actions',
            template=ButtonsTemplate(
                title='農地圖片風格轉換',
                text='請給一張照片',
                actions=[
                    CameraAction(label='開啟相機'),
                    CameraRollAction(label='開啟相簿')
                ]
            )
    )

    return [
        camara
    ]

