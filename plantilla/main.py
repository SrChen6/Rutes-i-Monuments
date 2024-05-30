from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point


def show_graph(filename: str) -> None:
    """Given the filename, shows the maps of the region"""
    points = segments.load_points(filename)
    print("Showing all the points imported...")
    segments.show_segments(points, filename)
    print("Showing the most common routes...")
    graph = graphmaker.make_graph(points, 300)
    viewer.export_PNG(graph, filename)
    viewer.export_KML(graph, filename)
    print("A KML file has been created, you can upload it to Google Earth to view it")
    print("Showing the shortest routes to some monuments")
    #TODO: Get box
    #TODO: export monuments graph
    

def new_region() -> None:
    """shows the map of a new region"""
    print("Please enter the coordenates of the new region ")
    print("Write the coordenates of the south, west, north, east boundaries separated by spaces")
    bl = Point(read(float), read(float), -1)
    tr = Point(read(float), read(float), -1)
    box = Box(bl, tr)
    print("Please enter a name for this region")
    name = read(str)
    segments.download_points(box, name)
    show_graph(name)


def old_region() -> None:
    print("Please enter the name of the region")
    name = read(str)
    show_graph(name)


def user_input() ->int:
    """First interactions with the user. Returns the name of the region that the 
    user wants to plot."""
    print("====================")
    print("Welcome! Ready to explore the world?")
    print("Please write one of the following digits.")
    print("1 - Show the map of a new region.")
    print("2 - Show the map of a region already downloaded")
    print("3 - Download the monuments of Catalonia")
    return read(int)   


def main() -> None:
    command = user_input()
    if command == 1:
        new_region()
    elif command == 2:
        old_region()
    elif command == 3:
        monuments.download_monuments("Monuments")
    else:
        print("""The input is not valid. Please re-execute the program and 
              introduce a valid one""")
        
    print("Thank you for using out app, we hope that it's benn usefull :)")


if __name__ == "__main__":
    main()



