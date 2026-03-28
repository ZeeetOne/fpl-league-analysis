"""Shared UI components and styling for FPL League Analysis."""

import streamlit as st

# ── CSS ───────────────────────────────────────────────────────────────────────

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main container */
.block-container {
    padding-top: 1.5rem !important;
    max-width: 1400px;
}

/* ── Metric cards ── */
.fpl-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-top: 3px solid #37003c;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-top-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
.fpl-card:hover {
    border-top-color: #5c0064;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(55, 0, 60, 0.1);
}
.fpl-card .card-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #6b7280;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
.fpl-card .card-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0f0a1e;
    line-height: 1.1;
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.fpl-card .card-delta {
    font-size: 0.78rem;
    font-weight: 500;
    margin-top: 0.25rem;
    font-family: 'DM Sans', sans-serif;
}
.fpl-card .card-delta.positive { color: #16a34a; }
.fpl-card .card-delta.negative { color: #dc2626; }
.fpl-card .card-delta.neutral  { color: #6b7280; }

/* ── Section headers ── */
.fpl-section-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin: 1.75rem 0 0.5rem;
}
.fpl-section-header .accent-bar {
    width: 4px;
    height: 22px;
    background: #37003c;
    border-radius: 2px;
    flex-shrink: 0;
}
.fpl-section-header h3 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #0f0a1e !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin: 0 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
}
.fpl-section-header .section-caption {
    font-size: 0.78rem;
    color: #6b7280;
    margin-left: 0.15rem;
    font-family: 'DM Sans', sans-serif;
}

/* ── Page header ── */
.fpl-page-header {
    margin-bottom: 1.5rem;
}
.fpl-page-header .page-eyebrow {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #37003c;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 0.3rem;
}
.fpl-page-header h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: #0f0a1e !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 0.02em;
    line-height: 1.1 !important;
    margin: 0 0 0.3rem !important;
}
.fpl-page-header .page-subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    font-family: 'DM Sans', sans-serif;
}

/* ── Welcome screen ── */
.fpl-welcome {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 65vh;
    text-align: center;
    padding: 3rem 2rem;
}
.fpl-welcome .welcome-ball {
    font-size: 4.5rem;
    animation: float 3s ease-in-out infinite;
    margin-bottom: 1.5rem;
    display: block;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-14px); }
}
.fpl-welcome h2 {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #0f0a1e !important;
    margin-bottom: 1rem !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    line-height: 1.15 !important;
    letter-spacing: 0.02em;
}
.fpl-welcome h2 span { color: #37003c; }
.fpl-welcome p {
    font-size: 1rem;
    color: #6b7280;
    max-width: 380px;
    line-height: 1.7;
    margin-bottom: 2rem;
    font-family: 'DM Sans', sans-serif;
}
.fpl-welcome .arrow-hint {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #37003c;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    animation: nudge 1.8s ease-in-out infinite;
}
@keyframes nudge {
    0%, 100% { transform: translateX(0); }
    50%       { transform: translateX(-8px); }
}

/* ── Sidebar brand ── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.25rem 0 1.25rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid #e5e7eb;
}
.sidebar-brand .brand-ball { font-size: 1.9rem; }
.sidebar-brand .brand-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: #37003c;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'Barlow Condensed', sans-serif;
    line-height: 1.15;
}
.sidebar-brand .brand-sub {
    font-size: 0.62rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'DM Sans', sans-serif;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}
"""


def inject_css() -> None:
    """Inject global FPL styles. Call once in app.py before pg.run()."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


# ── Components ────────────────────────────────────────────────────────────────

def metric_card(
    label: str,
    value: str,
    delta: str = None,
    delta_type: str = "neutral",
) -> None:
    """Render a styled FPL metric card inside the current column."""
    delta_html = (
        f'<div class="card-delta {delta_type}">{delta}</div>' if delta else ""
    )
    st.markdown(
        f"""
        <div class="fpl-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, caption: str = "") -> None:
    """Render a section header with a green accent bar."""
    caption_html = (
        f'<span class="section-caption">{caption}</span>' if caption else ""
    )
    st.markdown(
        f"""
        <div class="fpl-section-header">
            <div class="accent-bar"></div>
            <h3>{title}</h3>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, eyebrow: str = "", subtitle: str = "") -> None:
    """Render a styled page title block."""
    eyebrow_html = (
        f'<div class="page-eyebrow">{eyebrow}</div>' if eyebrow else ""
    )
    subtitle_html = (
        f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="fpl-page-header">
            {eyebrow_html}
            <h1>{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand() -> None:
    """Render the FPL brand block at the top of the sidebar."""
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-ball">⚽</div>
            <div>
                <div class="brand-name">FPL Analysis</div>
                <div class="brand-sub">League Dashboard</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def welcome_screen() -> None:
    """Render the onboarding screen when no league ID is set, then stop."""
    st.markdown(
        """
        <div class="fpl-welcome">
            <span class="welcome-ball">⚽</span>
            <h2>Your <span>FPL League</span>,<br>Analysed.</h2>
            <p>Enter your mini-league ID in the sidebar and click
               <strong>Analyze</strong> to unlock
               standings, stats, and insights for your league.</p>
            <div class="arrow-hint">← Enter your league ID in the sidebar</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()
