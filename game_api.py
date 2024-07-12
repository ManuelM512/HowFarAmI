from lxml import html
import multiprocessing
from multiprocessing import Manager
import requests
from datetime import datetime


def scraper(
    url: str,
    link_dict: dict,
    searched_link: str,
    result: multiprocessing.Queue,
    session: requests.Session,
    keys_links,
):
    # This could be a function
    # Try to send an HTTP request
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        r8_now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"An error occurred: {e}")
        print(f"{r8_now} - URL: {url}")
        return False
    # Another function to parse HTML
    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)
    div = tree.xpath("//div[@id='mw-content-text']")[0]
    excluded_links = ["#cite_note", "/wiki/Ayuda:", "/w/index", "/wiki/Archivo:"]
    # Extract <p>
    ptags = div.xpath(".//p")
    for ptag in ptags:
        # Extract links that aren't buttons
        links_ptag = ptag.xpath(".//a[not(@role='button')]/@href")
        for link in links_ptag:
            if not any(excluded in link for excluded in excluded_links):
                if link_dict.get(link, 0) == 0:
                    link_dict[link] = url[24:]
                    keys_links.append(link)
                if link == searched_link:
                    result.put(searched_link)
                    return True
    return False


def start_searching(actual_url: str, searched_link: str):
    # Define the URL of the website to scrape
    # Define wikipedia as context
    context_part = "https://es.wikipedia.org"
    i = 0
    manager = Manager()
    bea_links = manager.dict()
    bea_links[actual_url] = ""
    session = requests.Session()
    # Trying to multiprocess
    num_processes = multiprocessing.cpu_count()
    found = multiprocessing.Queue()
    print(datetime.now().strftime("%H:%M:%S.%f")[:-3])
    keys_links = manager.list()
    keys_links.append(actual_url)
    while actual_url != searched_link:
        processes = []
        for _ in range(num_processes):
            if i < len(keys_links):
                actual_url = keys_links[i]
                i += 1
                p = multiprocessing.Process(
                    target=scraper,
                    args=(
                        context_part + actual_url,
                        bea_links,
                        searched_link,
                        found,
                        session,
                        keys_links,
                    ),
                )
                processes.append(p)
                p.start()

        for p in processes:
            p.join()
        if not found.empty():
            break
    return bea_links


def reconstruct_path(searched_link: str, link_dict: dict):
    previous_link = searched_link
    path = [previous_link]
    while previous_link != "":
        previous_link = link_dict.get(previous_link, 0)
        path.insert(0, previous_link)
    return path


def main():
    end_link = "/wiki/Aceite_de_ballena"
    first_link = "/wiki/Pok%C3%A9mon"
    links_dict = start_searching(first_link, end_link)
    path = reconstruct_path(end_link, links_dict)
    print(path)
    print(f"Links encontrados: {len(links_dict)}")
    print(datetime.now().strftime("%H:%M:%S.%f")[:-3])


if __name__ == "__main__":
    main()
