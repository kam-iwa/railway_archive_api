from flask import Flask
from flasgger import Swagger

from database import DB


def create_models():
    from models.trains.models_routes import Route
    from models.trains.models_stations import Station
    from models.trains.models_stops import Stop

    with DB:
        DB.execute_sql("CREATE SCHEMA IF NOT EXISTS trains")
        DB.create_tables([
            Route,
            Station,
            Stop
        ])


# Register blueprints
def register_blueprints():
    from blueprints.trains import route_mod, station_mod, stop_mod
    from blueprints.trains_timetables import timetable_mod

    app.register_blueprint(route_mod)
    app.register_blueprint(station_mod)
    app.register_blueprint(stop_mod)
    app.register_blueprint(timetable_mod)


if __name__ == '__main__':
    app = Flask(__name__)

    swagger = Swagger(app)

    create_models()
    register_blueprints()
    app.run(host='0.0.0.0', debug=True)
