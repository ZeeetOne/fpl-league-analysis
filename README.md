# FPL League Analysis

A Fantasy Premier League dashboard to analyze our mini-league performance and have some fun with the data.

## What's This?

This is a personal project to track and analyze our FPL mini-league. It pulls data from the official FPL API and shows:

- **Dashboard**: Quick overview of the league
- **Standings**: Current league table
- **League Insights**: Points trends and rank movements over time
- **Head-to-Head**: Compare managers directly
- **Point Sources**: Where are the points coming from?
- **Transfer Analysis**: Who's been most active in the transfer market
- **Captain Picks**: Track captain choices each gameweek
- **Player Ownership**: Which players are popular in our league
- **Best Squad**: What the best team would look like

## Setup

1. Clone this repo:
```bash
git clone <repo-url>
cd fpl-league-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Update `config.py` with your league ID:
```python
LEAGUE_ID = your_league_id_here
```

## Running It

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## How to Find Your League ID

Go to your FPL league page, the URL will look like:
`https://fantasy.premierleague.com/leagues/320644/standings/c`

The number (320644) is your League ID.

## Tech Stack

- Streamlit for the web app
- Pandas for data handling
- Plotly for charts
- FPL API for the data

## Notes

- The FPL API might be down during gameweek updates (usually around match times)
- All data is pulled live from the FPL servers, so make sure you're connected to the internet

---

Made with ⚽ for analyzing our league
