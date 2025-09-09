import pandas as pd
import os

JD_DIR = os.path.join("data", "jds")
os.makedirs(JD_DIR, exist_ok=True)

def load_df(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path, encoding="ISO-8859-1")
    else:
        return pd.read_excel(path)

def convert_all():
    for fname in os.listdir(JD_DIR):
        if not fname.lower().endswith((".csv", ".xlsx", ".xls")):
            continue
        full = os.path.join(JD_DIR, fname)
        print(f"🔁 Converting {fname}")
        df = load_df(full)
        for i, row in df.iterrows():
            title = row.get("Job Title", f"job_{i}")
            desc  = row.get("Job Description", "")
            safe = "".join(c if c.isalnum() else "_" for c in title)[:50]
            out  = os.path.join(JD_DIR, f"{safe}_{i}.txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write(desc)
            print(f"  ✅ Wrote {out}")
    print("✅ Done converting all JDs.")

if __name__ == "__main__":
    convert_all()
