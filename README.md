# Employee Leave Management System

## About the Project

The **Employee Leave Management System** is a beginner-friendly Python learning project built using **Python and Streamlit**. It helps manage employee information, check leave balances, and apply for full-day or half-day leave.

This project was developed to practice Python programming concepts and apply them in a practical application.

## Features

- Add and manage employee information.
- Search employees using their employee ID.
- View employee leave balances.
- Apply for full-day and half-day leave.
- Validate employee IDs and leave dates.
- Prevent leave applications for past dates.
- Check leave balance before applying for leave.
- Store employee and leave information in text files.
- Display leave status and summaries using charts.

## Technologies Used

- Python
- Streamlit
- File handling using text files
- `datetime` for date validation and calculations
- Git and GitHub for version control

## Project Structure

```text
leave_project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── services/
├── styles/
├── utils/
└── views/
```

- **app.py** — Main application entry point.
- **data/** — Stores employee and leave-related data in text files.
- **services/** — Contains employee and leave management logic.
- **styles/** — Contains styling-related files.
- **utils/** — Contains helper functions and formatting utilities.
- **views/** — Contains the Streamlit user interface components.
- **requirements.txt** — Lists the Python dependencies required to run the project.

## Leave Management Rules

- Employees can apply for full-day or half-day leave.
- Full-day leave can be applied for a date range.
- Saturdays and Sundays are excluded from full-day leave calculations, according to the configured rules.
- Half-day leave can be applied for the first half or second half of a single day.
- Past dates are not allowed.
- Duplicate leave applications for the same date are prevented according to the application's validation rules.
- Leave applications are rejected when the employee has insufficient leave balance.
- Employee and leave records are stored in text files.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DivyaWaman/employee-leave-management-system.git
```

### 2. Open the Project Folder

```bash
cd employee-leave-management-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, or Streamlit will provide a local URL to open.

## Learning Objectives

Through this project, I practiced:

- Python variables, data types, dictionaries, and functions.
- Conditional statements and loops.
- File handling and data storage.
- Exception handling and input validation.
- Date and time calculations using `datetime`.
- Organizing code into separate modules.
- Building interactive user interfaces using Streamlit.
- Displaying data using charts.
- Using Git and GitHub for version control.

## Project Purpose

This project is part of my Python learning journey. It demonstrates how Python fundamentals can be combined to build a simple, practical application while improving my problem-solving and coding skills.

## Future Improvements

- Add employee authentication.
- Introduce a database for persistent data storage.
- Add leave approval workflows.
- Improve reporting and employee dashboards.
