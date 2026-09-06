import sqlite3
from datetime import datetime, timedelta

DB_NAME = "saas_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application TEXT,
        employee TEXT,
        department TEXT,
        plan TEXT,
        monthly_cost REAL,
        license_status TEXT,
        last_login TEXT,
        monthly_logins INTEGER,
        features_used TEXT,
        renewal_date TEXT,
        owner TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee TEXT PRIMARY KEY,
        department TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application TEXT,
        plan TEXT,
        minimum_licenses INTEGER,
        renewal_date TEXT,
        annual_cost REAL,
        cancellation_notice_days INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM subscriptions")
    count = cursor.fetchone()[0]

    if count == 0:
        today = datetime.now()

        subscriptions = [
            ("Adobe Creative Cloud", "Rahul", "Finance", "Enterprise", 3500, "Active",
             "2026-06-12", 2, "Photoshop", "2026-09-25", "Finance IT"),
            ("Adobe Creative Cloud", "Priya", "Marketing", "Enterprise", 3500, "Active",
             "2026-09-02", 28, "Photoshop,Illustrator,Premiere", "2026-09-25", "Marketing IT"),
            ("Adobe Creative Cloud", "Arun", "Engineering", "Enterprise", 3500, "Active",
             "2026-02-10", 0, "", "2026-09-25", "Engineering IT"),
            ("Canva", "Meena", "Marketing", "Pro", 1200, "Active",
             "2026-08-30", 18, "Design", "2026-10-15", "Marketing"),
            ("Canva", "Karthik", "Finance", "Pro", 1200, "Active",
             "2026-05-02", 1, "Presentation", "2026-10-15", "Finance"),
            ("Canva", "Divya", "HR", "Pro", 1200, "Active",
             "2026-03-12", 0, "", "2026-10-15", "HR"),
            ("Slack", "Rahul", "Finance", "Business", 900, "Active",
             "2026-09-04", 150, "Messaging,Channels", "2027-01-20", "IT"),
            ("Slack", "Priya", "Marketing", "Business", 900, "Active",
             "2026-09-04", 180, "Messaging,Channels,Canvas", "2027-01-20", "IT"),
            ("Zoom", "Arun", "Engineering", "Enterprise", 1500, "Active",
             "2026-08-01", 4, "Meetings", "2026-09-18", "Engineering"),
            ("Zoom", "Meena", "Marketing", "Enterprise", 1500, "Active",
             "2026-07-10", 3, "Meetings", "2026-09-18", "Marketing"),
            ("Figma", "Divya", "HR", "Professional", 1800, "Active",
             "2026-01-05", 0, "", "2026-12-10", "HR"),
            ("Notion", "Karthik", "Finance", "Business", 700, "Active",
             "2026-09-01", 45, "Documents,Wiki", "2027-02-11", "Finance"),
            ("GitHub", "Arun", "Engineering", "Enterprise", 2100, "Active",
             "2026-09-05", 220, "Repositories,Actions", "2027-04-15", "Engineering"),
            ("GitHub", "Meena", "Marketing", "Enterprise", 2100, "Active",
             "2026-01-02", 0, "", "2027-04-15", "Marketing"),
            ("Jira", "Priya", "Marketing", "Standard", 850, "Active",
             "2026-08-25", 12, "Projects", "2026-11-18", "Marketing")
        ]

        cursor.executemany("""
        INSERT INTO subscriptions
        (application, employee, department, plan, monthly_cost,
         license_status, last_login, monthly_logins, features_used,
         renewal_date, owner)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, subscriptions)

        employees = [
            ("Rahul", "Finance", "Active"),
            ("Priya", "Marketing", "Active"),
            ("Arun", "Engineering", "Active"),
            ("Meena", "Marketing", "Active"),
            ("Karthik", "Finance", "Active"),
            ("Divya", "HR", "Active"),
            ("Suresh", "Engineering", "Left"),
            ("Anitha", "HR", "Active")
        ]

        cursor.executemany("""
        INSERT INTO employees
        (employee, department, status)
        VALUES (?, ?, ?)
        """, employees)

        contracts = [
            ("Adobe Creative Cloud", "Enterprise", 3, "2026-09-25", 126000, 30),
            ("Canva", "Pro", 3, "2026-10-15", 43200, 15),
            ("Slack", "Business", 2, "2027-01-20", 21600, 30),
            ("Zoom", "Enterprise", 2, "2026-09-18", 36000, 30),
            ("Figma", "Professional", 1, "2026-12-10", 21600, 30),
            ("Notion", "Business", 1, "2027-02-11", 8400, 30),
            ("GitHub", "Enterprise", 2, "2027-04-15", 50400, 30),
            ("Jira", "Standard", 1, "2026-11-18", 10200, 30)
        ]

        cursor.executemany("""
        INSERT INTO contracts
        (application, plan, minimum_licenses, renewal_date,
         annual_cost, cancellation_notice_days)
        VALUES (?, ?, ?, ?, ?, ?)
        """, contracts)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")