import multiprocessing
from lxml import html
import requests
from url_utils import get_url


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
                    result.put(url[24:])
                    return True
    return False
