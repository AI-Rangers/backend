from linebot.models import *
from linebot.models.template import *
from linebot.models.actions import *
from ..models.message_request import MessageRequest
from . import add_skill
# from dal.azure_table_repository import AzureTableRepository
from .. import database

@add_skill('/start')
def get(message_request: MessageRequest):

    user = database.exists_member(message_request.user_id)
    # 更新使用者當前對話場景為 q1
    user[u'CurrentIntent'] = 'q1'
    database.update_member(user)

    text = TextSendMessage(text="請開始輸入三碼數字")
    
    return [
        text
    ]
