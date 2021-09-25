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

line_bot_api = LineBotApi('F3wxw5f1SzY7d5DgxkJPwW5qdVWI/iDCZ0+Kj/OHvrviNYBd2WH+qm8rLANu/x/xsLXRijx5qR/NTDfBrCJtukltAum5r3SP2hX5ClN8A671UjlUiqisf1SlaWH4Wom1FKibFtLcdV4rLyzK0aZSmQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c220d0e085bf26cf5dba48f2eccf928e')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
