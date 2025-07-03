# agents/shortlister.py
import os
import sqlite3

THRESHOLD = 0.35  # You can adjust this threshold as needed

class Shortlister:
    def __init__(self, db_path=None):
         if db_path is None:
             db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/ai_recruiter.db"))
             self.conn = sqlite3.connect(db_path)
             self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS shortlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            resume_path TEXT,
            matched_job TEXT,
            match_score REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def shortlist(self, resume_filename, matched_jobs, candidate_name):
        """
        Filters and stores matches above threshold into the database.

        Parameters:
            - resume_filename: str → Path to the resume file
            - matched_jobs: List of tuples (score, role, jd_filename)
            - candidate_name: str → Extracted from the resume
        Returns:
            - shortlisted: List of jobs above the threshold
        """
        print(f"\n🧮 Shortlisting jobs for: {resume_filename}")
        shortlisted = []

        for score, role, jd_file in matched_jobs:
            if score >= THRESHOLD:
                self.conn.execute("""
                    INSERT INTO shortlist (candidate_name, resume_path, matched_job, match_score)
                    VALUES (?, ?, ?, ?)""",
                    (candidate_name, resume_filename, role, score))
                shortlisted.append((score, role, jd_file))

        self.conn.commit()

        if not shortlisted:
            print("⚠️ No matches passed the shortlisting threshold.")
        else:
            print(f"✅ {len(shortlisted)} jobs shortlisted with score >= {THRESHOLD}.")

        return shortlisted

