from peewee import Model, CharField, IntegerField
from .db import db
from peewee import Model, CharField, IntegerField
from .db import db  # dbインスタンスのインポート
class User(Model):
    name = CharField()
    hp = IntegerField()
    at = IntegerField()
    df = IntegerField()


    class Meta:
        database = db
