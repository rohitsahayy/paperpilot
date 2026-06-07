# PaperPilot 🚀

PaperPilot is a multi-agent AI research assistant that takes a research topic, fetches content from 5 sources in parallel, and generates a structured research brief using LangGraph and Groq LLM. It surfaces agreements, contradictions, and knowledge gaps across sources so you can understand a topic fast.

**Live Demo:** https://paperpilot-ochre.vercel.app
**Backend API Docs:** https://paperpilot-api-lm7r.onrender.com/docs

---

## Architecture

```
Next.js Frontend (Vercel)
        │
        │ POST /api/v1/research
        ▼
FastAPI Backend (Render)
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
  │      └── surfaces agreements /         │
  │          contradictions / gaps         │
  │                ↓                        │
  │  [4] Writer Agent (Groq LLM)            │
  │      └── structured markdown brief     │
  └─────────────────────────────────────────┘
        │
        ▼
Next.js renders markdown brief + source links
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Next.js + Tailwind CSS |
| Frontend Hosting | Vercel |
| Backend | FastAPI |
| Backend Hosting | Render |
| Agent Orchestration | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Web Search | Tavily |
| Containerisation | Docker |

---

## Project Structure

```
paperpilot/
├── app/
│   ├── agents/
│   │   ├── fetcher.py       ← fetches from 5 sources in parallel
│   │   ├── summariser.py    ← 3-sentence summary per source
│   │   ├── critic.py        ← surfaces contradictions & gaps
│   │   └── writer.py        ← generates structured markdown brief
│   ├── pipeline/
│   │   └── graph.py         ← LangGraph orchestration
│   ├── api/
│   │   └── routes.py        ← FastAPI endpoints
│   └── main.py              ← FastAPI app entry point
├── frontend/                ← Next.js app (deployed on Vercel)
│   ├── app/
│   │   ├── page.tsx         ← main page
│   │   └── layout.tsx       ← root layout
│   └── components/
│       └── Sidebar.tsx      ← research controls
├── streamlit_backup/        ← archived Streamlit frontend
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key → [console.groq.com](https://console.groq.com)
- Tavily API key → [tavily.com](https://tavily.com)

### Backend

```bash
git clone https://github.com/rohitsahayy/paperpilot.git
cd paperpilot

cp .env.example .env
# add GROQ_API_KEY and TAVILY_API_KEY to .env

pip install -r requirements.txt
uvicorn app.main:app --reload
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install

# create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
# UI running at http://localhost:3000
```

### Docker (backend only)

```bash
docker build -t paperpilot .
docker run -p 8000:8000 --env-file .env paperpilot
```

---

## API

```
POST /api/v1/research
```

Request:
```json
{
  "query": "attention mechanism in transformers",
  "audience": "Academic Researchers",
  "research_type": "Comprehensive",
  "page_length": 1000
}
```

Response:
```json
{
  "brief": "markdown string",
  "sources": [
    {
      "source_label": "ArXiv Papers",
      "urls": ["https://..."],
      "summary": "..."
    }
  ],
  "status": "success"
}
```

Full interactive API docs: https://paperpilot-api-lm7r.onrender.com/docs

---

## Environment Variables

**Backend `.env`:**

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM calls |
| `TAVILY_API_KEY` | Tavily API key for web search |

**Frontend `.env.local`:**

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API base URL |

---

## Deployment

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://paperpilot-ochre.vercel.app |
| Backend | Render | https://paperpilot-api-lm7r.onrender.com |

Auto-deploys on every push to `main`.

> **Note:** Backend is on Render free tier — first request after inactivity may take 30–50 seconds to wake up.