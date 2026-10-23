from datetime import datetime, date, timedelta

from utils.constants import DATE_FORMAT, WEEKEND_DAYS, LEAVE_TYPES
from utils.formatters import format_days

from services.employee_service import (
    load_employees,
    find_employee,
    save_employees
)

from services.record_service import (
    get_employee_records,
    save_record
)


# =========================================================
# COUNT WORKING DAYS
# =========================================================

def count_working_days(start_date, end_date):

    days = 0

    current = start_date

    while current <= end_date:

        if current.weekday() not in WEEKEND_DAYS:

            days = days + 1

        current = current + timedelta(days=1)

    return days


# =========================================================
# CALCULATE ONE DAY LEAVE
# =========================================================

def calculate_one_day_leave(leave_type, leave_date):

    # -----------------------------------------------------
    # Weekend
    # -----------------------------------------------------

    if leave_date.weekday() in WEEKEND_DAYS:

        return 0

    # -----------------------------------------------------
    # Full Day
    # -----------------------------------------------------

    if leave_type == "Full Day":

        return 1

    # -----------------------------------------------------
    # Half Day
    # -----------------------------------------------------

    if (
        leave_type == "Half Day (First Half)"
        or
        leave_type == "Half Day (Second Half)"
    ):

        return 0.5

    return 0


# =========================================================
# CHECK OVERLAP FOR ONE DATE
# =========================================================

def has_overlap(emp_id, leave_date):

    records = get_employee_records(emp_id)

    for record in records:

        try:

            # Convert datetime -> date
            old_start = datetime.strptime(
                record["start_date"],
                DATE_FORMAT
            ).date()

            old_end = datetime.strptime(
                record["end_date"],
                DATE_FORMAT
            ).date()

        except (ValueError, KeyError):

            continue

        # -------------------------------------------------
        # Check whether requested date falls inside
        # an existing leave period
        # -------------------------------------------------

        if old_start <= leave_date <= old_end:

            return True

    return False


# =========================================================
# APPLY MULTIPLE LEAVE DATES
# =========================================================

def apply_leave(emp_id, leave_dates):

    """
    Example:

    [
        (date(2026, 10, 1), "Half Day (First Half)"),
        (date(2026, 10, 2), "Full Day"),
        (date(2026, 10, 3), "Full Day"),
        (date(2026, 10, 4), "Half Day (Second Half)")
    ]
    """

    # -----------------------------------------------------
    # Find employee
    # -----------------------------------------------------

    employees = load_employees()

    employee = find_employee(
        employees,
        emp_id
    )

    if employee is None:

        return False, "Employee ID not found."

    # -----------------------------------------------------
    # Check whether dates were selected
    # -----------------------------------------------------

    if len(leave_dates) == 0:

        return False, "Please select at least one leave date."

    # -----------------------------------------------------
    # Prevent duplicate dates in the same application
    # -----------------------------------------------------

    selected_dates = set()

    for leave_date, leave_type in leave_dates:

        if leave_date in selected_dates:

            return False, (
                f"{leave_date.strftime(DATE_FORMAT)} "
                f"has been selected more than once."
            )

        selected_dates.add(leave_date)

    # -----------------------------------------------------
    # Calculate total leave
    # -----------------------------------------------------

    total_days = 0

    # -----------------------------------------------------
    # Validate every selected date
    # -----------------------------------------------------

    for leave_date, leave_type in leave_dates:

        # -------------------------------------------------
        # Validate leave type
        # -------------------------------------------------

        if leave_type not in LEAVE_TYPES:

            return False, "Invalid leave type."

        # -------------------------------------------------
        # Validate date type
        # -------------------------------------------------

        if not isinstance(leave_date, date):

            return False, "Invalid leave date."

        # -------------------------------------------------
        # Check past date
        # -------------------------------------------------

        if leave_date < date.today():

            return False, (
                f"You cannot apply leave for "
                f"{leave_date.strftime(DATE_FORMAT)}."
            )

        # -------------------------------------------------
        # Calculate leave days
        # -------------------------------------------------

        days = calculate_one_day_leave(
            leave_type,
            leave_date
        )

        # -------------------------------------------------
        # Check weekend
        # -------------------------------------------------

        if days == 0:

            return False, (
                f"{leave_date.strftime(DATE_FORMAT)} "
                f"is a weekend holiday."
            )

        # -------------------------------------------------
        # Check existing leave
        # -------------------------------------------------

        if has_overlap(
            employee["empid"],
            leave_date
        ):

            return False, (
                f"Leave already exists for "
                f"{leave_date.strftime(DATE_FORMAT)}."
            )

        # -------------------------------------------------
        # Add to total
        # -------------------------------------------------

        total_days = total_days + days

    # -----------------------------------------------------
    # Check leave balance
    # -----------------------------------------------------

    if total_days > employee["leave_balance"]:

        return False, (
            "Insufficient leave balance. "
            "Available: " +
            format_days(
                employee["leave_balance"]
            ) +
            " day(s)."
        )

    # -----------------------------------------------------
    # Deduct total leave
    # -----------------------------------------------------

    employee["leave_balance"] = (
        employee["leave_balance"] - total_days
    )

    # -----------------------------------------------------
    # Save updated employee
    # -----------------------------------------------------

    save_employees(employees)

    # -----------------------------------------------------
    # Save every leave date
    # -----------------------------------------------------

    for leave_date, leave_type in leave_dates:

        days = calculate_one_day_leave(
            leave_type,
            leave_date
        )

        save_record(
            employee,
            leave_type,
            leave_date,
            days
        )

    # -----------------------------------------------------
    # Success message
    # -----------------------------------------------------

    return True, (
        f"{format_days(total_days)} day(s) "
        f"of leave approved successfully."
    )