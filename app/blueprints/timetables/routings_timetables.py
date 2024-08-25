from flask import jsonify
from flasgger import swag_from

from blueprints.timetables import timetable_mod
from models.core.models_routes import Route
from models.core.models_stations import Station
from models.core.models_stops import Stop


@timetable_mod.route('/api/timetable/departures/<int:station_id>', methods=['GET'])
@swag_from('docs/timetable.departures.station_id.get.yml')
def timetable_departures_station_id_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_departures(station)

    return jsonify({"data": data})


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.get.yml')
def timetable_arrivals_station_id_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_arrivals(station)

    return jsonify({"data": data})


def get_station_departures(station: Station):
    station_id = station.id

    routes = Stop.select(
                Stop.arrival_time.cast('text'), Stop.arrival_day,
                Stop.departure_time.cast('text'), Stop.departure_day, Route
        ).order_by(
            Stop.arrival_time
        ).join(
            Route, on=(Route.id == Stop.route)
        ).join(
            Station, on=(Station.id == Stop.station)
        ).where(
            Stop.station == station_id
        ).order_by(
            Stop.departure_time
        ).dicts()

    result = {"data": {
        "station": station.name,
        "routes": []
    }}
    for route in routes:
        query = Stop.select(
            Station.name, Stop.arrival_time.cast('text'), Stop.arrival_day
        ).where(
            Stop.route == route['id']
        ).join(
            Station, on=(Station.id == Stop.station)
        ).where(
            (
                    ((Stop.arrival_time > route["arrival_time"]) & (Stop.arrival_day == route["arrival_day"])) |
                    ((Stop.arrival_time < route["arrival_time"]) & (Stop.arrival_day > route["arrival_day"])))
        ).order_by(
            Stop.arrival_day, Stop.arrival_time
        )

        route_data = {
            "train_name": route['name'],
            "train_number": route['number'],
            "departure_time": route['departure_time'][:-3],
            "intermediate_stops": [],
            "destination": [],
            "type": route['type'],
        }
        for row in query.dicts():
            route_data['intermediate_stops'].append({"station": row['name'], "arrival_time": row['arrival_time'][:-3]})

        try:
            route_data['destination'] = route_data['intermediate_stops'][-1]
            route_data['intermediate_stops'].pop()
            result['data']['routes'].append(route_data)
        except IndexError:
            route_data['destination'] = []

    return result


def get_station_arrivals(station: Station):
    station_id = station.id

    routes = Stop.select(
        Stop.arrival_time.cast('text'), Stop.arrival_day, Stop.departure_time.cast('text'), Stop.departure_day, Route
    ).order_by(
        Stop.departure_time
    ).join(
        Route, on=(Route.id == Stop.route)
    ).join(
        Station, on=(Station.id == Stop.station)
    ).where(
        Stop.station == station_id
    ).order_by(
        Stop.arrival_time
    ).dicts()

    result = {"data": {
        "station": station.name,
        "routes": []
    }}

    for route in routes:
        query = Stop.select(
            Station.name, Stop.departure_time.cast('text'), Stop.departure_day
        ).where(
            Stop.route == route['id']
        ).join(
            Station, on=(Station.id == Stop.station)
        ).where(
            (
                    ((Stop.departure_time < route["departure_time"]) & (Stop.departure_day <= route["departure_day"])) |
                    ((Stop.departure_time > route["departure_time"]) & (Stop.departure_day < route["departure_day"]))
            )
        ).order_by(
            Stop.departure_day.asc(), Stop.departure_time
        )

        route_data = {
            "train_name": route['name'],
            "train_number": route['number'],
            "arrival_time": route['arrival_time'][:-3],
            "intermediate_stops": [],
            "origin": [],
            "type": route['type'],
        }
        for row in query.dicts():
            route_data['intermediate_stops'].append({"station": row['name'], "departure_time": row['departure_time'][:-3]})

        try:
            route_data['origin'] = route_data['intermediate_stops'][0]
            route_data['intermediate_stops'].pop(0)
            result['data']['routes'].append(route_data)
        except IndexError:
            route_data['origin'] = []

    return result
