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
# ADMIN PROFILE
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
# VIEW USERS
# ============================================================

def view_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            full_name,
            role,
            batch,
            section
        FROM users
        ORDER BY
            CASE role
                WHEN 'admin' THEN 1
                WHEN 'faculty' THEN 2
                WHEN 'technician' THEN 3
                WHEN 'student' THEN 4
            END,
            id
    """)

    users = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 100)
    print("                         USERS")
    print("=" * 100)

    print(
        f"{'ID':<6}"
        f"{'Username':<28}"
        f"{'Name':<22}"
        f"{'Role':<15}"
        f"{'Batch':<10}"
        f"{'Section':<10}"
    )

    print("-" * 100)

    for user in users:

        (
            user_id,
            username,
            full_name,
            role,
            batch,
            section
        ) = user

        batch = batch if batch is not None else "-"
        section = section if section is not None else "-"

        print(
            f"{user_id:<6}"
            f"{username[:27]:<28}"
            f"{full_name[:21]:<22}"
            f"{role:<15}"
            f"{batch:<10}"
            f"{section:<10}"
        )

    print("=" * 100)


# ============================================================
# VIEW LABS
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
    print("                         LABS")
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

    print("\n" + "=" * 105)
    print("                      COMPUTER STATUS")
    print("=" * 105)

    print(
        f"{'ID':<6}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Processor':<18}"
        f"{'RAM':<8}"
        f"{'Storage':<10}"
        f"{'Status':<20}"
    )

    print("-" * 105)

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
            f"{computer_id:<6}"
            f"{computer_name:<18}"
            f"{lab_name:<20}"
            f"{processor:<18}"
            f"{ram:<8}"
            f"{storage:<10}"
            f"{status:<20}"
        )

    print("=" * 105)


# ============================================================
# VIEW SOFTWARE
# ============================================================

def view_software():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            software_name,
            version,
            license_type
        FROM software
        ORDER BY id
    """)

    software = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 75)
    print("                         SOFTWARE")
    print("=" * 75)

    print(
        f"{'ID':<6}"
        f"{'Software':<25}"
        f"{'Version':<15}"
        f"{'License':<20}"
    )

    print("-" * 75)

    for item in software:

        (
            software_id,
            software_name,
            version,
            license_type
        ) = item

        print(
            f"{software_id:<6}"
            f"{software_name:<25}"
            f"{version:<15}"
            f"{license_type:<20}"
        )

    print("=" * 75)


# ============================================================
# VIEW ALL ISSUES
# ============================================================

def view_all_issues():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.id,
            c.computer_name,
            reporter.full_name,
            technician.full_name,
            i.title,
            i.priority,
            i.status,
            i.reported_at
        FROM issues i

        JOIN computers c
            ON i.computer_id = c.id

        JOIN users reporter
            ON i.reported_by = reporter.id

        LEFT JOIN users technician
            ON i.assigned_to = technician.id

        ORDER BY
            CASE i.status
                WHEN 'OPEN' THEN 1
                WHEN 'IN_PROGRESS' THEN 2
                WHEN 'RESOLVED' THEN 3
                ELSE 4
            END,
            i.reported_at DESC
    """)

    issues = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 120)
    print("                         ALL ISSUES")
    print("=" * 120)

    if not issues:

        print("No issues found.")

        print("=" * 120)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Reported By':<20}"
        f"{'Technician':<20}"
        f"{'Title':<25}"
        f"{'Priority':<12}"
        f"{'Status':<15}"
    )

    print("-" * 120)

    for issue in issues:

        (
            issue_id,
            computer_name,
            reporter,
            technician,
            title,
            priority,
            status,
            reported_at
        ) = issue

        technician = technician if technician else "Not Assigned"

        print(
            f"{issue_id:<5}"
            f"{computer_name:<18}"
            f"{reporter[:19]:<20}"
            f"{technician[:19]:<20}"
            f"{title[:24]:<25}"
            f"{priority:<12}"
            f"{status:<15}"
        )

    print("=" * 120)


# ============================================================
# ASSIGN ISSUE TO TECHNICIAN
# ============================================================

def assign_issue():

    print("\n" + "=" * 70)
    print("                  ASSIGN ISSUE TO TECHNICIAN")
    print("=" * 70)

    try:

        issue_id = int(
            input("Enter Issue ID: ")
        )

    except ValueError:

        print("\nInvalid Issue ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Find issue
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            i.id,
            c.computer_name,
            i.title,
            i.priority,
            i.status
        FROM issues i
        JOIN computers c
            ON i.computer_id = c.id
        WHERE i.id = ?
    """, (issue_id,))

    issue = cursor.fetchone()

    if issue is None:

        conn.close()

        print("\nIssue not found.")

        return

    (
        issue_id,
        computer_name,
        title,
        priority,
        status
    ) = issue

    print("\nIssue Information")
    print("-" * 50)
    print(f"Issue ID    : {issue_id}")
    print(f"Computer    : {computer_name}")
    print(f"Title       : {title}")
    print(f"Priority    : {priority}")
    print(f"Status      : {status}")

    # --------------------------------------------------------
    # Display technicians
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            username,
            full_name
        FROM users
        WHERE role = 'technician'
        ORDER BY id
    """)

    technicians = cursor.fetchall()

    if not technicians:

        conn.close()

        print("\nNo technicians found.")

        return

    print("\nTechnicians")
    print("-" * 60)

    print(
        f"{'ID':<6}"
        f"{'Username':<25}"
        f"{'Name':<25}"
    )

    print("-" * 60)

    for technician in technicians:

        technician_id, username, full_name = technician

        print(
            f"{technician_id:<6}"
            f"{username:<25}"
            f"{full_name:<25}"
        )

    print("-" * 60)

    try:

        technician_id = int(
            input("Enter Technician ID: ")
        )

    except ValueError:

        conn.close()

        print("\nInvalid Technician ID.")

        return

    # --------------------------------------------------------
    # Validate technician
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            full_name
        FROM users
        WHERE id = ?
          AND role = 'technician'
    """, (technician_id,))

    technician = cursor.fetchone()

    if technician is None:

        conn.close()

        print("\nInvalid technician.")

        return

    # --------------------------------------------------------
    # Assign issue
    # --------------------------------------------------------

    cursor.execute("""
         UPDATE issues
         SET assigned_to = ?
        WHERE id = ?
   """, (
    technician_id,
    issue_id
    ))

    conn.commit()

    conn.close()

    print("\n" + "=" * 70)
    print("                    ISSUE ASSIGNED")
    print("=" * 70)

    print(f"Issue ID       : {issue_id}")
    print(f"Computer       : {computer_name}")
    print(f"Technician     : {technician[1]}")
    

    print("=" * 70)


