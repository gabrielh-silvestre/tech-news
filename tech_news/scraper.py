import requests

from typing import Dict, List, Union
from time import sleep
from parsel import Selector
from datetime import datetime

from tech_news.database import create_news


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
def scrape_noticia(html_content: str):
    MAPPED_FIELDS = {
        "url": "link[rel=canonical]",
        "title": "h1.entry-title",
        "timestamp_original": "li.meta-date",
        "timestamp_modified": "p.post-modified-info",
        "writer": "a.fn",
        "comments_count": "ol.comment-list > li",
        "summary": "div.entry-content > p:nth-of-type(1)",
        "tags": "section.post-tags > ul > li > a",
        "category": "a.category-style > span.label",
    }

    parsed_content = Selector(text=html_content)

    url = parsed_content.css(f"{MAPPED_FIELDS['url']}::attr(href)").get()
    title = parsed_content.css(f"{MAPPED_FIELDS['title']}::text").get()
    writer = parsed_content.css(f"{MAPPED_FIELDS['writer']}::text").get()
    tags = parsed_content.css(f"{MAPPED_FIELDS['tags']}::text").getall()
    category = parsed_content.css(f"{MAPPED_FIELDS['category']}::text").get()
    comments_count = parsed_content.css(
        MAPPED_FIELDS["comments_count"]
    ).getall()
    summary = parsed_content.css(
        f"{MAPPED_FIELDS['summary']} *::text"
    ).getall()
    timestamp = parsed_content.css(
        f"{MAPPED_FIELDS['timestamp_original']}::text"
    ).get()

    if not timestamp:
        timestamp = parsed_content.css(
            f"{MAPPED_FIELDS['timestamp_modified']}::text"
        ).get()

    formatted_timestamp = datetime.strptime(timestamp, "%d/%m/%Y")
    formatted_timestamp = formatted_timestamp.strftime("%d/%m/%Y")

    return {
        "url": url,
        "title": title.strip(),
        "timestamp": formatted_timestamp,
        "writer": writer,
        "comments_count": len(comments_count),
        "summary": "".join(summary).strip(),
        "tags": tags,
        "category": category,
    }


def get_page_content(page_url: str, amount: int) -> Dict:
    page = fetch(page_url)
    news_links = scrape_novidades(page)
    next_page = scrape_next_page_link(page)

    news_limit = min(amount, len(news_links))
    news = []

    for news_number in range(news_limit):
        page_news = fetch(news_links[news_number])
        news.append(scrape_noticia(page_news))

    return {"news": news, "next_page": next_page}


# Requisito 5
def get_tech_news(amount: int) -> List[Dict]:
    URL = "https://blog.betrybe.com"

    news = []

    while len(news) < amount:
        content = get_page_content(URL, amount - len(news))
        news.extend(content["news"])
        URL = content["next_page"]

    create_news(news)
    return news
