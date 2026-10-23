from anyio import Path
import streamlit as st
from datetime import date

from views.add_employee import render as render_add_employee
from views.employee_leave import render as render_employee_leave
from utils.components import page_header

st.set_page_config(
    page_title="Employee Leave Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------
# Styling. This is only the look (CSS), not Python logic.
# Colour meaning everywhere:  blue = assigned, amber = consumed,
# green = available / good, red = problem.
# The main colours of buttons, tabs and the sidebar are in .streamlit/config.toml
# ---------------------------------------------------------------
css_file = Path(__file__).parent / "styles" / "style.css"

with open(css_file, "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# ---------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------

# Reserve the top area for branding
brand_area = st.sidebar.empty()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------

st.sidebar.divider()

page = st.sidebar.radio(
    "Menu",
    ["Leave Dashboard", "Add Employee"],
    key="main_menu"
)


# ---------------------------------------------------------------
# Sidebar Branding
# ---------------------------------------------------------------

if page == "Leave Dashboard":

    brand_area.markdown(
        '<div class="brand-logo">📋</div>'
        '<div class="brand-title">Leave Manager</div>'
        '<div class="brand-caption">'
        'Check your leave balance, apply for leave and view your records.'
        '</div>',
        unsafe_allow_html=True,
    )

else:

    brand_area.markdown(
        '<div class="brand-logo employee-logo">''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" '
                'xmlns="http://www.w3.org/2000/svg">'
                '<circle cx="12" cy="8" r="4" stroke="white" stroke-width="2"/>'
                '<path d="M4 21C4 16.58 7.58 13 12 13C16.42 13 20 16.58 20 21" '
                'stroke="white" stroke-width="2" stroke-linecap="round"/>'
                '</svg>'
        '</div>'
        '<div class="brand-title">Employee Manager</div>'
        '<div class="brand-caption">'
        'Add employees and manage employee information.'
        '</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------
# Employee ID
# Only show this on Leave Dashboard
# ---------------------------------------------------------------

emp_id = ""

if page == "Leave Dashboard":

    st.sidebar.divider()

    emp_id = st.sidebar.text_input(
        "Employee ID",
        placeholder="Example: VC01",
        key="employee_id_input"
    ).strip().upper()

    st.sidebar.caption(
        "Type your Employee ID to open your dashboard."
    )
# ---------------------------------------------------------------
# Page header and the selected page
# ---------------------------------------------------------------

today_text = date.today().strftime("%A, %d %B %Y")

if page == "Add Employee":
    page_header("Employee Management", "Add employees and see everyone's leave balance.", today_text)
    render_add_employee()
else:
    page_header("Leave Dashboard", "Check your balance and apply for full day or half day leave.", today_text)
    render_employee_leave(emp_id)
