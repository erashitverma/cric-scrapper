import requests
from bs4 import BeautifulSoup


def get_page_data_from_url(page_url):
    """
    :return soup of the page retrieved

    :param page_url url of the page to be retrieved
    """
    try:
        page = requests.get(page_url)
        if page.status_code == 200:
            html_content = page.text
            return BeautifulSoup(html_content, "lxml")
    except requests.exceptions.RequestException as e:
        print("Get request failed for " + e.request)
