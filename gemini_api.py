from dotenv import load_dotenv
import os 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_SECRET = os.getenv("GEMINI_API_SECRET")

headers = {
    'Content-Type': 'application/json',
    'X-GEMINI-APIKEY': GEMINI_API_KEY,
}

response = requests.get("https://api.gemini.com/v1/symbols", headers=headers)
print(response.json())
