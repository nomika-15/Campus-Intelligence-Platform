import sqlite3


def create_database():

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        college_name TEXT,
        department TEXT,
        semester TEXT,
        placement_probability REAL,
        success_score REAL,
        profile_rating TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_student(
    student_name,
    college_name,
    department,
    semester,
    placement_probability,
    success_score,
    profile_rating
):

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (
        student_name,
        college_name,
        department,
        semester,
        placement_probability,
        success_score,
        profile_rating
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        college_name,
        department,
        semester,
        placement_probability,
        success_score,
        profile_rating
    ))

    conn.commit()
    conn.close()


def get_students():

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    conn.close()

    return rows


create_database()