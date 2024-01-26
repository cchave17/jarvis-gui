import requests
from utils.config import OPENAI_API_KEY

class OpenAIClient:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.chat_base_url = "https://api.openai.com/v1/chat/completions"

    def query_chat_model(self, model, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": model,
            "messages": [{"role": "system", "content": "This is a test run."}, 
                         {"role": "user", "content": prompt}]
        }
        response = requests.post(self.chat_base_url, json=data, headers=headers)
        return response.json()

    def test_query(self):
        test_prompt = "Translate 'Hello, world!' into French."
        response = self.query_chat_model('gpt-4-0125-preview', test_prompt)
        print("Test Query Response:", response)