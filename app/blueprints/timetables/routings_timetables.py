import datetime

from flask import jsonify
from flasgger import swag_from

from blueprints.timetables import timetable_mod
from models.core.models_stations import Station
from utils.timetables.functions import get_station_arrivals_by_relations, get_station_arrivals, \
    get_station_departures_by_relations, get_station_departures


@timetable_mod.route('/api/timetable/departures/<date_start>/<date_end>/<int:station_id>/data', methods=['GET'])
@swag_from('docs/timetable.departures.date_start.date_end.station_id.data.get.yml')
def timetable_departures_date_start_date_end_station_id_data_get(station_id: int, date_start: str, date_end: str):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})

    data = get_station_departures(station, date_start, date_end)

    return jsonify({"data": data})


@timetable_mod.route('/api/timetable/departures/relations/<date_start>/<date_end>/<int:station_id>/data', methods=['GET'])
@swag_from('docs/timetable.departures.relations.date_start.date_end.station_id.data.get.yml')
def timetable_departures_relations_date_start_date_end_station_id_data_get(station_id: int, date_start: str, date_end: str):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})

    data, dates = get_station_departures_by_relations(station, date_start, date_end)

    return jsonify({"data": {"relations": data, "dates": dates}})


@timetable_mod.route('/api/timetable/arrivals/<date_start>/<date_end>/<int:station_id>/data', methods=['GET'])
@swag_from('docs/timetable.arrivals.date_start.date_end.station_id.data.get.yml')
def timetable_arrivals_date_start_date_end_station_id_data_get(station_id: int, date_start: str, date_end: str):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})

    data = get_station_arrivals(station, date_start, date_end)

    return jsonify({"data": data})


@timetable_mod.route('/api/timetable/arrivals/relations/<date_start>/<date_end>/<int:station_id>/data', methods=['GET'])
@swag_from('docs/timetable.arrivals.relations.date_start.date_end.station_id.data.get.yml')
def timetable_arrivals_relations_date_start_date_end_station_id_data_get(station_id: int, date_start: str, date_end: str):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})

    data, dates = get_station_arrivals_by_relations(station, date_start, date_end)

    return jsonify({"data": {"relations": data, "dates": dates}})


