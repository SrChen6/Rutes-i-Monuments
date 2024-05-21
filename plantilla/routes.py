import networkx as nx
from haversine import haversine
from typing import TypeAlias

from segments import Point
from monuments import Monuments


Route: TypeAlias = list[Point]
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

    for end in endpoints:
        end_node = __nearest_node(graph, end.location)
        try:
            path = nx.algorithms.dijkstra_path(graph, start_node, end_node, 'dist')
            routes.append([node for node in path])
        except nx.NodeNotFound:
            print("WTF")
        except nx.NetworkXNoPath:
            print(f"No path found from startpoint to monument: {end.name}")
    ...

def export_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    ...


def export_KML(routes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    ...