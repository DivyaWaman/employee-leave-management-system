# Employee Leave Management System

A simple Python + Streamlit project. Employees can check their leave balance and apply for
**full day** or **half day** leave. Every approved leave is saved in a txt file.

## Files

| File | Job |
|---|---|
| `app.py` | The screen (Streamlit frontend) |
| `backend.py` | Rules, date calculation, reading/writing files |
| `employee_data.txt` | Employee ID, name, assigned leaves, leave balance |
| `leave_records.txt` | One line for every approved leave |
| `requirements.txt` | Packages to install |
| `EXPLANATION_FOR_SIR.md` | Mistakes found, full explanation, test cases, viva questions |

## How to run

1. Open this folder in VS Code.
2. Open the terminal and run: `pip install -r requirements.txt`
3. Then run: `streamlit run app.py`
4. The browser opens by itself. Try Employee ID: `VC01`, `VC02`, `VC03`, `VC04`.

## Leave rules

- Full Day: choose From and To date. Saturday and Sunday are not counted.
- Half Day: choose First Half or Second Half and ONE date. It uses 0.5 day.
- Past dates are not allowed.
- The same date cannot be applied twice.
- Leave is rejected if the balance is not enough.

To change the weekend holidays, edit `WEEKEND_DAYS` at the top of `backend.py`.
