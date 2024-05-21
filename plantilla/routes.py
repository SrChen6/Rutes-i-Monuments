import networkx as nx
from staticmap import Line, StaticMap
from simplekml import Kml
from haversine import haversine

from typing import TypeAlias
from segments import Point
from monuments import Monuments

# for testing
if __name__ == "__main__":
    import monuments
    import graphmaker
    import csv

# TODO: This is shit! Must have monument names.
Route: TypeAlias = list[tuple[float, float]]
Routes: TypeAlias = list[Route]


def __nearest_node(graph: nx.Graph, point: Point) -> int:
    """
    Returns the node of the graph nearest to the given point.
    """
    return min(graph.nodes, key = lambda node:
               haversine(node['pos'], (point.lat, point.lon)))

def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    # TODO: Per cada monument:
    # - Aproximar cada monument a un node del graf (es pot fer lineal en principi).
    # - Buscar la ruta més curta del start al endpoint.
    routes = Routes()
    start_node = __nearest_node(graph, start)
    pos = nx.get_node_attributes(graph, 'pos')

    for end in endpoints:
        end_node = __nearest_node(graph, end.location)
        try:
            path = nx.algorithms.shortest_path(graph, start_node, end_node, 'dist')
            routes.append([pos[v] for v in path])
        except nx.NodeNotFound:
            print("A node was not found??")
        except nx.NetworkXNoPath:
            print(f"No path found from startpoint to monument: {end.name}")
    
    return routes


def export_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    map = StaticMap(1000, 1000)
    for route in routes:
        for i in range(len(route) - 1):
            map.add_line(Line((route[i], route[i+1]), 'black', 1))
    
    image = map.render()
    image.save(filename)       


def export_KML(routes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    # TODO: Make it pretty! Make it glow!
    kml = Kml()
    for route in routes:
        newline = kml.newlinestring(coords = route)
        newline.style.linestyle.color = "00000000"
        newline.style.linestyle.width = 5
    kml.save(filename)


def __testing(n: int, simplify: bool,
              max_dist: float, epsilon: float,
              png_file: str, kml_file: str) -> None:
    """Testing function."""

    print("Loading points...")
    fd = open("Ebre.csv", 'r')
    points = [Point(float(lat), float(lon), int(seg))
                for lon, lat, seg in csv.reader(fd)]
    
    print("Creating graph...")
    graph = graphmaker.make_graph(points, n)
    if simplify:
        graphmaker.simplify_graph(graph, max_dist, epsilon)
    
    print("Getting monuments...")


    print("Finding routes...")

    