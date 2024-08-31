from datetime import timedelta

from models.trains.models_routes import Route
from models.trains.models_stations import Station
from models.trains.models_stops import Stop


def get_station_departures(station: Station, date_start, date_end):
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

        if route["date_start"] is not None and route["date_end"] is not None:

            date_period = [
                route["date_start"]+timedelta(days=route["departure_day"]),
                route["date_end"]+timedelta(days=route["departure_day"])
            ]

            if route["date_start"] <= date_start and date_end <= route["date_end"]:
                 date_period = None
            elif route["date_start"] < date_start and date_end > route["date_end"]:
                date_period[0] = date_start
            elif route["date_start"] > date_start and date_end < route["date_end"]:
                date_period[1] = date_end

        else:
            date_period = None

        route_data = {
            "train_name": route['name'],
            "train_number": route['number'],
            "departure_time": route['departure_time'][:-3],
            "intermediate_stops": [],
            "destination": [],
            "type": route['type'],
            "date_period": date_period,
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


def get_station_departures_by_relations(station: Station, date_start, date_end):
    data = get_station_departures(station, date_start, date_end)

    dates = []

    routes = data["data"]["routes"]

    result = {}
    destinations = set([route["destination"]["station"] for route in routes])
    for destination in destinations:
        result[destination] = []

    for route in routes:
        try:
            dates_idx = dates.index(route["date_period"]) if route["date_period"] is not None else None
        except ValueError:
            dates.append(route["date_period"])
            dates_idx = len(dates) - 1

        result[route["destination"]["station"]].append(
            [route["departure_time"], route["type"], route["train_number"], dates_idx])
        for stop in route['intermediate_stops']:
            if stop["station"] in result:
                result[stop["station"]].append([route["departure_time"], route["type"], route["train_number"], dates_idx])

    return result, dates


def get_station_arrivals(station: Station, date_start, date_end):
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

        if route["date_start"] is not None and route["date_end"] is not None:

            date_period = [
                route["date_start"]+timedelta(days=route["arrival_day"]),
                route["date_end"]+timedelta(days=route["arrival_day"])
            ]

            if route["date_start"] <= date_start and date_end <= route["date_end"]:
                 date_period = None
            elif route["date_start"] < date_start and date_end > route["date_end"]:
                date_period[0] = date_start
            elif route["date_start"] > date_start and date_end < route["date_end"]:
                date_period[1] = date_end

        else:
            date_period = None

        route_data = {
            "train_name": route['name'],
            "train_number": route['number'],
            "arrival_time": route['arrival_time'][:-3],
            "intermediate_stops": [],
            "origin": [],
            "type": route['type'],
            "date_period": date_period,
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


def get_station_arrivals_by_relations(station: Station, date_start, date_end):
    data = get_station_arrivals(station, date_start, date_end)

    dates = []

    routes = data["data"]["routes"]

    result = {}
    origins = set([route["origin"]["station"] for route in routes])
    for origin in origins:
        result[origin] = []

    for route in routes:
        try:
            dates_idx = dates.index(route["date_period"]) if route["date_period"] is not None else None
        except ValueError:
            dates.append(route["date_period"])
            dates_idx = len(dates) - 1

        result[route["origin"]["station"]].append([route["arrival_time"], route["type"], route["train_number"], dates_idx])
        for stop in route['intermediate_stops']:
            if stop["station"] in result:
                result[stop["station"]].append([route["arrival_time"], route["type"], route["train_number"], dates_idx])

    return result, dates
