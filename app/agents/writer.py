import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

AUDIENCE_INSTRUCTIONS = {
    "Academic Researchers": "Use precise technical language, include methodology references, and cite sources formally.",
    "General Public": "Use plain language, avoid jargon, and explain concepts simply as if writing for a curious non-expert.",
    "Industry Professionals": "Focus on practical applications, business impact, and actionable takeaways.",
    "Students": "Use clear explanations, define key terms, and highlight foundational concepts first.",
}

RESEARCH_TYPE_STRUCTURES = {
    "Comprehensive": """
## Research Brief: {query}
### Overview
### Key Findings
### Points of Agreement
### Contradictions & Debates
### Gaps in Current Knowledge
### Recommended Next Steps""",
    "Literature Review": """
## Literature Review: {query}
### Abstract
### Background
### Key Papers & Sources
### Thematic Analysis
### Consensus & Debates
### Research Gaps
### Conclusion""",
    "Technical Deep-Dive": """
## Technical Deep-Dive: {query}
### Executive Summary
### Technical Background
### Core Mechanisms & Implementation
### Performance & Benchmarks
### Known Limitations
### Cutting-Edge Developments
### Resources for Further Study""",
    "Trend Analysis": """
## Trend Analysis: {query}
### Current State of the Field
### Emerging Trends
### Key Drivers
### Diverging Perspectives
### What to Watch Next
### Strategic Implications""",
}


# Generates the final markdown research brief shaped by audience, type, and length
def write_brief(
    query: str,
    summaries: list,
    analysis: dict,
    audience: str = "Academic Researchers",
    research_type: str = "Comprehensive",
    page_length: int = 1000,
) -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    audience_note = AUDIENCE_INSTRUCTIONS.get(audience, AUDIENCE_INSTRUCTIONS["Academic Researchers"])
    structure = RESEARCH_TYPE_STRUCTURES.get(research_type, RESEARCH_TYPE_STRUCTURES["Comprehensive"])
    structure = structure.replace("{query}", query)

    system = f"""You are a research writer producing a {research_type.lower()} for {audience}.
{audience_note}

Use exactly this structure:
{structure}

Target approximately {page_length} words. Keep it factual, concise, and useful. No padding."""

    summaries_text = "\n\n".join(
        f"**{s['source_label']}**: {s['summary']}" for s in summaries
    )

    analysis_text = (
        f"Agreements: {analysis.get('agreements', [])}\n"
        f"Contradictions: {analysis.get('contradictions', [])}\n"
        f"Gaps: {analysis.get('gaps', [])}"
    )

    human_content = (
        f"Query: {query}\n\n"
        f"Source Summaries:\n{summaries_text}\n\n"
        f"Critical Analysis:\n{analysis_text}"
    )

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=human_content[:6000]),
    ]

    response = llm.invoke(messages)
    return response.content
