from dataclasses import dataclass
import requests
import gpxpy
import csv
from os.path import isfile #checks if file exists
from staticmap import Line, StaticMap


# TODO: IMPLEMENT EXCEPTIONS


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
    print('Downloading point data...')
    num_seg = 0
    page = 0
    region = f"{box.bottom_left.lon},{box.bottom_left.lat},{box.top_right.lon},{box.top_right.lat}"
    f = open(f"{filename}.csv", "w")

    # The first two points in the csv file are the Box's limits.
    # These points are ignored when loading data from file with 'load_points'.
    f.write(f"{box.bottom_left.lat},{box.bottom_left.lon},{-1}\n")
    f.write(f"{box.top_right.lat},{box.top_right.lon},{-1}\n")

    while True:
        url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={region}&page={page}"
        response = None
        while response is None:
            try: response = requests.get(url)
            except: pass

        # We have never had an error occur when parsing GPX files,
        # but better safe than sorry.
        gpx_content = response.content.decode("utf-8")
        try: gpx = gpxpy.parse(gpx_content)
        except:
            print(f"An error ocurred while trying to parse data from downloaded GPX file. Skiping page {page}...")
            continue

        if len(gpx.tracks) == 0:
            break
        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    segment.points.sort(key = lambda p: p.time)  # type: ignore
                    for point in segment.points:
                        f.write(f"{point.latitude},{point.longitude},{num_seg}\n")
                num_seg += 1
        
        print(f"Finished importing page {page}...")                
        page += 1

    print("Finished importing point data for the region.")
    f.close()


# TODO: Hao, si prefereixes com era abans, m'ho dius, encara que crec que ara
# és una funció més concisa i més eficient perquè no copia el fitxer a una llista.
def load_points(filename: str) -> list[Point]:
    """Load points from the file."""
    print(f"Loading point data from {filename}.csv...")

    if not isfile(f'{filename}.csv'):
        print(f"ERROR: {filename}.csv does not exist.")
        print("You will have to download point data from the region again.")
        exit()

    try:
        with open(f'{filename}.csv', 'r', newline = '') as f:
            reader = csv.reader(f)
            # Skips over the first two points (they define the box of the region).
            next(reader, None)
            next(reader, None)
            data =  [Point(float(lat), float(lon), int(s)) for lat, lon, s in reader]
            if len(data) == 0:
                print(f"WARNING: Point data for {filename} is empty.")
            return data
    except:
        print(f"ERROR: An error ocurred while trying to read point data from {filename}.csv.")
        print("The file may be corrupted; you may have to download point data from the region again.")
        exit()

    # pts: list[Point] = []

    # #Obrir CSV
    # with open(f'{filename}.csv', 'r', newline='') as f:
    #     reader = csv.reader(f)
    #     #Ignorem els dos primers punts (del box)
    #     next(reader)
    #     next(reader)
    #     data = list(reader)
    # #Llegir fila
    # for lat, lon, s in data:
    #     pts.append(Point(float(lat), float(lon), int(s)))
    # return pts


def load_box(filename: str) -> Box:
    """Load the box from the point file."""
    try:
        with open(f'{filename}.csv', 'r', newline = '') as f:
            reader = csv.reader(f)
            min_lat, min_lon, _ = next(reader)
            max_lat, max_lon, _ = next(reader)
            return Box(Point(float(min_lat), float(min_lon), -1),
                    Point(float(max_lat), float(max_lon), -1))
    except:
        print(f"ERROR: An exception ocurred while trying to read region data from file {filename}.csv.")
        print("The file may not exist, be corrupted or be located in a different folder.")
        print("You may have to download point data from the region again.")
        exit()


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
    m = StaticMap(1000, 1000)
    prev_pt = Point(-1, -1, -1)
    for pt in pts:
        if prev_pt != Point(-1, -1, -1) and pt.seg == prev_pt.seg:
            m.add_line(Line(((prev_pt.lon, prev_pt.lat), (pt.lon, pt.lat)), 'blue', 1))
        prev_pt = pt
    
    # An error may occur if the map is empty (when there are no points.).
    try:
        img = m.render()
        img.save(f"{filename}_points.png")
    except:
        print("ERROR: Failed to render StaticMaps image (point map).")


if __name__ == "__main__":
    from yogi import read
    print("Testing segments.py module.")
    N = read(int)
    for _ in range(N):
        box = Box(Point(read(float), read(float), -1),
                  Point(read(float), read(float), -1))
        filename = read(str)
        download_points(box, filename)
        points = load_points(filename)
        show_segments(points, filename)
    # box = Box(Point(41.940344, 2.778792, -1),
    #           Point(42.018007, 2.849885, -1)
    # )
    # filename = "Girona"
    # download_points(box, filename)
    # load_points(filename)

