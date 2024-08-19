from datetime import datetime
import requests
import urllib.parse

CONTEXT_LIST = ["https://es.wikipedia.org", "https://en.wikipedia.org"]


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


def valid_context(links: list[str]) -> str:
    if links[0][:24] != links[1][:24]:
        return "Contextos distintos!"
    invalid_links = ""
    for link in links:
        if link[:24] not in CONTEXT_LIST:
            invalid_links += link
    return None if invalid_links == "" else f"Contexto no válido: {invalid_links}"


def sanitize_links(links: list[str]) -> (str, str):
    sanitized_links = []
    for link in links:
        decoded = urllib.parse.unquote(link)
        if decoded != link:
            sanitized_links.append(link)
        else:
            sanitized_links.append(urllib.parse.quote(link, safe=":/"))
    return tuple(sanitized_links)


def validate_links(links: list[str], session: requests.Session) -> (str, str):
    not_valid_context = valid_context(links)
    if not_valid_context:
        return "error", not_valid_context
    first, last = sanitize_links(links)
    if get_url(session, first) and get_url(session, last):
        return first, last
    return "error", "No se puede llegar a los links!"
