# agents/matcher.py
import os
import sqlite3
import json
import numpy as np
import fitz  # PyMuPDF
from tabulate import tabulate
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/job_embeddings.db"))


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"❌ Failed to extract text from {pdf_path}: {e}")
        return ""

def generate_embedding(text):
    return model.encode(text).tolist()

def get_all_job_embeddings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, filename, embedding FROM job_descriptions")
    rows = cursor.fetchall()
    conn.close()

    jobs = []
    for row in rows:
        job_id, role, filename, embedding_str = row
        embedding = None
        try:
          embedding = json.loads(embedding_str)
          if not isinstance(embedding, list):
             embedding = None
        except Exception as e:
            embedding = None

        jobs.append({
            "id": job_id,
            "role": role,
            "filename": filename,
            "embedding": embedding
        })
    return jobs

def cosine_similarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def match_single_resume(resume_path, top_k=5):
    filename = os.path.basename(resume_path)
    print("\n" + "=" * 80)
    print(f"📄 Matching for Resume: {filename}")
    print("=" * 80)

    print(f"\n📂 Scanning resume: {resume_path}")
    resume_text = extract_text_from_pdf(resume_path)

    if not resume_text.strip():
        print("❌ No text extracted from resume.")
        return []

    print("🧾 Extracted text (first 300 chars):")
    print(resume_text[:300] + "...")

    top_matches = match_resume_to_jobs(resume_text, top_k)

    if top_matches:
        print("\n🎯 Top Job Matches for:", filename)
        table = [(role, job_file, f"{float(score):.4f}") for score, role, job_file in top_matches]
        print(tabulate(table, headers=["Role", "Job File", "Score"], tablefmt="fancy_grid"))
    else:
        print("❌ No good matches found for this resume.")

    return top_matches


def match_resume_to_jobs(resume_text, top_k=5):
    print("📥 Generating embedding for resume text...")
    resume_embedding = generate_embedding(resume_text)
    
    if not resume_embedding:
        print("⚠️ Could not generate embedding for resume.")
        return []
    
    print(f"🔢 Resume embedding length: {len(resume_embedding)}")

    jobs = get_all_job_embeddings()
    scored_jobs = []

    for job in jobs:
        if job["embedding"] is None:
           # print(f"⚠️ Skipping job with no embedding: {job['role']}")
            continue
        
        if len(job["embedding"]) != len(resume_embedding):
            #print(f"❌ Embedding length mismatch for {job['role']}: Resume={len(resume_embedding)}, Job={len(job['embedding'])}")
            continue

        score = cosine_similarity(resume_embedding, job["embedding"])
       # print(f"🔍 Match Score with {job['role']} ({job['filename']}): {round(score, 4)}")
        scored_jobs.append((score, job["role"], job["filename"]))

    scored_jobs.sort(reverse=True)

    if not scored_jobs:
        print("❌ No matches found.")
    else:
        print("✅ Matches found.")

    return scored_jobs[:top_k]

def match_all_resumes(resume_folder="data/cvs"):
    print(f"\n📂 Scanning resumes in: {resume_folder}")
    resumes = [f for f in os.listdir(resume_folder) if f.endswith(".pdf") and f[0].lower() == 'c' and f[1:5].isdigit()]
    
    if not resumes:
        print("❌ No resumes found.")
        return

    print(f"📝 Resumes found: {resumes}")

    for file in resumes:
        print("\n" + "="*80)
        print(f"📄 Matching for Resume: {file}")
        print("="*80)

        pdf_path = os.path.join(resume_folder, file)
        resume_text = extract_text_from_pdf(pdf_path)
        
        if not resume_text.strip():
            print("❌ No text extracted from resume.")
            continue

        print("🧾 Extracted text (first 300 chars):")
        print(resume_text[:300] + "...")
        
        top_matches = match_resume_to_jobs(resume_text)

        if top_matches:
            print("\n🎯 Top Job Matches for:", file)
            table = [(role, filename, f"{float(score):.4f}") for score, role, filename in top_matches]
            print(tabulate(table, headers=["Role", "Job File", "Score"], tablefmt="fancy_grid"))
        else:
            print("❌ No good matches found for this resume.")

    print("\n✅ All resumes processed.")


if __name__ == "__main__":
     match_all_resumes()

