# agents/scheduler.py
EMAIL_ENABLED = False

from tools import emailer
from datetime import datetime, timedelta

def generate_schedule_options():
    """Generate 3 mock interview time slots (next 3 days at 10 AM)."""
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%A, %d %B %Y at 10:00 AM") for i in range(1, 4)]

def format_email(candidate_name, job_role, interview_slots):
    """Create a nicely formatted email text."""
    slots_text = "\n".join([f"- {slot}" for slot in interview_slots])
    email_body = f"""
Dear {candidate_name},

Congratulations! Based on your profile, we would like to invite you for an interview for the role of **{job_role}**.

Please select one of the following interview time slots:

{slots_text}

Reply to this email with your preferred time.

Best regards,  
AI Recruiter Team
"""
    return email_body

def schedule(candidate_name, candidate_email, shortlisted_jobs):
    """
    For each shortlisted job, generate an interview schedule message and simulate sending an email.
    """
    print(f"\n📅 Scheduling interviews for {candidate_name}")

    for score, job_role, jd_file in shortlisted_jobs:
        slots = generate_schedule_options()
        email_text = format_email(candidate_name, job_role, slots)

        # Simulated email sending
        if EMAIL_ENABLED:
            emailer.send_email(
                to_email=candidate_email,
                subject=f"Interview Invitation for {job_role}",
                body=email_text,
                simulate=False
            )
        else:
            print(f"\n[Email DISABLED] Would send to: {candidate_email}")
            print(f"Subject: Interview Invitation for {job_role}")
            print(email_text)


    print("\n📨 Interview Email:")
    print(email_text)


# Run test manually
if __name__ == "__main__":
    candidate_name = "John Doe"
    candidate_email = "john.doe@example.com"
    shortlisted_jobs = [
        (0.42, "Data Scientist", "jd_001.json"),
        (0.55, "AI Researcher", "jd_003.json")
    ]

    schedule(candidate_name, candidate_email, shortlisted_jobs)
