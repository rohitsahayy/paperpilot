from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.agents.fetcher import fetch_all_sources
from app.agents.summariser import summarise_sources
from app.agents.critic import analyse_sources
from app.agents.writer import write_brief


class ResearchState(TypedDict):
    query: str
    scope: str
    audience: str
    research_type: str
    page_length: int
    raw_content: dict
    summaries: list
    analysis: dict
    brief: str
    sources: list


# Node: fetches raw content from all 5 sources
def fetch_node(state: ResearchState) -> ResearchState:
    raw = fetch_all_sources(state["query"], state["scope"])
    return {**state, "raw_content": raw}


# Node: summarises each source using Groq LLM
def summarise_node(state: ResearchState) -> ResearchState:
    summaries = summarise_sources(state["raw_content"])
    return {**state, "summaries": summaries, "sources": summaries}


# Node: analyses agreements, contradictions, and gaps across summaries
def critic_node(state: ResearchState) -> ResearchState:
    analysis = analyse_sources(state["summaries"])
    return {**state, "analysis": analysis}


# Node: writes the final research brief in markdown
def write_node(state: ResearchState) -> ResearchState:
    brief = write_brief(
        query=state["query"],
        summaries=state["summaries"],
        analysis=state["analysis"],
        audience=state["audience"],
        research_type=state["research_type"],
        page_length=state["page_length"],
    )
    return {**state, "brief": brief}


# Build and compile the LangGraph pipeline
_builder = StateGraph(ResearchState)
_builder.add_node("fetch", fetch_node)
_builder.add_node("summarise", summarise_node)
_builder.add_node("critic", critic_node)
_builder.add_node("write", write_node)

_builder.set_entry_point("fetch")
_builder.add_edge("fetch", "summarise")
_builder.add_edge("summarise", "critic")
_builder.add_edge("critic", "write")
_builder.add_edge("write", END)

graph = _builder.compile()


# Runs the full research pipeline and returns brief and sources
def run_research_pipeline(
    query: str,
    scope: str = "Comprehensive",
    audience: str = "Academic Researchers",
    research_type: str = "Comprehensive",
    page_length: int = 1000,
) -> dict:
    result = graph.invoke({
        "query": query,
        "scope": scope,
        "audience": audience,
        "research_type": research_type,
        "page_length": page_length,
        "raw_content": {},
        "summaries": [],
        "analysis": {},
        "brief": "",
        "sources": [],
    })
    return {
        "brief": result["brief"],
        "sources": result["summaries"],
    }
