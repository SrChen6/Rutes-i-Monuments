import csv
import networkx as nx
from sklearn.cluster import KMeans
from haversine import haversine
import math

import viewer
from segments import Point, Box


REFERENCE_CLUSTERS = 300
REFERENCE_ANGLE = 2 * 0.08726646259971647   # 5º ~ 0.087 rad is the minimum angle between edges
REFERENCE_DISTANCE = 4  # 4 km is the max distance an edge can have


Vec2D = tuple[float, float]


def __module(vec: Vec2D) -> float:
    """Returns the module of the 2D vector."""
    return math.sqrt(vec[0]**2 + vec[1]**2)

def __scalar_product(A: Vec2D, B: Vec2D) -> float:
    """Returns the scalar product of A and B."""
    return A[0] * B[0] + A[1] * B[1]


def __angle_between(A: Vec2D, B: Vec2D, C: Vec2D) -> float:
    """Returns the angle between AB and BC."""
    vec1 = (B[0] - A[0], B[1] - A[1])
    vec2 = (C[0] - B[0], C[1] - B[1])
    return math.acos(__scalar_product(vec1, vec2) / __module(vec1) / __module(vec2))


def __simplify_by_angle(graph: nx.Graph, angle: float) -> nx.Graph:
    """
    Simplifies the graph by joining consecutive edges
    which do not differ more than the given angle.
    """
    pos = nx.get_node_attributes(graph, 'pos')
    for node in list(graph.nodes):
        edges = list(graph.edges(node))
        if len(edges) == 2:
            u, v = tuple(n for edge in edges for n in edge
                         if n != node)
            if angle > __angle_between(pos[u], pos[node], pos[v]):
                graph.add_edge(u, v, dist = haversine(pos[u], pos[v]))
                graph.remove_node(node)
    return graph


def __simplify_by_distance(graph: nx.Graph, distance: float) -> None:
    """
    Simplifies the graph by removing edges which are longer
    than the given distance.
    """
    dist = nx.get_edge_attributes(graph, 'dist')
    graph.remove_edges_from(edge for edge in graph.edges if dist[edge] > distance)


def make_graph(points: list[Point], n: int) -> nx.Graph:
    """
    Creates the graph from the list of points.

    points: The list of points obtained by loading from a .csv file
    with segments.py module. The list is ordered by number of segment
    and, for each segment, the points are ordered previously by time
    (all of this is done by segments.py).

    n: The number of clusters which will form the graph.
    """
    print("Making graph...")
    # clustering
    kmeans = KMeans(n_clusters = n, random_state = 0, n_init = "auto").fit([(point.lat, point.lon) for point in points])
    
    # Inicialization of the graf
    graph = nx.Graph()
    for i in range(len(kmeans.cluster_centers_)):
        graph.add_node(i, pos = kmeans.cluster_centers_[i])

    # Defining edges
    pos = nx.get_node_attributes(graph, 'pos')
    prev_seg, prev_lab = -1, -1
    for point, lab in zip(points, kmeans.labels_):
        if prev_seg == point.seg and prev_lab != lab:
            graph.add_edge(prev_lab, lab, dist = 
                           haversine(pos[prev_lab], pos[lab]))
        prev_seg = point.seg
        prev_lab = lab
    
    print("Simplifying graph...")
    __simplify_by_distance(graph, REFERENCE_DISTANCE)
    __simplify_by_angle(graph, REFERENCE_ANGLE)

    return graph


if __name__ == "__main__":
    import viewer
    import segments
    from yogi import read

    N = read(int)
    for _ in range(N):
        filename = read(str)
        points = segments.load_points(filename)
        box = segments.load_box(filename)
        graph = make_graph(points, REFERENCE_CLUSTERS)
        viewer.export_PNG(graph, filename)
