# tools/cv_parser.py

import re
import fitz  # PyMuPDF for reading PDFs

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with fitz.open(pdf_path) as doc:
        return " ".join(page.get_text() for page in doc)

def extract_name_and_email(text):
    """Extract candidate name and email using basic heuristics."""
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group() if email_match else "unknown@example.com"

    # Heuristic: Assume candidate name is in the first few words
    words = text.strip().split()
    name = " ".join(words[:2]) if len(words) >= 2 else "Candidate"

    return name, email

def parse_resume(pdf_path):
    """Extracts name and email from the resume PDF."""
    text = extract_text_from_pdf(pdf_path)
    return extract_name_and_email(text)
