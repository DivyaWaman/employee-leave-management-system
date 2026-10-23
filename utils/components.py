# Small helpers that draw the parts of the screen that repeat on many pages.

import streamlit as st


def page_header(title, subtitle, right_text):
    """Page title on the left, a small date pill on the right."""
    st.markdown(
        f'<div class="page-head"><div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-sub">{subtitle}</div>'
        f'</div><div class="today-pill">{right_text}</div></div>',
        unsafe_allow_html=True,
    )


def section(title, subtitle=""):
    """A small heading with an optional grey line below it."""
    html = f'<div class="section-title">{title}</div>'
    if subtitle != "":
        html = html + f'<div class="section-sub">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)


def stat_card(label, value, note, color, small=False):
    """Return the HTML of one number card.
    color can be: blue, green, amber or red (the coloured bar on the left)."""
    size = "stat-small" if small else ""
    return (
        f'<div class="stat stat-{color} {size}">'
        f'<div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}<span class="stat-unit">days</span></div>'
        f'<div class="stat-note">{note}</div>'
        f'</div>'
    )
