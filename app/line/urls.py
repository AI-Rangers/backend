from fastapi import APIRouter, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from . import message_event, user_event, config
import circlegan
from google.cloud import storage


line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

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

    # 發送風格轉換的圖片給用戶
    img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.reply_message(event.reply_token, img_message)