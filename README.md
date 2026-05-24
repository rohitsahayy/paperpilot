# PaperPilot 🔬

PaperPilot is a multi-agent AI research assistant that takes a research topic, fetches content from 5 free sources in parallel, and generates a structured research brief using LangGraph and Groq LLM. It surfaces agreements, contradictions, and knowledge gaps across sources so you can understand a topic fast.

## Architecture

```
User (Streamlit UI)
        │
        ▼
FastAPI Backend (POST /api/v1/research)
        │
        ▼
LangGraph Pipeline
  ┌─────────────────────────────────────────┐
  │                                         │
  │  [1] Fetcher Agent                      │
  │      ├── ArXiv API (papers)             │
  │      ├── HackerNews API (discussions)   │
  │      ├── Wikipedia API (overview)       │
  │      ├── Tavily Search (web)            │
  │      └── DEV.to API (articles)         │
  │                ↓                        │
  │  [2] Summariser Agent (Groq LLM)        │
  │      └── 3-sentence summary per source │
  │                ↓                        │
  │  [3] Critic Agent (Groq LLM)            │
  │      └── agreements / contradictions   │
  │                ↓                        │
  │  [4] Writer Agent (Groq LLM)            │
  │      └── structured markdown brief     │
  └─────────────────────────────────────────┘
        │
        ▼
Streamlit renders markdown brief + source links
```

## How to Run Locally

### Prerequisites
- Docker installed
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Tavily API key (free at [tavily.com](https://tavily.com))

### Steps

1. Clone the repo:
   ```bash
   git clone https://github.com/rohitsahayy/paperpilot.git
   cd paperpilot
   ```

2. Create your `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. Build the Docker image:
   ```bash
   docker build -t paperpilot .
   ```

4. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env paperpilot
   ```

5. Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

6. Run the Streamlit frontend (in a separate terminal):
   ```bash
   pip install streamlit requests
   streamlit run frontend/streamlit_app.py
   ```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for LLM calls |
| `TAVILY_API_KEY` | Tavily API key for web search |
| `FASTAPI_URL` | FastAPI backend URL (default: `http://localhost:8000`) |

## Live Demo

[Live Demo](https://huggingface.co/spaces/rohitsahayy/paperpilot)

## Tech Stack

- **LangGraph** — multi-agent pipeline orchestration
- **Groq** (llama-3.3-70b-versatile) — fast, free-tier LLM
- **FastAPI** — REST API backend
- **Streamlit** — frontend UI
- **Docker** — single-container deployment
- **httpx** — async HTTP client
- **feedparser** — ArXiv XML parser
- **tavily-python** — Tavily search SDK
