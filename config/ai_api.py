from dotenv import load_dotenv
import os
from google import genai
load_dotenv()
api_key=os.getenv("GIMINI_API_KEY")
client=genai.Client(api_key=api_key)