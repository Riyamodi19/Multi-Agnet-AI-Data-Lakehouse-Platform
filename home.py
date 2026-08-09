"""
Unified Project Portal & Dashboard Launcher (home.py)
Run with: streamlit run home.py
"""

import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup System Paths
BASE_DIR = r"d:\final_end_game"
AGENTIC_DIR = os.path.join(BASE_DIR, "agenticAI")
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if AGENTIC_DIR not in sys.path:
    sys.path.append(AGENTIC_DIR)

# Streamlit Configuration
st.set_page_config(
    page_title="Multi-Agent AI Data Lakehouse Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Home Portal & Sidebar
st.markdown("""
<style>
    /* Dark Theme Setup */
    .main, .stApp { background-color: #080B11 !important; color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #121826 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Hero Title & Description */
    .home-hero-box {
        background: linear-gradient(135deg, #101524 0%, #161D30 100%);
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .home-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 40%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .home-subtitle {
        font-size: 1.05rem;
        color: #38BDF8;
        font-weight: 600;
        margin-bottom: 14px;
    }
    
    .home-desc {
        font-size: 0.95rem;
        color: #94A3B8;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    
    /* Flow Step Card */
    .flow-card {
        background: #111726;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .flow-step-num { color: #A855F7; font-weight: bold; font-size: 1.1rem; }
    .flow-step-title { color: #FFFFFF; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; }
    .flow-step-desc { color: #8A99AD; font-size: 0.88rem; line-height: 1.45; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION MENU
# ---------------------------------------------------------
st.sidebar.markdown("<h2 style='color: #FFFFFF; font-size: 1.3rem; margin-bottom: 10px;'>⚡ Navigation Menu</h2>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Select Platform View:",
    ["🏠 Home (Project Overview)", "📊 Trained Data Dashboard (app.py)", "🕵️ Try Agentic AI Dashboard (app_agentic.py)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.8rem; color: #8A99AD; line-height: 1.4;">
    <b>Direct Launch Commands:</b><br>
    • Main App: <code>streamlit run app.py</code><br>
    • Agentic AI: <code>streamlit run agenticAI/app_agentic.py</code><br>
    • Portal: <code>streamlit run home.py</code>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: HOME PAGE (PROJECT OVERVIEW & PIPELINE HOW IT WORKS)
# ---------------------------------------------------------
if app_mode == "🏠 Home (Project Overview)":
    st.markdown("""
    <div class="home-hero-box">
        <div class="home-title">⚡ Multi-Agent AI Data Lakehouse & Payment Intelligence Platform</div>
        <div class="home-subtitle">Big Data Pipeline • MinIO Lakehouse • Scikit-Learn ML • Autonomous Multi-Agent AI</div>
        <div class="home-desc">
            Welcome to the <b>Multi-Agent AI Payment Intelligence Platform</b>. This project is an end-to-end Big Data & Agentic AI system built to scrape, stream, store, clean, and analyze payment gateway accounts across online betting platforms (<i>Melbet, 22Bet, 10Cric, 1xBet</i>, and newly added sites). It identifies mule bank accounts, rogue UPI IDs, tracks financial risk, and provides zero-hallucination natural language Q&A.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ How the Platform Works (End-to-End Pipeline Architecture)")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="flow-card">
            <div class="flow-step-num">Step 1</div>
            <div class="flow-step-title">🕷️ Automated Web Scraping (Playwright & Scrapy)</div>
            <div class="flow-step-desc">Extracts raw HTML DOM pages and payment cell cards across Melbet, 22Bet, 10Cric, and 1xBet. Generated 549 raw JSON file payloads.</div>
        </div>
        
        <div class="flow-card">
            <div class="flow-step-num">Step 2</div>
            <div class="flow-step-title">⚡ Kafka Distributed Real-Time Streaming</div>
            <div class="flow-step-desc">Streams scraped payment JSON records through Apache Kafka topics into bronze lakehouse storage with sub-second latency.</div>
        </div>
        
        <div class="flow-card">
            <div class="flow-step-num">Step 3</div>
            <div class="flow-step-title">📦 MinIO Data Lakehouse & PySpark Cleaning</div>
            <div class="flow-step-desc">Stores raw payloads in Bronze Parquet storage and cleans/deduplicates them (99.8% noise reduction) into Silver Parquet tables (340 unique methods).</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="flow-card">
            <div class="flow-step-num">Step 4</div>
            <div class="flow-step-title">🤖 Scikit-Learn Machine Learning Models</div>
            <div class="flow-step-desc">Trains Random Forest Classification (100% Acc), Isolation Forest Anomaly Detection (flagging rogue accounts), and K-Means Clustering.</div>
        </div>
        
        <div class="flow-card">
            <div class="flow-step-num">Step 5</div>
            <div class="flow-step-title">🔎 FAISS 384-D Vector Search & RAG Chatbot</div>
            <div class="flow-step-desc">Encodes payment methods into 384-D dense vector space to provide zero-hallucination context retrieval for natural language Q&A.</div>
        </div>
        
        <div class="flow-card">
            <div class="flow-step-num">Step 6</div>
            <div class="flow-step-title">🕵️ Autonomous Multi-Agent AI Orchestrator</div>
            <div class="flow-step-desc">ONE Intelligent Master Agent equipped with 8 Tools & 9 Capabilities capable of scraping and analyzing new websites on demand.</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: TRAINED DATA DASHBOARD (APP.PY)
# ---------------------------------------------------------
elif app_mode == "📊 Trained Data Dashboard (app.py)":
    from app import render_app
    render_app()

# ---------------------------------------------------------
# VIEW 3: TRY AGENTIC AI DASHBOARD (APP_AGENTIC.PY)
# ---------------------------------------------------------
elif app_mode == "🕵️ Try Agentic AI Dashboard (app_agentic.py)":
    from agenticAI.app_agentic import render_agentic_app
    render_agentic_app()
