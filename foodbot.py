import os
# from dotenv import load_dotenv
# from pathlib import Path
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage
)
from model.ifoodie import IFoodie

# env_path = Path('~/automation/config/line/.env').expanduser()
# load_dotenv(env_path)

acc_code = os.environ['CYBER_SVC_TOKEN']
secr = os.environ['CYBER_SVC_SECRET']

line_bot_api = LineBotApi(acc_code)  # 你的LINE存取代碼
handler = WebhookHandler(secr)  # 你的LINE頻道密鑰

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Line Bot!'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.default()
def default(event):
    print('捕捉到事件：', event)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    txt = event.message.text
    food = IFoodie(txt)  #使用者傳入的訊息文字
    # print(food.scrape())  # 回應前五間最高人氣且營業中的餐廳訊息文字
    reply_txt = TextSendMessage(text=food.scrape())
    reply_stk = StickerSendMessage(
        package_id=3,
        sticker_id=233 )
    line_bot_api.reply_message(
        event.reply_token, 
        [reply_txt, reply_stk]
    )

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    pid = event.message.package_id
    sid = event.message.sticker_id
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=pid, sticker_id=sid)
    )

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True, port=80)

    