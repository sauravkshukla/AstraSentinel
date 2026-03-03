# from fastapi import FastAPI, Form
# from pydantic import BaseModel
# from fastapi.responses import PlainTextResponse
# from xml.etree.ElementTree import Element, tostring
# import uvicorn

# from .database import init_db, log_conversation
# from .tools import detect_risk_level, call_emergency
# from .ai_agent import graph, SYSTEM_PROMPT, parse_response
# from .config import EMAIL_USER
# from fastapi import Request
# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="ai_therapist_app")

# user_location_store = {}

# # Debug: confirm .env loaded
# print("Loaded Email:", EMAIL_USER)

# init_db()

# app = FastAPI()


# # ==============================
# # Request Model
# # ==============================
# class Query(BaseModel):
#     message: str
#     location: str | None = None


# # ==============================
# # Web Frontend Endpoint
# # ==============================
# @app.post("/ask")
# async def ask(query: Query):

#     try:
#         inputs = {
#             "messages": [
#                 ("system", SYSTEM_PROMPT),
#                 ("user", query.message)
#             ]
#         }

#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)

#         if not final_response:
#             final_response = "I'm here to support you."

#         # Risk detection
#         risk_level = detect_risk_level(query.message)

#         # 🚨 Emergency trigger
#         if risk_level == "HIGH":
#             location = user_location_store.get("frontend_user", "Unknown")
#             call_emergency("frontend_user", query.message, location)

#         # Log conversation
#         log_conversation(
#             "frontend_user",
#             query.message,
#             final_response,
#             risk_level
#         )

#         return {
#             "response": final_response,
#             "tool_called": tool_called_name
#         }

#     except Exception as e:
#         print("Error in /ask:", e)
#         return {
#             "response": "System error occurred.",
#             "tool_called": "None"
#         }


# # ==============================
# # WhatsApp Twilio Endpoint
# # ==============================
# def _twiml_message(body: str):
#     response_el = Element("Response")
#     message_el = Element("Message")
#     message_el.text = body
#     response_el.append(message_el)
#     xml_bytes = tostring(response_el, encoding="utf-8")
#     return PlainTextResponse(content=xml_bytes, media_type="application/xml")


# @app.post("/whatsapp_ask")
# async def whatsapp_ask(Body: str = Form(...)):

#     try:
#         user_text = Body.strip() if Body else ""

#         inputs = {
#             "messages": [
#                 ("system", SYSTEM_PROMPT),
#                 ("user", user_text)
#             ]
#         }

#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)

#         if not final_response:
#             final_response = "I'm here to support you."

#         # Risk detection
#         risk_level = detect_risk_level(user_text)

#         # 🚨 Emergency trigger
#         if risk_level == "HIGH":
#             call_emergency("whatsapp_user", user_text, "WhatsApp User")

#         # Log conversation
#         log_conversation(
#             "whatsapp_user",
#             user_text,
#             final_response,
#             risk_level
#         )

#         return _twiml_message(final_response)

#     except Exception as e:
#         print("Error in /whatsapp_ask:", e)
#         return _twiml_message("System error occurred.")


# # ==============================
# # Run Server
# # ==============================
# if __name__ == "__main__":
#     uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)




# @app.post("/set_location")
# async def set_location(request: Request):
#     data = await request.json()
#     lat = data.get("latitude")
#     lon = data.get("longitude")

#     try:
#         location = geolocator.reverse((lat, lon), language="en")
#         city = location.raw["address"].get("city", "Unknown")
#         user_location_store["frontend_user"] = city
#     except:
#         user_location_store["frontend_user"] = "Unknown"

#     return {"status": "Location Stored"}




from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from xml.etree.ElementTree import Element, tostring
import uvicorn
import requests

from .database import init_db, log_conversation
from .tools import detect_risk_level, call_emergency
from .ai_agent import graph, SYSTEM_PROMPT, parse_response
from .config import EMAIL_USER

