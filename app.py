"""
BharatQuant — Predictive Indian Stock Market Dashboard
=======================================================
Run with:  streamlit run app.py

Tech Stack:
  Streamlit · yFinance · Pandas · NumPy · Plotly · Feedparser · FinBERT (HuggingFace)
"""

import streamlit as st

st.set_page_config(
    page_title="BharatQuant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .stApp { background:#0a0e1a; color:#f0f4ff; }
  .block-container { padding:1rem 2rem; max-width:100%; }
  section[data-testid="stSidebar"] {
    background:#0f1525;
    border-right:1px solid rgba(99,120,180,0.18);
  }
  div[data-testid="metric-container"] {
    background:#111827;
    border:1px solid rgba(99,120,180,0.18);
    border-radius:10px; padding:12px;
  }
  h1,h2,h3 { color:#f0f4ff !important; }
  .stTabs [data-baseweb="tab"]     { color:#8b9cc8; font-size:13px; }
  .stTabs [aria-selected="true"]   { color:#3b82f6; border-bottom-color:#3b82f6; }
  .badge-bull { background:rgba(16,185,129,.13); color:#10b981;
    padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
  .badge-bear { background:rgba(239,68,68,.13); color:#ef4444;
    padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
  .badge-neu  { background:rgba(139,156,200,.10); color:#8b9cc8;
    padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
  .news-card { background:#111827; border:1px solid rgba(99,120,180,0.18);
    border-radius:10px; padding:14px 16px; margin-bottom:10px; }
  .news-title { font-size:13px; font-weight:600; color:#f0f4ff; line-height:1.4; }
  .news-meta  { font-size:11px; color:#4a5578; margin-top:4px; }
  .stDataFrame thead th { background:#111827 !important; color:#8b9cc8 !important; }
  div[data-testid="stSelectbox"] label { color:#8b9cc8 !important; }
</style>
""", unsafe_allow_html=True)

from components.sidebar   import render_sidebar
from pages.dashboard      import render_dashboard
from pages.stock_analysis import render_stock_analysis
from pages.news_sentiment import render_news_sentiment
from pages.screener       import render_screener

def main():
    cfg  = render_sidebar()
    page = cfg["page"]
    if   page == "Dashboard":      render_dashboard(cfg)
    elif page == "Stock Analysis": render_stock_analysis(cfg)
    elif page == "News Sentiment": render_news_sentiment(cfg)
    elif page == "Screener":       render_screener(cfg)

if __name__ == "__main__":
    main()
