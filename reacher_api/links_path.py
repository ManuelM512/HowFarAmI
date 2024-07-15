def reconstruct_path(last_link: str, searched_link: str, link_dict: dict):
    previous_link = last_link
    path = [previous_link, searched_link]
    while previous_link != "":
        previous_link = link_dict.get(previous_link, 0)[24:]
        path.insert(0, previous_link)
    return path


def beautify_path(path: list):
    beautified = path[1]
    for link in path[2:]:
        beautified += f" -> {link}"
    return beautified
