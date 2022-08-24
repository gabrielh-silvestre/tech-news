from datetime import datetime
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
def search_by_date(date: str) -> List[Tuple[str, str]]:
    news: Dict[str, Any] = find_news()
    formatted_date = None

    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    return [
        (news["title"], news["url"])
        for news in news
        if formatted_date == datetime.strptime(news["timestamp"], "%d/%m/%Y")
    ]


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
