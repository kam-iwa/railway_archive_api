from flask import jsonify
from flasgger import swag_from

from blueprints.timetables import timetable_mod
from database import DB
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


@timetable_mod.route('/api/timetable/departures/<int:station_id>/relations', methods=['GET'])
@swag_from('docs/timetable.departures.station_id.relations.get.yml')
def timetable_departures_station_id_relations_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_departures(station)

    routes = data["data"]["routes"]

    destinations = {}
    dests = set([route["destination"]["station"] for route in routes])
    for dest in dests:
        destinations[dest] = []

    for route in routes:
        destinations[route["destination"]["station"]].append([route["departure_time"], route["type"], route["train_number"]])
        for stop in route['intermediate_stops']:
            if stop["station"] in destinations:
                destinations[stop["station"]].append([route["departure_time"], route["type"], route["train_number"]])
                print(stop["station"])

    return jsonify({"data": destinations})


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.get.yml')
def timetable_arrivals_station_id_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_arrivals(station)

    return jsonify({"data": data})


@timetable_mod.route('/api/timetable/arrivals/<int:station_id>/relations', methods=['GET'])
@swag_from('docs/timetable.arrivals.station_id.relations.get.yml')
def timetable_arrivals_station_id_relations_get(station_id: int):
    station = Station.get_or_none(Station.id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})

    data = get_station_arrivals_by_relations(station)

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


def get_station_departures_by_relations(station: Station):
    data = get_station_departures(station)

    routes = data["data"]["routes"]

    result = {}
    destinations = set([route["destination"]["station"] for route in routes])
    for destination in destinations:
        result[destination] = []

    for route in routes:
        result[route["destination"]["station"]].append(
            [route["departure_time"], route["type"], route["train_number"]])
        for stop in route['intermediate_stops']:
            if stop["station"] in result:
                result[stop["station"]].append([route["departure_time"], route["type"], route["train_number"]])

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


def get_station_arrivals_by_relations(station: Station):
    data = get_station_arrivals(station)

    routes = data["data"]["routes"]

    result = {}
    origins = set([route["origin"]["station"] for route in routes])
    for origin in origins:
        result[origin] = []

    for route in routes:
        result[route["origin"]["station"]].append([route["arrival_time"], route["type"], route["train_number"]])
        for stop in route['intermediate_stops']:
            if stop["station"] in result:
                result[stop["station"]].append([route["arrival_time"], route["type"], route["train_number"]])

    return result
