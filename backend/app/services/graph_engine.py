import heapq
from app.db.sqlite_client import get_sqlite_conn

def get_metro_route(source_name: str, destination_name: str):
    """
    Computes the shortest route (based on travel time) between the source and 
    destination metro stations using Dijkstra's algorithm.
    Reads station, connection, and interchange graphs dynamically from SQLite.
    """
    with get_sqlite_conn() as conn:
        stations = {
            row["id"]: dict(row)
            for row in conn.execute("SELECT id, name, line FROM stations")
        }
        source = conn.execute(
            "SELECT id FROM stations WHERE lower(name) = lower(?) ORDER BY id LIMIT 1",
            (source_name,),
        ).fetchone()
        destination = conn.execute(
            "SELECT id FROM stations WHERE lower(name) = lower(?) ORDER BY id LIMIT 1",
            (destination_name,),
        ).fetchone()

        if not source or not destination:
            raise ValueError("One or both selected stations were not found.")

        source_id, destination_id = source["id"], destination["id"]
        if source_id == destination_id:
            raise ValueError("Source and destination stations cannot be the same.")

        graph = {station_id: [] for station_id in stations}
        for row in conn.execute(
            "SELECT station_a_id, station_b_id, travel_time_minutes, fare_inr FROM connections"
        ):
            edge = (row["travel_time_minutes"], row["fare_inr"], "connection")
            graph[row["station_a_id"]].append((row["station_b_id"], *edge))
            graph[row["station_b_id"]].append((row["station_a_id"], *edge))
        for row in conn.execute(
            "SELECT station_from_id, station_to_id, transfer_time_minutes FROM interchanges"
        ):
            edge = (row["transfer_time_minutes"], 0, "interchange")
            graph[row["station_from_id"]].append((row["station_to_id"], *edge))
            graph[row["station_to_id"]].append((row["station_from_id"], *edge))

    queue = [(0, 0, source_id)]
    best = {source_id: (0, 0)}
    previous = {}
    while queue:
        time, fare, station_id = heapq.heappop(queue)
        if (time, fare) != best.get(station_id):
            continue
        if station_id == destination_id:
            break
        for next_id, edge_time, edge_fare, edge_type in graph[station_id]:
            candidate = (time + edge_time, fare + edge_fare)
            if candidate < best.get(next_id, (float("inf"), float("inf"))):
                best[next_id] = candidate
                previous[next_id] = (station_id, edge_type)
                heapq.heappush(queue, (*candidate, next_id))

    if destination_id not in best:
        raise ValueError("No route is available between the selected stations.")

    path = [destination_id]
    edge_types = []
    while path[-1] != source_id:
        parent_id, edge_type = previous[path[-1]]
        edge_types.append(edge_type)
        path.append(parent_id)
    path.reverse()
    edge_types.reverse()

    itinerary = []
    for index, station_id in enumerate(path):
        item = {
            "station_name": stations[station_id]["name"],
            "line": stations[station_id]["line"],
            "is_interchange": False,
            "transfer_to": None,
        }
        if index < len(edge_types) and edge_types[index] == "interchange":
            item["is_interchange"] = True
            item["transfer_to"] = stations[path[index + 1]]["line"]
        itinerary.append(item)

    total_time, total_fare = best[destination_id]
    return {
        "route_summary": {
            "source": stations[source_id]["name"],
            "destination": stations[destination_id]["name"],
            "total_travel_time_minutes": total_time,
            "total_fare_inr": total_fare,
            "interchanges_count": edge_types.count("interchange"),
        },
        "ordered_itinerary": itinerary,
    }