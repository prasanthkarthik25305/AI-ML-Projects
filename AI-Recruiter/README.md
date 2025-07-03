# 🤖 AI Recruiter - On-Prem Multi-Agent AI Recruitment Assistant

**AI Recruiter** is a fully on-premise, privacy-focused recruitment automation system powered by **Ollama LLMs**, **embedding models**, and a **multi-agent architecture**. It automates job description analysis, candidate CV matching, shortlisting, and interview scheduling — all while keeping your data local and secure.

---

## 🧠 System Architecture

```text
┌────────────┐
│ Job Inputs │
└─────┬──────┘
      ▼
┌────────────────────────────┐
│   JD Summarizer Agent      │
│  (Extracts role, skills)   │
└─────┬──────────────────────┘
      ▼
┌────────────────────────────┐
│       Jobs Database        │
└─────┬──────────────────────┘
      ▼
┌────────────────────────────┐        ┌──────────────────────┐
│     Recruiting Agent       │◀───────│   Candidate CVs      │
│ - CV Parsing               │        └──────────────────────┘
│ - Info Extraction (LLM)    │
└─────┬──────────────────────┘
      ▼
┌──────────────────────────────┐
│ Embedding + Matching Agent   │
│  - Generates vector embeddings│
│  - Calculates similarity      │
└─────┬─────────────────────────┘
      ▼
┌──────────────────────────────┐
│      Shortlister Agent       │
│ - Filters candidates ≥ 80%   │
└─────┬────────────────────────┘
      ▼
┌──────────────────────────────┐
│  Interview Scheduler Agent   │
│ - Suggests time slots        │
│ - Sends email notifications  │
└──────────────────────────────┘

---

### 💡 Key Features – AI Recruiter

| 🧠 Agent | ✨ Capability |
|---------|---------------|
| 🧾 **JD Summarizer Agent** | Extracts **role**, **skills**, **qualifications**, and **responsibilities** from job descriptions using local LLMs via **Ollama**. |
| 📄 **Recruiting Agent** | Parses CVs using a hybrid of **traditional parsers** (`pdfplumber`, `python-docx`) and **LLM-based info extraction**. |
| 🧠 **Matching Agent** | Embeds JD and CV data using **Ollama embedding models**, then matches them using **cosine similarity**. |
| 📊 **Shortlister Agent** | Selects **top candidates** based on a **match score threshold** (e.g., ≥ 80%). |
| 📅 **Interview Scheduler Agent** | Crafts **personalized emails** using LLMs and sends them via **SMTP** or logs them for offline review. |
| 💽 **SQLite Memory** | Manages structured data for **JDs**, **candidate profiles**, **scores**, and **agent states** in a local database. |
| 🔐 **Privacy-First** | Entire system runs **locally**. No cloud. No leaks. 100% **on-prem** AI recruiting. |

---

## ⚙️ Tech Stack Overview

| 🧩 Component           | 🔧 Stack / Technology                           |
|------------------------|------------------------------------------------|
| 🧠 LLMs & Embeddings   | [**Ollama**](https://ollama.com) (Local LLMs & Embeddings) |
| 🧑‍💼 Multi-Agent Control | Modular, custom-built **Python framework**      |
| 📄 CV Parsing          | `pdfplumber`, `python-docx`, + ML-based NER    |
| 📊 Matching Logic      | **Vector Embedding + Cosine Similarity**       |
| 🗃️ Storage             | **SQLite** – Lightweight, local-first DB       |
| 📅 Scheduling & Email  | **SMTP (via smtplib)** or **offline logging**  |
| 🔌 Add-ons             | Web scraping modules, plug-in friendly design  |

---

## ✨ Benefits

- ✅ **Modular Agents** – Easily customizable or extendable for different workflows.
- 🚀 **Fully Local** – Secure, fast, and no internet dependency.
- 🧠 **LLM-Powered** – Accurate parsing and intelligent candidate matching.
- 📧 **Email Automation** – Interview emails that feel *personal*, not robotic.
- 💡 **Insightful Filtering** – Shortlists only the best-fit candidates.

Sure! Here's your **🚀 Installation & Setup** section rewritten in clean and professional **README.md** format, with improved clarity, formatting, and consistent styling:

---

```markdown
## 🚀 Installation & Setup

