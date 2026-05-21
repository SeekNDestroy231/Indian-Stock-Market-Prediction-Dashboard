# BharatQuant — Predictive Indian Stock Market Dashboard

> Real-time NSE/BSE market intelligence powered by yFinance, FinBERT, and Plotly.

---

## Tech Stack

| Layer | Library | Purpose |
|-------|---------|---------|
| UI | **Streamlit** | Dashboard framework |
| Market Data | **yFinance** | Live NSE/BSE OHLCV + fundamentals |
| Analysis | **Pandas + NumPy** | SMA, EMA, RSI, MACD, Bollinger, ATR, OBV |
| Charts | **Plotly** | Interactive candlestick + indicator charts |
| News | **Feedparser** | Google News RSS ingestion |
| Sentiment | **HuggingFace FinBERT** | `ProsusAI/finbert` — Bullish/Bearish/Neutral |

---

## Project Structure

```
bharatquant/
├── app.py                    # Main entry point + global CSS
├── requirements.txt
│
├── components/
│   └── sidebar.py            # Navigation, watchlist, settings
│
├── pages/
│   ├── dashboard.py          # Market overview (indices, chart, breadth, news)
│   ├── stock_analysis.py     # Deep-dive: chart + S/R + fundamentals + news
│   ├── news_sentiment.py     # Bulk FinBERT analysis + timeline + export
│   └── screener.py           # Technical screener with 7+ filters
│
├── utils/
│   ├── data_fetcher.py       # yFinance wrapper with TTL caching
│   ├── indicators.py         # All TA: SMA/EMA/RSI/MACD/BB/ATR/OBV + signals
│   └── charts.py             # Plotly factory functions (dark theme)
│
└── models/
    ├── sentiment.py          # FinBERT pipeline + keyword fallback
    └── news_fetcher.py       # Feedparser RSS + HTML cleanup + sentiment
```

---

## Setup & Run

### 1. Clone / create the project folder
```bash
cd bharatquant
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note on PyTorch:** For CPU-only servers (no GPU), install the lighter wheel:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

### 4. Run the app
```bash
streamlit run app.py
```
Opens at **http://localhost:8501**

---

## Pages

### 📊 Dashboard
- Live quotes for all 8 major indices (NIFTY 50, SENSEX, BANK NIFTY, etc.)
- Candlestick price chart with SMA/EMA/Bollinger toggles
- RSI, MACD, and Volume sub-charts
- Buy/Sell signal markers from composite indicator strategy
- FinBERT sentiment gauge from live RSS news
- Market breadth donut (Advancing / Unchanged / Declining)
- Top 5 gainers and losers from NIFTY 50
- Sector performance horizontal bar chart

### 🔍 Stock Analysis
- Full quote header with 52W range and fundamentals
- Per-stock candlestick + all indicators
- Pivot-based Support & Resistance level detection
- Composite signal summary (BUY / HOLD / SELL)
- Stock-specific news with FinBERT scores
- Company description and website link

### 📰 News Sentiment
- Select any of 6 RSS feeds (NSE/BSE, NIFTY, IT, Banking, Economy...)
- Bulk FinBERT analysis across up to 30 articles
- Sentiment gauge + distribution bar
- Per-article score bar chart
- Filter cards by Bullish / Neutral / Bearish
- Export full analysis as CSV

### 🎯 Screener
- Scan all 30 NIFTY 50 stocks simultaneously
- Filters: RSI range, 1M % change, MACD crossover, price vs SMA, signal strength
- RSI vs Return scatter bubble chart
- Colour-coded results table
- Export filtered results as CSV

---

## Technical Indicators

| Indicator | Parameters | Signal Logic |
|-----------|-----------|-------------|
| SMA | 20, 50, 200 | Golden cross (SMA20 > SMA50) → BUY |
| EMA | 9, 21 | Fast EMA crossover |
| RSI | 14-period, Wilder's | < 35 → BUY candidate, > 70 → SELL candidate |
| MACD | 12/26/9 | MACD crosses above Signal line → BUY |
| Bollinger | 20 SMA ± 2σ | BB% position (0=lower band, 1=upper band) |
| ATR | 14-period | Volatility measure for position sizing |
| OBV | — | Volume trend confirmation |

Composite signal strength: 0–3 (more indicators aligned = stronger signal)

---

## Sentiment Model

**ProsusAI/finbert** — fine-tuned BERT for financial text.

- Input: article headline + first 256 chars of summary
- Output: `positive` → **Bullish**, `negative` → **Bearish**, `neutral` → **Neutral**
- Composite score: `P(bullish) − P(bearish)` → range [−1, +1]
- Aggregate across N articles → overall market sentiment

**Fallback:** If `transformers`/`torch` are unavailable, a keyword-based scorer activates automatically.

---

## Data Sources

| Data | Source | Refresh |
|------|--------|---------|
| Index quotes | yFinance (Yahoo Finance NSE feed) | Every 60s |
| OHLCV history | yFinance | Every 5 min |
| Fundamentals | yFinance `.info` | Every 1 hour |
| News | Google News RSS via Feedparser | Every 10 min |

NSE symbols use `.NS` suffix (e.g. `RELIANCE.NS`)
Indices use `^NSEI`, `^BSESN`, `^NSEBANK` etc.

---

## Adding Custom Stocks

In `utils/data_fetcher.py`, add to `NIFTY50_STOCKS`:
```python
"ZOMATO": "ZOMATO.NS",
"PAYTM":  "PAYTM.NS",
```

---

## Streamlit Configuration (optional)

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true
enableCORS = false

[theme]
base = "dark"
primaryColor = "#3b82f6"
backgroundColor = "#0a0e1a"
secondaryBackgroundColor = "#0f1525"
textColor = "#f0f4ff"
```
