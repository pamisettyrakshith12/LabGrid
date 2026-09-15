import sqlite3
import hashlib
import re


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_NAME = "computer_lab.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


conn = get_connection()
cursor = conn.cursor()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# STUDENT ID CONFIGURATION
# ============================================================

STUDENT_ID_PATTERN = r"^cb\.sc\.u4cse(23|24|25|26)[0-7](0[1-9]|[1-5][0-9]|6[0-8])$"


def validate_student_id(student_id):
    return re.match(STUDENT_ID_PATTERN, student_id) is not None


def extract_student_details(student_id):

    if not validate_student_id(student_id):
        raise ValueError("Invalid student ID format")

    # Example:
    # cb.sc.u4cse24035
    #
    # c b . s c . u 4 c s e 2 4 0 3 5
    #
    # batch   = 24
    # section = 0
    # roll    = 35

    batch = student_id[11:13]
    section = int(student_id[13])
    roll_number = int(student_id[14:])

    return batch, section, roll_number


def generate_student_id(batch, section, roll_number):

    student_id = f"cb.sc.u4cse{batch}{section}{roll_number:02d}"

    if not validate_student_id(student_id):
        raise ValueError(f"Invalid generated student ID: {student_id}")

    return student_id


# ============================================================
# CREATE USERS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    full_name TEXT NOT NULL,

    role TEXT NOT NULL
        CHECK(role IN ('student', 'faculty', 'technician', 'admin')),

    batch TEXT,

    section INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        role != 'student'
        OR (
            batch IN ('23', '24', '25', '26')
            AND section BETWEEN 0 AND 7
        )
    )
)
""")


# ============================================================
# CREATE LABS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS labs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    lab_name TEXT NOT NULL UNIQUE,

    building TEXT NOT NULL,

    floor INTEGER NOT NULL,

    total_computers INTEGER NOT NULL
        CHECK(total_computers > 0)
)
""")


# ============================================================
# CREATE COMPUTERS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS computers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    lab_id INTEGER NOT NULL,

    computer_name TEXT NOT NULL UNIQUE,

    processor TEXT NOT NULL,

    ram TEXT NOT NULL,

    storage TEXT NOT NULL,

    operating_system TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'AVAILABLE'
        CHECK(
            status IN (
                'AVAILABLE',
                'IN_USE',
                'UNDER_MAINTENANCE',
                'OUT_OF_SERVICE'
            )
        ),

    FOREIGN KEY (lab_id)
        REFERENCES labs(id)
        ON DELETE CASCADE
)
""")


# ============================================================
# CREATE ISSUES TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS issues (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    computer_id INTEGER NOT NULL,

    reported_by INTEGER NOT NULL,

    assigned_to INTEGER,

    title TEXT NOT NULL,

    description TEXT,

    priority TEXT NOT NULL DEFAULT 'MEDIUM'
        CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),

    status TEXT NOT NULL DEFAULT 'OPEN'
        CHECK(
            status IN (
                'OPEN',
                'IN_PROGRESS',
                'RESOLVED',
                'CLOSED'
            )
        ),

    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    resolved_at TIMESTAMP,

    FOREIGN KEY (computer_id)
        REFERENCES computers(id)
        ON DELETE CASCADE,

    FOREIGN KEY (reported_by)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (assigned_to)
        REFERENCES users(id)
        ON DELETE SET NULL
)
""")


# ============================================================
# CREATE MAINTENANCE TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    computer_id INTEGER NOT NULL,

    issue_id INTEGER,

    technician_id INTEGER NOT NULL,

    action_taken TEXT NOT NULL,

    maintenance_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    remarks TEXT,

    FOREIGN KEY (computer_id)
        REFERENCES computers(id)
        ON DELETE CASCADE,

    FOREIGN KEY (issue_id)
        REFERENCES issues(id)
        ON DELETE SET NULL,

    FOREIGN KEY (technician_id)
        REFERENCES users(id)
        ON DELETE CASCADE
)
""")


# ============================================================
# CREATE SOFTWARE TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS software (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    software_name TEXT NOT NULL UNIQUE,

    version TEXT NOT NULL,

    license_type TEXT NOT NULL
)
""")


