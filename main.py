from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageAction
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import User

app=Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# test.db (DB) と連結するための object である engine を作り、DB を session に代入する。
# engine = create_engine('sqlite:///linebot.db')
engine = create_engine('postgresql://fkvmwrougwmslh:1a7671b9b51229d5cc0dcd7e1d8b18c3323511a094ae1984e93af0e64f32b407@ec2-52-21-0-111.compute-1.amazonaws.com:5432/d7j3ihuk920d4i')
session = sessionmaker(bind=engine)()


@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    status_msg = profile.status_message
    if status_msg != "None":
        # LINEに登録されているstatus_messageが空の場合は、"なし"という文字列を代わりの値とする
        status_msg = "なし"
    
    messages = TemplateSendMessage(alt_text="Buttons template",
                                    template=ButtonsTemplate(
                                        thumbnail_image_url=profile.picture_url,
                                        title=profile.display_name,
                                        text=f"User Id: {profile.user_id[:5]}...\n"
                                            f"Status Message: {status_msg}",
                                        actions=[MessageAction(label="成功", text="次は何を実装しましょうか？")]))

    #データベースに保存
    # name = profile.display_name
    # user_id = profile.user_id
    name = "master"
    user_id = "sds00011"
    new_user = User(name=name, user_id=user_id)
    session.add(new_user)
    session.commit()

    line_bot_api.reply_message(event.reply_token, messages=messages)
    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)