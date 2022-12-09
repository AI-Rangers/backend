from linebot.models import TextSendMessage
from ..models.message_request import MessageRequest
from . import add_skill
from datetime import date
from .. import database

@add_skill('/finish')
def get(message_request: MessageRequest):
    
    # 使用者當前兌獎紀錄撈出來
    entities = database.get_mission(message_request.user_id)
    results = list(entities)
    results_wins = list(filter(lambda c: c['Result'] == True, results))

    # 批次更新 (結算)
    database.batch_update_mission(message_request.user_id)
  
    # 更新意圖
    user = database.exists_member(message_request.user_id)
    # 更新使用者當前對話場景為 空
    user[u'CurrentIntent'] = ''
    database.update_member(user)

    text = TextSendMessage(text=f'本次兌獎結果: {len(results_wins)}/{len(results)}')

    return [
        text
    ]
