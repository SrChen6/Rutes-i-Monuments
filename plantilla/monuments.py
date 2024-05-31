import requests
import bs4
import json
import csv
from os.path import isfile

from dataclasses import dataclass
from segments import Point, Box
from typing import TypeAlias


@dataclass
class Monument:
    name: str
    location: Point

Monuments: TypeAlias = list[Monument]


# Website link from which to download monument information (Catalunya Medieval).
CM_LINK = "https://www.catalunyamedieval.es/comarques/"

# In the HTML file, the script that needs to be downloaded is the eighth found by
# Beautiful Soup's lineal search. If the web is updated and problems arise,
# we should check if the script has been moved or removed.
SCRIPT_NUM = 7


def __print_monuments(monuments: Monuments) -> None:
    """Print the list of monuments. (For testing.)"""
    for i, mon in enumerate(monuments):
        print(f"{i}. {mon.name}, ({mon.location.lat}, {mon.location.lon})")


def __monuments_to_csv(monuments: Monuments, filename: str) -> None:
    """Convert a list of monuments into a .csv file."""
    fd = open(f"{filename}", "w")
    for mon in monuments:
        fd.write(f"\"{mon.name}\",{mon.location.lat},{mon.location.lon}\n")
    fd.close()


def download_monuments(filename: str) -> Monuments:
    """Download monuments from Catalunya Medieval into a file."""
    response = None
    while response is None:
        try: response = requests.get(CM_LINK)
        except: pass
    
    # This block of code gets the JSONs from the java script.
    monuments = Monuments()
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script', type = "text/javascript")
    for line in scripts[SCRIPT_NUM].get_text().splitlines():
        line = line.strip()
        if line and line[0] == "v":
            json_data = line[len(line.split("=")[0])+1:-1]
            parsed_data = json.loads(json_data)
            for item in parsed_data:
                monuments.append(Monument(
                    item["title"],
                    Point(item["position"]["lat"], item["position"]["long"], -1)
                    )
                )
    
    __monuments_to_csv(monuments, filename)
    return monuments


def load_monuments(box: Box, filename: str) -> Monuments:
    """Load monuments from a file."""
    fd = open(filename, "r")
    reader = csv.reader(fd)
    try:
        return [Monument(name, Point(float(lat), float(lon), -1))
                for name, lat, lon in reader
                if box.bottom_left.lat < float(lat) < box.top_right.lat
                    and box.bottom_left.lon < float(lon) < box.top_right.lon]
    except:
        print(f"An error ocurred while trying to load monument information from file {filename}.")
        exit()


def get_monuments(box: Box, filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    if not isfile(f"{filename}.csv"):
        print(f"File not found. Downloading monuments from {CM_LINK} into a new file with this name...")
        download_monuments(filename)
    print("Loading and filtering monuments by location...")
    return load_monuments(box, filename)


if __name__ == "__main__":
    """Testing."""
    from yogi import read
    box = Box(Point(read(float), read(float), -1),
              Point(read(float), read(float), -1))
    mons = get_monuments(box, "prova.csv")
    __print_monuments(mons)
    