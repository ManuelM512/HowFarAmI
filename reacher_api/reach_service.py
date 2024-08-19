from datetime import datetime
from links_path import beautify_path, reconstruct_path
from search import start_searching
import requests
from url_utils import validate_links


def reach(first_link: str, end_link: str):
    session = requests.Session()
    first, last = validate_links([first_link, end_link], session)
    if first != "error":
        page_context = first[:24]
        start_time = datetime.now()
        links_dict, pre_last_link = start_searching(
            session,
            page_context,
            first[24:],
            last[24:],
        )
        path = reconstruct_path(pre_last_link, last[24:], links_dict)
        path_beautified = beautify_path(path)
        end_time = datetime.now()
        return {
            "links": len(links_dict),
            "path": path_beautified,
            "time": str(end_time - start_time)[:-3],
        }
    return {"error": last}
