import os
from datetime import datetime, date, timedelta


# =========================================================
# FILE PATHS
# =========================================================

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_FOLDER, "data")

EMPLOYEE_FILE = os.path.join(DATA_FOLDER, "employee_data.txt")
RECORDS_FILE = os.path.join(DATA_FOLDER, "leave_records.txt")


# =========================================================
# SETTINGS
# =========================================================

DATE_FORMAT = "%d-%m-%Y"


# Monday = 0
# Tuesday = 1
# Wednesday = 2
# Thursday = 3
# Friday = 4
# Saturday = 5
# Sunday = 6

WEEKEND_DAYS = [5, 6]

LEAVE_TYPES = [
    "Full Day",
    "Half Day (First Half)",
    "Half Day (Second Half)"
]


MAX_DAYS_AT_A_TIME = 31           
EMPLOYEE_FIELDS = ["empid", "name", "assigned_leaves", "leave_balance"]
RECORD_FIELDS = ["empid", "name", "leave_date", "leave_type", "days", "applied_on"]
