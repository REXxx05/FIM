import sqlite3
from config import DATABASE_PATH
def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def initialize_database():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    # Table 1 — baseline snapshot of all files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baseline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL,
            size INTEGER NOT NULL,
            modified_time REAL NOT NULL,
            permissions TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    # Table 2 — log of every detected change
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            filepath TEXT NOT NULL,
            old_hash TEXT,
            new_hash TEXT,
            alert_level TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")
def save_baseline(filepath, hash, size, modified_time, permissions):
    """Save or update a file in the baseline."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO baseline (filepath, hash, size, modified_time, permissions)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(filepath) DO UPDATE SET
            hash = excluded.hash,
            size = excluded.size,
            modified_time = excluded.modified_time,
            permissions = excluded.permissions,
            created_at = datetime('now')
    """, (filepath, hash, size, modified_time, permissions))
    conn.commit()
    conn.close()
def get_baseline():
    """Return all files in the baseline as a dictionary."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM baseline")
    rows = cursor.fetchall()
    conn.close()
    # Return as dict keyed by filepath for fast lookup
    return {row["filepath"]: dict(row) for row in rows}
def log_event(event_type, filepath, old_hash, new_hash, alert_level):
    """Log a detected change to the events table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (event_type, filepath, old_hash, new_hash, alert_level)
        VALUES (?, ?, ?, ?, ?)
    """, (event_type, filepath, old_hash, new_hash, alert_level))
    conn.commit()
    conn.close()
def get_events(limit=50):
    """Return the most recent events."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
if __name__ == "__main__":
    initialize_database()


