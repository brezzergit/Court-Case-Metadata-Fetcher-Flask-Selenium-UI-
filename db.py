import sqlite3
import os

DB_FILE = "queries.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                raw_html TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

def log_query(case_type, case_number, filing_year, raw_html):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (case_type, case_number, filing_year, raw_html)
        VALUES (?, ?, ?, ?)
    """, (case_type, case_number, filing_year, raw_html))
    conn.commit()
    conn.close()