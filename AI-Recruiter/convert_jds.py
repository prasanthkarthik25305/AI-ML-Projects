import pandas as pd
import os

# Path to your Excel file
excel_file = "job_description.csv"  # <-- Change this to your filename

# Load Excel
df = pd.read_csv(excel_file, encoding='ISO-8859-1')  # OR encoding='latin1'



# Create jds folder if not exists
os.makedirs("data/jds", exist_ok=True)

# Loop through rows and write each JD to a separate text file
for idx, row in df.iterrows():
    job_title = row['Job Title'].strip().lower().replace(' ', '_').replace('/', '_')
    jd_text = row['Job Description'].strip()

    # Save to text file
    filename = f"data/jds/{job_title}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(jd_text)

    print(f"[✅] Saved: {filename}")
