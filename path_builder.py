from haversine import haversine
import networkx as nx
from sklearn.cluster import KMeans
import csv
from matplotlib import pyplot as plt
from staticmap import *


from clustering import cluster

import yogi


Point = tuple[float, float]
Path = list[tuple[Point, Point]]


def distance(p1: Point, p2: Point) -> float:
    """Returns the distance between two points on Earth expressed in
    spherical coordinates (longitude, latitude)."""
    return haversine((p1[1], p1[0]), (p2[1], p2[0])) 

def cluster_paths(clust_center: list[Point]) -> nx.Graph:
    """
    L'entrada és una llista de tuples corresponents als centres dels clusters
    Es retorna el graf amb els camins
    """
    #Afegir nodes
    G = nx.Graph()
    for i in range(len(clust_center)):
        G.add_node(i, pos=clust_center[i])
    pos = nx.get_node_attributes(G, 'pos')

    #Generar el staticmap
    m = StaticMap(1000, 1000)

    #Obrir CSV
    with open('ebre_clusters.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    #Buscar Arestes
    prev_seg = -1
    prev_label = -1
    for _, _, s, c in data:
        if prev_seg == int(s) and prev_label != int(c):
            if distance(pos[prev_label], pos[int(c)]) < 5:
                G.add_edge(prev_label, int(c), dist=distance(pos[prev_label], pos[int(c)]))
                m.add_line(Line((pos[prev_label], pos[int(c)]), 'blue', 1))
        prev_seg = int(s)
        prev_label = int(c)
    
    #Save staticmap image
    image = m.render()
    image.save('map.png')

    #Graph Plot
    nx.draw(G, pos, node_color='red', node_size=2)
    plt.show()
    return G


def create_graph(cluster_paths: list[list[Point]], filename: str) -> nx.Graph:
    """
    Entrada: Una llista de camins
    
    Retorna un graf amb els clusters com a nodes i les connexions entre clusters
    com a arestes.
    """
    graph = nx.Graph()
    for path in cluster_paths:
        for i in range(len(path) - 1):
            graph.add_edge(path[i], path[i+1], dist = distance(path[i], path[i+1]))
    return graph

    ...

def simplify_graph(graph: nx.Graph) -> nx.Graph:
    """
    Simplifica el graf.
    """
    ...

def testing() -> None:
    """
    Prova les funcions del mòdul.
    """
    cluster_paths(cluster(100))
    ...

if __name__ == "__main__": testing()