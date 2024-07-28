from flask import jsonify, request
from flasgger import swag_from
from peewee import fn

from app.blueprints.core import station_mod
from app.models.core.models_stations import Station


@station_mod.route('/api/stations', methods=['GET'])
@swag_from('docs/stations.get.yml')
def stations_get():
    stations = Station.select()
    return jsonify(
        [{"name": station.name, "lat": station.lat, "lon": station.lon, "type": station.type} for station in
         stations])


@station_mod.route('/api/stations/<station_name>', methods=['GET'])
@swag_from('docs/stations.station_name.get.yml')
def stations_station_get(station_name: str):
    station = Station.get_or_none(fn.lower(Station.name) == station_name.strip().lower())
    if station is None:
        return jsonify({'error': 'Station not found.'})

    return jsonify({"name": station.name, "lat": station.lat, "lon": station.lon, "type": station.type})


@station_mod.route('/api/stations', methods=['POST'])
@swag_from('docs/stations.post.yml')
def stations_create():
    data = request.get_json()["data"]
    station = Station.create(**data)

    return jsonify({'data': station.id}), 201


@station_mod.route('/api/stations/<int:station_id>', methods=["PUT"])
# @swag_from('docs/stations.station_id.put.yml')
def stations_edit(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = request.get_json()["data"]
    station = Station.update(**data)

    return jsonify({}), 200


@station_mod.route('/api/stations/<int:station_id>', methods=["DELETE"])
# @swag_from('docs/stations.station_id.delete.yml')
def stations_delete(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    Station.delete().where(Station.id == station_id)
    return jsonify({}), 204
