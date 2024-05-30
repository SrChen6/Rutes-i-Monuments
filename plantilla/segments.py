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
    page = 0
    region = f"{box.bottom_left.lon},{box.bottom_left.lat},{box.top_right.lon},{box.top_right.lat}"
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
                        f.write(f"{p1.latitude},{p1.longitude},{num_seg}")
                        f.write("\n")
                num_seg += 1
        
        print(f"finished importing page {page}")                
        page += 1

    print("finished importing")
    f.close()

def load_points(filename: str) -> list[Point]:
    """Load segments from the file."""
    pts: list[Point] = []

    #Obrir CSV
    with open(f'{filename}.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    #Llegir fila
    for lat, lon, s in data:
        pts.append(Point(float(lat), float(lon), int(s)))
    return pts

#TODO: no pinta molt útil, si al final no l'utilitzem el borrem
def get_points(box: Box, filename: str) -> list[Point]:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    if isfile(f'{filename}.csv'):
        return load_points(filename)
    else:
        download_points(box, filename)
    return load_points(filename)

def show_segments(pts: list[Point], filename: str) -> None:
    """Show all segments in a PNG file using staticmaps."""
    #TODO: plotejar tots els camins
    m = StaticMap(1000, 1000)
    prev_pt = Point(-1, -1, -1)
    for pt in pts:
        if prev_pt != Point(-1, -1, -1) and pt.seg == prev_pt.seg:
            m.add_line(Line(((prev_pt.lat, prev_pt.lon), (pt.lat, pt.lon)), 'blue', 1))
        prev_pt = pt
    img = m.render() #TODO: Check if this works (requires internet)
    img.save(f"{filename}_total.png")
    img.show()



if __name__ == "__main__":
    box = Box(Point(40.5363713, 0.5739316671, -1),
              Point(40.79886535, 0.9021482, -1)
    )
    filename = "prova_points"
    download_points(box, filename)
    load_points(filename)

