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

    data = get_station_departures_by_relations(station)

    return jsonify({"data": data})


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
    station_id = station.id

    sql = f"""
    select 
        intermediate_stop[array_upper( intermediate_stop , 1)] as destination_station, 
        array_agg( intermediate_stop ) as intermediate_stations, 
        array_agg( array[departure::text, subquery.route_id::text] order by departure ) as departures_routes 
    from ( 
        select
            (
                select array_agg(stt.name order by stp.departure_day, stp.departure_time) 
                from station as stt
                join stop stp on stt.id = stp.station  
                where (stp.route = st.route) and ( 
                    ( (stp.departure_time > st.departure_time) and (stp.departure_day = st.departure_day ) ) or
                    ( (stp.departure_day > st.departure_day ))
                    )
            ) as "intermediate_stop",
            st.route as route_id, 
            st.departure_time as departure,
            st.station as station_id
        from stop st ) subquery
    join station s on s.id = subquery.station_id
    where ( 
        (s.id = {station_id}) and array_length(subquery.intermediate_stop, 1) > 0
        )
    group by destination_station
    order by destination_station, departures_routes;
    """

    query = DB.execute_sql(sql)

    result = {}
    data = {}
    for row in query:
        trains = []
        for idx in range(0, len(row[1])):
            intermediate_stations = row[1][idx]
            departure = row[2][idx][0][:-3]
            route_id = int(row[2][idx][1])
            trains.append([intermediate_stations, departure, route_id])
        data[row[0]] = trains
        result[row[0]] = []

    destinations = result.keys()

    for station in destinations:
        for train in data[station]:
            train_destinations = list(set(destinations) & set(train[0]))
            for dest in train_destinations:
                result[dest].append((train[1], train[2]))

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
    station_id = station.id

    sql = f"""
    select 
        intermediate_stop[array_lower( intermediate_stop , 1)] as destination_station, 
        intermediate_stop, 
        array_agg( array[arrival::text, subquery.route_id::text] order by arrival ) as departures_routes 
    from ( 
        select
         (
            select array_agg(stt.name order by stp.arrival_day, stp.arrival_time) 
            from station as stt
            join stop stp on stt.id = stp.station  
            where (stp.route = st.route) and ( 
                ( (stp.arrival_time < st.arrival_time) and (stp.arrival_day = st.arrival_day ) ) or
                ( (stp.arrival_day < st.arrival_day ))
                )
        ) as "intermediate_stop",
                st.route as route_id, 
                st.arrival_time as arrival,
                st.station as station_id
        from stop st ) subquery
    join station s on s.id = subquery.station_id
    where ( 
        (s.id = {station_id}) and array_length(subquery.intermediate_stop, 1) > 0
        )
    group by intermediate_stop
    order by destination_station, departures_routes;
    """

    query = DB.execute_sql(sql)

    result = {}
    data = {}
    for row in query:
        intermediate_stations = row[1]
        departures = [departure[0][:-3] for departure in row[2]]
        route_ids = [int(departure[1]) for departure in row[2]]

        trains = [intermediate_stations, departures, route_ids]

        data[row[0]] = trains
        result[row[0]] = []

    destinations = data.keys()

    for station in destinations:
        train_destinations = list(set(destinations) & set(data[station][0]))

        for dest in train_destinations:
            arrivals = data[station][1]
            route_ids = data[station][2]
            for idx in range(0, len(arrivals)):
                result[dest].append((arrivals[idx], route_ids[idx]))

    return result
