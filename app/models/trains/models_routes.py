from enum import Enum
from peewee import AutoField, TextField, DateField

from models.trains.models import TrainModel


class RouteType(Enum):
    LOCAL = "local"
    FAST = "fast"
    EXPRESS = "express"


class Route(TrainModel):
    id = AutoField(primary_key=True)
    number = TextField()
    name = TextField()
    type = TextField(default=RouteType.LOCAL)
    date_start = DateField(null=True)
    date_end = DateField(null=True)
