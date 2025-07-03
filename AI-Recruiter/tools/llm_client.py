# tools/llm_client.py

import subprocess

def query_llm(prompt, model="llama3.2"):
    process = subprocess.Popen(
    ["ollama", "run", "llama3.2"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

    stdout, stderr = process.communicate(prompt.encode('utf-8'))
    return stdout.decode('utf-8')

