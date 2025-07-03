# main.py

from agents.jd_summarizer import JDSummarizer
from agents import recruiter

def process_jd(file_path):
    with open(file_path, 'r') as f:
        jd_text = f.read()

    jd_agent = JDSummarizer()
    summary = jd_agent.summarize(jd_text)

    print("📄 JD Summary:")
    print(summary)

if __name__ == "__main__":
    # 1. Summarize a JD (optional preview)
    #process_jd("./data/jds")

    # 2. Run the full resume processing pipeline
    print("\n🔁 Starting Resume Processing...")
    recruiter.process_resumes()
