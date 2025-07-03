# agents/embedding_generator.py
import os
import sqlite3
import json
import hashlib
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

DB_PATH = "data/job_embeddings.db"
JD_FOLDER = "data/summaries"  # Make sure your files are in this folder


def compute_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS job_descriptions")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            filename TEXT UNIQUE,
            embedding TEXT,
            hash TEXT UNIQUE       
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ SQLite database and table created.")

def generate_embedding(text):
    return model.encode(text).tolist()

def store_embedding(role, filename, embedding, text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    jd_hash = compute_hash(text)
    cursor.execute('''
        INSERT OR IGNORE INTO job_descriptions (role, filename, embedding, hash)
        VALUES (?, ?, ?, ?)
    ''', (role, filename, json.dumps(embedding), jd_hash))
    conn.commit()
    conn.close()
    print(f"✅ Inserted embedding for {filename}")

def convert_structured_summary_to_text(data):
    role = data.get("Role", "Unknown Role")
    parts = []

    if isinstance(data.get("Required Skills"), list):
        parts.append("Required Skills: " + ", ".join(data["Required Skills"]))

    if isinstance(data.get("Experience"), list):
        parts.append("Experience: " + ". ".join(data["Experience"]))

    if isinstance(data.get("Responsibilities"), list):
        parts.append("Responsibilities: " + ". ".join(data["Responsibilities"]))

    if isinstance(data.get("Qualifications"), dict):
        for key, value in data["Qualifications"].items():
            if value:
                parts.append(f"{key}: {value}")

    combined_text = f"{role} | " + " | ".join(parts)
    return role, combined_text

def process_job_descriptions():
    for file in os.listdir(JD_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(JD_FOLDER, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    role, description = convert_structured_summary_to_text(data)
                    embedding = generate_embedding(description)
                    store_embedding(role, file, embedding, description)

                except Exception as e:
                    print(f"❌ Failed to process {file}: {e}")

if __name__ == "__main__":
    create_db()
    process_job_descriptions()

    # 🔍 Debug: Show how many were added
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM job_descriptions")
    count = cursor.fetchone()[0]
    print(f"🗂️ Total job descriptions in DB: {count}")
    conn.close()
