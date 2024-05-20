# Mòdul per descarregar els monuments de https://www.catalunyamedieval.es/.
# De moment, només de prova.

import requests
import bs4

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


def __load_monuments(filename: str) -> None:
    """"""
    # TODO: Com guardarem els monuments?
    ...

if __name__ == "__main__":
    # __download_and_print_links()
    __download_monuments()