from flasgger import swag_from
from flask import jsonify, request

from blueprints.trains import stop_mod
from models.trains.models_routes import Route
from models.trains.models_stations import Station
from models.trains.models_stops import Stop
from utils.trains.decorators import validate_request


@stop_mod.route('/api/stops', methods=['GET'])
@swag_from('docs/stops.get.yml')
def stops_get():
    stops = Stop.select()
    return jsonify([{
        "id": stop.id,
        "route": stop.route.id,
        "station": stop.station.id,
        "arrival_time": str(stop.arrival_time),
        "departure_time": str(stop.departure_time)
    } for stop in stops])


@stop_mod.route('/api/stops/<int:stop_id>', methods=['GET'])
@swag_from('docs/stops.stop_id.get.yml')
def stops_stop_id_get(stop_id: int):
    stop = Stop.get_or_none(Stop.id == stop_id)
    if stop is None:
        return jsonify({'error': 'Stop not found.'})

    return jsonify({
        "id": stop.id,
        "route": stop.route.id,
        "station": stop.station.id,
        "arrival_time": str(stop.arrival_time),
        "departure_time": str(stop.departure_time)
    })


@stop_mod.route('/api/stops', methods=['POST'])
@validate_request(
    required_keys=["route", "station", "arrival_time", "departure_time"],
    optional_keys=["arrival_day", "departure_day"]
)
@swag_from('docs/stops.post.yml')
def stops_create():
    data = request.get_json()["data"]

    route = Route.get_or_none(Route.id == data["route"])
    if route is None:
        return jsonify({'error': 'Route not found.'})

    station = Station.get_or_none(Station.id == data["station"])
    if station is None:
        return jsonify({'error': 'Station not found.'})

    stop = Stop.create(**data)

    return jsonify({'data': stop.id}), 201


@stop_mod.route('/api/stops/<int:stop_id>', methods=["PUT"])
@validate_request(optional_keys=["route", "station", "arrival_time", "departure_time", "arrival_day", "departure_day"])
@swag_from('docs/stops.stop_id.put.yml')
def stop_update(stop_id: int):
    stop = Stop.get_or_none(Stop.id == stop_id)
    if stop is None:
        return jsonify({'error': 'Stop not found.'})

    data = request.get_json()["data"]
    query = Stop.update(**data).where(Stop.id == stop_id)
    query.execute()

    return jsonify({}), 200


@stop_mod.route('/api/stops/<int:stop_id>', methods=["DELETE"])
@swag_from('docs/stops.stop_id.delete.yml')
def stop_delete(stop_id: int):
    stop = Stop.get_or_none(Stop.id == stop_id)
    if stop is None:
        return jsonify({'error': 'stop not found.'})

    query = Stop.delete().where(Stop.id == stop_id)
    query.execute()

    return jsonify({}), 204
