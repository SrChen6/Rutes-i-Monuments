import networkx as nx
from staticmap import Line, StaticMap

def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    map = StaticMap(1000, 1000)
    pos = nx.get_node_attributes(graph, 'pos')

    for u, v in graph.edges:
        map.add_line(Line((pos[u], pos[v]), 'black', 1))
    
    image = map.render()
    image.save(filename)


def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    ...
