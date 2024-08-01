from flasgger import swag_from
from flask import jsonify, request

from blueprints.core import stop_mod
from models.core.models_stops import Stop


@stop_mod.route('/stops', methods=['GET'])
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


@stop_mod.route('/stops/<int:stop_id>', methods=['GET'])
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


@stop_mod.route('/stops', methods=['POST'])
@swag_from('docs/stops.post.yml')
def stops_create():
    data = request.get_json()["data"]
    stop = Stop.create(**data)

    return jsonify({'data': stop.id}), 201


@stop_mod.route('/stops/<int:stop_id>', methods=["PUT"])
@swag_from('docs/stops.stop_id.put.yml')
def stop_update(stop_id: int):
    stop = Stop.get_or_none(Stop.id == stop_id)
    if stop is None:
        return jsonify({'error': 'Stop not found.'})

    data = request.get_json()["data"]
    query = Stop.update(**data).where(Stop.id == stop_id)
    query.execute()

    return jsonify({}), 200


@stop_mod.route('/stops/<int:stop_id>', methods=["DELETE"])
@swag_from('docs/stops.stop_id.delete.yml')
def stop_delete(stop_id: int):
    stop = Stop.get_or_none(Stop.id == stop_id)
    if stop is None:
        return jsonify({'error': 'stop not found.'})

    query = Stop.delete().where(Stop.id == stop_id)
    query.execute()

    return jsonify({}), 204
