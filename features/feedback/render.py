"""Feedback form rendering with Formspree integration."""

import requests
import streamlit as st

from config import FORMSPREE_ENDPOINT

_PAGE_OPTIONS = [
    "Dashboard",
    "Standings",
    "League Insights",
    "Head-to-Head",
    "Point Sources",
    "Transfer Analysis",
    "Captain Picks",
    "Player Ownership",
    "Season Stats",
    "Player Rankings",
    "Global Transfers",
    "Global Ownership",
    "Best Squad",
    "Other",
]


def _submit(data: dict) -> bool:
    """Post feedback to Formspree. Returns True on success."""
    if not FORMSPREE_ENDPOINT:
        st.error("Feedback endpoint is not configured.")
        return False
    try:
        resp = requests.post(
            FORMSPREE_ENDPOINT,
            json=data,
            headers={"Accept": "application/json"},
            timeout=10,
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def render_feedback_form() -> None:
    """Render the feedback form with three tabs."""
    tab_bug, tab_feature, tab_general = st.tabs([
        "Report a Bug",
        "Request a Feature",
        "General Feedback",
    ])

    with tab_bug:
        with st.form("bug_report_form", clear_on_submit=True):
            st.markdown("##### Describe the bug you encountered")
            page = st.selectbox("Which page is affected?", _PAGE_OPTIONS, key="bug_page")
            description = st.text_area(
                "What happened?",
                placeholder="Describe what went wrong...",
                key="bug_desc",
            )
            steps = st.text_area(
                "Steps to reproduce (optional)",
                placeholder="1. Go to...\n2. Click on...\n3. See error...",
                key="bug_steps",
            )
            expected = st.text_area(
                "What did you expect? (optional)",
                placeholder="What should have happened instead...",
                key="bug_expected",
            )
            submitted = st.form_submit_button(
                "Submit Bug Report", type="primary", use_container_width=True,
            )
        if submitted:
            if not description.strip():
                st.warning("Please describe the bug before submitting.")
            elif _submit({
                "_subject": "Bug Report — FPL League Analysis",
                "type": "bug",
                "page": page,
                "description": description,
                "steps_to_reproduce": steps,
                "expected_behavior": expected,
            }):
                st.success("Bug report submitted — thank you!")
            else:
                st.error("Failed to submit. Please try again later.")

    with tab_feature:
        with st.form("feature_request_form", clear_on_submit=True):
            st.markdown("##### Suggest a new feature or improvement")
            area = st.selectbox("Related area", _PAGE_OPTIONS, key="feat_area")
            feature_desc = st.text_area(
                "What would you like to see?",
                placeholder="Describe the feature or improvement...",
                key="feat_desc",
            )
            alternatives = st.text_area(
                "Alternatives considered (optional)",
                placeholder="Have you tried any workarounds?",
                key="feat_alt",
            )
            submitted = st.form_submit_button(
                "Submit Feature Request", type="primary", use_container_width=True,
            )
        if submitted:
            if not feature_desc.strip():
                st.warning("Please describe the feature before submitting.")
            elif _submit({
                "_subject": "Feature Request — FPL League Analysis",
                "type": "feature",
                "area": area,
                "description": feature_desc,
                "alternatives": alternatives,
            }):
                st.success("Feature request submitted — thank you!")
            else:
                st.error("Failed to submit. Please try again later.")

    with tab_general:
        with st.form("general_feedback_form", clear_on_submit=True):
            st.markdown("##### Share your thoughts")
            rating = st.select_slider(
                "How would you rate your experience?",
                options=["Poor", "Fair", "Good", "Great", "Excellent"],
                value="Good",
                key="gen_rating",
            )
            message = st.text_area(
                "Your feedback",
                placeholder="Tell us what you think...",
                key="gen_msg",
            )
            submitted = st.form_submit_button(
                "Submit Feedback", type="primary", use_container_width=True,
            )
        if submitted:
            if not message.strip():
                st.warning("Please enter your feedback before submitting.")
            elif _submit({
                "_subject": "General Feedback — FPL League Analysis",
                "type": "general",
                "rating": rating,
                "message": message,
            }):
                st.success("Feedback submitted — thank you!")
            else:
                st.error("Failed to submit. Please try again later.")
