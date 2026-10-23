import streamlit as st

from services.employee_service import load_employees, add_employee
from utils.formatters import format_days
from utils.components import section, stat_card


def render():
    with st.container(border=True):
        section("Add a new employee", "Enter the details below to create a new employee profile.")

        with st.form("add_employee_form"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                new_id = st.text_input("Employee ID", placeholder="e.g. VC05")
            with col2:
                new_name = st.text_input("Employee Name", placeholder="e.g. Amit Patil")
            with col3:
                new_leaves = st.number_input(
                    "Assigned Leaves",
                    min_value=1,
                    max_value=60,
                    value=10,
                    step=1,
                    help="Number of leave days given to this employee.",
                )
            submitted = st.form_submit_button("Add Employee", type="primary")

        if submitted:
            success, message = add_employee(new_id, new_name, new_leaves)
            if success:
                st.success(message)
            else:
                st.error(message)

    # ---- Directory ----
    employees = load_employees()

    total_assigned = 0
    total_available = 0
    for employee in employees:
        total_assigned = total_assigned + employee["assigned_leaves"]
        total_available = total_available + employee["leave_balance"]

    section("Employee directory", "Everyone in the system and their current leave balance.")

    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f'<div class="stat stat-blue"><div class="stat-label">Employees</div>'
        f'<div class="stat-value">{len(employees)}</div><div class="stat-note">Registered in the system</div></div>',
        unsafe_allow_html=True,
    )
    c2.markdown(stat_card("Total assigned", format_days(total_assigned), "Across all employees", "blue"),
                unsafe_allow_html=True)
    c3.markdown(stat_card("Total available", format_days(total_available), "Across all employees", "green"),
                unsafe_allow_html=True)

    st.write("")

    if len(employees) == 0:
        st.markdown(
            '<div class="empty"><div class="empty-title">No employees yet</div>'
            '<div class="empty-text">Add the first employee using the form above.</div></div>',
            unsafe_allow_html=True,
        )
        return

    # Numbers are kept as numbers (not text), so sorting by a column works correctly.
    table = []
    for employee in employees:
        table.append({
            "Employee ID": employee["empid"],
            "Employee Name": employee["name"],
            "Assigned": employee["assigned_leaves"],
            "Consumed": employee["assigned_leaves"] - employee["leave_balance"],
            "Available": employee["leave_balance"],
        })

    st.dataframe(
        table,
        hide_index=True,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="small"),
            "Employee Name": st.column_config.TextColumn("Employee Name", width="large"),
            "Assigned": st.column_config.NumberColumn("Assigned", format="%.1f"),
            "Consumed": st.column_config.NumberColumn("Consumed", format="%.1f"),
            "Available": st.column_config.NumberColumn("Available", format="%.1f"),
        },
    )
