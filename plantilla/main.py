from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point

def print_points(filename: str) -> None:
    print(segments.load_points(filename))

def user_pov() ->None:
    print("Welcome! Please enter a region")
    print("Enter the west, south, east, north edges separated by spaces")
    bl = Point(read(float), read(float), -1)
    tr = Point(read(float), read(float), -1)
    box = Box(bl, tr)
    print("Please enter a name for this region")
    name = read(str)
    # segments.download_points(box, name)
    segments.show_segments(segments.load_points(name), name)
    graph = graphmaker.make_graph(segments.load_points(name), 300)
    viewer.export_PNG(graph, name)
    viewer.export_KML(graph, name)


def tests() -> None:
    name = read(str)
    graph = graphmaker.make_graph(segments.load_points(name), 300)
    viewer.export_KML(graph, name)
    viewer.export_PNG(graph, name)


def main() -> None:
    print("If user, write 1. If developer, write 2")
    n = read(int)
    if n==1:
        user_pov()
    elif n == 2:
        tests()
    print("Finsied :)")


if __name__ == "__main__":
    main()



