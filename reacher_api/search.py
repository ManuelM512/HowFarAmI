from multiprocessing import cpu_count, Manager, Process, Queue
import requests
from scrape_utils import scraper


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
    num_processes = cpu_count()
    found = Queue()
    i = 0
    while found.empty():
        processes = []
        for _ in range(num_processes):
            if i < len(keys_links):
                actual_url = keys_links[i]
                i += 1
                p = Process(
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
    return bea_links, found.get()
