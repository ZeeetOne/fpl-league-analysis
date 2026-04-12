"""Configuration constants for FPL League Analysis."""

DEFAULT_LEAGUE_ID = 0
APP_TITLE = "FPL League Analysis"
APP_ICON = "⚽"

# Formspree endpoint for feedback form (https://formspree.io)
# Set via Streamlit secrets: add FORMSPREE_ENDPOINT to .streamlit/secrets.toml (local)
# or the Streamlit Cloud secrets manager (deployed).
FORMSPREE_ENDPOINT: str = ""
