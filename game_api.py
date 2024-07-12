from lxml import html
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime


class DictWithIndex:
    def __init__(self):
        self.__dicc = {}

    # Only sets the pair if the key isn't in the dict
    def set_item(self, key, value):
        if self.__dicc.get(key, 0) == 0:
            self.__dicc[key] = value

    def get_item(self, key, default=0):
        return self.__dicc.get(key, default)

    def get_key_by_index(self, index):
        if index < len(self.__dicc):
            return list(self.__dicc.keys())[index]
        return 0

    def pop_item(self, key):
        if self.__dicc.get(key, 0) != 0:
            self.__dicc.pop(key)

    def __len__(self):
        return len(self.__dicc)


def scraper(url: str, dict_with_index: DictWithIndex, searched_link: str):
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    # Try to send an HTTP request
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(f"URL {url}")
        # Is this necessary? to review...
        dict_with_index.pop_item(url[24:])
        return False
    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)
    div = tree.xpath("//div[@id='mw-content-text']")[0]
    excluded_links = ["#cite_note", "Ayuda:", "/w/index", "Archivo:"]
    # Extract <p>
    ptags = div.xpath(".//p")
    for ptag in ptags:
        # Extract links that aren't buttons
        links_ptag = ptag.xpath(".//a[not(@role='button')]/@href")
        for link in links_ptag:
            if not any(excluded in link for excluded in excluded_links):
                dict_with_index.set_item(link, url[24:])
                if link == searched_link:
                    return True
    return False


def start_searching(actual_url: str, searched_link: str):
    # Define the URL of the website to scrape
    # Define wikipedia as context
    context_part = "https://es.wikipedia.org"
    i = 0
    bea_links = DictWithIndex()
    bea_links.set_item(actual_url, "")
    while actual_url != searched_link:
        actual_url = bea_links.get_key_by_index(i)
        i += 1
        if scraper(context_part + actual_url, bea_links, searched_link):
            break
    return bea_links


def reconstruct_path(searched_link: str, dict_with_index: DictWithIndex):
    previous_link = searched_link
    path = [previous_link]
    while previous_link != "":
        previous_link = dict_with_index.get_item(previous_link)
        path.insert(0, previous_link)
    return path


def main():
    # Get the current time
    current_time = datetime.now()
    print(f"Inicio: {current_time.strftime('%H:%M:%S.%f')[:-3]}")
    end_link = "/wiki/Jugador_de_videojuegos"
    first_link = "/wiki/Pok%C3%A9mon"
    links_dict_with_index = start_searching(first_link, end_link)
    path = reconstruct_path(end_link, links_dict_with_index)
    print(path)
    print(f"Links encontrados: {len(links_dict_with_index)}")
    current_time = datetime.now()
    print(f"Fin: {current_time.strftime('%H:%M:%S.%f')[:-3]}")


main()
