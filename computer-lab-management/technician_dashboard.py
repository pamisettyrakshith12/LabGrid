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
# VIEW TECHNICIAN PROFILE
# ============================================================

def view_profile(user):

    print("\n" + "=" * 60)
    print("                 MY PROFILE")
    print("=" * 60)

    print(f"Name        : {user['full_name']}")
    print(f"Username    : {user['username']}")
    print(f"Role        : {user['role'].upper()}")

    print("=" * 60)


# ============================================================
# VIEW ASSIGNED ISSUES
# ============================================================

def view_assigned_issues(user):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            c.computer_name,
            l.lab_name,
            u.full_name,
            i.title,
            i.description,
            i.priority,
            i.status,
            i.reported_at
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        JOIN labs l
            ON c.lab_id = l.id
        JOIN users u
            ON i.reported_by = u.id
        WHERE i.assigned_to = ?
        ORDER BY
            CASE i.priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            i.reported_at DESC
    """, (user["id"],))

    issues = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 115)
    print("                    MY ASSIGNED ISSUES")
    print("=" * 115)

    if not issues:

        print("No issues have been assigned to you.")

        print("=" * 115)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<18}"
        f"{'Reported By':<20}"
        f"{'Title':<25}"
        f"{'Priority':<12}"
        f"{'Status':<15}"
    )

    print("-" * 115)

    for issue in issues:

        (
            issue_id,
            computer_name,
            lab_name,
            reported_by,
            title,
            description,
            priority,
            status,
            reported_at
        ) = issue

        print(
            f"{issue_id:<5}"
            f"{computer_name:<18}"
            f"{lab_name:<18}"
            f"{reported_by[:19]:<20}"
            f"{title[:24]:<25}"
            f"{priority:<12}"
            f"{status:<15}"
        )

    print("=" * 115)


# ============================================================
# VIEW ISSUE DETAILS
# ============================================================

def view_issue_details(user):

    try:

        issue_id = int(
            input("\nEnter Issue ID: ")
        )

    except ValueError:

        print("\nInvalid Issue ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            c.computer_name,
            l.lab_name,
            u.full_name,
            u.username,
            i.title,
            i.description,
            i.priority,
            i.status,
            i.reported_at
            
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        JOIN labs l
            ON c.lab_id = l.id
        JOIN users u
            ON i.reported_by = u.id
        WHERE i.id = ?
          AND i.assigned_to = ?
    """, (issue_id, user["id"]))

    issue = cursor.fetchone()

    conn.close()

    if issue is None:

        print("\nIssue not found or this issue is not assigned to you.")

        return

    (
        issue_id,
        computer_name,
        lab_name,
        reporter_name,
        reporter_username,
        title,
        description,
        priority,
        status,
        reported_at
    ) = issue

    print("\n" + "=" * 65)
    print("                    ISSUE DETAILS")
    print("=" * 65)

    print(f"Issue ID       : {issue_id}")
    print(f"Computer       : {computer_name}")
    print(f"Lab            : {lab_name}")
    print(f"Reported By    : {reporter_name}")
    print(f"Username       : {reporter_username}")
    print(f"Title          : {title}")
    print(f"Description    : {description}")
    print(f"Priority       : {priority}")
    print(f"Status         : {status}")
    print(f"Reported At    : {reported_at}")
  

    print("=" * 65)


# ============================================================
# START MAINTENANCE
# ============================================================

