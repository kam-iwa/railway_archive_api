from enum import Enum
from peewee import Model, AutoField, TextField, DecimalField

from app.app import db


class StationType(Enum):
    STOP = "stop"
    STATION = "station"


class Station(Model):

    class Meta:
        database = db

    id = AutoField(primary_key=True)
    name = TextField(unique=True)
    type = TextField(null=True)
    lat = DecimalField(null=True)
    lon = DecimalField(null=True)