import sqlite3
import pandas as pd

DB_NAME = "results.db"


def init_db():
    """Database aur table create karta hai agar exist nahi karta"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            maths INTEGER NOT NULL,
            physics INTEGER NOT NULL,
            chemistry INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_student(roll, name, maths, physics, chemistry):
    """Naya student add karta hai. Return: (success, message)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (roll, name, maths, physics, chemistry) VALUES (?, ?, ?, ?, ?)",
            (roll, name, maths, physics, chemistry)
        )
        conn.commit()
        conn.close()
        return True, f"Record added: {roll} | {name}"
    except sqlite3.IntegrityError:
        return False, f"(a) Roll number {roll} already exists."
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_all_students():
    """Saare students Pandas DataFrame mein return karta hai"""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df


def get_ranked_students():
    """SQL query se rank nikalta hai (Total descending)"""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT roll, name, maths, physics, chemistry,
               (maths + physics + chemistry) AS total
        FROM students
        ORDER BY total DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df