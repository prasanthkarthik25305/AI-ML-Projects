# agents/jd_summarizer.py

from tools.llm_client import query_llm
from utils.prompt_templates import jd_summary_prompt
import json
import os
import re

class JDSummarizer:
    def __init__(self):
        pass

    def summarize(self, jd_text):
        prompt = jd_summary_prompt(jd_text)
        response = query_llm(prompt)

        # 🔍 Try extracting the JSON from within markdown-style formatting
        match = re.search(r"{.*}", response, re.DOTALL)
        if match:
            try:
                summary = json.loads(match.group())
                return summary
            except json.JSONDecodeError:
                print("⚠️ Extracted JSON is invalid, returning raw response")
                return {"raw_summary": response}
        else:
            print("⚠️ LLM response not in JSON format, returning raw text")
            return {"raw_summary": response}

if __name__ == "__main__":
    input_folder = "data/jds"
    output_folder = "data/summaries"
    os.makedirs(output_folder, exist_ok=True)

    summarizer = JDSummarizer()
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                jd_text = file.read()
                print(f"\n📄 Processing {filename}...\n")
                summary = summarizer.summarize(jd_text)
                print(f"✅ Summary for {filename}:\n{json.dumps(summary, indent=2)}\n")

                # 💾 Save the summary
                output_path = os.path.join(output_folder, filename.replace(".txt", ".json"))
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(summary, f, indent=2)
                print(f"💾 Saved to {output_path}")
