from lxml import html
import requests


def scraper(url):
    # Send an HTTP request to the website and retrieve the HTML content
    response = requests.get(url)

    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)

    div = tree.xpath("//div[@id='mw-content-text']")[0]
    excluded_links = ["#cite_note", "Ayuda:", "/w/index", "Archivo:"]
    # Extract the links from the body
    links = []
    ptags = div.xpath(".//p")
    for ptag in ptags:
        links_ptag = ptag.xpath(".//a[not(@role='button')]/@href")
        for link in links_ptag:
            if not any(excluded in link for excluded in excluded_links):
                links.append(link)

    return links


# Define the URL of the website to scrape
# Define wikipedia as context
context_part = 'https://es.wikipedia.org'
new_url = '/wiki/Pok%C3%A9mon'
print(new_url)
i = 0
visited_links = []
while new_url != "/wiki/Filosof%C3%ADa":
    visited_links.append(new_url)
    i += 1
    repeated = 0
    print(f"{i} pasada")
    new_links = scraper(context_part+new_url)
    while new_links[repeated] in visited_links:
        repeated += 1
    new_url = new_links[repeated]
    print(new_url)