# ============================================================
# CREATE COMPUTER_SOFTWARE TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS computer_software (

    computer_id INTEGER NOT NULL,

    software_id INTEGER NOT NULL,

    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (computer_id, software_id),

    FOREIGN KEY (computer_id)
        REFERENCES computers(id)
        ON DELETE CASCADE,

    FOREIGN KEY (software_id)
        REFERENCES software(id)
        ON DELETE CASCADE
)
""")


# ============================================================
# CREATE LAB_SESSIONS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS lab_sessions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,

    computer_id INTEGER NOT NULL,

    lab_id INTEGER NOT NULL,

    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    logout_time TIMESTAMP,

    purpose TEXT,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (computer_id)
        REFERENCES computers(id)
        ON DELETE CASCADE,

    FOREIGN KEY (lab_id)
        REFERENCES labs(id)
        ON DELETE CASCADE
)
""")


# ============================================================
# INSERT USER FUNCTIONS
# ============================================================

def insert_student(full_name, batch, section, roll_number):

    student_id = generate_student_id(
        batch,
        section,
        roll_number
    )

    password = f"{batch}{section}{roll_number:02d}"

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            username,
            password_hash,
            full_name,
            role,
            batch,
            section
        )
        VALUES (?, ?, ?, 'student', ?, ?)
    """, (
        student_id,
        password_hash,
        full_name,
        batch,
        section
    ))


def insert_faculty(full_name, username):

    password = "faculty123"

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            username,
            password_hash,
            full_name,
            role
        )
        VALUES (?, ?, ?, 'faculty')
    """, (
        username,
        hash_password(password),
        full_name
    ))


def insert_technician(full_name, username):

    password = "tech123"

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            username,
            password_hash,
            full_name,
            role
        )
        VALUES (?, ?, ?, 'technician')
    """, (
        username,
        hash_password(password),
        full_name
    ))


def insert_admin(full_name, username):

    password = "admin123"

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            username,
            password_hash,
            full_name,
            role
        )
        VALUES (?, ?, ?, 'admin')
    """, (
        username,
        hash_password(password),
        full_name
    ))


# ============================================================
# INSERT FACULTY
# ============================================================

faculty_members = [

    ("Dhaniya", "faculty_dhaniya"),

    ("Vidya", "faculty_vidya"),

    ("Raghesh", "faculty_raghesh"),

    ("Vandhana", "faculty_vandhana"),

    ("Senthil Kumar", "faculty_senthilkumar"),

    ("Radhika", "faculty_radhika"),

    ("Arjun PK", "faculty_arjunpk"),

    ("Anantha Narayana", "faculty_ananthanarayana"),

    ("Jeykumar", "faculty_jeykumar"),

    ("Uma", "faculty_uma")
]


for full_name, username in faculty_members:

    insert_faculty(
        full_name,
        username
    )


# ============================================================
# INSERT TECHNICIANS
# ============================================================

technicians = [

    ("Varun Bramha", "tech_varun"),

    ("Vikranth", "tech_vikranth"),

    ("Jeevan", "tech_jeevan"),

    ("Rakesh Uchiha", "tech_rakesh"),

    ("Parineethi", "tech_parineethi"),

    ("Sowya", "tech_sowya"),

    ("Varshini", "tech_varshini")
]


for full_name, username in technicians:

    insert_technician(
        full_name,
        username
    )


# ============================================================
# INSERT ADMINS
# ============================================================

admins = [

    ("Rakshith", "admin"),

    ("P.R", "pr"),

    ("Pruthve", "pruthve")
]


for full_name, username in admins:

    insert_admin(
        full_name,
        username
    )


# ============================================================
# STUDENT COUNTS
# ============================================================

student_counts = {

    "23": {
        0: 64,
        1: 67,
        2: 61,
        3: 66,
        4: 63,
        5: 68,
        6: 65,
        7: 62
    },

    "24": {
        0: 66,
        1: 64,
        2: 68,
        3: 62,
        4: 65,
        5: 67,
        6: 63,
        7: 60
    },

    "25": {
        0: 63,
        1: 65,
        2: 61,
        3: 67,
        4: 64,
        5: 66,
        6: 62,
        7: 60
    },

    "26": {
        0: 65,
        1: 63,
        2: 66,
        3: 62,
        4: 64,
        5: 68,
        6: 61,
        7: 60
    }
}


# ============================================================
# INSERT STUDENTS
# ============================================================

for batch, sections in student_counts.items():

    for section, total_students in sections.items():

        for roll_number in range(1, total_students + 1):

            full_name = (
                f"Student "
                f"{batch}-"
                f"{chr(65 + section)}-"
                f"{roll_number}"
            )

            insert_student(
                full_name,
                batch,
                section,
                roll_number
            )


