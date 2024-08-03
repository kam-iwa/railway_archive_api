from flask import jsonify, request
from flasgger import swag_from

from blueprints.core import route_mod
from database import DB
from models.core.models_routes import Route
from models.core.models_stations import Station
from models.core.models_stops import Stop
from utils.core.decorators import validate_request


@route_mod.route('/api/routes', methods=['GET'])
@swag_from('docs/routes.get.yml')
def routes_get():
    routes = Route.select()
    return jsonify([{"id": route.id, "number": route.number, "name": route.name} for route in routes])


@route_mod.route('/api/routes/<int:route_id>', methods=['GET'])
@swag_from('docs/routes.route_id.get.yml')
def routes_route_id_get(route_id: int):
    route = Route.get_or_none(Route.id == route_id)
    if route is None:
        return jsonify({'error': 'Route not found.'})

    result = {
        "id": route.id,
        "name": route.name,
        "number": route.number,
        "stops": []
    }
    stops = Stop.select().where(Stop.route == route.id).order_by(Stop.departure_time)
    for stop in stops:
        result["stops"].append(
            {"station": stop.station.id, "arrival": str(stop.arrival_time), "departure": str(stop.departure_time)})

    return jsonify({'data': result})


@route_mod.route('/api/routes', methods=['POST'])
@validate_request(
    required_keys=["number", "name", "type", "stops"],
    optional_keys=["date_start", "date_end", "parent_route"]
)
@swag_from('docs/routes.post.yml')
def routes_create():
    data = request.get_json()["data"]
    route = Route.create(**data)

    stops = data["stops"]

    for stop in stops:
        if set(stop.keys()) - {"station", "arrival_time", "departure_time"}:
            return jsonify({'error': 'Invalid `stops` payload'})
        if {"station", "arrival_time", "departure_time"} - set(stop.keys()):
            return jsonify({'error': 'Invalid `stops` payload'})

        stop["route"] = route.id
        station = Station.get_or_none(Station.id == stop["station"])
        if station is None:
            return jsonify({'error': 'Station not found.'})

        Stop.create(**stop)

    return jsonify({'data': route.id}), 201


@route_mod.route('/api/routes/<int:route_id>', methods=["PUT"])
@validate_request(optional_keys=["number", "name", "type", "date_start", "date_end", "parent_route"])
@swag_from('docs/routes.route_id.put.yml')
def route_update(route_id: int):
    route = Route.get_or_none(Route.id == route_id)
    if route is None:
        return jsonify({'error': 'Route not found.'})

    data = request.get_json()["data"]

    query = Route.update(**data).where(Route.id == route_id)
    query.execute()

    return jsonify({}), 200


@route_mod.route('/api/routes/<int:route_id>', methods=["DELETE"])
@swag_from('docs/routes.route_id.delete.yml')
def route_delete(route_id: int):
    route = Route.get_or_none(Route.id == route_id)
    if route is None:
        return jsonify({'error': 'route not found.'})

    with DB.atomic():
        query_stop = Stop.delete().where(Stop.route == route_id)
        query_stop.execute()

        query = Route.delete().where(Route.id == route_id)
        query.execute()

    return jsonify({}), 204
