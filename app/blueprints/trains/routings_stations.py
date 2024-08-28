from flask import jsonify, request
from flasgger import swag_from

from blueprints.trains import station_mod
from database import DB
from models.trains.models_stations import Station
from models.trains.models_stops import Stop
from utils.trains.decorators import validate_request


@station_mod.route('/api/stations', methods=['GET'])
@swag_from('docs/stations.get.yml')
def stations_get():
    stations = Station.select()
    return jsonify(
        [{"id": station.id, "name": station.name, "lat": station.lat, "lon": station.lon, "type": station.type} for station in stations])


@station_mod.route('/api/stations/<station_id>', methods=['GET'])
@swag_from('docs/stations.station_id.get.yml')
def stations_station_get(station_id: str):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    return jsonify({"id": station.id, "name": station.name, "lat": station.lat, "lon": station.lon, "type": station.type})


@station_mod.route('/api/stations', methods=['POST'])
@validate_request(required_keys=["name", "type", "lon", "lat"])
@swag_from('docs/stations.post.yml')
def stations_create():
    data = request.get_json()["data"]

    same_named_stations_count = Station.select().where(Station.name == data["name"]).count()
    if same_named_stations_count > 0:
        return jsonify({'error': 'Station with this name is exist.'})

    station = Station.create(**data)

    return jsonify({'data': station.id}), 201


@station_mod.route('/api/stations/<int:station_id>', methods=["PUT"])
@validate_request(optional_keys=["name", "type", "lon", "lat"])
@swag_from('docs/stations.station_id.put.yml')
def stations_update(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = request.get_json()["data"]

    if "name" in data.keys():
        same_named_stations_count = Station.select().where(Station.name == data["name"]).count()
        if same_named_stations_count > 0:
            return jsonify({'error': 'Station with this name is exist.'})

    query = Station.update(**data).where(Station.id == station_id)
    query.execute()

    return jsonify({}), 200


@station_mod.route('/api/stations/<int:station_id>', methods=["DELETE"])
@swag_from('docs/stations.station_id.delete.yml')
def stations_delete(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    with DB.atomic():
        query_stop = Stop.delete().where(Stop.station == station_id)
        query_stop.execute()

        query = Station.delete().where(Station.id == station_id)
        query.execute()

    return jsonify({}), 204
