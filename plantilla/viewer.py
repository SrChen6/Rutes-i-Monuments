import networkx as nx
from staticmap import Line, StaticMap
import simplekml


def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    print("exporting PNG...")
    pos = nx.get_node_attributes(graph, 'pos')
    map = StaticMap(1000, 1000)
    
    for u, v in graph.edges:
        map.add_line(Line(((pos[u][1], pos[u][0]), (pos[v][1], pos[v][0])), 'black', 1))
    
    image = map.render()
    image.save(f"{filename}.png")
    image.show()


def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    print("Exporting KML...")
    kml = simplekml.Kml()
    pos = nx.get_node_attributes(graph, 'pos')
    for u, v in graph.edges:
        lin = kml.newlinestring(
            name="Segment",
            description="Ruta comuna",
            coords = [(pos[u][1], pos[u][0]), (pos[v][1], pos[v][0])]
        )
        lin.style.linestyle.width = 1

    kml.save(f"{filename}.kml")