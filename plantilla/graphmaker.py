
from segments import Point

import networkx as nx
from sklearn.cluster import KMeans

from segments import Point
from haversine import haversine

def make_graph(segments: Point, clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    ...

def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""
    ...

def make_graph(points: list[Point], n: int) -> nx.Graph:
    """
    Crea el graf a partir de la llista de punts.
    points: La llista de punts obtinguda al descarregar el fitxer GPX.
    La llista està ordenada segons el seu nombre de segment i, per cada
    segment, els punts estàn ordenats prèviament per temps.

    n: El nombre de clusters del que estarà format el graf.
    """

    # clustering
    kmeans = KMeans(n_clusters = n, random_state = 0,
                    n_init = "auto").fit([(point.lat, point.lon) for point in points])
    
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

    return graph


def simplify_graph(graph: nx.Graph, max_dist: float, epsilon: float) -> nx.Graph:
    """Simplifies the graph."""
    # TODO: Simplificació per distància 
    # (dos clusters que estan connectats pero molt allunyats)
    ...

    # TODO: Simplificació per angle.
    # (lo del github)
    ...
