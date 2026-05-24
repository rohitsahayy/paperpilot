import os
import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(
    page_title="PaperPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load external CSS
with open(os.path.join(os.path.dirname(__file__), "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔬 Research Controls")
    st.divider()

    audience = st.selectbox(
        "Target Audience",
        ["Academic Researchers", "General Public", "Industry Professionals", "Students"],
    )
    research_type = st.selectbox(
        "Research Type",
        ["Comprehensive", "Literature Review", "Technical Deep-Dive", "Trend Analysis"],
    )
    page_length = st.slider("Target Length (words)", 500, 5000, 1000, step=100)

    st.divider()
    st.caption("Advanced Options")
    enable_citations = st.checkbox("Enable Citations", value=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🚀 Agentic Research Assistant")
st.caption("Advanced AI-Powered Research Automation System · Multi-Agent Architecture")
st.divider()

# ── Search bar ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. machine learning for physics",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("🚀 Research", type="primary", use_container_width=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Researching across ArXiv, HackerNews, Wikipedia, Tavily and DEV.to..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/api/v1/research",
                    json={
                        "query": topic,
                        "audience": audience,
                        "research_type": research_type,
                        "page_length": page_length,
                    },
                    timeout=180,
                )
                response.raise_for_status()
                st.session_state.result = response.json()
            except Exception as e:
                st.error(f"Research failed: {e}")
                st.session_state.result = None

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result:
    data = st.session_state.result
    sources = data.get("sources", [])
    brief = data.get("brief", "")

    num_sources = len(sources)
    all_urls = [u for s in sources for u in s.get("urls", []) if u]
    brief_len = len(brief)
    insight_lines = [l for l in brief.split("\n") if l.strip().startswith("-")]
    quality = min(10.0, round(5.0 + num_sources * 1.0, 1))

    # Metrics
    st.subheader("📊 Agentic Research Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Sources", num_sources, help="Literature sources fetched")
    c2.metric("💡 Insights", len(insight_lines), help="Key data points extracted")
    c3.metric("📝 Length", f"{brief_len:,}", help="Characters in brief")
    c4.metric("⭐ Quality", f"{quality}/10", help="Quality score based on source coverage")

    st.divider()

    # Brief + outputs side by side
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📄 Research Brief")
        st.markdown(brief)

    with col_right:
        st.subheader("🗂 Research Outputs")

        with st.expander("📖 Literature Sources", expanded=True):
            for s in sources:
                label = s.get("source_label", s.get("source", ""))
                urls = s.get("urls", [])
                if urls:
                    for url in urls[:2]:
                        st.markdown(f"- [{label}]({url})")
                else:
                    st.write(f"- {label}")

        with st.expander("💡 Data Insights", expanded=True):
            for s in sources:
                summary = s.get("summary", "")
                if summary:
                    st.caption(s.get("source_label", ""))
                    st.write(summary)
                    st.divider()

        if enable_citations and all_urls:
            with st.expander("🔗 Citations"):
                for i, url in enumerate(all_urls[:8], 1):
                    st.markdown(f"{i}. {url}")

else:
    # Empty state metrics
    st.subheader("📊 Agentic Research Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Sources", "—")
    c2.metric("💡 Insights", "—")
    c3.metric("📝 Length", "—")
    c4.metric("⭐ Quality", "—")

    st.divider()
    st.info("Enter a research topic above and click **Research** to generate your brief.")
