import sqlite3
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE = "computer_lab.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# VIEW FACULTY PROFILE
# ============================================================

def view_profile(user):

    print("\n" + "=" * 60)
    print("                    MY PROFILE")
    print("=" * 60)

    print(f"Name        : {user['full_name']}")
    print(f"Username    : {user['username']}")
    print(f"Role        : {user['role'].upper()}")

    print("=" * 60)


# ============================================================
# VIEW ALL LABS
# ============================================================

def view_labs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            lab_name,
            building,
            floor,
            total_computers
        FROM labs
        ORDER BY id
    """)

    labs = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 75)
    print("                         LAB DETAILS")
    print("=" * 75)

    print(
        f"{'ID':<5}"
        f"{'Lab Name':<22}"
        f"{'Building':<12}"
        f"{'Floor':<10}"
        f"{'Computers':<12}"
    )

    print("-" * 75)

    for lab in labs:

        lab_id, lab_name, building, floor, total = lab

        print(
            f"{lab_id:<5}"
            f"{lab_name:<22}"
            f"{building:<12}"
            f"{floor:<10}"
            f"{total:<12}"
        )

    print("=" * 75)


# ============================================================
# VIEW ALL COMPUTERS
# ============================================================

def view_computers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.computer_name,
            l.lab_name,
            c.processor,
            c.ram,
            c.storage,
            c.operating_system,
            c.status
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        ORDER BY l.id, c.id
    """)

    computers = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 100)
    print("                       COMPUTER STATUS")
    print("=" * 100)

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Processor':<18}"
        f"{'RAM':<8}"
        f"{'Storage':<10}"
        f"{'Status':<20}"
    )

    print("-" * 100)

    for computer in computers:

        (
            computer_id,
            computer_name,
            lab_name,
            processor,
            ram,
            storage,
            operating_system,
            status
        ) = computer

        print(
            f"{computer_id:<5}"
            f"{computer_name:<18}"
            f"{lab_name:<20}"
            f"{processor:<18}"
            f"{ram:<8}"
            f"{storage:<10}"
            f"{status:<20}"
        )

    print("=" * 100)


# ============================================================
# VIEW AVAILABLE COMPUTERS
# ============================================================

def view_available_computers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.computer_name,
            l.lab_name,
            c.processor,
            c.ram,
            c.storage,
            c.operating_system
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        WHERE c.status = 'AVAILABLE'
        ORDER BY l.id, c.id
    """)

    computers = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 85)
    print("                    AVAILABLE COMPUTERS")
    print("=" * 85)

    if not computers:

        print("No computers are currently available.")
        print("=" * 85)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Processor':<18}"
        f"{'RAM':<8}"
        f"{'Storage':<10}"
    )

    print("-" * 85)

    for computer in computers:

        (
            computer_id,
            computer_name,
            lab_name,
            processor,
            ram,
            storage,
            operating_system
        ) = computer

        print(
            f"{computer_id:<5}"
            f"{computer_name:<18}"
            f"{lab_name:<20}"
            f"{processor:<18}"
            f"{ram:<8}"
            f"{storage:<10}"
        )

    print("=" * 85)


# ============================================================
# VIEW ACTIVE LAB SESSIONS
# ============================================================

def view_active_sessions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ls.id,
            u.full_name,
            u.username,
            c.computer_name,
            l.lab_name,
            ls.login_time,
            ls.purpose
        FROM lab_sessions ls
        JOIN users u
            ON ls.student_id = u.id
        JOIN computers c
            ON ls.computer_id = c.id
        JOIN labs l
            ON ls.lab_id = l.id
        WHERE ls.logout_time IS NULL
        ORDER BY ls.login_time DESC
    """)

    sessions = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 110)
    print("                    ACTIVE LAB SESSIONS")
    print("=" * 110)

    if not sessions:

        print("No active lab sessions.")
        print("=" * 110)

        return

    print(
        f"{'ID':<5}"
        f"{'Student':<22}"
        f"{'Student ID':<25}"
        f"{'Computer':<18}"
        f"{'Lab':<18}"
        f"{'Started':<20}"
    )

    print("-" * 110)

    for session in sessions:

        (
            session_id,
            student_name,
            student_username,
            computer_name,
            lab_name,
            login_time,
            purpose
        ) = session

        print(
            f"{session_id:<5}"
            f"{student_name[:21]:<22}"
            f"{student_username:<25}"
            f"{computer_name:<18}"
            f"{lab_name:<18}"
            f"{login_time:<20}"
        )

    print("=" * 110)


