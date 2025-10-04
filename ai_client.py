# ai_client.py
import os, requests, json

class AIClient:
    def __init__(self, api_key=None):
        # API key should be provided via environment variable or secure backend
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    def ask(self, prompt):
        # first try local - placeholder (we can use memory first)
        if not self.api_key:
            # no API key -> cannot ask online
            return None
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role":"user","content":prompt}],
            "max_tokens": 300
        }
        try:
            r = requests.post(url, headers=headers, json=data, timeout=15)
            if r.status_code == 200:
                j = r.json()
                return j["choices"][0]["message"]["content"].strip()
            else:
                print("AIClient error:", r.status_code, r.text)
                return None
        except Exception as e:
            print("AIClient exception:", e)
            return None
