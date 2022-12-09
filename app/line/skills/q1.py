from linebot.models import TextSendMessage
from linebot.models.flex_message import FlexSendMessage
# from dal.azure_table_repository import AzureTableRepository
from .. import database
from ..models.message_request import MessageRequest
from . import add_skill
import uuid
import json
import os

from pathlib import Path


@add_skill('/q1')
def get(message_request: MessageRequest):
        
    # /invoice-compare 123
    msg_array = message_request.intent.split()
    number = msg_array[1]
    
    if len(number) != 3 :
        return [ TextSendMessage(text=f'您輸入的非三碼數字')]
    
    if number.isnumeric() == False:
        return [ TextSendMessage(text=f'{number} 非數字')]
    
    # 當期中獎發票
    answer = [555, 666, 777]
    
    result = int(number) in answer
    
    # 寫入資料庫
    create_event = {
            u'PartitionKey': message_request.user_id,
            u'RowKey': str(uuid.uuid1()),
            u'Result': result,
            u'CalcDate': ''
    }
    database.update_mission(create_event)
    entities = database.get_mission(message_request.user_id)

    # entities = repo.get(f"PartitionKey eq '{message_request.user_id}' and CalcDate eq ''")
    results = list(entities)
    print("results====", results)
    results_wins = list(filter(lambda c: c['Result'] == True, results))
    print("results_wins====", results_wins)

    # Flex Message (含兌獎結束的按鈕)
    flexjson = Path("app/line/line_message_json/invoice-compare.json").absolute()
    flex = json.load(
        open(flexjson, 'r', encoding='utf-8'))

    # msg = TextSendMessage(text="請開始輸入")
    if result == True:
        flex['body']['contents'][2]['text'] = f'中獎 !!! 累積中獎數: {len(results_wins)}/{len(results)}'
        msg = FlexSendMessage(alt_text='兌獎結果', contents=flex)
    else:
        flex['body']['contents'][2]['text'] = f'未中獎 ... 累積中獎數: {len(results_wins)}/{len(results)}'
        msg = FlexSendMessage(alt_text='兌獎結果', contents=flex)
    
    return[
        msg
    ]
    