Follow these steps to get the AI Recruiter up and running locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-recruiter.git
cd ai-recruiter
```

---

### 2️⃣ Install Dependencies

Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Start Ollama Locally

Install [Ollama](https://ollama.com) if you haven’t already.

Pull and run the required models:

```bash
ollama run llama2             # For LLM-based tasks
ollama run nomic-embed-text   # For embedding-based matching
```

---

### 4️⃣ Initialize the Database

Set up the SQLite database with required tables:

```bash
python db/init_db.py
```

---

### 5️⃣ (Optional) Convert Raw Job Descriptions

Pre-process job descriptions before feeding them into the pipeline:

```bash
python convert_jds.py
```

---

### ▶️ Run the Full Pipeline

Run the main pipeline with a job description and a folder of candidate CVs:

```bash
python main.py --jd ./data/jds/jd1.txt --cvs ./data/cvs/
```

---

### ⚙️ Run Individual Agents (Optional)

You can also run specific agents for testing or modular development:

```bash
# Recruiter Agent
python -m agents.recruiter

# Embedding Matcher Agent
python -m agents.matcher

# Shortlister Agent
python -m agents.shortlister

# Interview Scheduler Agent
python -m agents.scheduler
```

---

### ✅ You're Ready to Go!

Your AI-powered recruiter is now set up and ready to parse, match, and schedule candidates — all locally and privately.
```

Let me know if you'd like a version of this in a **PowerPoint-friendly format** as well!
## 📁 Project Structure

```text
ai-recruiter/
├── agents/
│   ├── embedding_generator.py
│   ├── jd_summarizer.py
│   ├── recruiter.py
│   ├── matcher.py
│   ├── shortlister.py
│   └── scheduler.py
│
├── data/
│   ├── cvs/
│   ├── jds/
│   ├── summaries/
│   ├── ai_recruiter.db
│   └── job_embeddings.db
│
├── db/
│   └── init_db.py
│
├── tools/
│   ├── cv_parser.py
│   ├── emailer.py
│   ├── embedding_client.py
│   ├── llm_client.py
│   ├── ml_model.py
│   └── web_scraper.py
│
├── utils/
│   └── prompt_templates.py
│
├── convert_jds.py
├── job_description.csv
├── main.py
├── README.md
└── requirements.txt
---

## 🧠 Matching Logic (Sample)

```python
def calculate_match_score(jd_embed, candidate_embed):
    return cosine_similarity(jd_embed, candidate_embed)
```

> Candidates with score ≥ 0.8 are shortlisted.

---

## 📬 Email Output (Example)

```text
Subject: Interview Invitation - Data Analyst Role

Hi Priya,

Thank you for applying for the Data Analyst position. Based on your qualifications and experience, we’re excited to invite you for an interview.

Proposed Time Slots:
- Tuesday, 10:00 AM IST
- Wednesday, 2:00 PM IST

Interview Format: Zoom / Google Meet

Best regards,  
AI Recruiter Team
```

---

## 🛡️ Privacy & Local-first Approach

No data leaves your machine. Everything — from parsing to LLM usage — runs on your local system via **Ollama**. Perfect for enterprise and data-sensitive applications.

---

## 📄 License

MIT License

---

## 🏁 Built For

> 🔥 Hack the Future — A GenAI sprint powered by Data.

---

Let me know if you want:
- 🧪 Unit test support
- 🖥️ Lightweight web UI
- 🧩 Prebuilt JD/CV examples
- 📦 Packaging for offline deployment
