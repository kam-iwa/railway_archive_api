from flask import Flask
from flasgger import Swagger

from database import DB


def create_models():
    from models.core.models_routes import Route
    from models.core.models_stations import Station
    from models.core.models_stops import Stop

    with DB:
        DB.create_tables([
            Route,
            Station,
            Stop
        ])


# Register blueprints
def register_blueprints():
    from blueprints.core import route_mod, station_mod, stop_mod

    app.register_blueprint(route_mod)
    app.register_blueprint(station_mod)
    app.register_blueprint(stop_mod)


if __name__ == '__main__':
    app = Flask(__name__)
    swagger = Swagger(app)

    create_models()
    register_blueprints()
    app.run(host='0.0.0.0', debug=True)
