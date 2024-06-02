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

def find_routes(graph: nx.Graph, start: Point, 
                endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and
      all the endpoints."""
    routes = Routes()
    start_node = __nearest_node(graph, start)
    pos = nx.get_node_attributes(graph, 'pos')
    dist = nx.get_edge_attributes(graph, 'dist')

    for end in endpoints:
        end_node = __nearest_node(graph, end.location)
        try:
            node_path = nx.algorithms.shortest_path(graph, start_node, 
                                                    end_node, 'dist')
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
    print("Exporting routes to PNG file...")
    map = StaticMap(1000, 1000)
    for route in routes:
        for i in range(len(route.path) - 1):
            map.add_line(Line((route.path[i][::-1], 
                               route.path[i+1][::-1]), 'black', 1))
    
    try:
        image = map.render()
        image.save(f"{filename}_routes.png")
    except:
        print("ERROR: Failed to render StaticMaps image (route map).")     


def export_KML(routes: Routes, filename: str) -> None:
    """Export the routes to a KML file."""
    # TODO: Make it pretty! Make it glow!
    kml = Kml()
    for route in routes:
        newline = kml.newlinestring(
            name = route.name,
            description = f"Shortest route to {route.name}, {route.dist} km.",
            coords = (coord[::-1] for coord in route.path)
        )
        newline.style.linestyle.color = "red"
        newline.style.linestyle.width = 5
    kml.save(f"{filename}_routes.kml")


if __name__ == "__main__":
    import monuments
    import graphmaker
    import segments
    from segments import Box
    from yogi import read

    N = read(int)

    for _ in range(N):
        box = Box(Point(read(float), read(float), -1),
                  Point(read(float), read(float), -1))
        filename = read(str)
        start = Point(read(float), read(float), -1)

        points = segments.load_points(filename)
        graph = graphmaker.make_graph(points, 300)
        mons = monuments.get_monuments(box, "monuments")
        routes = find_routes(graph, start, mons)
        export_PNG(routes, filename)
        export_KML(routes, filename)

    