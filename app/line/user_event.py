# import json
# from . import config
# from linebot import LineBotApi
# from linebot.models import ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage 
# from linebot.models.template import *

# line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

# def detect_json_array_to_new_message_array(fileName):

#     #開啟檔案，轉成json
#     with open(fileName) as f:
#         jsonArray = json.load(f)
    
#     # 解析json
#     returnArray = []
#     for jsonObject in jsonArray:

#         # 讀取其用來判斷的元件
#         message_type = jsonObject.get('type')
        
#         if message_type == 'text':
#             returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
#         elif message_type == 'imagemap':
#             returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
#         elif message_type == 'template':
#             returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
#         elif message_type == 'image':
#             returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
#         elif message_type == 'location':
#             returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))

#     return returnArray



def handle_follow(event) -> None:
    """Event - User follow LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    user_id = event.source.user_id
    print(f"User follow! user_id: {user_id}")

def handle_unfollow(event) -> None:
    """Event - User ban LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    user_id = event.source.user_id
    print(f"User leave! user_id: {user_id}")
