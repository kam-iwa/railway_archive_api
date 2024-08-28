from peewee import AutoField, ForeignKeyField, TimeField, IntegerField

from models.trains.models import TrainModel
from models.trains.models_stations import Station
from models.trains.models_routes import Route


class Stop(TrainModel):
    id = AutoField(primary_key=True)
    route = ForeignKeyField(Route, column_name='route')
    station = ForeignKeyField(Station, column_name='station')
    arrival_time = TimeField()
    arrival_day = IntegerField(default=0)
    departure_time = TimeField()
    departure_day = IntegerField(default=0)
