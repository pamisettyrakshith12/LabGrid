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
# STUDENT PROFILE
# ============================================================

def view_profile(user):

    print("\n" + "=" * 55)
    print("                    MY PROFILE")
    print("=" * 55)

    print(f"Name        : {user['full_name']}")
    print(f"Student ID  : {user['username']}")
    print(f"Role        : {user['role']}")
    print(f"Batch       : {user['batch']}")
    print(f"Year        : {user['year']}")
    print(f"Section     : {user['section_name']}")
    print(f"Roll No     : {user['roll']}")

    print("=" * 55)


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
            c.operating_system,
            c.status
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        ORDER BY l.id, c.id
    """)

    computers = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 90)
    print("                     COMPUTER STATUS")
    print("=" * 90)

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Processor':<18}"
        f"{'RAM':<8}"
        f"{'Status':<20}"
    )

    print("-" * 90)

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
            f"{status:<20}"
        )

    print("=" * 90)


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

    print("\n" + "=" * 75)
    print("                 AVAILABLE COMPUTERS")
    print("=" * 75)

    if not computers:

        print("No computers are currently available.")
        print("=" * 75)

        return

    print(
        f"{'ID':<5}"
        f"{'Computer':<18}"
        f"{'Lab':<20}"
        f"{'Processor':<18}"
        f"{'RAM':<8}"
    )

    print("-" * 75)

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
        )

    print("=" * 75)


# ============================================================
# CHECK ACTIVE SESSION
# ============================================================

def get_active_session(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ls.id,
            ls.computer_id,
            c.computer_name,
            l.lab_name,
            ls.login_time,
            ls.purpose
        FROM lab_sessions ls
        JOIN computers c
            ON ls.computer_id = c.id
        JOIN labs l
            ON ls.lab_id = l.id
        WHERE ls.student_id = ?
          AND ls.logout_time IS NULL
        ORDER BY ls.login_time DESC
        LIMIT 1
    """, (student_id,))

    session = cursor.fetchone()

    conn.close()

    return session


# ============================================================
# VIEW CURRENT SESSION
# ============================================================

def view_current_session(user):

    session = get_active_session(user["id"])

    print("\n" + "=" * 60)
    print("                  CURRENT SESSION")
    print("=" * 60)

    if session is None:

        print("You do not have an active lab session.")

        print("=" * 60)

        return

    (
        session_id,
        computer_id,
        computer_name,
        lab_name,
        login_time,
        purpose
    ) = session

    print(f"Session ID  : {session_id}")
    print(f"Lab         : {lab_name}")
    print(f"Computer    : {computer_name}")
    print(f"Started     : {login_time}")
    print(f"Purpose     : {purpose}")

    print("Status      : ACTIVE")

    print("=" * 60)


# ============================================================
# START LAB SESSION
# ============================================================

