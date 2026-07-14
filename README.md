# Security Orchestration (SOAR) Implementation

## Internship Details

- **Intern ID:** CITS3861
- **Full Name:** Sahil Yar Khan
- **Number of Weeks:** 6 Weeks
- **Task:** Task 4
- **Domain:** Cyber Security
- **Organization:** CodTech IT Solutions

## Project Description

The SOAR Security Automation Platform is a Python-based cybersecurity application developed to automate basic security incident processing and management.

The application parses simulated Snort-format security alerts, classifies incidents into HIGH, MEDIUM, and LOW severity levels, executes simulated response playbooks, prevents duplicate incidents, and stores incident information in an SQLite database.

A Flask-based web dashboard is provided to view incidents and manage their status as OPEN, INVESTIGATING, or RESOLVED. The application also maintains audit logs and generates incident reports in CSV format.

## Features

- Security alert parsing
- Severity classification
- Automated response playbooks
- Duplicate incident prevention
- SQLite incident database
- Flask security dashboard
- Incident status management
- Audit logging
- CSV incident report generation

## Tools and Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Visual Studio Code

## Project Structure

```text
SOAR-Security-Automation-Platform/
├── alerts/
├── logs/
├── reports/
├── templates/
├── Screenshots/
├── alert_parser.py
├── database.py
├── playbook.py
├── soar.py
├── dashboard.py
├── report_generator.py
├── README.md
├── requirements.txt
└── Task4_SOAR_Documentation.pdf
```

## How to Run

Install the required package:

```bash
pip install -r requirements.txt
```

Run the SOAR engine:

```bash
python soar.py
```

Start the security dashboard:

```bash
python dashboard.py
```

Open the dashboard in the browser at `http://127.0.0.1:5000`.

Generate the incident report:

```bash
python report_generator.py
```

## Output

The application:

- Processes simulated security alerts.
- Classifies incident severity.
- Executes simulated response playbooks.
- Stores incidents and prevents duplicates.
- Displays incidents on a web dashboard.
- Manages incident lifecycle status.
- Maintains security audit logs.
- Generates a CSV incident report.


## Learning Outcomes

- Understanding of SOAR concepts and security automation.
- Practical experience with Flask and SQLite.
- Implementation of incident severity classification and response playbooks.
- Knowledge of incident management, audit logging, and security reporting.

