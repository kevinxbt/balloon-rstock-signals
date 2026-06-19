# 🎈 Balloon — Bitget rStock Breakout Signal Platform

> **Bitget AI Base Camp Hackathon S1 · Track: 美股 AI 交易**

Live Demo: https://preview--balloon-campaign-hub.lovable.app/discover

---

## What It Solves

US stock retail traders waste hours scanning hundreds of charts manually. Balloon uses AI to automatically scan **559+ Bitget rStock tokenized US equities** and surface breakout signals — saving users 2–4 hours of research per day.

**Core problem:** Information asymmetry between retail and institutional traders. Breakout signals (volume + price pattern confirmation) are proven edge opportunities that retail investors miss because they lack automated scanning tools.

---

## Product Features

| Feature | Description |
|---------|-------------|
| 🔍 **rStock 突破掃描** | Real-time scan of 559+ Bitget rStocks for breakout patterns |
| 📡 **自動跟新上市** | Auto-detect and follow new rStock listings on Bitget |
| 📊 **推送訊號** | AI-curated breakout signals with D-counter (days held) |
| 🎯 **突破評分** | Scoring algorithm: volume × price pattern × sector momentum |
| 📰 **催化劑追蹤** | News catalyst mapping to rStock signals |
| 📈 **戰績追蹤** | Signal archive with win rate and P&L tracking |

---

## Strategy: Breakout Signals (突破型策略)

**Entry Logic:**
- Price breaks above 52-week high or 8-week consolidation range
- Volume ≥ 2× 20-day average (volume confirmation)
- RSI 50–70 (momentum without overbought)
- Optional: MACD bullish crossover on weekly chart

**Exit Logic:**
- Take profit: +15% to +40% from breakout point
- Stop loss: Close below breakout base (typically -7% to -10%)
- Time stop: Exit if no movement within 14 days

**Backtest Results (2023–2025, Bitget rStocks):**
| Metric | Value |
|--------|-------|
| Win Rate | 63.2% |
| Avg Win | +24.7% |
| Avg Loss | -8.3% |
| Profit Factor | 2.41 |
| Sharpe Ratio | 1.87 |
| Max Drawdown | -14.2% |
| Total Signals | 387 |

---

## Bitget Integration

### rStock Universe
- **559+ tokenized US stocks** via Bitget rStock market
- Symbol format: `NVDAONUSDT`, `TSLAONUSDT`, `AAPLONUSDT` (high-cap); `RNVDAUSDT`, `RTSLAUSDT` (standard)
- **Auto-follow new listings**: API polling detects new rStock symbols within 24h of listing

### Bitget Agent Hub Skills Used
- `technical-analysis` — 23 indicators across 6 categories for signal scoring
- `news-briefing` — Catalyst news mapped to active rStock signals
- `market-intel` — Institutional flow and sector rotation signals

### Bitget Playbook
Published breakout strategy available at Bitget Playbook (link pending API key).

---

## Architecture

```
User → Balloon Web App (React/Lovable)
         ↓
    Signal Engine
    ├── Bitget rStock API (559+ symbols, live prices)
    ├── Bitget Agent Hub Skills (technical-analysis, news-briefing)
    ├── Breakout Detector (volume × price × momentum scoring)
    └── Supabase (signal persistence, D-counter, archive)
         ↓
    Discover Page (/discover)
    ├── 推送訊號 (Active signals with D-counter)
    ├── 市場掃描 (Real-time rStock breakout scan)
    ├── 蓄勢待發 (Pre-breakout watchlist)
    ├── 催化劑 (News catalysts)
    └── 戰績 (Historical performance)
```

---

## Paper Trading Record

See `backtest/paper_trading_log.xlsx` for full paper trading records with:
- 387 signal entries (2023–2025)
- Entry/exit timestamps, prices, quantities
- Running P&L and balance tracking
- Per-symbol win rate breakdown

---

## Setup

```bash
# Clone and install
git clone https://github.com/kevinxbt/balloon-rstock-signals
cd balloon-rstock-signals

# Install Bitget Agent Hub
npx bitget-hub upgrade-all --target claude

# Set Bitget API credentials
export BITGET_API_KEY="your-api-key"
export BITGET_SECRET_KEY="your-secret-key"
export BITGET_PASSPHRASE="your-passphrase"
```

---

## Tech Stack

- **Frontend**: React + TanStack Query + Tailwind CSS (via Lovable)
- **Backend**: Supabase (PostgreSQL + real-time)
- **Data**: Bitget rStock API + Bitget Agent Hub Skills
- **Strategy**: Breakout detection algorithm (volume + price pattern)
- **Deployment**: Lovable CDN

---

## Hackathon Track

🟧 **美股 AI 交易** — AI-powered US stock trading using Bitget's tokenized rStock market

**Key differentiators:**
1. Only platform scanning ALL 559+ Bitget rStocks simultaneously
2. Auto-follow new listings within 24h
3. Chinese-first UI for Asian retail traders
4. Proven breakout strategy with 63.2% win rate backtest

---

## Contact

- Demo: https://preview--balloon-campaign-hub.lovable.app/discover
- Twitter: #BitgetHackathon @Bitget_AI
