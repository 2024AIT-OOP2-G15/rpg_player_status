from peewee import Model, CharField, DecimalField
from .db import db

class Item(Model):
# 装備とそのステータス（装備名 HP AT DF)
    name = CharField()
    hitpoint = DecimalField()
    defence = DecimalField()
    attack = DecimalField()

    class Meta:
        database = db