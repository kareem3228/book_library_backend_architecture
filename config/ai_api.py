from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
load_dotenv()
api_key=os.getenv("GIMINI_API_KEY")
client=genai.Client(api_key=api_key,
                   http_options=types.HttpOptions(timeout=5000))

