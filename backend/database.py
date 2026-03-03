import sqlite3
from datetime import datetime

DB_NAME = "safespace.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        message TEXT,
        response TEXT,
        risk_level TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        risk_level TEXT,
        timestamp TEXT,
        alert_status TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_conversation(user_id, message, response, risk_level):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conversation_logs (user_id, message, response, risk_level, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, message, response, risk_level, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def log_emergency(user_id, risk_level, timestamp, alert_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO emergency_logs (user_id, risk_level, timestamp, alert_status)
    VALUES (?, ?, ?, ?)
    """, (user_id, risk_level, timestamp, alert_status))

    conn.commit()
    conn.close()