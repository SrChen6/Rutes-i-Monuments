import json
import requests
import bs4


CM_LINK = "https://www.catalunyamedieval.es/comarques/"

def __get_json():
    """"""
    print(f"Downloading from {CM_LINK}...")
    response = None
    while response is None:
        try: response = requests.get(CM_LINK)
        except: pass

    print("Finding JSON file...")
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script')
    print(json.loads(scripts[2].text))

if __name__ == "__main__":
    __get_json()