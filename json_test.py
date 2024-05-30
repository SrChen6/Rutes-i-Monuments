import json
import requests
import bs4

from typing import Any


# Website link from which to download monument information (Catalunya Medieval).
CM_LINK = "https://www.catalunyamedieval.es/comarques/"

# In the HTML file, the script that needs to be downloaded is the eighth found by
# Beautiful Soup's lineal search. If the web is updated and problems arise,
# we should check if the script has been moved or removed.
SCRIPT_NUM = 7


def __get_json() -> Any:
    """Retrieves the JSON containing monument information
    from Catalunya Medieval."""
    print(f"Downloading monument data from {CM_LINK}...")

    response = None
    while response is None:
        try: response = requests.get(CM_LINK)
        except: pass
    
    monuments = 
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script', type = "text/javascript")
    for line in scripts[SCRIPT_NUM].get_text().splitlines():
        line = line.strip()
        if line and line[0] == "v":
            json_data = line[len(line.split("=")[0])+1:-1]
            parsed_data = json.loads(json_data)
            for item in parsed_data:
                pass
        
def __retrieve_monuments() -> None:
    """Retrieves monument data from """
    data = __get_json()
    
    print("Transforming data into .csv file...")
    print(data)


if __name__ == "__main__":
    __get_json()