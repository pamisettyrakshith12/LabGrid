import sqlite3
import hashlib
import re
from student_dashboard import student_dashboard
from faculty_dashboard import faculty_dashboard
from technician_dashboard import technician_dashboard
from admin_dashboard import admin_dashboard
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
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# STUDENT ID VALIDATION
# ============================================================

STUDENT_ID_PATTERN = (
    r"^cb\.sc\.u4cse"
    r"(23|24|25|26)"
    r"[0-7]"
    r"(0[1-9]|[1-5][0-9]|6[0-8])$"
)


def validate_student_id(student_id):
    return re.match(STUDENT_ID_PATTERN, student_id) is not None


# ============================================================
# EXTRACT STUDENT DETAILS
# ============================================================

def extract_student_details(student_id):

    if not validate_student_id(student_id):
        raise ValueError("Invalid student ID")

    # Example:
    # cb.sc.u4cse24035
    #
    # batch   = 24
    # section = 0
    # roll    = 35

    batch = student_id[11:13]

    section = int(student_id[13])

    roll = int(student_id[14:])

    return batch, section, roll


# ============================================================
# SECTION NAME
# ============================================================

def get_section_name(section):

    sections = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H"
    }

    return sections.get(section, "Unknown")


# ============================================================
# YEAR CALCULATION
# ============================================================

def get_year(batch):

    years = {
        "23": "4th Year",
        "24": "3rd Year",
        "25": "2nd Year",
        "26": "1st Year"
    }

    return years.get(batch, "Unknown")


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(password, stored_hash):

    return hash_password(password) == stored_hash


# ============================================================
# STUDENT LOGIN
# ============================================================

def student_login(username, password):

    if not validate_student_id(username):

        print("\nInvalid student ID format.")

        return None

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            password_hash,
            full_name,
            role,
            batch,
            section
        FROM users
        WHERE username = ?
          AND role = 'student'
    """, (username,))

    student = cursor.fetchone()

    conn.close()

    if student is None:

        print("\nStudent account not found.")

        return None

    (
        user_id,
        db_username,
        stored_hash,
        full_name,
        role,
        batch,
        section
    ) = student

    if not verify_password(password, stored_hash):

        print("\nIncorrect password.")

        return None

    roll = int(username[14:])

    print("\n" + "=" * 50)
    print("           STUDENT LOGIN SUCCESSFUL")
    print("=" * 50)

    print(f"Name     : {full_name}")
    print(f"Username : {db_username}")
    print(f"Role     : {role}")
    print(f"Batch    : {batch}")
    print(f"Year     : {get_year(batch)}")
    print(f"Section  : {get_section_name(section)}")
    print(f"Roll No  : {roll}")

    print("=" * 50)

    return {
        "id": user_id,
        "username": db_username,
        "full_name": full_name,
        "role": role,
        "batch": batch,
        "section": section,
        "section_name": get_section_name(section),
        "year": get_year(batch),
        "roll": roll
    }


# ============================================================
# STAFF LOGIN
# ============================================================

def staff_login(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            password_hash,
            full_name,
            role
        FROM users
        WHERE username = ?
          AND role IN (
              'faculty',
              'technician',
              'admin'
          )
    """, (username,))

    staff = cursor.fetchone()

    conn.close()

    if staff is None:

        print("\nStaff account not found.")

        return None

    (
        user_id,
        db_username,
        stored_hash,
        full_name,
        role
    ) = staff

    if not verify_password(password, stored_hash):

        print("\nIncorrect password.")

        return None

    print("\n" + "=" * 50)
    print("             LOGIN SUCCESSFUL")
    print("=" * 50)

    print(f"Name     : {full_name}")
    print(f"Username : {db_username}")
    print(f"Role     : {role}")

    print("=" * 50)

    return {
        "id": user_id,
        "username": db_username,
        "full_name": full_name,
        "role": role
    }


# ============================================================
# GENERAL LOGIN
# ============================================================

def login(username, password):

    username = username.strip()

    # --------------------------------------------------------
    # Student Login
    # --------------------------------------------------------

    if username.startswith("cb.sc.u4cse"):

        return student_login(
            username,
            password
        )

    # --------------------------------------------------------
    # Faculty / Technician / Admin Login
    # --------------------------------------------------------

    return staff_login(
        username,
        password
    )


# ============================================================
# DASHBOARD SELECTION
# ============================================================

def open_dashboard(user):
    
    if user is None:
        return

    role = user["role"]

    if role == "student":
        student_dashboard(user)

    elif role == "faculty":
        faculty_dashboard(user)

    elif role == "technician":
        technician_dashboard(user)

    elif role == "admin":
        admin_dashboard(user)

    else:
        print("\nUnknown role.")

# ============================================================
# COMMAND LINE LOGIN
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("       COMPUTER LAB MANAGEMENT SYSTEM")
    print("                 LOGIN")
    print("=" * 50)

    username = input("Username : ").strip()

    password = input("Password : ").strip()

    user = login(
        username,
        password
    )

    if user:

        open_dashboard(user)

    else:

        print("\nLogin failed.")