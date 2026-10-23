from datetime import date, datetime

from utils.constants import RECORDS_FILE, DATE_FORMAT
from utils.formatters import format_days


# =========================================================
# LOAD LEAVE RECORDS
# =========================================================

def load_records():

    records = []

    try:

        with open(RECORDS_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if line == "":
                    continue

                data = line.split("|")

                # -------------------------------------------------
                # Old format:
                #
                # empid
                # name
                # leave_type
                # start_date
                # end_date
                # days
                # applied_on
                #
                # New format:
                #
                # empid
                # name
                # leave_type
                # start_date
                # end_date
                # days
                # applied_on
                # status
                # -------------------------------------------------

                if len(data) < 7:
                    continue

                if len(data) >= 8:

                    # New record format
                    record = {
                        "empid": data[0],
                        "name": data[1],
                        "leave_type": data[2],
                        "start_date": data[3],
                        "end_date": data[4],
                        "days": data[5],
                        "applied_on": data[6],
                        "status": data[7]
                    }

                else:

                    # -------------------------------------------------
                    # Support old records
                    # -------------------------------------------------

                    record = {
                        "empid": data[0],
                        "name": data[1],
                        "leave_type": data[2],
                        "start_date": data[3],
                        "end_date": data[4],
                        "days": data[5],
                        "applied_on": data[6],
                        "status": "Approved"
                    }

                records.append(record)

    except FileNotFoundError:

        return []

    return records


# =========================================================
# SAVE ONE LEAVE RECORD
# =========================================================

def save_record(
    employee,
    leave_type,
    leave_date,
    days
):

    with open(RECORDS_FILE, "a") as file:

        line = (
            employee["empid"] + "|" +
            employee["name"] + "|" +
            leave_type + "|" +
            leave_date.strftime(DATE_FORMAT) + "|" +
            leave_date.strftime(DATE_FORMAT) + "|" +
            format_days(days) + "|" +
            datetime.today().strftime(DATE_FORMAT) + "|" +
            "Approved" +
            "\n"
        )

        file.write(line)


# =========================================================
# GET EMPLOYEE LEAVE RECORDS
# =========================================================

def get_employee_records(emp_id):

    emp_id = emp_id.strip().upper()

    records = []

    for record in load_records():

        if record["empid"].upper() == emp_id:

            records.append(record)

    records.reverse()

    return records


# =========================================================
# GET TAKEN DATES
# =========================================================

def get_taken_dates(emp_id):

    taken = {}

    for record in get_employee_records(emp_id):

        taken[record["start_date"]] = record["leave_type"]

    return taken


# =========================================================
# GET UPCOMING LEAVES
# =========================================================

def get_upcoming_leaves(emp_id, limit=4):

    upcoming = []

    for record in get_employee_records(emp_id):

        try:

            leave_date = datetime.strptime(
                record["start_date"],
                DATE_FORMAT
            ).date()

        except (ValueError, KeyError):

            continue

        today = date.today()

        if leave_date >= today:

            upcoming.append(
                (
                    leave_date,
                    record["leave_type"],
                    record["days"]
                )
            )

    upcoming.sort(
        key=lambda item: item[0]
    )

    return upcoming[:limit]