def start_maintenance(user):

    print("\n" + "=" * 65)
    print("                  START MAINTENANCE")
    print("=" * 65)

    try:

        issue_id = int(
            input("Enter Issue ID: ")
        )

    except ValueError:

        print("\nInvalid Issue ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            i.computer_id,
            c.computer_name,
            i.title,
            i.status
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        WHERE i.id = ?
          AND i.assigned_to = ?
    """, (issue_id, user["id"]))

    issue = cursor.fetchone()

    if issue is None:

        conn.close()

        print("\nIssue not found or not assigned to you.")

        return

    (
        issue_id,
        computer_id,
        computer_name,
        title,
        status
    ) = issue

    if status == "RESOLVED":

        conn.close()

        print("\nThis issue has already been resolved.")

        return

    if status == "IN_PROGRESS":

        conn.close()

        print("\nMaintenance for this issue is already in progress.")

        return

    action = input(
        "\nEnter maintenance action being performed: "
    ).strip()

    if not action:

        conn.close()

        print("\nMaintenance action cannot be empty.")

        return

    maintenance_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO maintenance
        (
            computer_id,
            issue_id,
            technician_id,
            action_taken,
            maintenance_date,
            remarks
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        computer_id,
        issue_id,
        user["id"],
        action,
        maintenance_date,
        "Maintenance started."
    ))

    cursor.execute("""
        UPDATE issues
        SET status = 'IN_PROGRESS'
        WHERE id = ?
    """, (issue_id,))

    cursor.execute("""
        UPDATE computers
        SET status = 'UNDER_MAINTENANCE'
        WHERE id = ?
    """, (computer_id,))

    conn.commit()
    conn.close()

    print("\n" + "=" * 65)
    print("                 MAINTENANCE STARTED")
    print("=" * 65)

    print(f"Issue ID    : {issue_id}")
    print(f"Computer    : {computer_name}")
    print(f"Action      : {action}")
    print(f"Started     : {maintenance_date}")
    print("Issue Status: IN_PROGRESS")
    print("Computer    : UNDER_MAINTENANCE")

    print("=" * 65)


# ============================================================
# COMPLETE MAINTENANCE
# ============================================================

def complete_maintenance(user):

    print("\n" + "=" * 65)
    print("                COMPLETE MAINTENANCE")
    print("=" * 65)

    try:

        issue_id = int(
            input("Enter Issue ID: ")
        )

    except ValueError:

        print("\nInvalid Issue ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            i.computer_id,
            c.computer_name,
            i.title,
            i.status
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        WHERE i.id = ?
          AND i.assigned_to = ?
    """, (issue_id, user["id"]))

    issue = cursor.fetchone()

    if issue is None:

        conn.close()

        print("\nIssue not found or not assigned to you.")

        return

    (
        issue_id,
        computer_id,
        computer_name,
        title,
        status
    ) = issue

    if status != "IN_PROGRESS":

        conn.close()

        print(
            f"\nThis issue cannot be completed because its "
            f"current status is {status}."
        )

        return

    remarks = input(
        "\nEnter maintenance remarks: "
    ).strip()

    if not remarks:

        remarks = "Maintenance completed successfully."

    completion_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Update latest maintenance record

    cursor.execute("""
        UPDATE maintenance
        SET remarks = ?
        WHERE id = (
            SELECT id
            FROM maintenance
            WHERE issue_id = ?
              AND technician_id = ?
            ORDER BY maintenance_date DESC
            LIMIT 1
        )
    """, (
        remarks,
        issue_id,
        user["id"]
    ))

    # Resolve issue

    cursor.execute("""
        UPDATE issues
        SET status = 'RESOLVED',
            resolved_at = ?
        WHERE id = ?
    """, (
        completion_time,
        issue_id
    ))

    # Make computer available

    cursor.execute("""
        UPDATE computers
        SET status = 'AVAILABLE'
        WHERE id = ?
    """, (computer_id,))

    conn.commit()
    conn.close()

    print("\n" + "=" * 65)
    print("               MAINTENANCE COMPLETED")
    print("=" * 65)

    print(f"Issue ID      : {issue_id}")
    print(f"Computer      : {computer_name}")
    print(f"Completed     : {completion_time}")
    print(f"Remarks       : {remarks}")
    print("Issue Status  : RESOLVED")
    print("Computer      : AVAILABLE")

    print("=" * 65)


# ============================================================
# VIEW MAINTENANCE HISTORY
# ============================================================

def view_maintenance_history(user):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.id,
            c.computer_name,
            i.title,
            m.action_taken,
            m.maintenance_date,
            m.remarks
        FROM maintenance m
        JOIN computers c
            ON m.computer_id = c.id
        JOIN issues i
            ON m.issue_id = i.id
        WHERE m.technician_id = ?
        ORDER BY m.maintenance_date DESC
    """, (user["id"],))

    records = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 110)
    print("                  MY MAINTENANCE HISTORY")
    print("=" * 110)

    if not records:

        print("No maintenance records found.")

        print("=" * 110)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Issue':<25}"
        f"{'Action':<30}"
        f"{'Date':<20}"
    )

    print("-" * 110)

    for record in records:

        (
            maintenance_id,
            computer_name,
            title,
            action,
            maintenance_date,
            remarks
        ) = record

        print(
            f"{maintenance_id:<5}"
            f"{computer_name:<18}"
            f"{title[:24]:<25}"
            f"{action[:29]:<30}"
            f"{maintenance_date:<20}"
        )

    print("=" * 110)


# ============================================================
# VIEW COMPUTERS
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
            c.status
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        ORDER BY l.id, c.id
    """)

    computers = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 100)
    print("                    COMPUTER STATUS")
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
# TECHNICIAN DASHBOARD
# ============================================================

def technician_dashboard(user):

    while True:

        print("\n")
        print("=" * 65)
        print("                  TECHNICIAN DASHBOARD")
        print("=" * 65)

        print(f"Welcome, {user['full_name']}")
        print(f"Username: {user['username']}")

        print("-" * 65)

        print("1. My Profile")
        print("2. View Assigned Issues")
        print("3. View Issue Details")
        print("4. Start Maintenance")
        print("5. Complete Maintenance")
        print("6. View Maintenance History")
        print("7. View Computers")
        print("8. Logout")

        print("-" * 65)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            view_profile(user)

        elif choice == "2":

            view_assigned_issues(user)

        elif choice == "3":

            view_issue_details(user)

        elif choice == "4":

            start_maintenance(user)

        elif choice == "5":

            complete_maintenance(user)

        elif choice == "6":

            view_maintenance_history(user)

        elif choice == "7":

            view_computers()

        elif choice == "8":

            print("\nLogging out...")

            return

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\nTechnician Dashboard module loaded successfully.")

    print(
        "This file should normally be opened "
        "through auth.py."
    )