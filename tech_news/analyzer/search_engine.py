from typing import Any, Dict, List, Tuple

from tech_news.database import find_news


# Requisito 6
def search_by_title(title: str) -> List[Tuple[str, str]]:
    news: Dict[str, Any] = find_news()

    return [
        (news["title"], news["url"])
        for news in news
        if title.lower() in news["title"].lower()
    ]


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
