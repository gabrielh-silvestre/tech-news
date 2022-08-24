from typing import Any, Dict, List, Tuple

from tech_news.database import find_news


# Requisito 10
def top_5_news() -> List[Tuple[str, int]]:
    found_news: Dict[str, Any] = find_news()

    # sorted with lambda ref
    # https://docs.python.org/3/howto/sorting.html#key-functions
    sorted_news = sorted(
        found_news, key=lambda news: news["comments_count"], reverse=True
    )

    return [(news["title"], news["url"]) for news in sorted_news[:5]]


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
