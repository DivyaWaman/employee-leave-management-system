import streamlit as st
import plotly.express as px
from datetime import date, datetime, timedelta

from services.employee_service import load_employees, find_employee
from services.leave_service import apply_leave, calculate_one_day_leave
from services.record_service import get_employee_records, get_taken_dates, get_upcoming_leaves
from utils.constants import LEAVE_TYPES, WEEKEND_DAYS, DATE_FORMAT, MAX_DAYS_AT_A_TIME
from utils.formatters import format_days, get_initials
from utils.components import section, stat_card

# Chart colours (same colours as the CSS in app.py)
AMBER = "#F2994A"
GREEN = "#12A87A"
GREY = "#CBD5E1"
NAVY = "#0E1F3F"


def day_chip(day, state):
    """The left part of a date row: a small calendar badge and the date.
    state is 'work' (normal day), 'off' (weekend) or 'done' (already applied)."""
    badge_class = "" if state == "work" else state
    text_class = "off" if state == "off" else ""
    return (
        f'<div class="day-chip"><div class="day-badge {badge_class}">'
        f'<span>{day.strftime("%a")}</span><b>{day.strftime("%d")}</b></div>'
        f'<div class="day-text {text_class}">{day.strftime("%d %b %Y")}</div></div>'
    )


def render(emp_id):
    # ---------------------------------------------------------
    # Find the employee
    # ---------------------------------------------------------
    if emp_id == "":
        st.markdown(
            '<div class="empty"><div style="font-size:2.4rem;">👋</div>'
            '<div class="empty-title">Enter your Employee ID</div>'
            '<div class="empty-text">Type your Employee ID in the sidebar (for example VC01) '
            'to see your leave balance and apply for leave.</div></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    employees = load_employees()
    if len(employees) == 0:
        st.error("⚠️ **No employee records found.** Please add an employee to continue.")
        st.stop()

    employee = find_employee(employees, emp_id)
    if employee is None:
        st.error("Invalid Employee ID. Please enter a registered Employee ID.")
        st.stop()

    assigned = employee["assigned_leaves"]
    available = employee["leave_balance"]
    consumed = assigned - available          # calculated, so it can never go out of sync

    # ---------------------------------------------------------
    # Profile card
    # ---------------------------------------------------------
    st.markdown(
        f'<div class="profile"><div class="avatar">{get_initials(employee["name"])}</div><div>'
        f'<div class="profile-hello">Welcome back</div>'
        f'<div class="profile-name">{employee["name"]}</div>'
        f'<div class="profile-id">Employee ID: {employee["empid"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Number cards
    # ---------------------------------------------------------
    c1, c2, c3 = st.columns(3)
    c1.markdown(stat_card("Assigned", format_days(assigned), "Total leave given", "blue"), unsafe_allow_html=True)
    c2.markdown(stat_card("Consumed", format_days(consumed), "Leave already used", "amber"), unsafe_allow_html=True)
    c3.markdown(stat_card("Available", format_days(available), "Leave remaining", "green"), unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------------
    # Chart + upcoming leave
    # ---------------------------------------------------------
    chart_col, side_col = st.columns([3, 2], gap="large")

    with chart_col:
        with st.container(border=True):
            section("Leave utilization", "How much of your leave is used and how much is left.")

            if assigned > 0:
                used_percent = consumed / assigned * 100
            else:
                used_percent = 0

            if consumed == 0 and available == 0:
                chart_names, chart_values, chart_colors = ["No leave"], [1], [GREY]
            else:
                chart_names, chart_values, chart_colors = ["Consumed", "Available"], [consumed, available], [AMBER, GREEN]

            donut = px.pie(names=chart_names, values=chart_values, hole=0.7)
            donut.update_traces(
                marker=dict(colors=chart_colors),
                textinfo="none",
                sort=False,
                hovertemplate="%{label}: %{value} day(s)<extra></extra>",
            )
            donut.add_annotation(           # text in the middle of the donut
                text=f"<b>{used_percent:.0f}%</b><br>used",
                showarrow=False, font=dict(size=22, color=NAVY),
            )
            donut.update_layout(
                height=290, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=-0.03, x=0.5, xanchor="center"),
            )
            st.plotly_chart(donut, config={"displayModeBar": False})

    with side_col:
        with st.container(border=True):
            section("Upcoming leave", "Your next approved leave dates.")

            upcoming = get_upcoming_leaves(emp_id)
            if len(upcoming) == 0:
                st.markdown('<div class="muted">No upcoming leave. Use the Apply Leave tab to add some.</div>',
                            unsafe_allow_html=True)
            for leave_date, leave_type, days in upcoming:
                unit = "day" if days == "1" else "days"
                st.markdown(
                    f'<div class="up-row"><div><div class="up-date">{leave_date.strftime("%a, %d %b %Y")}</div>'
                    f'<div class="up-type">{leave_type}</div></div>'
                    f'<div class="up-days">{days} {unit}</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<div style="margin-top:18px;" class="meter-text">Leave used: '
                f'<b>{format_days(consumed)}</b> of <b>{format_days(assigned)}</b> days</div>'
                f'<div class="meter"><div class="meter-fill" style="width:{min(used_percent, 100):.0f}%;"></div></div>',
                unsafe_allow_html=True,
            )

    st.write("")

    # ---------------------------------------------------------
    # Tabs
    # ---------------------------------------------------------
    tab_apply, tab_records = st.tabs(["Apply Leave", "My Leave Records"])

    # =========================================================
    # TAB 1: Apply Leave
    # =========================================================
    
    with tab_apply:
        approved_message = st.session_state.pop("approved_message", None)
        if approved_message:
            st.success("**Leave approved.** " + approved_message)

        today = date.today()

        # ---- Step 1: dates ----
        with st.container(border=True):
            section("Step 1: Choose your dates",
                    f"You can apply for up to {MAX_DAYS_AT_A_TIME} days at a time.")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("From Date", value=today, min_value=today, format="DD-MM-YYYY")
            with col2:
                end_date = st.date_input(
                    "To Date", value=start_date, min_value=start_date,
                    max_value=start_date + timedelta(days=MAX_DAYS_AT_A_TIME - 1),
                    format="DD-MM-YYYY",
                )

        # ---- Step 2: Full Day / Half Day for each date ----
        taken = get_taken_dates(emp_id)      # dates that already have leave
        leave_dates = []                     # list of pairs: (date, leave type)

        with st.container(border=True):
            section("Step 2: Full day or half day for each date",
                    "Pick one option for all dates, then change any single date if needed.")
            default_type = st.radio("Set all dates to", LEAVE_TYPES, horizontal=True)

            current_date = start_date
            while current_date <= end_date:          # <= so the last date is also included
                date_text = current_date.strftime(DATE_FORMAT)
                left, right = st.columns([2, 3])

                if current_date.weekday() in WEEKEND_DAYS:
                    left.markdown(day_chip(current_date, "off"), unsafe_allow_html=True)
                    right.markdown('<div class="side-note">Weekend holiday, no leave needed</div>',
                                   unsafe_allow_html=True)
                elif date_text in taken:
                    left.markdown(day_chip(current_date, "done"), unsafe_allow_html=True)
                    right.markdown(f'<div class="side-note done">Already applied: {taken[date_text]}</div>',
                                   unsafe_allow_html=True)
                else:
                    left.markdown(day_chip(current_date, "work"), unsafe_allow_html=True)
                    chosen_type = right.selectbox(
                        current_date.strftime("%d %b %Y"),
                        LEAVE_TYPES,
                        index=LEAVE_TYPES.index(default_type),
                        # The key must be different for every date, employee and default type
                        key=f"type_{emp_id}_{date_text}_{default_type}",
                        label_visibility="collapsed",
                    )
                    leave_dates.append((current_date, chosen_type))

                current_date = current_date + timedelta(days=1)       # go to the next date

        # ---- Step 3: check and submit ----
        total_days = 0
        
        
        for leave_date, leave_type in leave_dates:
        
            days = calculate_one_day_leave(
                leave_type,
                leave_date
            )
        
            total_days = total_days + days
        
        balance_after = available - total_days

        with st.container(border=True):
            section("Step 3: Check and submit")
            s1, s2, s3 = st.columns(3)
            s1.markdown(stat_card("Working days selected", str(len(leave_dates)), "Weekends are skipped", "blue", True),
                        unsafe_allow_html=True)
            s2.markdown(stat_card("Leave to be used", format_days(total_days), "Full day = 1, half day = 0.5", "amber", True),
                        unsafe_allow_html=True)
            if balance_after < 0:
                s3.markdown(stat_card("Balance after leave", format_days(balance_after), "Not enough balance", "red", True),
                            unsafe_allow_html=True)
            else:
                s3.markdown(stat_card("Balance after leave", format_days(balance_after), "What you will have left", "green", True),
                            unsafe_allow_html=True)

            st.write("")
            if len(leave_dates) == 0:
                st.info("Nothing to apply for in this period. It has only weekends or dates that already have leave.")
            elif balance_after < 0:
                st.error("Requested leave is more than your available balance.")

            # The button is switched off when there is nothing to apply or the balance is too low.
            cannot_apply = len(leave_dates) == 0 or balance_after < 0

            if st.button("Submit leave request", type="primary", disabled=cannot_apply):
                success, message = apply_leave(emp_id, leave_dates)
                if success:
                    st.session_state["approved_message"] = message
                    st.rerun()
                else:
                    st.error("**Leave not approved.** " + message)

    # =========================================================
    # TAB 2: My Leave Records
    # =========================================================

    with tab_records:

        records = get_employee_records(emp_id)

        # -----------------------------------------------------
        # No records
        # -----------------------------------------------------

        if len(records) == 0:

            st.markdown(
                '<div class="empty"><div class="empty-title">No leave yet</div>'
                '<div class="empty-text">Leave you apply for will be listed here.</div></div>',
                unsafe_allow_html=True,
            )

        # -----------------------------------------------------
        # Records exist
        # -----------------------------------------------------

        else:

            total_taken = 0
            upcoming_count = 0
            table = []

            # -------------------------------------------------
            # Read every leave record
            # -------------------------------------------------

            for record in records:

                # ---------------------------------------------
                # Convert days into number
                # ---------------------------------------------

                try:

                    days = float(record["days"])

                except (ValueError, KeyError):

                    continue

                total_taken = total_taken + days

                # ---------------------------------------------
                # Convert saved date into Python date
                # ---------------------------------------------

                try:

                    leave_date = datetime.strptime(
                        record["start_date"],
                        DATE_FORMAT
                    ).date()

                except (ValueError, KeyError):

                    continue

                # ---------------------------------------------
                # Check whether leave is upcoming
                # ---------------------------------------------

                if leave_date >= date.today():

                    upcoming_count = upcoming_count + 1

                # ---------------------------------------------
                # Add record to table
                # ---------------------------------------------

                table.append({
                    "Leave Date": record["start_date"],
                    "Leave Type": record["leave_type"],
                    "Days": days,
                    "Applied On": record["applied_on"],
                    "Status": record["status"],
                })

            # -------------------------------------------------
            # Summary cards
            # -------------------------------------------------

            r1, r2, r3 = st.columns(3)

            r1.markdown(
                stat_card(
                    "Leave dates",
                    str(len(table)),
                    "Total records",
                    "blue",
                    True
                ),
                unsafe_allow_html=True
            )

            r2.markdown(
                stat_card(
                    "Days used",
                    format_days(total_taken),
                    "Completed and booked",
                    "amber",
                    True
                ),
                unsafe_allow_html=True
            )

            r3.markdown(
                stat_card(
                    "Upcoming dates",
                    str(upcoming_count),
                    "Today or later",
                    "green",
                    True
                ),
                unsafe_allow_html=True
            )

            st.write("")

            # -------------------------------------------------
            # Leave history
            # -------------------------------------------------

            section(
                "Leave history",
                "Every approved leave date, in the order it was applied."
            )

            st.dataframe(
                table,
                hide_index=True,
                column_config={

                    "Leave Date": st.column_config.TextColumn(
                        "Leave Date",
                        width="small"
                    ),

                    "Leave Type": st.column_config.TextColumn(
                        "Leave Type",
                        width="medium"
                    ),

                    "Days": st.column_config.NumberColumn(
                        "Days",
                        format="%.1f",
                        width="small"
                    ),

                    "Applied On": st.column_config.TextColumn(
                        "Applied On",
                        width="small"
                    ),

                    "Status": st.column_config.TextColumn(
                        "Status",
                        width="small"
                    ),
                },
            )