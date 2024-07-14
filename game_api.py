from lxml import html
import multiprocessing
from multiprocessing import Manager
import requests
from datetime import datetime


def get_url(session: requests.Session, url: str):
    # Try to send an HTTP request
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        r8_now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"An error occurred: {e}")
        print(f"{r8_now} - URL: {url}")
        return False


def get_links_in_page(response: requests.Response):
    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)
    div = tree.xpath("//div[@id='mw-content-text']")[0]
    # Extract <p>
    links_to_search = div.xpath(
        ".//p//a[not(@role='button') and not(starts-with(@href, '/wiki/Ayuda:'))"
        + "and not(starts-with(@href, '/w/index')) and not(starts-with(@href, '/wiki/Archivo:'))]/@href"
    )
    return links_to_search


def scraper(
    url: str,
    link_dict: dict,
    searched_link: str,
    result: multiprocessing.Queue,
    session: requests.Session,
    keys_links,
):
    response = get_url(session, url)
    if response:
        p_tags = get_links_in_page(response)
        for link in p_tags:
            if "#cite_note" not in link:
                if link_dict.get(link, 0) == 0:
                    # We could discuss the use of slicing,
                    # as the context will always be the same
                    # It would be a win/lose between memory and time complexity
                    # link_dict[link] = url[24:] # With slicing
                    # For the time being, I want it to be faster
                    link_dict[link] = url
                    keys_links.append(link)
                if link == searched_link:
                    result.put(searched_link)
                    return True
    return False


def start_searching(
    session: requests.Session, context: str, actual_url: str, searched_link: str
):
    i = 0
    manager = Manager()
    bea_links = manager.dict()
    bea_links[actual_url] = ""
    num_processes = multiprocessing.cpu_count()
    found = multiprocessing.Queue()
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
                        context + actual_url,
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
        previous_link = link_dict.get(previous_link, 0)[24:]
        path.insert(0, previous_link)
    return path


def main():
    page_context = "https://es.wikipedia.org"
    end_link = "/wiki/Aceite_de_ballena"
    first_link = "/wiki/Pok%C3%A9mon"
    session = requests.Session()
    check_invalid_first = get_url(session, page_context + first_link)
    check_invalid_second = get_url(session, page_context + end_link)
    if check_invalid_first and check_invalid_second:
        print(datetime.now().strftime("%H:%M:%S.%f")[:-3])
        links_dict = start_searching(session, page_context, first_link, end_link)
        path = reconstruct_path(end_link, links_dict)
        print(path)
        print(f"Links found: {len(links_dict)}")
        print(datetime.now().strftime("%H:%M:%S.%f")[:-3])
    else:
        if not check_invalid_first and not check_invalid_second:
            not_valid_link = f"{first_link} and {end_link}"
        else:
            not_valid_link = first_link if not check_invalid_first else end_link
        print(f"{not_valid_link} not valid!")


if __name__ == "__main__":
    main()
