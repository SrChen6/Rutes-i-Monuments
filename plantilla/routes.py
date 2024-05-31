import networkx as nx
from staticmap import Line, StaticMap
from simplekml import Kml
from haversine import haversine

from typing import TypeAlias
from dataclasses import dataclass
from segments import Point
from monuments import Monuments


Coord: TypeAlias = tuple[float, float]

@dataclass
class Route:
    path: list[Coord]
    dist: float
    name: str
    
Routes: TypeAlias = list[Route]


def __nearest_node(graph: nx.Graph, point: Point) -> int:
    """
    Returns the node of the graph nearest to the given point.
    """
    pos = nx.get_node_attributes(graph, 'pos')
    return min(graph.nodes, key = lambda node:
               haversine(pos[node], (point.lat, point.lon)))

def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    routes = Routes()
    start_node = __nearest_node(graph, start)
    pos = nx.get_node_attributes(graph, 'pos')

    for end in endpoints:
        end_node = __nearest_node(graph, end.location)
        try:
            node_path = nx.algorithms.shortest_path(graph, start_node, end_node, 'dist')
            route = Route(
                path = [pos[v] for v in node_path],
                dist = sum(graph[node_path[i]][node_path[i+1]]['dist']
                           for i in range(len(node_path) - 1)),
                name = end.name
            )
            routes.append(route)
        except nx.NetworkXNoPath:
            print(f"No path found from startpoint to monument: {end.name}")
    
    return routes


def export_PNG(routes: Routes, filename: str) -> None:
    """Export the routes to a PNG file using staticmaps."""
    map = StaticMap(1000, 1000)
    for route in routes:
        for i in range(len(route.path) - 1):
            map.add_line(Line((route.path[i][::-1], route.path[i+1][::-1]), 'black', 1))
    
    # TODO: Soluciona error de connexió amb python
    image = map.render()
    image.save(filename)       


def export_KML(routes: Routes, filename: str) -> None:
    """Export the routes to a KML file."""
    # TODO: Make it pretty! Make it glow!
    kml = Kml()
    for route in routes:
        newline = kml.newlinestring(
            name = route.name,
            coords = route.path
        )
        newline.style.linestyle.color = "00000000"
        newline.style.linestyle.width = 5
    kml.save(filename)


if __name__ == "__main__":
    import monuments
    import graphmaker
    import segments
    from yogi import read

    box = segments.Box(Point(read(float), read(float), -1),
                       Point(read(float), read(float), -1))
    filename = read(str)
    start = Point(read(float), read(float), -1)
    points = segments.get_points(box, filename)

    graph = graphmaker.make_graph(points, 300)
    mons = monuments.get_monuments(box, "prova_rutes.csv")
    routes = find_routes(graph, start, mons)
    export_PNG(routes, "prova_rutes2.png")

    