# ============================================================
# REPORT COMPUTER ISSUE
# ============================================================

def report_issue(user):

    print("\n" + "=" * 65)
    print("                    REPORT COMPUTER ISSUE")
    print("=" * 65)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.computer_name,
            l.lab_name,
            c.status
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        ORDER BY l.id, c.id
    """)

    computers = cursor.fetchall()

    conn.close()

    print(
        f"\n{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Status':<20}"
    )

    print("-" * 65)

    for computer in computers:

        print(
            f"{computer[0]:<5}"
            f"{computer[1]:<18}"
            f"{computer[2]:<20}"
            f"{computer[3]:<20}"
        )

    print("-" * 65)

    try:

        computer_id = int(
            input("Enter Computer ID: ")
        )

    except ValueError:

        print("\nInvalid computer ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.computer_name
        FROM computers c
        WHERE c.id = ?
    """, (computer_id,))

    computer = cursor.fetchone()

    if computer is None:

        conn.close()

        print("\nComputer not found.")

        return

    title = input(
        "Enter issue title: "
    ).strip()

    if not title:

        conn.close()

        print("\nIssue title cannot be empty.")

        return

    description = input(
        "Enter issue description: "
    ).strip()

    if not description:

        description = "No additional description provided."

    print("\nPriority:")
    print("1. LOW")
    print("2. MEDIUM")
    print("3. HIGH")
    print("4. CRITICAL")

    priority_choice = input(
        "Select priority: "
    ).strip()

    priority_map = {
        "1": "LOW",
        "2": "MEDIUM",
        "3": "HIGH",
        "4": "CRITICAL"
    }

    priority = priority_map.get(
        priority_choice,
        "MEDIUM"
    )

    cursor.execute("""
        INSERT INTO issues
        (
            computer_id,
            reported_by,
            title,
            description,
            priority,
            status
        )
        VALUES (?, ?, ?, ?, ?, 'OPEN')
    """, (
        computer_id,
        user["id"],
        title,
        description,
        priority
    ))

    conn.commit()
    conn.close()

    print("\n" + "=" * 65)
    print("                     ISSUE REPORTED")
    print("=" * 65)

    print(f"Computer    : {computer[1]}")
    print(f"Title       : {title}")
    print(f"Priority    : {priority}")
    print("Status      : OPEN")

    print("=" * 65)


# ============================================================
# VIEW FACULTY'S REPORTED ISSUES
# ============================================================

def view_my_issues(user):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            c.computer_name,
            i.title,
            i.description,
            i.priority,
            i.status,
            i.reported_at
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        WHERE i.reported_by = ?
        ORDER BY i.reported_at DESC
    """, (user["id"],))

    issues = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 100)
    print("                    MY REPORTED ISSUES")
    print("=" * 100)

    if not issues:

        print("You have not reported any issues.")

        print("=" * 100)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Title':<25}"
        f"{'Priority':<12}"
        f"{'Status':<15}"
        f"{'Reported At':<20}"
    )

    print("-" * 100)

    for issue in issues:

        (
            issue_id,
            computer_name,
            title,
            description,
            priority,
            status,
            reported_at
        ) = issue

        print(
            f"{issue_id:<5}"
            f"{computer_name:<18}"
            f"{title[:24]:<25}"
            f"{priority:<12}"
            f"{status:<15}"
            f"{reported_at:<20}"
        )

    print("=" * 100)


# ============================================================
# FACULTY DASHBOARD
# ============================================================

def faculty_dashboard(user):

    while True:

        print("\n")
        print("=" * 65)
        print("                     FACULTY DASHBOARD")
        print("=" * 65)

        print(f"Welcome, {user['full_name']}")
        print(f"Username: {user['username']}")

        print("-" * 65)

        print("1. My Profile")
        print("2. View All Labs")
        print("3. View All Computers")
        print("4. View Available Computers")
        print("5. View Active Lab Sessions")
        print("6. Report Computer Issue")
        print("7. View My Reported Issues")
        print("8. Logout")

        print("-" * 65)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            view_profile(user)

        elif choice == "2":

            view_labs()

        elif choice == "3":

            view_computers()

        elif choice == "4":

            view_available_computers()

        elif choice == "5":

            view_active_sessions()

        elif choice == "6":

            report_issue(user)

        elif choice == "7":

            view_my_issues(user)

        elif choice == "8":

            print("\nLogging out...")

            return

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\nFaculty Dashboard module loaded successfully.")

    print(
        "This file should normally be  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV         "
        "through auth.py."
    )