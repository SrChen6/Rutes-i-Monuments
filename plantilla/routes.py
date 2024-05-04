import networkx as nx
from segments import Point
from monuments import Monuments


class Routes:
    ...

def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    ...

def export_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    ...


def export_KML(groutes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    ...