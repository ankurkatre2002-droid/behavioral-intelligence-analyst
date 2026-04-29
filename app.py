"""
Behavioral Intelligence Analyst — Streamlit Application
An agentic conversational system for behavioral analysis.
"""

import streamlit as st
from dotenv import load_dotenv
from agents import clarifier_agent, analyst_agent

# Load environment variables from .env file
load_dotenv()

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="Behavioral Intelligence Analyst", layout="centered")

# ─── Custom Styling ───────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* ── Typography ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header ─────────────────────────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .main-header h1 {
        font-size: 1.9rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0;
    }

    /* ── Sidebar ────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #c4b5fd;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #cbd5e1;
        font-size: 0.85rem;
    }

    .example-card {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.75rem;
        font-size: 0.82rem;
        color: #e2e8f0;
        line-height: 1.45;
        transition: border-color 0.2s;
    }
    .example-card:hover {
        border-color: rgba(139, 92, 246, 0.5);
    }
    .example-label {
        font-weight: 600;
        color: #a78bfa;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }

    /* ── Divider ────────────────────────────────────────────────── */
    .header-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
        margin: 0.25rem 0 1.25rem 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>🧠 Behavioral Intelligence Analyst</h1>
    <p>Describe your users or customers in plain language — get instant behavioral analysis.</p>
</div>
<div class="header-divider"></div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 💡 Example Queries")
    st.markdown("Copy any of these into the chat to get started:")

    st.markdown("""
    <div class="example-card">
        <div class="example-label">Example 1 — Mobile App Engagement</div>
        I have 1000 mobile app users. 300 log in daily with long sessions, 400 log in occasionally and sessions are getting shorter, and 300 haven't opened the app in 3 weeks. What does this tell me?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="example-card">
        <div class="example-label">Example 2 — E-Commerce Behavior</div>
        Our e-commerce site has customers who browse frequently but rarely purchase, and a smaller group who purchase repeatedly. How should I think about these two groups?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="example-card">
        <div class="example-label">Example 3 — SaaS Retention</div>
        My SaaS product has users who were very active in month 1 but activity dropped sharply in month 2. Some recovered, most didn't. What behavioral patterns should I be looking for?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#64748b; font-size:0.75rem;'>"
        "Powered by LLaMA 3.3 70B via Groq</p>",
        unsafe_allow_html=True,
    )

# ─── Session State Initialization ────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_clarification" not in st.session_state:
    st.session_state.awaiting_clarification = False

if "original_query" not in st.session_state:
    st.session_state.original_query = ""

# ─── Display Chat History ────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Chat Input Handling ─────────────────────────────────────────────────────

user_input = st.chat_input("Describe your users or customer behavior…")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ── Branch: awaiting clarification response ──────────────────────────
    if st.session_state.awaiting_clarification:
        st.session_state.awaiting_clarification = False

        # Run analyst with full conversation history
        with st.chat_message("assistant"):
            with st.spinner("Analyzing behavioral patterns…"):
                analysis = analyst_agent(st.session_state.messages)
            st.markdown(analysis)
        st.session_state.messages.append({"role": "assistant", "content": analysis})

    # ── Branch: new query ────────────────────────────────────────────────
    else:
        st.session_state.original_query = user_input

        # Step 1: Clarifier Agent
        with st.spinner("Evaluating query…"):
            clarification = clarifier_agent(st.session_state.messages)

        if clarification["sufficient"]:
            # Directly run analyst
            with st.chat_message("assistant"):
                with st.spinner("Analyzing behavioral patterns…"):
                    analysis = analyst_agent(st.session_state.messages)
                st.markdown(analysis)
            st.session_state.messages.append({"role": "assistant", "content": analysis})
        else:
            # Ask clarifying question
            question = clarification["question"]
            with st.chat_message("assistant"):
                st.markdown(question)
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.awaiting_clarification = True