# SQLAlchemy はデータベース(DB)を object のように扱えるライブラリである。
# 今回は DB との連結を担当する。
# models.py の User クラスで、どのような object として扱うかを決める。
from flask import Flask,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import User

app = Flask(__name__)

# test.db (DB) と連結するための object である engine を作り、DB を session に代入する。
engine = create_engine('sqlite:///linebot.db')
session = sessionmaker(bind=engine)()

# /index2 へアクセスがあった場合に、 index2.html を返す。
@app.route("/")
def hello():
    return "first page"

@app.route("/register")
def index():
    # users = session.query(User).all()
    name = "yuzuki"
    user_id = "sda00011"
    new_user = User(name=name, user_id=user_id)
    session.add(new_user)
    session.commit()
    return "hello world"


if __name__ == "__main__":
    app.run(debug=True)