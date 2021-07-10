from flask import Flask, request, abort
import os


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

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["HYqFu+Xyf72EwDpaPzjNzPy46FJ4Jk7c3ViXdyGQbCxf0XEEfdLb/QUv9HYyxQEpH0CZvS/S7p/B2R4VsilzIO0scAG0QYHTEndSAXJE9QNEjxkLlEqM1EuQrOUhGpglWP9VXSgeK95cMzBZ1ZsoEgdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["385a2ceff0bf70423ed74c66b6df061d"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)