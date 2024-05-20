from yogi import read
import segments
import graphmaker
import monuments
import routes
import viewer
from segments import Box, Point


def main() -> None:
    print("Welcome! Please enter a region (bottom left, top right)")
    bl = Point(read(float), read(float), -1, -1)
    tr = Point(read(float), read(float), -1, -1)
    box = Box(bl, tr)
    print("Please enter a name for this region")
    name = read(str)
    print(box, name)
    segments.download_points(box, name)




