from datetime import datetime
from lxml import html
import multiprocessing
from multiprocessing import Manager
import requests


def get_url(session: requests.Session, url: str):
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
    tree = html.fromstring(response.content)
    div = tree.xpath("//div[@id='mw-content-text']")[0]
    # Extract links from <p> that aren't buttons and not an unwanted link
    links_to_search = div.xpath(
        ".//p//a[not(@role='button') and not(starts-with(@href, '/wiki/Ayuda:'))"
        + " and not(starts-with(@href, '/w/index')) and not(starts-with(@href, '/wiki/Archivo:'))]/@href"
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
                    # For the time being, I want it to be faster rather to save memory
                    link_dict[link] = url
                    keys_links.append(link)
                if link == searched_link:
                    result.put(searched_link)
                    return True
    return False


def get_structures(first_link: str):
    manager = Manager()
    man_dict = manager.dict()
    man_dict[first_link] = ""
    man_list = manager.list()
    man_list.append(first_link)
    return man_list, man_dict


def start_searching(
    session: requests.Session, context: str, actual_url: str, searched_link: str
):
    keys_links, bea_links = get_structures(actual_url)
    num_processes = multiprocessing.cpu_count()
    found = multiprocessing.Queue()
    i = 0
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


def beautify_path(path: list):
    beautified = path[1]
    for link in path[2:]:
        beautified += f" -> {link}"
    return beautified


def reach(first_link: str, end_link: str):
    page_context = "https://es.wikipedia.org"
    session = requests.Session()
    check_invalid_first = get_url(session, page_context + first_link)
    check_invalid_second = get_url(session, page_context + end_link)
    if check_invalid_first and check_invalid_second:
        start_time = datetime.now()
        links_dict = start_searching(session, page_context, first_link, end_link)
        path = reconstruct_path(end_link, links_dict)
        path_beautified = beautify_path(path)
        end_time = datetime.now()
        return (
            # It ended like this in order to get a quick front
            f"<b>Links found:</b> {len(links_dict)}"
            + f"<br><b>Shortest path:</b> {path_beautified}"
            + f"<br><b>Time needed:</b> {str(end_time-start_time)[:-3]}"
        )
    if not check_invalid_first and not check_invalid_second:
        not_valid_link = f"{first_link} and {end_link}"
    else:
        not_valid_link = first_link if not check_invalid_first else end_link
    return f"{not_valid_link} no es/son válido/s!"
