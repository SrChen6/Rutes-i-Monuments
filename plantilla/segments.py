from dataclasses import dataclass
import requests
import gpxpy
import csv
from os.path import isfile #checks if file exists
from staticmap import Line, StaticMap


@dataclass
class Point:
    lat: float
    lon: float
    seg: int

@dataclass
class Box:
    bottom_left: Point
    top_right: Point


def download_points(box: Box, filename: str) -> None:
    """Download all segments in the box and save them to the file."""
    print('downloading points...')
    num_seg = 0
    started = False
    page = 0
    region = f"{box.bottom_left.lat},{box.bottom_left.lon},{box.top_right.lat},{box.top_right.lon}"
    f = open(f"{filename}.csv", "w")
    while True:
        url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={region}&page={page}"
        response = requests.get(url)
        gpx_content = response.content.decode("utf-8")
        gpx = gpxpy.parse(gpx_content)

        if len(gpx.tracks) == 0:
            break
        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    segment.points.sort(key=lambda p: p.time)  # type: ignore
                    for i in range(len(segment.points)):
                        p1 = segment.points[i]
                        if not started:
                            print("started importing")
                            started= True
                        f.write(f"{p1.longitude},{p1.latitude},{num_seg}")
                        f.write("\n")
                num_seg += 1
        print(f"finished importing page {page}")                
        page += 1

    print("finished importing")
    f.close()

def load_points(filename: str) -> list[Point]:
    """Load segments from the file."""
    print('loading points...')
    pts: list[Point] = []

    #Obrir CSV
    with open(f'{filename}.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    #Llegir fila
    for x, y, s in data:
        #Mentre no es fagi el cluster, Point.clust = -1
        pts.append(Point(float(x), float(y), int(s)))
    return pts

def get_points(box: Box, filename: str) -> list[Point]:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    print('getting points...')
    if not isfile(filename):
        download_points(box, filename)
    return load_points(filename)

def show_segments(pts: list[Point], filename: str) -> None:
    """Show all segments in a PNG file using staticmaps."""
    #TODO: plotejar tots els camins
    print("exporting segments to a PNG...")
    m = StaticMap(1000, 1000)
    prev_pt = Point(-1, -1, -1)
    for pt in pts:
        if prev_pt != Point(-1, -1, -1) and pt.seg == prev_pt.seg:
            m.add_line(Line(((prev_pt.lat, prev_pt.lon), (pt.lat, pt.lon)), 'blue', 1))
        prev_pt = pt
    img = m.render() #TODO: Check if this works (requires internet)
    img.save(f"{filename}_total.png")