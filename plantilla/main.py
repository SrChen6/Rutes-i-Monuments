from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point

def print_points(filename: str) -> None:
    print(segments.load_points(filename))

def main() -> None:
    print("Welcome! Please enter a region")
    print("Enter the bottom left and the top right points separated by spaces")
    bl = Point(read(float), read(float), -1, -1)
    tr = Point(read(float), read(float), -1, -1)
    box = Box(bl, tr)
    print("Please enter a name for this region")
    name = read(str)
    segments.download_points(box, name)

if __name__ == "__main__":
    main()



