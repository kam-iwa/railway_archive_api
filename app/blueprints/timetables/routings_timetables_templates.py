from flask import jsonify, request, render_template
from flasgger import swag_from

from blueprints.timetables import timetable_mod, get_station_departures, get_station_arrivals, \
    get_station_departures_by_relations, get_station_arrivals_by_relations
from models.core.models_routes import Route
from models.core.models_stations import Station


@timetable_mod.route('/api/timetable/departures/<int:station_id>/html', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.html.get.yml')
def timetable_departures_station_id_html_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_departures(station)

    return render_template('timetables_departures.html',
                           station_name=station.name,
                           routes=data['data']['routes'])


@timetable_mod.route('/api/timetable/departures/<int:station_id>/relations/html', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.relations.html.get.yml')
def timetable_departures_station_id_relations_html_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data, dates = get_station_departures_by_relations(station)
    data = dict(sorted(data.items()))

    return render_template('timetables_departures_relations.html',
                           station_name=station.name,
                           data=data, dates=dates)


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>/html', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.html.get.yml')
def timetable_arrivals_station_id_html_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_arrivals(station)

    return render_template('timetables_arrivals.html',
                           station_name=station.name,
                           routes=data['data']['routes'])


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>/relations/html', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.relations.html.get.yml')
def timetable_arrivals_station_id_relations_html_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data, dates = get_station_arrivals_by_relations(station)
    data = dict(sorted(data.items()))

    return render_template('timetables_arrivals_relations.html',
                           station_name=station.name,
                           data=data, dates=dates)
