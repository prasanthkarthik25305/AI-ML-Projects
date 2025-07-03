import sqlite3

# Path to your database file
db_path = "data/job_embeddings.db"  # or ai_recruiter.db

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📋 Tables in the database:")
for table in tables:
    print(f"  - {table[0]}")

# Optional: Show columns in 'job_descriptions' table
if any("job_descriptions" in t for t in tables):
    print("\n🔍 Columns in job_descriptions:")
    cursor.execute("PRAGMA table_info(job_descriptions);")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

conn.close()
