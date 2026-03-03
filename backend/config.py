import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMERGENCY_EMAIL = os.getenv("EMERGENCY_EMAIL")






















# TWILIO_ACCOUNT_SID = "AC95e55b64c60dda87d3348dc15b2cebae"
# TWILIO_AUTH_TOKEN = "afe11ff661fc4398f36efe4c5dcfc9a6"
# TWILIO_FROM_NUMBER = "+18647138626"  # your Twilio number
# EMERGENCY_CONTACT = "+917004714283"  # or your local emergency number
# GROQ_API_KEY = "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"
# GOOGLE_MAPS_API_KEY="AIzaSyBeM80VgnvEmb7dHZdcUKDtB-chxOKvyV0"

# EMAIL_USER=arebabu73@gmail.com
# EMAIL_PASS=your_16_character_app_password