from peewee import Model, IntegerField, ForeignKeyField
from .db import db
from .user import User
from .item import Item

class Status(Model):
    name = ForeignKeyField(User, backref='status')
    item = ForeignKeyField(Item, backref='status')
    hp = IntegerField()
    at = IntegerField()
    df = IntegerField()

    class Meta:
        database = db