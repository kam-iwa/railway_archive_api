import datetime

from flask import jsonify, render_template
from flasgger import swag_from

from blueprints.trains_timetables import timetable_mod
from models.trains.models_stations import Station
from utils.trains_timetables.functions import get_station_departures, get_station_departures_by_relations, \
    get_station_arrivals, get_station_arrivals_by_relations


@timetable_mod.route('/timetable/departures/<date_start>/<date_end>/<station_name>', methods=['GET'])
@swag_from('docs/timetable.departures.date_start.date_end.station_name.get.yml')
def timetable_departures_date_start_date_end_station_id_get(station_name: str, date_start: str, date_end: str):
    station = Station.get_or_none(Station.name == station_name)
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

    return render_template('trains_timetables_departures.html',
                           station_name=station.name,
                           date_period=[date_start, date_end],
                           routes=data['data']['routes'])


@timetable_mod.route('/timetable/departures/relations/<date_start>/<date_end>/<station_name>', methods=['GET'])
@swag_from('docs/timetable.departures.date_start.date_end.station_name.get.yml')
def timetable_departures_relations_date_start_date_end_station_id_get(station_name: str, date_start: str, date_end: str):
    station = Station.get_or_none(Station.name == station_name)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})


    routes, dates = get_station_departures_by_relations(station, date_start, date_end)
    routes = dict(sorted(routes.items()))

    return render_template('trains_timetables_departures_relations.html',
                           station_name=station.name,
                           date_period=[date_start, date_end],
                           routes=routes, dates=dates)


@timetable_mod.route('/timetable/arrivals/<date_start>/<date_end>/<station_name>', methods=['GET'])
@swag_from('docs/timetable.arrivals.date_start.date_end.station_name.get.yml')
def timetable_arrivals_date_start_date_end_station_name_get(station_name: str, date_start: str, date_end: str):
    station = Station.get_or_none(Station.name == station_name)
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

    return render_template('trains_timetables_arrivals.html',
                           station_name=station.name,
                           date_period=[date_start, date_end],
                           routes=data['data']['routes'])


@timetable_mod.route('/timetable/arrivals/relations/<date_start>/<date_end>/<station_name>', methods=['GET'])
@swag_from('docs/timetable.arrivals.relations.date_start.date_end.station_name.get.yml')
def timetable_arrivals_relations_date_start_date_end_station_name_get(station_name: str, date_start: str, date_end: str):
    station = Station.get_or_none(Station.name == station_name)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    try:
        date_start = datetime.date.fromisoformat(date_start)
        date_end = datetime.date.fromisoformat(date_end)
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    if date_start > date_end:
        return jsonify({'error': 'Invalid date range'})


    routes, dates = get_station_arrivals_by_relations(station, date_start, date_end)
    routes = dict(sorted(routes.items()))

    return render_template('trains_timetables_arrivals_relations.html',
                           station_name=station.name,
                           date_period=[date_start, date_end],
                           routes=routes, dates=dates)
