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
    import shutil

    # helper to clear directories
    def clear_directory(path):
        if os.path.exists(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as del_err:
                    print(f"❌ Failed to delete {file_path}: {del_err}")

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    summary = "(No summary generated)"
    try:
        # 1) Save uploads
        jd_file = request.files["jd"]
        cvs    = request.files.getlist("cvs")

        data_dir = os.path.join(ROOT_DIR, "data")
        jd_dir   = os.path.join(data_dir, "jds")
        cv_dir   = os.path.join(data_dir, "cvs")

        # Ensure folders exist
        os.makedirs(jd_dir, exist_ok=True)
        os.makedirs(cv_dir, exist_ok=True)

        # Clear old uploads
        clear_directory(jd_dir)
        clear_directory(cv_dir)

        # Now save the new uploads
        jd_path = os.path.join(jd_dir, jd_file.filename)
        jd_file.save(jd_path)
        print(f"📄 Saved JD file: {jd_path}")

        for cv in cvs:
            path = os.path.join(cv_dir, cv.filename)
            cv.save(path)
            print(f"📄 Saved CV: {path}")

        # 2) Convert all JDs in data/jds → .txt
        print("🔁 Converting all uploaded JDs to .txt files…")
        subprocess.run(
            ["python", os.path.join(ROOT_DIR, "convert_jds.py")],
            check=True
        )

        # 3) Summarize the first .txt that appears
        txt_files = sorted([f for f in os.listdir(jd_dir) if f.endswith(".txt")])
        if not txt_files:
            raise RuntimeError("No .txt files found after conversion.")
        first_txt = os.path.join(jd_dir, txt_files[0])
        with open(first_txt, "r", encoding="utf-8") as f:
            jd_text = f.read()

        summarizer = jd_summarizer.JDSummarizer()
        summary = summarizer.summarize(jd_text)
        print("✅ JD Summary:")
        print(summary)

        # 4) Run the recruiter pipeline on exactly the CVs you uploaded
        print("🚀 Starting AI Recruiter pipeline…")
        recruiter.process_resumes(cv_dir)
        print("✅ Pipeline Complete.")

    except Exception as e:
        print(f"❌ Error occurred: {e}", file=sys.stderr)
        summary = "An error occurred during processing."

    finally:
        sys.stdout = old_stdout

    logs = mystdout.getvalue()
    return render_template("result.html", summary=summary, logs=logs)("result.html", summary=summary, logs=logs)
