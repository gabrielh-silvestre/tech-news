import requests

from typing import List, Union
from time import sleep
from parsel import Selector


# Requisito 1
def fetch(url: str) -> Union[str, None]:
    try:
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"}
        )

        if response.status_code == 200:
            return response.text

        return None
    except Exception as e:
        print(e)
        return None
    finally:
        sleep(1)


# Requisito 2
def scrape_novidades(html_content: str) -> List[str]:
    parsed_content = Selector(text=html_content)
    links = parsed_content.css("a.cs-overlay-link::attr(href)").getall()

    if len(links) > 0:
        return links

    return []


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
