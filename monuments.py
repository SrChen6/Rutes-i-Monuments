# Mòdul per descarregar els monuments de https://www.catalunyamedieval.es/.
# De moment, només de prova.

from definitions import Coord, Box
from dataclasses import dataclass
import csv
import requests
import bs4


@dataclass
class Monument:
    name: str
    coord: Coord


WEBSITE_URL = "https://www.catalunyamedieval.es/"

# Cada tupla conté una de les URLs, i la classe d'elements que busquem.
# Ho he guardat en un fitxer de text.
# Igualment, NO HO MODIFIQUIS (consulta'm abans).
URL_INFO: list[tuple[str, str]] = [
    ("edificacions-de-caracter-militar/castells/",                      "castell"),
    ("edificacions-de-caracter-militar/fortificacions-depoca-carlina/", "epoca-carlina"),
    ("edificacions-de-caracter-militar/muralles/",                      "muralles"),
    ("edificacions-de-caracter-militar/torres/",                        "torre"),
    ("edificacions-de-caracter-civil/cases-fortes/",                    "casa-forta"),
    ("edificacions-de-caracter-civil/palaus/",                          "palau"),
    ("edificacions-de-caracter-civil/ponts/",                           "pont"),
    ("edificacions-de-caracter-civil/torres-colomer/",                  "torre-colomer"),
    ("edificacions-de-caracter-religios/basiliques/",                   "basilica"),
    ("edificacions-de-caracter-religios/catedrals/",                    "catedral"),
    ("edificacions-de-caracter-religios/ermites/",                      "ermita"),
    ("edificacions-de-caracter-religios/esglesies/",                    "esglesia"),
    ("edificacions-de-caracter-religios/esglesies-fortificades/",       "esglesia-fortificada"),
    ("edificacions-de-caracter-religios/monestirs/",                    "monestir"),
    ("altres-llocs-dinteres/",                                          "altres-llocs-dinteres")
]


def __find_coordinate(text: str) -> Coord | None:
    """
    Donat un text, intenta trobar la coordenada
    (si no ho aconsegueix, retorna None).
    """
    # TODO: No tinc valor ara mateix
    ...

def __download_and_print_links() -> None:
    """
    Funció de testeig.
    Escriu tots els links i noms de les adreces de cada monument (tots!).
    """
    for url, monument_type in URL_INFO:
        response = None
        while response is None:
            try: response = requests.get(WEBSITE_URL+url)
            except: pass
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for li in soup.find_all("li", class_ = monument_type):
            link = li.find("a")
            print(link.get("href"), link.text)


# TODO: Fer funció per filtrar les coordenades.
# TODO: Parlar sobre com guardem els monuments
#       (jo voldria guardar-los tots en un csv, no crec que ocupi més de 5 MB)
def __download_monuments() -> None:
    """
    Funció de testeig.
    Escriu tots els noms i coordenades de cada monument (tots!).
    """
    for url, monument_type in URL_INFO:
        response = None
        while response is None:
            try: response = requests.get(WEBSITE_URL+url)
            except: pass
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for li in soup.find_all("li", class_ = monument_type):
            link = li.find("a")
            coordinates = "NOT FOUND"
            monument_resp = None
            while monument_resp is None:
                try: monument_resp = requests.get(link.get("href"))
                except: pass
            monument_soup = bs4.BeautifulSoup(monument_resp.content, "html.parser")
            for p in monument_soup.find_all("p"):
                strong = p.find("strong")
                if strong is not None and strong.text == "Localització":
                    coordinates = p.text
                    break
            print(coordinates, link.text)


def filter_monuments(filename: str, box: Box) -> list[Monument]:
    """
    Des d'un fitxer local, filtra els monuments segons si
    es troben dins de la caixa o no.
    """
    # TODO: Com guardarem els monuments?
    (low_lat, low_long), (high_lat, high_long) = box
    result = list[Monument]()

    with open(filename, newline='') as fd:
        reader = csv.reader(fd)
        next(reader)
        for name, _, lat, long in reader:
            try:
                if (low_lat <= float(lat) <= high_lat and
                    low_long <= float(long) <= high_long):
                    result.append(Monument(name, (float(lat), float(long))))
            except:
                print(f"Error reading monument: {name}")
    
    with open("mons_output.out", 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerows((mon.name, mon.coord[0], mon.coord[1]) for mon in result)
    return result
                

def __print_monuments(monuments: list[Monument]) -> None:
    """
    Printeja els monuments (for testing!).
    """
    for monument in monuments:
        print(monument.name, monument.coord)


BOX_EBRE: Box = ((40.5363713,0.5739316671),(40.79886535,0.9021482))

if __name__ == "__main__":
    # __download_and_print_links()
    # __download_monuments()
    monuments = filter_monuments("mons.csv", BOX_EBRE)
    __print_monuments(monuments)
    ...