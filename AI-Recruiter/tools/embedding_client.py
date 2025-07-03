import requests

def get_embedding(text, model="nomic-embed-text"):
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model, "prompt": text}
        )

        if response.status_code != 200:
            print("⚠️ Error from Ollama embedding model:", response.text)
            return None

        data = response.json()
        return data.get("embedding", [])
    except Exception as e:
        print("❌ Embedding error:", e)
        return None