# ============================================================
# VIEW MAINTENANCE RECORDS
# ============================================================

def view_maintenance_records():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        m.id,
        c.computer_name,
        i.title,
        u.full_name,
        m.action_taken,
        m.maintenance_date,
        m.remarks
    FROM maintenance m
    JOIN computers c
        ON m.computer_id = c.id
    JOIN issues i
        ON m.issue_id = i.id
    JOIN users u
        ON m.technician_id = u.id
    ORDER BY m.maintenance_date DESC
  """)

    records = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 115)
    print("                    MAINTENANCE RECORDS")
    print("=" * 115)

    if not records:

        print("No maintenance records found.")

        print("=" * 115)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Issue':<25}"
        f"{'Technician':<20}"
        f"{'Action':<30}"
        f"{'Date':<20}"
    )

    print("-" * 115)

    for record in records:

        (
            maintenance_id,
            computer_name,
            title,
            technician,
            action,
            maintenance_date,
            remarks
        ) = record

        print(
            f"{maintenance_id:<5}"
            f"{computer_name:<18}"
            f"{title[:24]:<25}"
            f"{technician[:19]:<20}"
            f"{action[:29]:<30}"
            f"{maintenance_date:<20}"
        )

    print("=" * 115)


# ============================================================
# VIEW LAB SESSIONS
# ============================================================

def view_lab_sessions():

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
            ls.logout_time,
            ls.purpose
        FROM lab_sessions ls
        JOIN users u
            ON ls.student_id = u.id
        JOIN computers c
            ON ls.computer_id = c.id
        JOIN labs l
            ON ls.lab_id = l.id
        ORDER BY ls.login_time DESC
    """)

    sessions = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 125)
    print("                       LAB SESSIONS")
    print("=" * 125)

    if not sessions:

        print("No lab sessions found.")

        print("=" * 125)

        return

    print(
        f"{'ID':<5}"
        f"{'Student':<20}"
        f"{'Student ID':<25}"
        f"{'Computer':<18}"
        f"{'Lab':<18}"
        f"{'Login':<20}"
        f"{'Logout':<20}"
    )

    print("-" * 125)

    for session in sessions:

        (
            session_id,
            student_name,
            student_username,
            computer_name,
            lab_name,
            login_time,
            logout_time,
            purpose
        ) = session

        logout_time = logout_time if logout_time else "ACTIVE"

        print(
            f"{session_id:<5}"
            f"{student_name[:19]:<20}"
            f"{student_username:<25}"
            f"{computer_name:<18}"
            f"{lab_name:<18}"
            f"{login_time:<20}"
            f"{logout_time:<20}"
        )

    print("=" * 125)


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard(user):

    while True:

        print("\n")
        print("=" * 65)
        print("                    ADMIN DASHBOARD")
        print("=" * 65)

        print(f"Welcome, {user['full_name']}")
        print(f"Username: {user['username']}")

        print("-" * 65)

        print("1. My Profile")
        print("2. View Users")
        print("3. View Labs")
        print("4. View Computers")
        print("5. View Software")
        print("6. View All Issues")
        print("7. Assign Issue to Technician")
        print("8. View Maintenance Records")
        print("9. View Lab Sessions")
        print("10. Logout")

        print("-" * 65)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            view_profile(user)

        elif choice == "2":

            view_users()

        elif choice == "3":

            view_labs()

        elif choice == "4":

            view_computers()

        elif choice == "5":

            view_software()

        elif choice == "6":

            view_all_issues()

        elif choice == "7":

            assign_issue()

        elif choice == "8":

            view_maintenance_records()

        elif choice == "9":

            view_lab_sessions()

        elif choice == "10":

            print("\nLogging out...")

            return

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\nAdmin Dashboard module loaded successfully.")

    print(
        "This file should normally be opened "
        "through auth.py."
    )