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
    pass


# Register blueprints
def register_blueprints():
    pass


if __name__ == '__main__':
    create_models()
    register_blueprints()
    app.run(host='0.0.0.0', debug=True)
