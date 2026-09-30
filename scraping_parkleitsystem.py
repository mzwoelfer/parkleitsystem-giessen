import requests
import json

from scraping_parkleitsystem_logic import (
    extract_parkhouse_data,
    extract_parkhouse_data_from_html_tag,
    get_last_updated_time,
    get_text_from_html_tag,
    scrape_webpage,
)


def download_parkhouse_html(parkhouse_webpage_url):
    response = requests.get(parkhouse_webpage_url)
    return response.text


def main():
    url = "https://www.giessen.de/Umwelt_und_Verkehr/Parken/"

    html = download_parkhouse_html(url)
    scraped_parkleitsystem = scrape_webpage(html)
    print(json.dumps(scraped_parkleitsystem, indent=2))

if __name__ == "__main__":
    main()