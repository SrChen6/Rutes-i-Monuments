import csv
import networkx as nx
from sklearn.cluster import KMeans
from haversine import haversine
import math

import viewer
from segments import Point


def make_graph(points: list[Point], n: int) -> nx.Graph:
    """
    Crea el graf a partir de la llista de punts.
    points: La llista de punts obtinguda al descarregar el fitxer GPX.
    La llista està ordenada segons el seu nombre de segment i, per cada
    segment, els punts estàn ordenats prèviament per temps.

    n: El nombre de clusters del que estarà format el graf.
    """
    # clustering
    print("making graph...")
    kmeans = KMeans(n_clusters = n, random_state = 0,
                    n_init = "auto").fit([(point.lon, point.lat) for point in points])
    
    # inicialització del graf
    graph = nx.Graph()
    for i in range(len(kmeans.cluster_centers_)):
        graph.add_node(i, pos = kmeans.cluster_centers_[i])

    # definició d'arestes
    pos = nx.get_node_attributes(graph, 'pos')
    prev_seg, prev_lab = -1, -1
    for point, lab in zip(points, kmeans.labels_):
        if prev_seg == point.seg and prev_lab != lab:
            graph.add_edge(prev_lab, lab, dist = haversine(pos[prev_lab], pos[lab]))
        prev_seg = point.seg
        prev_lab = lab

    simplify_graph(graph, 4, 0)

    return graph

def angle(graph: nx.Graph, u: int, v: int, w: int) -> float:
    """Given three connected nodes of a graph, returns the angle between v and w
    in degrees. If w=-1 it is returned 90"""
    if w == -1:
        return 90
    pos = nx.get_node_attributes(graph, 'pos')
    uv = (abs(pos[u][0] - pos[v][0]), abs(pos[u][1] - pos[v][1]))
    uw = (abs(pos[u][0] - pos[w][0]), abs(pos[u][1] - pos[w][1]))
    mod_uv = math.sqrt(uv[0]**2+uv[1]**2)
    mod_uw = math.sqrt(uw[0]**2+uw[1]**2)
    uv_uw = uv[0]*uw[0]+uv[1]*uw[1]
    return math.acos(uv_uw/(mod_uv*mod_uw))*180/math.pi
# TODO: functional but not finished

def simplify_graph(graph: nx.Graph, max_dist: float, epsilon: float) -> None:
    """Simplifies the graph."""
    print("simplifying graph...")
    pos = nx.get_node_attributes(graph, 'pos')
    dist = nx.get_edge_attributes(graph, 'dist')


    # Deletes the nodes that are comically long
    graph.remove_edges_from(edge for edge in graph.edges if dist[edge] > max_dist)
    prev_node = 1

    # Deletes the longest of tow edges that are too close together 
    edges_to_rm: list[tuple[int, int]] = []
    for u in graph.nodes:
        for v in graph.neighbors(u):
            ang = angle(graph, u, v, prev_node)
            if abs(ang) < 5:
                print(ang, "Too small!")
                edges_to_rm.append((u, v))
    graph.remove_edges_from(edges_to_rm)


def __testing(n: int, simplify: bool,
              max_dist: float, epsilon: float,
              filename: str) -> None:
    """Testing function."""

    print("Loading points...")
    fd = open("Ebre.csv", 'r')
    points = [Point(float(lat), float(lon), int(seg))
                for lon, lat, seg in csv.reader(fd)]
    
    print("Creating graph...")
    graph = make_graph(points, n)
    if simplify:
        simplify_graph(graph, max_dist, epsilon)
    
    print("Exporting graph...")
    viewer.export_PNG(graph, filename)


if __name__ == "__main__":
    __testing(300, True, 4.0, 0, "test_300_simple4km.png")
