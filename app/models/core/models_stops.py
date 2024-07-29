from peewee import Model, AutoField, ForeignKeyField, TimeField, IntegerField

from database import DB
from models.core.models_stations import Station
from models.core.models_routes import Route


class Stop(Model):

    class Meta:
        database = DB

    id = AutoField(primary_key=True)
    route = ForeignKeyField(Route, column_name='route')
    station = ForeignKeyField(Station, column_name='station')
    arrival_time = TimeField()
    arrival_day = IntegerField(default=0)
    departure_time = TimeField()
    departure_day = IntegerField(default=0)
