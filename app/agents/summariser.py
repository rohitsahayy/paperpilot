import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are a research assistant. Summarise the following content in exactly 3 sentences. "
    "Be factual. Include the key claim or finding. No fluff."
)


# Summarises each non-empty source using Groq LLM, returns list of summary dicts
def summarise_sources(raw_content: dict) -> list:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    source_configs = [
        {
            "key": "arxiv",
            "label": "ArXiv Papers",
            "extractor": _extract_arxiv,
        },
        {
            "key": "hackernews",
            "label": "HackerNews",
            "extractor": _extract_hackernews,
        },
        {
            "key": "wikipedia",
            "label": "Wikipedia",
            "extractor": _extract_wikipedia,
        },
        {
            "key": "tavily",
            "label": "Tavily Web Search",
            "extractor": _extract_tavily,
        },
        {
            "key": "devto",
            "label": "DEV.to Articles",
            "extractor": _extract_devto,
        },
    ]

    summaries = []
    for config in source_configs:
        data = raw_content.get(config["key"])
        text, urls = config["extractor"](data)
        if not text.strip():
            continue
        summary = _call_llm(llm, text)
        summaries.append({
            "source": config["key"],
            "source_label": config["label"],
            "summary": summary,
            "urls": urls,
        })

    return summaries


# Calls Groq LLM with the content and returns a 3-sentence summary
def _call_llm(llm: ChatGroq, content: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=content[:4000]),
    ]
    response = llm.invoke(messages)
    return response.content


def _extract_arxiv(data: list) -> tuple:
    if not data:
        return "", []
    texts = [f"Title: {p['title']}\nSummary: {p['summary']}" for p in data]
    urls = [p["url"] for p in data if p.get("url")]
    return "\n\n".join(texts), urls


def _extract_hackernews(data: list) -> tuple:
    if not data:
        return "", []
    texts = [f"Title: {p['title']}\nText: {p.get('text', '')}" for p in data]
    urls = [p["url"] for p in data if p.get("url")]
    return "\n\n".join(texts), urls


def _extract_wikipedia(data: dict) -> tuple:
    if not data or not data.get("extract"):
        return "", []
    text = f"Title: {data.get('title', '')}\nExtract: {data['extract']}"
    urls = [data["url"]] if data.get("url") else []
    return text, urls


def _extract_tavily(data: list) -> tuple:
    if not data:
        return "", []
    texts = [f"Title: {p['title']}\nContent: {p['content']}" for p in data]
    urls = [p["url"] for p in data if p.get("url")]
    return "\n\n".join(texts), urls


def _extract_devto(data: list) -> tuple:
    if not data:
        return "", []
    texts = [f"Title: {p['title']}\nDescription: {p.get('description', '')}" for p in data]
    urls = [p["url"] for p in data if p.get("url")]
    return "\n\n".join(texts), urls