def start_lab_session(user):

    # --------------------------------------------------------
    # Check whether student already has a session
    # --------------------------------------------------------

    active_session = get_active_session(user["id"])

    if active_session is not None:

        print("\nYou already have an active lab session.")

        print(
            f"Computer: {active_session[2]}"
        )

        return

    # --------------------------------------------------------
    # Show available computers
    # --------------------------------------------------------

    view_available_computers()

    try:

        computer_id = int(
            input("\nEnter Computer ID: ")
        )

    except ValueError:

        print("\nInvalid computer ID.")

        return

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Check selected computer
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            c.id,
            c.computer_name,
            c.lab_id,
            l.lab_name,
            c.status
        FROM computers c
        JOIN labs l
            ON c.lab_id = l.id
        WHERE c.id = ?
    """, (computer_id,))

    computer = cursor.fetchone()

    if computer is None:

        conn.close()

        print("\nComputer not found.")

        return

    (
        db_computer_id,
        computer_name,
        lab_id,
        lab_name,
        status
    ) = computer

    # --------------------------------------------------------
    # Check computer availability
    # --------------------------------------------------------

    if status != "AVAILABLE":

        conn.close()

        print(
            f"\n{computer_name} is not available."
        )

        print(f"Current status: {status}")

        return

    # --------------------------------------------------------
    # Get purpose
    # --------------------------------------------------------

    purpose = input(
        "Enter purpose of lab session: "
    ).strip()

    if not purpose:

        purpose = "General Lab Work"

    # --------------------------------------------------------
    # Create session
    # --------------------------------------------------------

    login_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO lab_sessions
        (
            student_id,
            computer_id,
            lab_id,
            login_time,
            purpose
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user["id"],
        db_computer_id,
        lab_id,
        login_time,
        purpose
    ))

    # --------------------------------------------------------
    # Change computer status
    # --------------------------------------------------------

    cursor.execute("""
        UPDATE computers
        SET status = 'IN_USE'
        WHERE id = ?
    """, (db_computer_id,))

    conn.commit()

    conn.close()

    print("\n" + "=" * 60)
    print("             LAB SESSION STARTED")
    print("=" * 60)

    print(f"Student   : {user['full_name']}")
    print(f"Lab       : {lab_name}")
    print(f"Computer  : {computer_name}")
    print(f"Started   : {login_time}")
    print(f"Purpose   : {purpose}")

    print("=" * 60)


# ============================================================
# END LAB SESSION
# ============================================================

def end_lab_session(user):

    session = get_active_session(user["id"])

    if session is None:

        print("\nYou do not have an active lab session.")

        return

    (
        session_id,
        computer_id,
        computer_name,
        lab_name,
        login_time,
        purpose
    ) = session

    print("\n" + "=" * 60)
    print("                END LAB SESSION")
    print("=" * 60)

    print(f"Lab        : {lab_name}")
    print(f"Computer   : {computer_name}")
    print(f"Started    : {login_time}")
    print(f"Purpose    : {purpose}")

    confirmation = input(
        "\nAre you sure you want to end the session? (y/n): "
    ).strip().lower()

    if confirmation != "y":

        print("\nSession was not ended.")

        return

    logout_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Update session
    # --------------------------------------------------------

    cursor.execute("""
        UPDATE lab_sessions
        SET logout_time = ?
        WHERE id = ?
    """, (
        logout_time,
        session_id
    ))

    # --------------------------------------------------------
    # Make computer available
    # --------------------------------------------------------

    cursor.execute("""
        UPDATE computers
        SET status = 'AVAILABLE'
        WHERE id = ?
    """, (computer_id,))

    conn.commit()

    conn.close()

    print("\n" + "=" * 60)
    print("              LAB SESSION ENDED")
    print("=" * 60)

    print(f"Computer   : {computer_name}")
    print(f"Logout     : {logout_time}")
    print("Computer   : AVAILABLE")

    print("=" * 60)


# ============================================================
# REPORT COMPUTER ISSUE
# ============================================================

def report_issue(user):

    print("\n" + "=" * 60)
    print("               REPORT COMPUTER ISSUE")
    print("=" * 60)

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

    print("\nComputers:")

    print(
        f"{'ID':<5}"
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

    # --------------------------------------------------------
    # Insert issue
    # --------------------------------------------------------

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

    print("\n" + "=" * 60)
    print("               ISSUE REPORTED")
    print("=" * 60)

    print(f"Computer    : {computer[1]}")
    print(f"Title       : {title}")
    print(f"Priority    : {priority}")
    print("Status      : OPEN")

    print("=" * 60)


# ============================================================
# VIEW MY ISSUES
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
# STUDENT DASHBOARD
# ============================================================

def student_dashboard(user):

    while True:

        print("\n")
        print("=" * 60)
        print("                 STUDENT DASHBOARD")
        print("=" * 60)

        print(f"Welcome, {user['full_name']}")
        print(f"Student ID: {user['username']}")

        print("-" * 60)

        print("1. My Profile")
        print("2. View All Computers")
        print("3. View Available Computers")
        print("4. Start Lab Session")
        print("5. End Lab Session")
        print("6. My Current Session")
        print("7. Report Computer Issue")
        print("8. My Reported Issues")
        print("9. Logout")

        print("-" * 60)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            view_profile(user)

        elif choice == "2":

            view_computers()

        elif choice == "3":

            view_available_computers()

        elif choice == "4":

            start_lab_session(user)

        elif choice == "5":

            end_lab_session(user)

        elif choice == "6":

            view_current_session(user)

        elif choice == "7":

            report_issue(user)

        elif choice == "8":

            view_my_issues(user)

        elif choice == "9":

            print("\nLogging out...")

            return

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\nStudent Dashboard module loaded successfully.")

    print(
        "This file should normally be opened "
        "through auth.py."
    )