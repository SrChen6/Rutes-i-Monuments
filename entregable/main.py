from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point


def show_graphs(filename: str, start: Point) -> None:
    """Given the points filename, shows the maps of the region."""

    print("Loading points from file...")
    points = segments.load_points(filename)
    print("Showing all the points imported...")
    segments.show_segments(points, filename)

    print("Finding the most common paths...")
    graph = graphmaker.make_graph(points, 300)
    viewer.export_PNG(graph, filename)
    viewer.export_KML(graph, filename)
    print("A KML file has been created, you can upload it to Google Earth"
          " to view the graph. A PNG file has also been created.")
    
    print("Finding the shortest routes to near monuments...")
    box = segments.load_box(filename)
    mons = monuments.get_monuments(box, "monuments")
    route_list = routes.find_routes(graph, start, mons)
    routes.export_PNG(route_list, f"{filename}_monuments")
    routes.export_KML(route_list, f"{filename}_monuments")
    print("A KML file has been created, you can upload it to Google Earth"
          " to view the routes. A PNG file has also been created.")
    

def new_region() -> None:
    """Asks for information of a new region and current location of the user
    Exports the maps of the new region."""

    print("Please enter the coordenates of the new region ")
    print("Write the coordenates of the south, west, north, east boundaries"
          " separated by spaces (north / south in latitude,"
          " east / west in longitude).")
    bl = Point(read(float), read(float), -1)
    tr = Point(read(float), read(float), -1)
    box = Box(bl, tr)

    print("Please enter a name for this region.")
    filename = read(str)
    print("Please enter your current location (latitude, longitude).")
    start = Point(read(float), read(float), -1)

    segments.download_points(box, filename)
    show_graphs(filename, start)


def old_region() -> None:
    """
    Asks for the name of an old region and current location of the user.
    Exports the maps of the old region.
    """
    print("Please enter the name of the region.")
    name = read(str)
    print("Please enter your current location (latitude, longitude).")
    start = Point(read(float), read(float), -1)
    show_graphs(name, start)


def user_input() -> int:
    """
    First interactions with the user.
    Returns the number associated with the user's option.
    - 1. Create the map of a new region.
    - 2. Create the map of a region already downloaded.
    """
    print("====================")
    print("Welcome! Ready to explore the world?")
    print("Please choose one of the following options.")
    print("1 - Show the map of a new region.")
    print("2 - Show the map of a region already downloaded.")
    return read(int)   


def main() -> None:
    command = user_input()
    if command == 1:
        new_region()
    elif command == 2:
        old_region()
    else:
        print("The input is not valid. Please re-execute the program and"
              " introduce a valid one")
        
    print("Thank you for using our app, we hope that it's been useful. :)")


if __name__ == "__main__":
    main()