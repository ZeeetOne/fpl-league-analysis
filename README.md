# ⚽ FPL League Analysis

> A public Fantasy Premier League dashboard — enter any mini-league ID to unlock standings, stats, insights, and global comparisons.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3f4f75?logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Live Demo

> **[Open the app →](https://fpl-league-analysis.streamlit.app)**  *(enter your league ID in the sidebar to get started)*

---

## ✨ Features

### League Pages
All league pages are scoped to your mini-league. Enter a league ID in the sidebar to unlock them.

| Page | Description |
|---|---|
| **Dashboard** | League summary, GW highlights, top standings |
| **Standings** | Full table with points, chips, transfers, captain stats |
| **League Insights** | Points-per-GW trends and rank movement chart |
| **Head-to-Head** | Compare any two managers across the season |
| **Point Sources** | Breakdown of points by position (GK/DEF/MID/FWD) |
| **Transfer Analysis** | Transfer volume, most active managers, popular ins/outs |
| **Captain Picks** | Captain choices and returns per gameweek |
| **Player Ownership** | Which players are held across the league |

### Global Pages
No league ID required — these show worldwide FPL data.

| Page | Description |
|---|---|
| **Season Stats** | Global GW averages, highest scores, chip usage |
| **Player Rankings** | All players ranked by points, form, value, ownership |
| **Global Transfers** | Most transferred in/out players this GW and season |
| **Global Ownership** | Most owned players by position + differentials |
| **Best Squad** | Optimal squad selection from bootstrap data |

---

## 🔍 How to Find Your League ID

1. Go to [fantasy.premierleague.com](https://fantasy.premierleague.com)
2. Navigate to **Leagues → Your mini-league**
3. The URL will look like:
   ```
   https://fantasy.premierleague.com/leagues/320644/standings/c
   ```
4. The number (`320644`) is your **League ID** — enter it in the sidebar and click **Analyze**

---

## 🛠️ Local Setup

```bash
# 1. Clone
git clone https://github.com/ZeeetOne/fpl-league-analysis.git
cd fpl-league-analysis

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

Open your browser to `http://localhost:8501`, enter a league ID, and click **Analyze**.

---

## 🏗️ Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Plotly](https://plotly.com/python) | Interactive charts |
| [Requests](https://requests.readthedocs.io) | FPL API calls |

Data is sourced from the official **[Fantasy Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/)**.

---

## 📁 Project Structure

```
fpl-league-analysis/
├── app.py                    # Entry point, navigation, sidebar
├── config.py                 # App constants
├── data_loader.py            # Cached data fetching helpers
├── fpl_api.py                # FPL API client
├── pages/                    # One file per page
├── features/                 # Reusable render functions per feature
│   ├── ui.py                 # Shared UI components (metric_card, page_header…)
│   ├── dashboard/
│   ├── standings/
│   ├── league_insights/
│   ├── head_to_head/
│   ├── transfers/
│   ├── captain/
│   ├── managers/
│   ├── ownership/
│   └── global_stats/
└── .streamlit/
    └── config.toml           # FPL light theme
```

---

## 🤝 Contributing

Bug reports and feature requests are welcome — use the [Issues](https://github.com/ZeeetOne/fpl-league-analysis/issues) tab.

---

*Made with ⚽ using the FPL API*
