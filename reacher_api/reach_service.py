from datetime import datetime
from links_path import beautify_path, reconstruct_path
from search import start_searching
import requests
from url_utils import get_url


def reach(first_link: str, end_link: str):
    page_context = "https://es.wikipedia.org"
    session = requests.Session()
    check_invalid_first = get_url(session, page_context + first_link)
    check_invalid_second = get_url(session, page_context + end_link)
    if check_invalid_first and check_invalid_second:
        start_time = datetime.now()
        links_dict, last_link = start_searching(
            session, page_context, first_link, end_link
        )
        path = reconstruct_path(last_link, end_link, links_dict)
        path_beautified = beautify_path(path)
        end_time = datetime.now()
        return {
            "links": len(links_dict),
            "path": path_beautified,
            "time": str(end_time - start_time)[:-3],
        }
    if not check_invalid_first and not check_invalid_second:
        not_valid_link = f"{first_link} and {end_link}"
    else:
        not_valid_link = first_link if not check_invalid_first else end_link
    return {"error": f"{not_valid_link} no es/son válido/s!"}
