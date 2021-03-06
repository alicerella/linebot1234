#app.py
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('2FyPEMQbaWe7KTl2R08r7ce35x4WOevW7Kjxsp/qroD43XLpfHzhs9eU6S7OoGnfZ6eFbmRuBsovLp7fX+sfseVceLv9qIHr08CoYjjKM6zu7jSjZOlA8YXpdvHOKsFUoqgJQDPbbgMFM4JxpXPa7wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ea52b45fc5c7e34d924aaae2d9f1f620')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
