import sqlite3
from datetime import datetime
from memory import search_memory

DB_NAME = "saas_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def subscription_search(application=None, department=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT application, employee, department, plan,
           monthly_cost, license_status, last_login,
           monthly_logins, features_used, renewal_date, owner
    FROM subscriptions
    WHERE 1=1
    """

    params = []

    if application:
        query += " AND LOWER(application) LIKE ?"
        params.append(f"%{application.lower()}%")

    if department:
        query += " AND LOWER(department) LIKE ?"
        params.append(f"%{department.lower()}%")

    cursor.execute(query, params)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for r in rows:
        results.append({
            "application": r[0],
            "employee": r[1],
            "department": r[2],
            "plan": r[3],
            "monthly_cost": r[4],
            "license_status": r[5],
            "last_login": r[6],
            "monthly_logins": r[7],
            "features_used": r[8],
            "renewal_date": r[9],
            "owner": r[10]
        })

    return results


def analyze_usage(application=None, min_logins=5):
    conn = get_connection()
    cursor = conn.cursor()

    if application:
        cursor.execute("""
        SELECT application, employee, department, plan,
               monthly_cost, last_login, monthly_logins,
               features_used
        FROM subscriptions
        WHERE LOWER(application) LIKE ?
        """, (f"%{application.lower()}%",))
    else:
        cursor.execute("""
        SELECT application, employee, department, plan,
               monthly_cost, last_login, monthly_logins,
               features_used
        FROM subscriptions
        """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for r in rows:
        logins = r[6]

        if logins == 0:
            status = "UNUSED"
        elif logins < min_logins:
            status = "LOW_USAGE"
        elif logins < 20:
            status = "MODERATE_USAGE"
        else:
            status = "HIGH_USAGE"

        results.append({
            "application": r[0],
            "employee": r[1],
            "department": r[2],
            "plan": r[3],
            "monthly_cost": r[4],
            "last_login": r[5],
            "monthly_logins": logins,
            "features_used": r[7],
            "usage_status": status
        })

    return results


def calculate_waste(application=None):
    conn = get_connection()
    cursor = conn.cursor()

    if application:
        cursor.execute("""
        SELECT application, employee, monthly_cost,
               monthly_logins
        FROM subscriptions
        WHERE LOWER(application) LIKE ?
        """, (f"%{application.lower()}%",))
    else:
        cursor.execute("""
        SELECT application, employee, monthly_cost,
               monthly_logins
        FROM subscriptions
        """)

    rows = cursor.fetchall()
    conn.close()

    results = []
    total_waste = 0

    for r in rows:
        app = r[0]
        employee = r[1]
        cost = r[2]
        logins = r[3]

        if logins == 0:
            waste_type = "UNUSED"
            waste = cost
        elif logins <= 3:
            waste_type = "VERY_LOW_USAGE"
            waste = cost * 0.75
        elif logins <= 10:
            waste_type = "LOW_USAGE"
            waste = cost * 0.40
        else:
            waste_type = "NORMAL_USAGE"
            waste = 0

        total_waste += waste

        results.append({
            "application": app,
            "employee": employee,
            "monthly_cost": cost,
            "monthly_waste_estimate": round(waste, 2),
            "annual_waste_estimate": round(waste * 12, 2),
            "waste_type": waste_type
        })

    return {
        "licenses": results,
        "total_monthly_waste": round(total_waste, 2),
        "total_annual_waste": round(total_waste * 12, 2)
    }


def renewal_analysis(days=30):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT application, employee, plan, monthly_cost, renewal_date
    FROM subscriptions
    """)

    rows = cursor.fetchall()
    conn.close()

    today = datetime.now().date()

    results = []

    for r in rows:
        try:
            renewal = datetime.strptime(r[4], "%Y-%m-%d").date()
            difference = (renewal - today).days

            if 0 <= difference <= days:
                results.append({
                    "application": r[0],
                    "employee": r[1],
                    "plan": r[2],
                    "monthly_cost": r[3],
                    "renewal_date": r[4],
                    "days_until_renewal": difference
                })
        except:
            pass

    return results


def contract_analysis(application=None):
    conn = get_connection()
    cursor = conn.cursor()

    if application:
        cursor.execute("""
        SELECT application, plan, minimum_licenses,
               renewal_date, annual_cost,
               cancellation_notice_days
        FROM contracts
        WHERE LOWER(application) LIKE ?
        """, (f"%{application.lower()}%",))
    else:
        cursor.execute("""
        SELECT application, plan, minimum_licenses,
               renewal_date, annual_cost,
               cancellation_notice_days
        FROM contracts
        """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for r in rows:
        results.append({
            "application": r[0],
            "plan": r[1],
            "minimum_licenses": r[2],
            "renewal_date": r[3],
            "annual_cost": r[4],
            "cancellation_notice_days": r[5]
        })

    return results


def memory_search(query):
    return search_memory(query)