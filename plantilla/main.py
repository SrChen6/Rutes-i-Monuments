from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point

def print_points(filename: str) -> None:
    print(segments.load_points(filename))

def user_input() ->tuple[Box, str]:
    """First interactions with the user. Returns the name of the region that the 
    user wants to plot."""
    print("Welcome! Ready to explore the world?")
    print("Would you like to download new routes?")
    print("Write 'yes' if you want to download new routes.")
    print("Write 'no' if you want to view an already existing graph.")
    while True:
        if read(str) == "yes":
            print("Enter the west, south, east, north boundaries separated by spaces.")
            bl = Point(read(float), read(float), -1)
            tr = Point(read(float), read(float), -1)
            box = Box(bl, tr)
            print("Please enter a name for this region.")
            return box, read(str)
        elif read(str) == "no":
            print("Please enter the name of the region you want to view.")
            # If the file already exists, the box won't be used
            # CONSULTAR AMB MARTÍ
            return Box(Point(0,0, -1), Point(0,0, -1)), read(str)
        else: print("This is not a valid input. Please write 'yes' or 'no'")

def user_pov() ->None:
    box, name = user_input()
    # segments.download_points(box, name)
    points = segments.get_points(box, name)
    segments.show_segments(points, name)
    graph = graphmaker.make_graph(points, 300)
    viewer.export_PNG(graph, name)
    viewer.export_KML(graph, name)
    


def tests() -> None:
    name = read(str)
    graph = graphmaker.make_graph(segments.load_points(name), 100)
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



