import sqlite3
from datetime import datetime

# Path to database file
DB_NAME = "data/fitness.db"


# ================== WORKOUT HISTORY TABLE ==================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        count INTEGER,
        calories REAL,
        duration INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_session(exercise, count, calories, duration):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO history(exercise, count, calories, duration, date)
    VALUES(?,?,?,?,?)
    """, (
        exercise,
        count,
        calories,
        duration,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM history ORDER BY id DESC")
    data = c.fetchall()

    conn.close()
    return data


# ================== USER PROFILE TABLE ==================

def init_profile():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        goal TEXT,
        bmi REAL
    )
    """)

    conn.commit()
    conn.close()


def save_profile(name, age, height, weight, goal, bmi):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Keep only one profile (simple system)
    c.execute("DELETE FROM profile")

    c.execute("""
    INSERT INTO profile(name, age, height, weight, goal, bmi)
    VALUES(?,?,?,?,?,?)
    """, (name, age, height, weight, goal, bmi))

    conn.commit()
    conn.close()


def get_profile():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM profile LIMIT 1")
    data = c.fetchone()

    conn.close()
    return data