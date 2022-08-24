from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

from tech_news.database import find_news


def search_builder(condition: Callable) -> List[Tuple[str, str]]:
    # lambda ref
    # https://www.w3schools.com/python/python_lambda.asp

    found_news: Dict[str, Any] = find_news()

    return [
        (news["title"], news["url"]) for news in found_news if condition(news)
    ]


# Requisito 6
def search_by_title(title: str) -> List[Tuple[str, str]]:
    return search_builder(lambda news: title.lower() in news["title"].lower())


# Requisito 7
def search_by_date(date: str) -> List[Tuple[str, str]]:
    formatted_date = None

    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    return search_builder(
        lambda news: formatted_date
        == datetime.strptime(news["timestamp"], "%d/%m/%Y")
    )


# Requisito 8
def search_by_tag(tag: str) -> List[Tuple[str, str]]:
    return search_builder(
        lambda news: tag.lower() in [t.lower() for t in news["tags"]]
    )


# Requisito 9
def search_by_category(category: str) -> List[Tuple[str, str]]:
    return search_builder(
        lambda news: category.lower() == news["category"].lower()
    )
