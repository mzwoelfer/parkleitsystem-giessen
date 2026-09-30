from bs4 import BeautifulSoup


def extract_parkhouse_data_from_html_tag(tag):
    soup = BeautifulSoup(tag, "html.parser")

    free_spaces = int(soup.find("span", {"class": "free"}).text.split(":")[1].strip())
    max_spaces = int(soup.find("span", {"class": "max"}).text.split(":")[1].strip())

    return {
        "name": soup.find("span", {"class": "slot-name"}).text,
        "free_spaces": free_spaces,
        "occupied_spaces": max_spaces - free_spaces,
        "max_spaces": max_spaces,
    }


def get_text_from_html_tag(html_string, search_object):
    soup = BeautifulSoup(html_string, "html.parser")
    html_text = soup.find(
        search_object["html_element"],
        {search_object["html_attribute"]: search_object["attribute_value"]},
    )
    if html_text is None:
        raise TypeError(
            f"No {search_object['html_element']} element with "
            f"{search_object['html_attribute']} '{search_object['attribute_value']}' found"
        )
    return str(html_text)


def extract_parkhouse_data(html):
    soup = BeautifulSoup(html, "html.parser")
    panels = soup.find_all("div", {"class": "info-panel"})
    return [extract_parkhouse_data_from_html_tag(str(panel)) for panel in panels]


def get_last_updated_time(html):
    soup = BeautifulSoup(html, "html.parser")
    update_text = soup.find("small", {"class": "last-update"}).text
    last_updated = update_text.split(":", 1)[1].strip()
    time = "".join(last_updated.split()[0].split(":"))
    date = "".join(last_updated.split()[-1].split("."))
    return f"{date}-{time}"


def scrape_webpage(html):
    return {
        "timestamp": get_last_updated_time(html),
        "parkhouses": extract_parkhouse_data(html),
    }