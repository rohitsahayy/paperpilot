import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a critical research analyst. You will be given summaries from multiple sources about the same topic.
Identify:
1. Key points that multiple sources AGREE on
2. Points where sources CONTRADICT or DISAGREE with each other
3. Important gaps — things not covered by any source

Be specific. Reference which sources agree or disagree.
Respond in this exact JSON format:
{
  "agreements": ["point 1", "point 2"],
  "contradictions": ["contradiction 1", "contradiction 2"],
  "gaps": ["gap 1", "gap 2"]
}"""


# Analyses cross-source agreements, contradictions, and gaps using Groq LLM
def analyse_sources(summaries: list) -> dict:
    if not summaries:
        return {"agreements": [], "contradictions": [], "gaps": []}

    combined = "\n\n".join(
        f"[{s['source_label']}]: {s['summary']}" for s in summaries
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=combined[:6000]),
    ]

    try:
        response = llm.invoke(messages)
        raw = response.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        analysis = json.loads(raw)
        return {
            "agreements": analysis.get("agreements", []),
            "contradictions": analysis.get("contradictions", []),
            "gaps": analysis.get("gaps", []),
        }
    except Exception as e:
        print(f"Critic analysis failed: {e}")
        return {"agreements": [], "contradictions": [], "gaps": []}
