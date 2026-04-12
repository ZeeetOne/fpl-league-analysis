"""Feedback & suggestions page."""

from features.feedback import render_feedback_form
from features.ui import page_header

page_header(
    "Feedback",
    eyebrow="Help Us Improve",
    subtitle="Report bugs, request features, or share your thoughts.",
)

render_feedback_form()