# ============================================================
# INSERT LABS
# ============================================================

labs = [

    ("PG Lab", "AB3", 2, 68),

    ("CP Lab 1", "AB3", 3, 65),

    ("CP Lab 2", "AB3", 3, 67),

    ("Hardware Lab", "AB3", 2, 70),

    ("IT Lab 1", "AB2", 0, 70),

    ("IT Lab 2", "AB2", 0, 69),

    ("IT Lab 3", "AB2", 1, 68)
]


for lab_name, building, floor, total_computers in labs:

    cursor.execute("""
        INSERT OR IGNORE INTO labs
        (
            lab_name,
            building,
            floor,
            total_computers
        )
        VALUES (?, ?, ?, ?)
    """, (
        lab_name,
        building,
        floor,
        total_computers
    ))


# ============================================================
# COMPUTER CONFIGURATION
# ============================================================

computer_config = [

    ("PG Lab", "PG-LAB-PC", 68),

    ("CP Lab 1", "CP1-PC", 65),

    ("CP Lab 2", "CP2-PC", 67),

    ("Hardware Lab", "HW-PC", 70),

    ("IT Lab 1", "IT1-PC", 70),

    ("IT Lab 2", "IT2-PC", 69),

    ("IT Lab 3", "IT3-PC", 68)
]


# ============================================================
# INSERT COMPUTERS
# ============================================================

for lab_name, prefix, total in computer_config:

    cursor.execute("""
        SELECT id
        FROM labs
        WHERE lab_name = ?
    """, (lab_name,))

    lab = cursor.fetchone()

    if lab is None:
        continue

    lab_id = lab[0]

    for number in range(1, total + 1):

        computer_name = f"{prefix}{number:02d}"

        cursor.execute("""
            INSERT OR IGNORE INTO computers
            (
                lab_id,
                computer_name,
                processor,
                ram,
                storage,
                operating_system,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, 'AVAILABLE')
        """, (
            lab_id,
            computer_name,
            "Intel Core i5",
            "16GB",
            "512GB",
            "Windows 11"
        ))


# ============================================================
# INSERT SOFTWARE
# ============================================================

software_list = [

    ("VS Code", "1.100", "Free"),

    ("Ubuntu", "24.04 LTS", "Open Source"),

    ("Keil uVision", "5", "Educational"),

    ("Jupyter Notebook", "7", "Open Source"),

    ("Cisco Packet Tracer", "8.2", "Educational"),

    ("MATLAB", "2025", "Educational"),

    ("IDLE", "3.13", "Open Source"),

    ("MySQL", "8.0", "Open Source"),

    ("Code::Blocks", "25.03", "Open Source"),

    ("Eclipse", "2025", "Open Source")
]


for software_name, version, license_type in software_list:

    cursor.execute("""
        INSERT OR IGNORE INTO software
        (
            software_name,
            version,
            license_type
        )
        VALUES (?, ?, ?)
    """, (
        software_name,
        version,
        license_type
    ))


# ============================================================
# SOFTWARE DISTRIBUTION BY LAB
# ============================================================

software_distribution = {

    "PG Lab": [

        "VS Code",
        "Ubuntu",
        "Keil uVision",
        "IDLE",
        "MySQL",
        "Eclipse"
    ],

    "CP Lab 1": [

        "VS Code",
        "Ubuntu",
        "Keil uVision",
        "Jupyter Notebook",
        "Cisco Packet Tracer",
        "MySQL",
        "Code::Blocks"
    ],

    "CP Lab 2": [

        "VS Code",
        "Ubuntu",
        "Jupyter Notebook",
        "Cisco Packet Tracer",
        "MySQL",
        "Code::Blocks"
    ],

    "Hardware Lab": [

        "VS Code",
        "Ubuntu",
        "Keil uVision",
        "MATLAB",
        "IDLE",
        "Eclipse"
    ],

    "IT Lab 1": [

        "VS Code",
        "Ubuntu",
        "Jupyter Notebook",
        "MATLAB",
        "IDLE",
        "Code::Blocks",
        "Eclipse"
    ],

    "IT Lab 2": [

        "VS Code",
        "Ubuntu",
        "Jupyter Notebook",
        "MATLAB",
        "IDLE",
        "Code::Blocks",
        "Eclipse"
    ],

    "IT Lab 3": [

        "VS Code",
        "Ubuntu",
        "Jupyter Notebook",
        "MATLAB",
        "IDLE",
        "Code::Blocks"
    ]
}


