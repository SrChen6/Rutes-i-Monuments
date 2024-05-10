from haversine import haversine
from networkx import Graph
from sklearn.cluster import KMeans

from random import randint
import yogi


Point = tuple[float, float]
Path = list[tuple[Point, Point]]


def distance(p1: Point, p2: Point) -> float:
    """Returns the distance between two points on Earth expressed in
    spherical coordinates (longitude, latitude)."""
    return haversine((p1[1], p1[0]), (p2[1], p2[0]))


# aquí he posat una funció que encapsularia tota la feina de clustering i de fer el graph
# TODO: si no t'agrada així o creus que ho hauríem de fer d'una altra manera,
# comenta-m'ho.

# TODO: capçalera subject to change, l'estructura de les dades pot canviar
def cluster_paths(data: list[tuple[Point, int]], n: int) -> list[Path]:
    """
    L'entrada és una llista de tuples i el nombre de clusters.
    En cada tupla, el primer element és un punt, el segon és l'ID del seu segment.

    Fa el clustering de tots els punts.
    Retorna una llista de camins entre clusters.
    """

    # Fa el clustering.
    coords = [coord for coord, _ in data]
    kmeans = KMeans(n_clusters = n, random_state = 0, n_init = "auto").fit(coords)

    # Inicialitza la llista resultat (una mica lleig, però bueno)
    last_segment = data[-1][1]
    paths: list[Path] = [[] for _ in range(last_segment)]

    # Crea els camins entre clusters.
    data_with_labels = zip(data, kmeans.labels_)
    prev_seg = -1
    prev_label = -1
    for (_, seg), label in data_with_labels:
        if prev_seg == seg and prev_label != label:
            clust1 = kmeans.cluster_centers_[prev_label]
            clust2 = kmeans.cluster_centers_[label]
            paths[seg].append((clust1, clust2))
        prev_seg = seg
        prev_label = label
    
    return paths
        

def create_graph_experimental(data: list[tuple[Point, int]], n: int) -> Graph:
    """
    L'entrada és una llista de tuples i el nombre de clusters.
    En cada tupla, el primer element és un punt, el segon és l'ID del seu segment.

    Fa el clustering de tots els punts.
    Retorna una llista de camins entre clusters.
    """
    paths = clustering()
    



def create_graph(cluster_paths: list[list[Point]], filename: str) -> Graph:
    """
    Entrada: Una llista de camins
    
    Retorna un graf amb els clusters com a nodes i les connexions entre clusters
    com a arestes.
    """
    graph = Graph()
    for path in cluster_paths:
        for i in range(len(path) - 1):
            graph.add_edge(path[i], path[i+1], dist = distance(path[i], path[i+1]))
    return graph

    ...

def simplify_graph(graph: Graph) -> Graph:
    """
    Simplifica el graf.
    """


def testing() -> None:
    """
    Prova les funcions del mòdul.
    """
    N = yogi.read(int)
    clusters = [(randint(0, 10**5) / 100, randint(0, 10**5) / 100) for _ in range(N)]
    create_graph(clusters, "your_mom")
    ...

if __name__ == "__main__": testing()