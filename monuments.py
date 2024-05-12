# Mòdul per descarregar els monuments de https://www.catalunyamedieval.es/.
# De moment, només de prova.

import requests
import bs4      # This

WEBSITE_URL = "https://www.catalunyamedieval.es/"

# Cada tupla conté una de les URLs, i la classe d'elements que busquem.
# Ho he guardat en un fitxer de text.
# Igualment, NO HO MODIFIQUIS (consulta'm abans).
URL_INFO = [
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
        response = requests.get(WEBSITE_URL+url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for li in soup.find_all("li", class_ = monument_type):
            link = li.find("a")
            print(link.get("href"), link.text)


# TODO: Arreglar error quan porta executant-se massa temps.
# TODO: Fer funció per extreure les coordenades.
# TODO: Parlar sobre com guardem els monuments
#       (jo voldria guardar-los tots en un csv, no crec que ocupi més de 5 MB)
def __download_monuments() -> None:
    """
    Funció de testeig.
    Escriu tots els noms i coordenades de cada monument (tots!).
    """
    for url, monument_type in URL_INFO:
        response = requests.get(WEBSITE_URL+url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for li in soup.find_all("li", class_ = monument_type):
            link = li.find("a")
            coordinates = "NOT FOUND"
            # TODO: Crec que el problema és aquesta línea...
            # El servidor es pensa que l'estic atacant o alguna cosa per l'estil.
            monument_resp = requests.get(link.get("href"))
            monument_soup = bs4.BeautifulSoup(monument_resp.content, "html.parser")
            for p in monument_soup.find_all("p"):
                strong = p.find("strong")
                if strong is not None and strong.text == "Localització":
                    coordinates = p.text
            print(coordinates, link.text)

# Troba les coordenades, però s'ha de filtrar el text.

# Al cap d'una estona de estar-se executant, DONA L'ERROR SEGÜENT.

# Traceback (most recent call last):
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 790, in urlopen
#     response = self._make_request(
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 536, in _make_request
#     response = conn.getresponse()
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connection.py", line 461, in getresponse
#     httplib_response = super().getresponse()
#   File "/usr/lib/python3.10/http/client.py", line 1375, in getresponse
#     response.begin()
#   File "/usr/lib/python3.10/http/client.py", line 318, in begin
#     version, status, reason = self._read_status()
#   File "/usr/lib/python3.10/http/client.py", line 287, in _read_status
#     raise RemoteDisconnected("Remote end closed connection without"
# http.client.RemoteDisconnected: Remote end closed connection without response

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/adapters.py", line 486, in send
#     resp = conn.urlopen(
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 844, in urlopen
#     retries = retries.increment(
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/util/retry.py", line 470, in increment
#     raise reraise(type(error), error, _stacktrace)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/util/util.py", line 38, in reraise
#     raise value.with_traceback(tb)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 790, in urlopen
#     response = self._make_request(
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 536, in _make_request
#     response = conn.getresponse()
#   File "/home/simpleman/.local/lib/python3.10/site-packages/urllib3/connection.py", line 461, in getresponse
#     httplib_response = super().getresponse()
#   File "/usr/lib/python3.10/http/client.py", line 1375, in getresponse
#     response.begin()
#   File "/usr/lib/python3.10/http/client.py", line 318, in begin
#     version, status, reason = self._read_status()
#   File "/usr/lib/python3.10/http/client.py", line 287, in _read_status
#     raise RemoteDisconnected("Remote end closed connection without"
# urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "/mnt/c/Users/Martí/OneDrive - Universitat Politècnica de Catalunya/Documents/ProjectesDebian/AP2/RutesMon/Rutes-i-Monuments/monuments.py", line 82, in <module>
#     __download_monuments()
#   File "/mnt/c/Users/Martí/OneDrive - Universitat Politècnica de Catalunya/Documents/ProjectesDebian/AP2/RutesMon/Rutes-i-Monuments/monuments.py", line 56, in __download_monuments
#     monument_resp = requests.get(link.get("href"))
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/api.py", line 73, in get
#     return request("get", url, params=params, **kwargs)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/api.py", line 59, in request
#     return session.request(method=method, url=url, **kwargs)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/sessions.py", line 589, in request
#     resp = self.send(prep, **send_kwargs)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/sessions.py", line 703, in send
#     r = adapter.send(request, **kwargs)
#   File "/home/simpleman/.local/lib/python3.10/site-packages/requests/adapters.py", line 501, in send
#     raise ConnectionError(err, request=request)
# requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))


def __load_monuments(filename: str) -> None:
    """"""
    # TODO: Com guardarem els monuments?
    ...

if __name__ == "__main__":
    __download_and_print_links()