from peewee import Model

from database import DB

class TrainModel(Model):

    class Meta:
        database = DB
        schema = "trains"