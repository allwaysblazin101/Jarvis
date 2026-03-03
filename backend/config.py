import os
from dotenv import load_dotenv

load_dotenv()

OWNER_NUMBER = os.getenv("OWNER_NUMBER")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OWNER_NUMBER:
    print("WARNING: OWNER_NUMBER not set in .env")
