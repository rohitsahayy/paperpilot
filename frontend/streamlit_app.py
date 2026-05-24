import os
import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Dark theme base */
    .stApp { background-color: #0f1117; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3148; }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #6c3fc5 0%, #4a2d8c 50%, #2d1f6e 100%);
        border-radius: 16px;
        padding: 40px 32px;
        text-align: center;
        margin-bottom: 28px;
    }
    .hero-banner h1 { font-size: 2.2rem; font-weight: 700; color: #fff; margin: 0 0 8px 0; }
    .hero-banner p { color: #c9b8f0; font-size: 1rem; margin: 4px 0; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #ddd;
        margin-top: 10px;
    }

    /* Metric cards */
    .metric-row { display: flex; gap: 16px; margin-bottom: 28px; }
    .metric-card {
        flex: 1;
        background: #1a1d27;
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
    }
    .metric-icon { font-size: 1.6rem; margin-bottom: 8px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #fff; }
    .metric-label { font-size: 0.78rem; color: #8a8fb5; margin-top: 4px; }

    /* Section cards */
    .section-card {
        background: #1a1d27;
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 20px 20px;
        margin-bottom: 20px;
    }
    .section-title { font-size: 1rem; font-weight: 600; color: #c9b8f0; margin-bottom: 14px; }

    /* Source item */
    .source-item {
        background: #22263a;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 3px solid #6c3fc5;
        font-size: 0.88rem;
    }
    .source-item a { color: #8b9bf0; text-decoration: none; }

    /* Insight item */
    .insight-item {
        background: #22263a;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 3px solid #3fc57a;
        font-size: 0.88rem;
        color: #c8d0e8;
    }
    .contradiction-item {
        background: #22263a;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 3px solid #e05c5c;
        font-size: 0.88rem;
        color: #c8d0e8;
    }
    .gap-item {
        background: #22263a;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 3px solid #e0a050;
        font-size: 0.88rem;
        color: #c8d0e8;
    }

    /* Hide default streamlit elements — NOT header (it holds the sidebar toggle) */
    #MainMenu, footer { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    div[data-testid="stMarkdownContainer"] p { color: #c8d0e8; }

    /* Search bar in main area */
    .search-row { display: flex; gap: 12px; align-items: flex-end; margin-bottom: 28px; }
    div[data-testid="stTextInput"] input {
        background: #1a1d27 !important;
        border: 1px solid #2d3148 !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar — advanced settings only ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔬 Research Controls")
    st.markdown("---")

    scope = st.selectbox("Research Scope", ["Comprehensive", "Focused", "Exploratory"])
    audience = st.selectbox("Target Audience", ["Academic Researchers", "General Public", "Industry Professionals", "Students"])
    research_type = st.selectbox("Research Type", ["Comprehensive", "Literature Review", "Technical Deep-Dive", "Trend Analysis"])
    page_length = st.slider("Target Page Length (words)", 500, 5000, 1000, step=100)

    st.markdown("---")
    st.markdown("**Advanced Options**")
    enable_citations = st.checkbox("Enable Citations", value=True)
    enable_plagiarism = st.checkbox("Enable Plagiarism Check", value=False)

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🚀 Agentic Research Assistant</h1>
    <p>Advanced AI-Powered Research Automation System</p>
    <span class="hero-badge">Multi-Agent Architecture with Agentic Features</span>
</div>
""", unsafe_allow_html=True)

# ── Topic input in main area ──────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input("", placeholder="Enter your research topic or question — e.g. 'machine learning for physics'", label_visibility="collapsed")
with col_btn:
    run_btn = st.button("🚀 Research", use_container_width=True, type="primary")

# ── State for results ─────────────────────────────────────────────────────────
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
                        "scope": scope,
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

# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.result:
    data = st.session_state.result
    sources = data.get("sources", [])
    brief = data.get("brief", "")

    # Count metrics
    num_sources = len(sources)
    all_urls = [u for s in sources for u in s.get("urls", []) if u]
    brief_len = len(brief)
    quality = min(10.0, round(5.0 + num_sources * 1.0, 1))

    # Pull analysis from brief heuristically (agreements/contradictions extracted by critic agent)
    # We'll count bullet points as insights
    insight_lines = [l for l in brief.split("\n") if l.strip().startswith("-")]
    num_insights = len(insight_lines)

    # ── Metric dashboard ──────────────────────────────────────────────────────
    st.markdown("### 📊 Agentic Research Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">📚</div>
            <div class="metric-value">{num_sources}</div>
            <div class="metric-label">Literature Sources</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">💡</div>
            <div class="metric-value">{num_insights}</div>
            <div class="metric-label">Data Points</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">📝</div>
            <div class="metric-value">{brief_len:,}</div>
            <div class="metric-label">Characters</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-value">{quality}/10</div>
            <div class="metric-label">Quality Score</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout: outputs + sources ──────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 📄 Research Brief")
        st.markdown(brief)

    with col_right:
        st.markdown("### 🗂 Research Outputs")

        # Literature sources
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📖 Literature Sources</div>', unsafe_allow_html=True)
        for s in sources:
            label = s.get("source_label", s.get("source", ""))
            urls = s.get("urls", [])
            if urls:
                for url in urls[:2]:
                    st.markdown(f'<div class="source-item"><a href="{url}" target="_blank">↗ {label}</a></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="source-item">{label}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Source summaries as data insights
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💡 Data Insights</div>', unsafe_allow_html=True)
        for s in sources:
            summary = s.get("summary", "")
            if summary:
                snippet = summary[:160] + "..." if len(summary) > 160 else summary
                st.markdown(f'<div class="insight-item"><strong>{s.get("source_label","")}</strong><br>{snippet}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Citations block
        if enable_citations and all_urls:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔗 Citations</div>', unsafe_allow_html=True)
            for i, url in enumerate(all_urls[:8], 1):
                st.markdown(f'<div class="source-item">[{i}] <a href="{url}" target="_blank">{url[:60]}{"…" if len(url)>60 else ""}</a></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("### 📊 Agentic Research Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label in zip(
        [c1, c2, c3, c4],
        ["📚", "💡", "📝", "⭐"],
        ["Literature Sources", "Data Points", "Characters", "Quality Score"],
    ):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">—</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.info("Enter a research topic in the sidebar and click **Start Research** to generate your brief.")
    with col_r:
        st.markdown('<div class="section-card"><div class="section-title">📖 Literature Sources</div><div class="source-item">Results will appear here</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-card"><div class="section-title">💡 Data Insights</div><div class="insight-item">Insights will appear here</div></div>', unsafe_allow_html=True)
