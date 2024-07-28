from peewee import Model, AutoField, ForeignKeyField, TimeField, IntegerField

from app.app import db
from app.models.stations import Station
from app.models.routes import Route


class Stop(Model):

    class Meta:
        database = db

    id = AutoField(primary_key=True)
    route = ForeignKeyField(Route, column_name='route')
    station = ForeignKeyField(Station, column_name='station')
    arrival_time = TimeField()
    arrival_day = IntegerField(default=0)
    departure_time = TimeField()
    departure_day = IntegerField(default=0)
