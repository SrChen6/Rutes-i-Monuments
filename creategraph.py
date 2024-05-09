import csv
from haversine import haversine
from networkx import Graph

from random import randint
import yogi


Point = tuple[float, float]
Path = list[float, float]


def distance(p1: Point, p2: Point) -> float:
    """Returns the distance between two points on Earth expressed in
    spherical coordinates (longitude, latitude)."""
    return haversine((p1[1], p1[0]), (p2[1], p2[0]))


# aquí he posat una funció que encapsularia


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