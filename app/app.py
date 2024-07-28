from flask import Flask
from flasgger import Swagger
from peewee import PostgresqlDatabase

# Create the Flask app
app = Flask(__name__)

# Create the database connection
db = PostgresqlDatabase(
    database='main',
    user='docker',
    password='docker',
    host='db',
    port=5432
)

# Create the Swagger instance
swagger = Swagger(app)


# Create models
def create_models():
    from models.core.models_routes import Route
    from models.core.models_stations import Station
    from models.core.models_stops import Stop

    with db:
        db.create_tables([
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
    create_models()
    register_blueprints()
    app.run(host='0.0.0.0', debug=True)
