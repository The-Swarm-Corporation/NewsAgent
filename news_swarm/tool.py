from newsapi import NewsApiClient
from typing import Optional, Dict, Union, List, Literal


def fetch_stock_news(
    query: str,
    newsapi_api_key: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_articles: int = 5,
    return_json: bool = False,
) -> Union[Dict[str, Union[str, List[Dict[str, str]]]], str]:
    """
    Fetches stock news for a query within a specified date range using NewsApiClient.

    Args:
        query (str): The query name or stock symbol to query news for.
        newsapi_api_key (str): Your API key for News API.
        start_date (Optional[str]): The start date for the news query in 'YYYY-MM-DD' format (default: None).
        end_date (Optional[str]): The end date for the news query in 'YYYY-MM-DD' format (default: None).
        max_articles (int): The maximum number of articles to retrieve (default: 5).
        return_json (bool): If True, return the result as a JSON object, otherwise return a formatted string (default: False).

    Returns:
        Union[Dict[str, Union[str, List[Dict[str, str]]]], str]:
        A JSON object (if return_json=True) containing articles and metadata, or a formatted string of the news articles.
    """

    # Initialize the NewsApiClient with the provided API key
    newsapi = NewsApiClient(api_key=newsapi_api_key)

    # Fetch news articles using NewsApiClient
    articles_data = newsapi.get_everything(
        q=query,
        from_param=start_date,
        to=end_date,
        language="en",
        sort_by="relevancy",
        page_size=max_articles,
    )

    if articles_data["status"] != "ok":
        raise ValueError("Failed to fetch news data from API")

    # Extract articles
    articles = articles_data.get("articles", [])

    if not articles:
        return "No articles found for the given query and date range."

    # Process each article and return metadata
    def process_article(article: Dict[str, str]) -> Dict[str, str]:
        """
        Process an article and return metadata.
        """
        return {
            "title": article.get("title", "No Title"),
            "description": article.get(
                "description", "No Description"
            ),
            "url": article.get("url", "No URL"),
            "published_at": article.get("publishedAt", "No Date"),
            "source": article.get("source", {}).get(
                "name", "Unknown Source"
            ),
        }

    # Process all articles
    processed_articles = [
        process_article(article) for article in articles
    ]

    # Create formatted string of articles and metadata
    formatted_result = f"News Articles for {query}:\n\n"
    for idx, article in enumerate(processed_articles, 1):
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        url = article.get("url", "No URL")
        published_at = article.get("published_at", "No Date")
        source = article.get("source", "Unknown Source")

        formatted_result += (
            f"\nArticle {idx}:\n"
            f"Title: {title}\n"
            f"Description: {description}\n"
            f"URL: {url}\n"
            f"Published At: {published_at}\n"
            f"Source: {source}\n"
            "\n"
        )

    # If return_json is true, return the raw JSON data with the formatted string
    data = {
        "query": query,
        "start_date": start_date,
        "end_date": end_date,
        "formatted_result": formatted_result,
        "articles": processed_articles,
    }

    return formatted_result, data


# # Example
# out = fetch_stock_news("Swarms")


def return_sources(
    source: Literal[
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    ],
    newsapi_api_key: str = None,
    *args,
    **kwargs,
):
    """
    Fetches stock news for a query within a specified date range using NewsApiClient.

    Args:
        query (str): The query name or stock symbol to query news for.
        newsapi_api_key (str): Your API key for News API.
        start_date (Optional[str]): The start date for the news query in 'YYYY-MM-DD' format (default: None).
        end_date (Optional[str]): The end date for the news query in 'YYYY-MM-DD' format (default: None).
        max_articles (int): The maximum number of articles to retrieve (default: 5).
        return_json (bool): If True, return the result as a JSON object, otherwise return a formatted string (default: False).

    Returns:
        Union[Dict[str, Union[str, List[Dict[str, str]]]], str]:
        A JSON object (if return_json=True) containing articles and metadata, or a formatted string of the news articles.
    """

    # Initialize the NewsApiClient with the provided API key
    newsapi = NewsApiClient(api_key=newsapi_api_key)

    data = newsapi.get_sources(category=source, *args, **kwargs)

    return data


def return_headlines(
    source: str = None, newsapi_api_key: str = None, *args, **kwargs
):
    """
    Fetches stock news for a query within a specified date range using NewsApiClient.

    Args:
        query (str): The query name or stock symbol to query news for.
        newsapi_api_key (str): Your API key for News API.
    """

    # Initialize the NewsApiClient with the provided API key
    newsapi = NewsApiClient(api_key=newsapi_api_key)

    data = newsapi.get_top_headlines(sources=source, *args, **kwargs)

    return data
