"""
components/sidebar.py
======================
Left navigation sidebar. Returns a config dict consumed by each page.
"""

import streamlit as st
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def render_sidebar() -> dict:
    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:4px 0 16px;">
          <div style="font-size:20px;font-weight:800;letter-spacing:-0.5px;color:#f0f4ff;">
            BHARAT<span style="color:#3b82f6;">QUANT</span>
          </div>
          <div style="font-size:10px;color:#4a5578;margin-top:2px;font-family:monospace;">
            Predictive Market Intelligence
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Market status ─────────────────────────────────────────────────
        now  = datetime.now(IST)
        wd   = now.weekday()
        h, m = now.hour, now.minute
        open_ = (wd < 5) and ((h > 9) or (h == 9 and m >= 15)) and \
                             ((h < 15) or (h == 15 and m <= 30))

        color  = "#10b981" if open_ else "#ef4444"
        status = "MARKET OPEN" if open_ else "MARKET CLOSED"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;
                    background:#111827;border:1px solid rgba(99,120,180,0.18);
                    border-radius:8px;padding:8px 12px;margin-bottom:12px;">
          <div style="width:8px;height:8px;border-radius:50%;
                      background:{color};
                      {'animation:pulse 1.4s infinite;' if open_ else ''}"></div>
          <div style="font-size:11px;font-weight:700;color:{color};font-family:monospace;">
            {status}
          </div>
          <div style="margin-left:auto;font-size:10px;color:#4a5578;font-family:monospace;">
            {now.strftime('%H:%M IST')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────
        st.markdown("<div style='font-size:10px;font-weight:700;color:#4a5578;"
                    "text-transform:uppercase;letter-spacing:1px;"
                    "margin-bottom:6px;'>Navigation</div>",
                    unsafe_allow_html=True)

        pages = {
            "Dashboard":      "📊",
            "Stock Analysis": "🔍",
            "News Sentiment": "📰",
            "Screener":       "🎯",
        }
        if "page" not in st.session_state:
            st.session_state.page = "Dashboard"

        for p, icon in pages.items():
            active = st.session_state.page == p
            bg     = "rgba(59,130,246,0.15)" if active else "transparent"
            border = "rgba(59,130,246,0.5)"  if active else "transparent"
            color  = "#3b82f6" if active else "#8b9cc8"
            if st.sidebar.button(f"{icon}  {p}", key=f"nav_{p}",
                                 use_container_width=True):
                st.session_state.page = p
                st.rerun()

        st.divider()

        # ── Settings ──────────────────────────────────────────────────────
        st.markdown("<div style='font-size:10px;font-weight:700;color:#4a5578;"
                    "text-transform:uppercase;letter-spacing:1px;"
                    "margin-bottom:8px;'>Settings</div>",
                    unsafe_allow_html=True)

        index = st.selectbox(
            "Active Index",
            ["NIFTY 50", "SENSEX", "BANK NIFTY", "NIFTY IT",
             "NIFTY MIDCAP", "NIFTY AUTO", "NIFTY PHARMA", "NIFTY FMCG"],
            key="active_index",
        )

        range_str = st.selectbox(
            "Chart Range",
            ["1D", "1W", "1M", "3M", "6M", "1Y", "3Y"],
            key="chart_range",
        )

        show_ma      = st.toggle("Moving Averages",   value=True,  key="show_ma")
        show_bb      = st.toggle("Bollinger Bands",   value=True,  key="show_bb")
        show_signals = st.toggle("Buy/Sell Signals",  value=True,  key="show_signals")
        auto_refresh = st.toggle("Auto-refresh (60s)",value=False, key="auto_refresh")

        st.divider()

        # ── Watchlist ─────────────────────────────────────────────────────
        st.markdown("<div style='font-size:10px;font-weight:700;color:#4a5578;"
                    "text-transform:uppercase;letter-spacing:1px;"
                    "margin-bottom:8px;'>Watchlist</div>",
                    unsafe_allow_html=True)

        if "watchlist" not in st.session_state:
            st.session_state.watchlist = ["RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK"]

        wl_input = st.text_input("Add symbol (NSE)", placeholder="e.g. WIPRO",
                                  key="wl_input", label_visibility="collapsed")
        if wl_input:
            sym = wl_input.strip().upper()
            if sym and sym not in st.session_state.watchlist:
                st.session_state.watchlist.append(sym)
                st.rerun()

        for sym in list(st.session_state.watchlist):
            col1, col2 = st.columns([4, 1])
            col1.markdown(
                f"<div style='font-size:12px;color:#f0f4ff;"
                f"font-family:monospace;padding:4px 0;'>{sym}</div>",
                unsafe_allow_html=True,
            )
            if col2.button("✕", key=f"rm_{sym}", help=f"Remove {sym}"):
                st.session_state.watchlist.remove(sym)
                st.rerun()

        st.divider()
        st.markdown(
            "<div style='font-size:10px;color:#4a5578;text-align:center;'>"
            "Data: NSE · BSE via yFinance<br>Sentiment: FinBERT (ProsusAI)</div>",
            unsafe_allow_html=True,
        )

    return {
        "page":         st.session_state.page,
        "index":        index,
        "range":        range_str,
        "show_ma":      show_ma,
        "show_bb":      show_bb,
        "show_signals": show_signals,
        "auto_refresh": auto_refresh,
        "watchlist":    st.session_state.watchlist,
    }
