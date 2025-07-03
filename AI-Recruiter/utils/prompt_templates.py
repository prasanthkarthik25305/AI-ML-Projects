# utils/prompt_templates.py

def jd_summary_prompt(jd_text):
    return f"""
You are an expert HR assistant. Summarize the following job description into structured fields: 
- Role
- Required Skills
- Qualifications
- Experience
- Responsibilities

Return the result as a JSON object with these exact keys.

Job Description:
\"\"\"
{jd_text}
\"\"\"
"""
