from flask import Blueprint

route_mod = Blueprint('route', __name__)
station_mod = Blueprint('station', __name__)
stop_mod = Blueprint('stop', __name__)

from blueprints.trains.routings_routes import *
from blueprints.trains.routings_stations import *
from blueprints.trains.routings_stops import *
