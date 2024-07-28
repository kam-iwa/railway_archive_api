from enum import Enum
from peewee import Model, AutoField, TextField, ForeignKeyField, DateField

from app.app import db


class RouteType(Enum):
    LOCAL = "local"
    FAST = "fast"
    EXPRESS = "express"


class Route(Model):

    class Meta:
        database = db

    id = AutoField(primary_key=True)
    number = TextField()
    name = TextField()
    type = TextField(default=RouteType.LOCAL)
    date_start = DateField(null=True)
    date_end = DateField(null=True)

    parent_route = ForeignKeyField('self', null=True, default=None)