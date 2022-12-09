from fastapi import APIRouter, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot.models import TextSendMessage

from . import message_event, user_event, config
from ..ai.circlegan import style_transfer
from ..ai.styletransfer import styleTransfer
from google.cloud import storage
from pathlib import Path


line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)
firebase_key = config.SERVICE_ACCOUNT_KEY
line_app = APIRouter()

@line_app.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot webhook callback
    Args:
        request (Request): Request Object.
    Raises:
        HTTPException: Invalid Signature Error
    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    
    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"

@handler.add(FollowEvent)
def handle_follow(event) -> None:
    """Event - User follow LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    user_event.handle_follow(event=event)
    print('follow', event)
    # 取得使用者個人資訊
    profile = line_bot_api.get_profile(event.source.user_id)
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    # 回傳歡迎訊息
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(f'Hi, {profile.display_name}'))

@handler.add(UnfollowEvent)
def handle_unfollow(event) -> None:
    """Event - User ban LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    user_event.handle_unfollow(event=event)

@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event) -> None:
    """Event - User sent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    message_event.handle_message(event=event)

# 接收事件 PostbackEvent
@handler.add(event=PostbackEvent)
def handle_message(event):
    print('postback', event.postback)
    print('----')
    print('params', event.postback.params)
    print('data', event.postback.data)



# 使用者傳送圖片
@handler.add(event=MessageEvent, message=ImageMessage)
def handle_message(event):
    print('image', event)
    # 取得訊息id
    message_id = event.message.id
    # 透過訊息id取得 line server上面的檔案
    message_content = line_bot_api.get_message_content(message_id)
    # 將圖片存到伺服器
    with open(Path(f"static/line_imgs/{message_id}.jpg").absolute(), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # 發送風格轉換的圖片給用戶
    origin_img_folder = "static/line_imgs/"
    styled_img_folder = "static/styled/"
    img_name = f"{message_id}.jpg"
    selected_style = "pink_style_1800.t7"
    # processed_image = styleTransfer(origin_img_folder, styled_img_folder, img_name, selected_style)
    # processed_image_path = f"{styled_img_folder}{processed_image}"

    processed_image = style_transfer(f"{origin_img_folder}{img_name}")
    processed_image_path = f"{styled_img_folder}{img_name}"
    processed_image.save(processed_image_path)
 
    print('processed_image_path')
    print(processed_image_path)

    # img_url = f"https://f328-118-150-160-200.jp.ngrok.io/{processed_image_path}"
    img_url = f"https://api.puff.tw/{processed_image_path}"
    print(f"{img_url}")
    img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.reply_message(event.reply_token, img_message)

"""
# 暫時註解
# cycle_gan_model.load_weights 載入模型會有錯誤
# OSError: Unable to open file (file signature not found)"

@handler.add(MessageEvent, message = ImageMessage)
def handle_image_message(event):
    image_blob = line_bot_api.get_message_content(event.message.id)
    raw_image_path = event.message.id + '.png'
    with open(raw_image_path, 'wb') as fd:
        for chunk in image_blob.iter_content():
            fd.write(chunk)

    # 使用CircleGan對圖片進行風格轉換，並保存下來
    style_image = circlegan.style_transfer(raw_image_path)
    style_image_path = event.message.id + "_transfered.png"
    style_image.save(style_image_path)

    # 將風格轉換的圖片上傳到 cloud storage
    storage_client = storage.Client()
    bucket_name = 'linebot-tibame01-storage'
    destination_blob_name = f'{event.source.user_id}/image/{event.message.id}.png'
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(style_image_path)

    img_url = ""

    # 發送風格轉換的圖片給用戶
    img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.reply_message(event.reply_token, img_message)

"""


# import firebase_admin 
# from firebase_admin import credentials 
# from firebase_admin import firestore 

# p = Path(f"{firebase_key}").absolute()

# print("p")
# print(p)


# cred = credentials.Certificate(f"{firebase_key}")
# firebase_admin.initialize_app(cred)
# firestore_client = firestore.client()

