import os
import httpx
import feedparser
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


# Fetches raw research content from all 5 sources; scope controls result depth
def fetch_all_sources(query: str, scope: str = "Comprehensive") -> dict:
    # Focused = fewer results, Comprehensive = default, Exploratory = broader search
    max_results = {"Focused": 2, "Comprehensive": 3, "Exploratory": 5}.get(scope, 3)
    search_depth = "advanced" if scope == "Exploratory" else "basic"

    results = {
        "arxiv": [],
        "hackernews": [],
        "wikipedia": {},
        "tavily": [],
        "devto": [],
    }

    results["arxiv"] = _fetch_arxiv(query, max_results)
    results["hackernews"] = _fetch_hackernews(query, max_results)
    results["wikipedia"] = _fetch_wikipedia(query)
    results["tavily"] = _fetch_tavily(query, max_results, search_depth)
    results["devto"] = _fetch_devto(query, max_results)

    return results


# Fetches recent papers from ArXiv and parses XML with feedparser
def _fetch_arxiv(query: str, max_results: int = 3) -> list:
    try:
        url = f"https://export.arxiv.org/api/query?search_query={query}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
        feed = feedparser.parse(response.text)
        papers = []
        for entry in feed.entries:
            papers.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "url": entry.get("link", ""),
            })
        return papers
    except Exception as e:
        print(f"ArXiv fetch failed: {e}")
        return []


# Fetches top HackerNews stories filtered by query keywords
def _fetch_hackernews(query: str, max_results: int = 3) -> list:
    try:
        with httpx.Client(timeout=10) as client:
            top_ids_resp = client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            top_ids = top_ids_resp.json()[:30]

            keywords = query.lower().split()
            stories = []
            for story_id in top_ids:
                item_resp = client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                item = item_resp.json()
                if item and item.get("title"):
                    title_lower = item["title"].lower()
                    if any(kw in title_lower for kw in keywords):
                        stories.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "text": item.get("text", ""),
                        })
                if len(stories) >= max_results:
                    break
        return stories
    except Exception as e:
        print(f"HackerNews fetch failed: {e}")
        return []


# Fetches Wikipedia page summary, returns empty dict on 404
def _fetch_wikipedia(query: str) -> dict:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
        if response.status_code == 404:
            return {}
        data = response.json()
        return {
            "title": data.get("title", ""),
            "extract": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception as e:
        print(f"Wikipedia fetch failed: {e}")
        return {}


# Searches Tavily for recent web content about the query
def _fetch_tavily(query: str, max_results: int = 3, search_depth: str = "basic") -> list:
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("TAVILY_API_KEY not set, skipping Tavily")
            return []
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query, max_results=max_results, search_depth=search_depth)
        articles = []
        for r in results.get("results", []):
            articles.append({
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", ""),
            })
        return articles
    except Exception as e:
        print(f"Tavily fetch failed: {e}")
        return []


# Fetches DEV.to articles tagged with the query topic
def _fetch_devto(query: str, max_results: int = 3) -> list:
    try:
        tag = query.replace(" ", "-").lower()
        url = f"https://dev.to/api/articles?tag={tag}&per_page={max_results}&top=7"
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
        articles = []
        for item in response.json():
            articles.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("url", ""),
            })
        return articles
    except Exception as e:
        print(f"DEV.to fetch failed: {e}")
        return []