# ============================================================
# INSTALL SOFTWARE ON COMPUTERS
# ============================================================

for lab_name, software_names in software_distribution.items():

    cursor.execute("""
        SELECT id
        FROM labs
        WHERE lab_name = ?
    """, (lab_name,))

    lab = cursor.fetchone()

    if lab is None:
        continue

    lab_id = lab[0]

    cursor.execute("""
        SELECT id
        FROM computers
        WHERE lab_id = ?
    """, (lab_id,))

    computers = cursor.fetchall()

    for (computer_id,) in computers:

        for software_name in software_names:

            cursor.execute("""
                SELECT id
                FROM software
                WHERE software_name = ?
            """, (software_name,))

            software = cursor.fetchone()

            if software is None:
                continue

            software_id = software[0]

            cursor.execute("""
                INSERT OR IGNORE INTO computer_software
                (
                    computer_id,
                    software_id
                )
                VALUES (?, ?)
            """, (
                computer_id,
                software_id
            ))


# ============================================================
# INSERT SAMPLE ISSUE
# ============================================================

cursor.execute("""
    SELECT id
    FROM users
    WHERE username = ?
""", ("cb.sc.u4cse24001",))

student = cursor.fetchone()


cursor.execute("""
    SELECT id
    FROM computers
    WHERE computer_name = ?
""", ("PG-LAB-PC01",))

computer = cursor.fetchone()


cursor.execute("""
    SELECT id
    FROM users
    WHERE username = ?
      AND role = 'technician'
""", ("tech_varun",))

technician = cursor.fetchone()


if student and computer and technician:

    student_id = student[0]

    computer_id = computer[0]

    technician_id = technician[0]

    cursor.execute("""
        SELECT id
        FROM issues
        WHERE title = ?
          AND computer_id = ?
    """, (
        "Keyboard not working",
        computer_id
    ))

    existing_issue = cursor.fetchone()

    if existing_issue is None:

        cursor.execute("""
            INSERT INTO issues
            (
                computer_id,
                reported_by,
                assigned_to,
                title,
                description,
                priority,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            computer_id,
            student_id,
            technician_id,
            "Keyboard not working",
            "Some keyboard keys are not responding.",
            "HIGH",
            "IN_PROGRESS"
        ))

        issue_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO maintenance
            (
                computer_id,
                issue_id,
                technician_id,
                action_taken,
                remarks
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            computer_id,
            issue_id,
            technician_id,
            "Keyboard checked and faulty keys repaired.",
            "Computer is currently under maintenance."
        ))

        cursor.execute("""
            UPDATE computers
            SET status = 'UNDER_MAINTENANCE'
            WHERE id = ?
        """, (computer_id,))


# ============================================================
# COMMIT DATABASE
# ============================================================

conn.commit()


# ============================================================
# DATABASE SUMMARY
# ============================================================

print("\n" + "=" * 55)
print("       COMPUTER LAB MANAGEMENT SYSTEM")
print("       DATABASE INITIALIZATION COMPLETE")
print("=" * 55)


cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role = 'student'
""")
student_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role = 'faculty'
""")
faculty_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role = 'technician'
""")
technician_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role = 'admin'
""")
admin_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM labs
""")
lab_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM computers
""")
computer_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM software
""")
software_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM issues
""")
issue_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM maintenance
""")
maintenance_count = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM lab_sessions
""")
session_count = cursor.fetchone()[0]


print(f"Students       : {student_count}")
print(f"Faculty        : {faculty_count}")
print(f"Technicians    : {technician_count}")
print(f"Admins         : {admin_count}")
print(f"Labs           : {lab_count}")
print(f"Computers      : {computer_count}")
print(f"Software       : {software_count}")
print(f"Issues         : {issue_count}")
print(f"Maintenance    : {maintenance_count}")
print(f"Lab Sessions   : {session_count}")

print("=" * 55)


# ============================================================
# LAB SUMMARY
# ============================================================

print("\nLAB DETAILS")
print("-" * 55)

cursor.execute("""
    SELECT
        lab_name,
        building,
        floor,
        total_computers
    FROM labs
    ORDER BY id
""")

for lab in cursor.fetchall():

    print(
        f"{lab[0]:20} "
        f"{lab[1]:5} "
        f"Floor {lab[2]:<2} "
        f"Computers: {lab[3]}"
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("\nDatabase connection closed.")
print("Database is ready to use.")