# Debug: confirm .env loaded
print("Loaded Email:", EMAIL_USER)

init_db()

app = FastAPI()


# ==============================
# 🌍 IP LOCATION DETECTION
# ==============================
def get_location_from_ip(ip_address: str):
    try:
        if ip_address in ["127.0.0.1", "localhost"]:
            ip_address = requests.get("https://api.ipify.org").text.strip()

        # ---- Try ipapi first ----
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # ---- Fallback to ipinfo if empty ----
        if not city or not latitude:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data = response.json()

            city = data.get("city")
            region = data.get("region")
            country = data.get("country")

            loc = data.get("loc")
            if loc:
                latitude, longitude = loc.split(",")
            else:
                latitude = None
                longitude = None

        # ---- Final Safety ----
        if not city:
            city = "Approximate Network Location"
        if not region:
            region = "Unknown"
        if not country:
            country = "Unknown"

        maps_link = None
        if latitude and longitude:
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        return (
            f"IP: {ip_address}\n"
            f"City: {city}\n"
            f"Region: {region}\n"
            f"Country: {country}\n"
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"
            f"Maps: {maps_link}"
        )

    except Exception as e:
        print("Location Error:", e)
        return "Location: Unable to detect"


# ==============================
# Request Model
# ==============================
class Query(BaseModel):
    message: str


# ==============================
# Web Frontend Endpoint
# ==============================
@app.post("/ask")
async def ask(query: Query, request: Request):

    try:
        inputs = {
            "messages": [
                ("system", SYSTEM_PROMPT),
                ("user", query.message)
            ]
        }

        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)

        if not final_response:
            final_response = "I'm here to support you."

        # 🔍 Detect Risk
        risk_level = detect_risk_level(query.message)

        # 🌍 Get Client IP (Production Safe)
        client_ip = request.headers.get(
            "X-Forwarded-For",
            request.client.host
        )

        location_info = get_location_from_ip(client_ip)

        # 🚨 Emergency trigger
        if risk_level == "HIGH":
            call_emergency("frontend_user", query.message, location_info)

        # Log conversation
        log_conversation(
            "frontend_user",
            query.message,
            final_response,
            risk_level
        )

        return {
            "response": final_response,
            "tool_called": "IP Location Detection"
        }

    except Exception as e:
        print("Error in /ask:", e)
        return {
            "response": "System error occurred.",
            "tool_called": "None"
        }


# ==============================
# WhatsApp Twilio Endpoint
# ==============================
def _twiml_message(body: str):
    response_el = Element("Response")
    message_el = Element("Message")
    message_el.text = body
    response_el.append(message_el)
    xml_bytes = tostring(response_el, encoding="utf-8")
    return PlainTextResponse(content=xml_bytes, media_type="application/xml")


@app.post("/whatsapp_ask")
async def whatsapp_ask(request: Request, Body: str = Form(...)):

    try:
        user_text = Body.strip() if Body else ""

        inputs = {
            "messages": [
                ("system", SYSTEM_PROMPT),
                ("user", user_text)
            ]
        }

        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)

        if not final_response:
            final_response = "I'm here to support you."

        # 🔍 Detect Risk
        risk_level = detect_risk_level(user_text)

        # 🌍 Get IP
        client_ip = request.headers.get(
            "X-Forwarded-For",
            request.client.host
        )

        location_info = get_location_from_ip(client_ip)
        # location_info = "Location unavailable via WhatsApp. User must share live location manually."

        # 🚨 Emergency trigger
        if risk_level == "HIGH":
            call_emergency("whatsapp_user", user_text, location_info)

        # Log conversation
        log_conversation(
            "whatsapp_user",
            user_text,
            final_response,
            risk_level
        )

        return _twiml_message(final_response)

    except Exception as e:
        print("Error in /whatsapp_ask:", e)
        return _twiml_message("System error occurred.")


# ==============================
# Run Server
# ==============================
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)