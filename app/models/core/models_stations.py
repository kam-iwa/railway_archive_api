from enum import Enum
from peewee import Model, AutoField, TextField, DecimalField

from database import DB


class StationType(Enum):
    STOP = "stop"
    STATION = "station"


class Station(Model):

    class Meta:
        database = DB

    id = AutoField(primary_key=True)
    name = TextField(unique=True)
    type = TextField(default=StationType.STOP)
    lat = DecimalField()
    lon = DecimalField()