# agents/recruiter.py

import os
from agents import matcher
from agents.shortlister import Shortlister
from agents import scheduler
from tools import cv_parser

def process_resumes(resume_folder='data/cvs/'):
    shortlister = Shortlister()

    for resume_file in os.listdir(resume_folder):
        if resume_file.endswith('.pdf'):
            resume_path = os.path.join(resume_folder, resume_file)
            print(f"\n📄 Processing resume: {resume_file}")

            # Extract candidate name and email
            candidate_name, candidate_email = cv_parser.parse_resume(resume_path)

            # Match jobs for this resume
            matched_jobs = matcher.match_single_resume(resume_path)
            if not matched_jobs:
                print(f"⚠️ No matches found for {resume_file}\n")
                continue

            # Shortlist candidates
            shortlisted = shortlister.shortlist(
                resume_filename=resume_path,
                matched_jobs=matched_jobs,
                candidate_name=candidate_name
            )

            # Schedule interviews
            if shortlisted:
                scheduler.schedule(
                    candidate_name=candidate_name,
                    candidate_email=candidate_email,
                    shortlisted_jobs=shortlisted
                )

if __name__ == "__main__":
    process_resumes()
