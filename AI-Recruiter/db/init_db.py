# db/init_db.py
import sqlite3
import os
def init_db(db_path="data/job_embeddings.db"):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        role TEXT,
        skills TEXT,
        qualifications TEXT,
        experience TEXT,
        responsibilities TEXT,
        embedding BLOB
    )
    """)

    conn.commit()
    conn.close()
    print("✅ SQLite database and table created.")
