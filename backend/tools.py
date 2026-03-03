# import smtplib
# from email.message import EmailMessage
# from datetime import datetime
# import ollama
# from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse

# from .database import log_emergency
# from .config import (
#     TWILIO_ACCOUNT_SID,
#     TWILIO_AUTH_TOKEN,
#     TWILIO_FROM_NUMBER,
#     EMERGENCY_CONTACT,
#     EMAIL_USER,
#     EMAIL_PASS,
#     EMERGENCY_EMAIL
# )


# # --------------------------------
# # 🚨 Risk Detection
# # --------------------------------
# def detect_risk_level(text: str):
#     triggers = [
#         "kill myself",
#         "suicide",
#         "end my life",
#         "harm myself",
#         "don't want to live",
#         "i want to die",
#         "i am going to die"
#     ]

#     text = text.lower()
#     for trigger in triggers:
#         if trigger in text:
#             return "HIGH"

#     return "LOW"


# # --------------------------------
# # 🚨 Emergency Handler
# # --------------------------------
# def call_emergency(user_id: str, user_message: str, location: str = "Unknown"):

#     timestamp = datetime.now().isoformat()

#     try:
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#         # --------------------------------
#         # 📞 Voice Call
#         # --------------------------------
#         voice_response = VoiceResponse()

#         voice_response.say(
#             f"Emergency alert. A user from {location} is at high suicide risk. "
#             "The person using the AI Therapist application "
#             "has expressed suicidal thoughts or intent to harm themselves. "
#             "Immediate support may be required. Please contact them immediately.",
#             voice="alice",
#             language="en-IN"
#         )

#         client.calls.create(
#             twiml=str(voice_response),
#             to=EMERGENCY_CONTACT,
#             from_=TWILIO_FROM_NUMBER
#         )

#         # --------------------------------
#         # 📩 SMS
#         # --------------------------------
#         client.messages.create(
#             body=(
#                 f"🚨 HIGH RISK DETECTED\n\n"
#                 f"User: {user_id}\n"
#                 f"Message: {user_message}\n"
#                 f"Location: {location}\n"
#                 f"Time: {timestamp}"
#             ),
#             from_=TWILIO_FROM_NUMBER,
#             to=EMERGENCY_CONTACT
#         )

#         # --------------------------------
#         # 📧 Email
#         # --------------------------------
#         if EMAIL_USER and EMAIL_PASS and EMERGENCY_EMAIL:

#             email = EmailMessage()
#             email["Subject"] = "🚨 AI Therapist Emergency Alert"
#             email["From"] = EMAIL_USER
#             email["To"] = EMERGENCY_EMAIL

#             email.set_content(
#                 f"🚨 HIGH RISK DETECTED\n\n"
#                 f"User ID: {user_id}\n"
#                 f"Message: {user_message}\n"
#                 f"Location: {location}\n"
#                 f"Time: {timestamp}"
#             )

#             with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#                 smtp.login(EMAIL_USER, EMAIL_PASS)
#                 smtp.send_message(email)

#         # Log success
#         log_emergency(user_id, "HIGH", timestamp, "ALERT_SENT")

#     except Exception as e:
#         print("Emergency error:", e)
#         log_emergency(user_id, "HIGH", timestamp, "FAILED")


# # --------------------------------
# # 🧠 AI Therapist
# # --------------------------------
# def query_medgemma(prompt: str) -> str:

#     system_prompt = """
# You are Dr. Emily Hartman, a compassionate clinical psychologist.
# Respond warmly, validate emotions, and give gentle guidance.
# Keep it concise (6-8 sentences).
# Ask one open-ended question at the end.
# """

#     try:
#         response = ollama.chat(
#             model="llama3",
#             messages=[
#                 {"role": "system", "content": system_prompt.strip()},
#                 {"role": "user", "content": prompt.strip()}
#             ],
#             options={
#                 "num_predict": 180,
#                 "temperature": 0.6
#             }
#         )

#         return response["message"]["content"].strip()

#     except Exception as e:
#         print("Ollama error:", e)
#         return "I'm having technical issues, but I'm here with you."

import smtplib
from email.message import EmailMessage
from datetime import datetime
import ollama
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from .database import log_emergency
from .config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    EMERGENCY_CONTACT,
    EMAIL_USER,
    EMAIL_PASS,
    EMERGENCY_EMAIL
)


# --------------------------------
# 🚨 Risk Detection
# --------------------------------
def detect_risk_level(text: str):
    triggers = [
        "kill myself",
        "suicide",
        "end my life",
        "harm myself",
        "don't want to live",
        "i want to die",
        "i am going to die"
    ]

    text = text.lower()
    for trigger in triggers:
        if trigger in text:
            return "HIGH"

    return "LOW"


# --------------------------------
# 🚨 Emergency Handler
# --------------------------------
def call_emergency(user_id: str, user_message: str, location: str = "Unknown"):

    timestamp = datetime.now().isoformat()

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        alert_text = (
            f"HIGH RISK DETECTED\n\n"
            f"User: {user_id}\n"
            f"Message: {user_message}\n"
            f"Location: {location}\n"
            f"Time: {timestamp}"
        )

        # --------------------------------
        # 📞 Voice Call
        # --------------------------------
        voice_response = VoiceResponse()

        voice_response.say(
            f"Emergency alert. A user from {location} is at high suicide risk. "
            "The AI Therapist application detected suicidal intent. "
            "Immediate attention may be required.",
            voice="alice",
            language="en-IN"
        )

        call = client.calls.create(
            twiml=str(voice_response),
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER
        )

        print("Call SID:", call.sid)

        # --------------------------------
        # 📩 SMS
        # --------------------------------
        sms = client.messages.create(
            body=alert_text,
            from_=TWILIO_FROM_NUMBER,
            to=EMERGENCY_CONTACT
        )

        print("SMS SID:", sms.sid)
        print("SMS Status:", sms.status)

        # --------------------------------
        # 📧 Email
        # --------------------------------
        if EMAIL_USER and EMAIL_PASS and EMERGENCY_EMAIL:

            email = EmailMessage()
            email["Subject"] = "AI Therapist Emergency Alert"
            email["From"] = EMAIL_USER
            email["To"] = EMERGENCY_EMAIL

            email.set_content(alert_text)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(email)

        # Log success
        log_emergency(user_id, "HIGH", timestamp, "ALERT_SENT")

    except Exception as e:
        print("Emergency error:", e)
        log_emergency(user_id, "HIGH", timestamp, "FAILED")


# --------------------------------
# 🧠 AI Therapist
# --------------------------------
def query_medgemma(prompt: str) -> str:

    system_prompt = """
You are Dr. Emily Hartman, a compassionate clinical psychologist.
Respond warmly, validate emotions, and give gentle guidance.
Keep it concise (6-8 sentences).
Ask one open-ended question at the end.
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": prompt.strip()}
            ],
            options={
                "num_predict": 180,
                "temperature": 0.6
            }
        )

        return response["message"]["content"].strip()

    except Exception as e:
        print("Ollama error:", e)
        return "I'm having technical issues, but I'm here with you."