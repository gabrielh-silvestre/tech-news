import requests

from typing import List, Union
from time import sleep
from parsel import Selector


def select_links(
    html_content: str, class_name: str, **kwargs: Union[None, bool]
) -> Union[List[str], str, None]:
    parsed_content = Selector(text=html_content)

    if kwargs["is_list"]:
        links = parsed_content.css(f"a.{class_name}::attr(href)").getall()
        return links if len(links) > 0 else []

    link = parsed_content.css(f"a.{class_name}::attr(href)").get()
    return link if link else None


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
    return select_links(html_content, "cs-overlay-link", is_list=True)


# Requisito 3
def scrape_next_page_link(html_content: str) -> Union[str, None]:
    return select_links(html_content, "next", is_list=False)


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
