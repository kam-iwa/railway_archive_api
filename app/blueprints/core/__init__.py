from flask import Blueprint

route_mod = Blueprint('route', __name__)
station_mod = Blueprint('station', __name__)
stop_mod = Blueprint('stop', __name__)

from blueprints.core.routings_routes import *
from blueprints.core.routings_stations import *
from blueprints.core.routings_stops import *
