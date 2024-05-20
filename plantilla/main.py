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
    print("Enter the bottom left and the top right points separated by spaces")
    bl = Point(read(float), read(float), -1, -1)
    tr = Point(read(float), read(float), -1, -1)
    box = Box(bl, tr)
    print("Please enter a name for this region")
    name = read(str)
    segments.download_points(box, name)
    segments.show_segments(segments.load_points(name), name)


def tests() -> None:
    name = read(str)
    segments.show_segments(segments.load_points(name), name)


def main() -> None:
    print("If user, write 1. If developer, write 2")
    n = read(int)
    if n==1:
        user_pov()
    elif n == 2:
        tests()


if __name__ == "__main__":
    main()



