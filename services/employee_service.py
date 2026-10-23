# from utils.constants import EMPLOYEE_FILE
# from utils.formatters import format_days

# # =========================================================
# # LOAD EMPLOYEES
# # =========================================================

# def load_employees():

#     employees = []

#     try:

#         with open(EMPLOYEE_FILE, "r") as file:

#             for line in file:

#                 line = line.strip()

#                 if line == "":
#                     continue

#                 data = line.split("|")

#                 employee = {
#                     "empid": data[0],
#                     "name": data[1],
#                     "assigned_leaves": float(data[2]),
#                     "leave_balance": float(data[3])
#                 }

#                 employees.append(employee)

#     except FileNotFoundError:

#         return []

#     return employees


# # =========================================================
# # SAVE EMPLOYEES
# # =========================================================

# def save_employees(employees):

#     with open(EMPLOYEE_FILE, "w") as file:

#         for employee in employees:

#             line = (
#                 employee["empid"] + "|" +
#                 employee["name"] + "|" +
#                 format_days(employee["assigned_leaves"]) + "|" +
#                 format_days(employee["leave_balance"]) +
#                 "\n"
#             )

#             file.write(line)

# # =========================================================
# # FIND EMPLOYEE
# # =========================================================

# def find_employee(employees, emp_id):

#     emp_id = emp_id.strip().upper()

#     for employee in employees:

#         if employee["empid"].upper() == emp_id:

#             return employee

#     return None

# # =========================================================
# # ADD EMPLOYEE
# # =========================================================

# def add_employee(emp_id, name, assigned_leaves):

#     emp_id = emp_id.strip().upper()
#     name = name.strip()

#     if emp_id == "" or name == "":
#         return False, "Employee ID and Name cannot be empty."

#     if not name.replace(" ", "").isalpha():
#         return False, "Name should contain only letters and spaces."

#     employees = load_employees()

#     if find_employee(employees, emp_id) is not None:

#         return False, "This Employee ID already exists."

#     employee = {
#         "empid": emp_id,
#         "name": name,
#         "assigned_leaves": float(assigned_leaves),
#         "leave_balance": float(assigned_leaves)
#     }

#     employees.append(employee)

#     save_employees(employees)

#     return True, (
#         f"Employee {name} ({emp_id}) "
#         f"added successfully."
#     )
from utils.constants import EMPLOYEE_FILE
from utils.formatters import format_days


# =========================================================
# LOAD EMPLOYEES
# =========================================================

def load_employees():

    employees = []

    try:

        with open(EMPLOYEE_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if line == "":
                    continue

                data = line.split("|")

                # Ignore invalid lines
                if len(data) < 4:
                    continue

                try:

                    employee = {
                        "empid": data[0],
                        "name": data[1],
                        "assigned_leaves": float(data[2]),
                        "leave_balance": float(data[3])
                    }

                except ValueError:
                    continue

                employees.append(employee)

    except FileNotFoundError:

        return []

    return employees


# =========================================================
# SAVE EMPLOYEES
# =========================================================

def save_employees(employees):

    with open(EMPLOYEE_FILE, "w") as file:

        for employee in employees:

            line = (
                employee["empid"] + "|" +
                employee["name"] + "|" +
                format_days(employee["assigned_leaves"]) + "|" +
                format_days(employee["leave_balance"]) +
                "\n"
            )

            file.write(line)


# =========================================================
# FIND EMPLOYEE
# =========================================================

def find_employee(employees, emp_id):

    emp_id = emp_id.strip().upper()

    for employee in employees:

        if employee["empid"].upper() == emp_id:

            return employee

    return None


# =========================================================
# ADD EMPLOYEE
# =========================================================

def add_employee(emp_id, name, assigned_leaves):

    emp_id = emp_id.strip().upper()
    name = name.strip()

    # -----------------------------------------------------
    # Validate Employee ID and Name
    # -----------------------------------------------------

    if emp_id == "" or name == "":
        return False, "Employee ID and Name cannot be empty."

    if not name.replace(" ", "").isalpha():
        return False, "Name should contain only letters and spaces."

    # -----------------------------------------------------
    # Validate Leave Amount
    # -----------------------------------------------------

    try:

        assigned_leaves = float(assigned_leaves)

    except (ValueError, TypeError):

        return False, "Assigned leaves must be a valid number."

    if assigned_leaves <= 0:

        return False, "Assigned leaves must be greater than 0."

    # -----------------------------------------------------
    # Load Existing Employees
    # -----------------------------------------------------

    employees = load_employees()

    # -----------------------------------------------------
    # Check Duplicate Employee
    # -----------------------------------------------------

    if find_employee(employees, emp_id) is not None:

        return False, "This Employee ID already exists."

    # -----------------------------------------------------
    # Create Employee
    # -----------------------------------------------------

    employee = {
        "empid": emp_id,
        "name": name,
        "assigned_leaves": assigned_leaves,
        "leave_balance": assigned_leaves
    }

    employees.append(employee)

    # -----------------------------------------------------
    # Save Employee
    # -----------------------------------------------------

    save_employees(employees)

    return True, (
        f"Employee {name} ({emp_id}) "
        f"added successfully."
    )