from flask import jsonify, request, render_template
from flasgger import swag_from

from blueprints.timetables import timetable_mod, get_station_departures, get_station_arrivals
from models.core.models_stations import Station


@timetable_mod.route('/api/timetable/departures/<int:station_id>/template', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.template.get.yml')
def timetable_departures_station_id_template_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_departures(station)

    return render_template('timetables_departures.html',
                           station_name=station.name,
                           routes=data['data']['routes'])


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>/template', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.template.get.yml')
def timetable_arrivals_station_id_template_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_arrivals(station)

    return render_template('timetables_arrivals.html',
                           station_name=station.name,
                           routes=data['data']['routes'])
