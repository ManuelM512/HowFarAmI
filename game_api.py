from lxml import html
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class DiccWithIndex:
    def __init__(self):
        self.__dicc = {}
        self.__keys = []

    def set_item(self, key, value):
        if self.__dicc.get(key, 0) == 0:
            self.__dicc[key] = value
            self.__keys.append(key)

    def get_item(self, key, default=0):
        return self.__dicc.get(key, default)

    def get_key_by_index(self, index):
        if len(self.__keys) > index:
            return self.__keys[index]
        return 0

    def remove_item(self, key):
        if key in self.__keys:
            self.__dicc.__delitem__(key)
            self.__keys.remove(key)


def scraper(url, dicc_with_index, searched_link):
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Send an HTTP request to the website and retrieve the HTML content

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    # response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(f"URL {url}")
        dicc_with_index.remove_item(url)
        return False
    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)

    div = tree.xpath("//div[@id='mw-content-text']")[0]
    excluded_links = ["#cite_note", "Ayuda:", "/w/index", "Archivo:"]
    # Extract the links from the body
    ptags = div.xpath(".//p")
    for ptag in ptags:
        links_ptag = ptag.xpath(".//a[not(@role='button')]/@href")
        for link in links_ptag:
            if not any(excluded in link for excluded in excluded_links):
                dicc_with_index.set_item(link, url[24:])
                if link == searched_link:
                    return True

    return False


# Define the URL of the website to scrape
# Define wikipedia as context
context_part = "https://es.wikipedia.org"
actual_url = "/wiki/Pok%C3%A9mon"
i = 0
bea_links = DiccWithIndex()
bea_links.set_item(actual_url, "")
searched_link = "/wiki/Apple_IIGS"
n = 1
while actual_url != searched_link:
    actual_url = bea_links.get_key_by_index(i)
    i += 1
    if scraper(context_part + actual_url, bea_links, searched_link):
        break

previous_link = searched_link
path = [previous_link]
while previous_link != "":
    previous_link = bea_links.get_item(previous_link)
    path.insert(0, previous_link)


print(path)
