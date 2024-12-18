from peewee import SqliteDatabase
from .db import db
from .user import User
from .item import Item
from .status import Status

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    User,
    Item,
    Status,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()