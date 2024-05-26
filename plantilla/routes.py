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
    return min(graph.nodes, key = lambda node:
               haversine(node['pos'], (point.lat, point.lon)))

def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    # TODO: Optimitzar (es pot treure 'get_node_attributes'?)
    print("finding routes...")
    routes = Routes()
    start_node = __nearest_node(graph, start)
    pos = nx.get_node_attributes(graph, 'pos')
    dist = nx.get_edge_attributes(graph, 'dist')

    for end in endpoints:
        end_node = __nearest_node(graph, end.location)
        try:
            node_path = nx.algorithms.shortest_path(graph, start_node, end_node, 'dist')
            route = Route(
                path = [pos[v] for v in node_path],
                dist = sum(dist[(node_path[i], node_path[i + 1])]
                           for i in range(len(node_path) - 1)),
                name = end.name
            )
            routes.append(route)
        except nx.NodeNotFound:
            print("A node was not found??")
        except nx.NetworkXNoPath:
            print(f"No path found from startpoint to monument: {end.name}")
    
    return routes


def export_PNG(routes: Routes, filename: str) -> None:
    """Export the routes to a PNG file using staticmaps."""
    print("exporting routes PNG...")
    map = StaticMap(1000, 1000)
    for route in routes:
        for i in range(len(route.path) - 1):
            map.add_line(Line((route.path[i], route.path[i+1]), 'black', 1))
    
    image = map.render()
    image.save(filename)       


def export_KML(routes: Routes, filename: str) -> None:
    """Export the routes to a KML file."""
    # TODO: Make it pretty! Make it glow!
    print("exporting KML routes...")
    kml = Kml()
    for route in routes:
        newline = kml.newlinestring(coords = route.path)
        newline.style.linestyle.color = "00000000"
        newline.style.linestyle.width = 5
    kml.save(filename)


def __testing(n: int,
              max_dist: float, epsilon: float,
              png_file: str, kml_file: str) -> None:
    """Testing function."""
    import monuments
    import graphmaker
    import csv

    print("Loading points...")
    fd = open("Ebre.csv", 'r')
    points = [Point(float(lat), float(lon), int(seg))
                for lon, lat, seg in csv.reader(fd)]
    
    print("Creating graph...")
    graph = graphmaker.make_graph(points, n)
    
    print("Getting monuments...")
    box = ((), ())
    mons = monuments.load_monuments()

    print("Finding routes...")

    