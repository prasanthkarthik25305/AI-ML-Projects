import sys
import os
from flask import Blueprint, render_template, request

# Set up root path and fix import
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)

from agents import jd_summarizer, recruiter

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/process", methods=["POST"])
def process():
    from io import StringIO
    import subprocess

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    summary = "(No summary generated)"
    try:
        jd_file = request.files["jd"]
        cvs = request.files.getlist("cvs")

        data_dir = os.path.join(ROOT_DIR, "data")
        jd_dir = os.path.join(data_dir, "jds")
        cv_dir = os.path.join(data_dir, "cvs")

        os.makedirs(jd_dir, exist_ok=True)
        os.makedirs(cv_dir, exist_ok=True)

        jd_path = os.path.join(jd_dir, jd_file.filename)
        jd_file.save(jd_path)

        print(f"\n📄 Saved JD file: {jd_path}")

        for cv in cvs:
            path = os.path.join(cv_dir, cv.filename)
            cv.save(path)
            print(f"📄 Saved CV: {path}")

        # === Process JD ===
        if jd_file.filename.endswith(".xlsx"):
            print("\n🔁 Converting JD Excel to individual text files...")
            subprocess.run(["python", os.path.join(ROOT_DIR, "convert_jds.py"), jd_path], check=True)

            jd_texts = [f for f in os.listdir(jd_dir) if f.endswith(".txt")]
            if jd_texts:
                with open(os.path.join(jd_dir, jd_texts[0]), "r", encoding="utf-8") as f:
                    jd_text = f.read()

                summarizer = jd_summarizer.JDSummarizer()
                summary = summarizer.summarize(jd_text)
                print("\n✅ Sample JD Summary:")
                print(summary)
        else:
            print("\n⚠️ JD file is not Excel (.xlsx), skipping conversion.")
            with open(jd_path, "r", encoding="utf-8") as f:
                jd_text = f.read()

            summarizer = jd_summarizer.JDSummarizer()
            summary = summarizer.summarize(jd_text)
            print("\n✅ JD Summary:")
            print(summary)

        # === Run recruiter pipeline ===
        print("\n🚀 Starting AI Recruiter pipeline...")
        recruiter.process_resumes(cv_dir)
        print("\n✅ Pipeline Complete.")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        summary = "An error occurred during processing."

    finally:
        sys.stdout = old_stdout

    logs = mystdout.getvalue()
    return render_template("result.html", summary=summary, logs=logs)
