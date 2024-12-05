from openai import OpenAI
from flask import current_app

class LLMClient:
    def __init__(self):
        self.client = None

    def _ensure_client(self):
        if not self.client:
            api_key = current_app.config['DEEPSEEK_API_KEY']
            self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def generate_response(self, prompt: str) -> str:
        self._ensure_client()
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"