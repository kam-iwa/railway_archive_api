from enum import Enum
from peewee import AutoField, TextField, DecimalField

from models.trains.models import TrainModel


class StationType(Enum):
    STOP = "stop"
    STATION = "station"


class Station(TrainModel):
    id = AutoField(primary_key=True)
    name = TextField(unique=True)
    type = TextField(default=StationType.STOP)
    lat = DecimalField()
    lon = DecimalField()