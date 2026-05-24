from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.pipeline.graph import run_research_pipeline

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str
    user_id: str = "anonymous"
    scope: str = "Comprehensive"
    audience: str = "Academic Researchers"
    research_type: str = "Comprehensive"
    page_length: int = 1000


# POST /research — runs the multi-agent pipeline and returns the research brief
@router.post("/research")
async def research(request: ResearchRequest):
    try:
        result = run_research_pipeline(
            query=request.query,
            scope=request.scope,
            audience=request.audience,
            research_type=request.research_type,
            page_length=request.page_length,
        )
        return {
            "brief": result["brief"],
            "sources": result["sources"],
            "query": request.query,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
