from langchain.agents import tool
from .tools import query_medgemma

# ==============================
# 🧠 Therapist Tool
# ==============================

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the AI therapist model.
    Use this tool for general emotional concerns,
    mental health guidance, and empathetic conversations.
    """
    return query_medgemma(query)


# ==============================
# 📍 Therapist Location Tool
# ==============================

import googlemaps
from .config import GOOGLE_MAPS_API_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Find licensed therapists near a specified city or area
    using Google Maps Places API.
    Returns top 5 nearby psychotherapists with phone numbers.
    """

    try:
        geocode_result = gmaps.geocode(location)

        if not geocode_result:
            return f"Could not find location: {location}"

        lat_lng = geocode_result[0]["geometry"]["location"]
        lat, lng = lat_lng["lat"], lat_lng["lng"]

        places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,
            keyword="Psychotherapist"
        )

        output = [f"Therapists near {location}:"]
        top_results = places_result.get("results", [])[:5]

        if not top_results:
            return f"No therapists found near {location}."

        for place in top_results:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "Address not available")

            details = gmaps.place(
                place_id=place["place_id"],
                fields=["formatted_phone_number"]
            )

            phone = details.get("result", {}).get(
                "formatted_phone_number",
                "Phone not available"
            )

            output.append(f"- {name} | {address} | {phone}")

        return "\n".join(output)

    except Exception as e:
        return f"Location lookup failed: {str(e)}"


# ==============================
# 🤖 Agent Setup
# ==============================

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from .config import GROQ_API_KEY


tools = [
    ask_mental_health_specialist,
    find_nearby_therapists_by_location
]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=GROQ_API_KEY
)

graph = create_react_agent(llm, tools=tools)


# ==============================
# 🧭 System Prompt
# ==============================

SYSTEM_PROMPT = """
You are an AI mental health assistant.

You have access to two tools:

1. ask_mental_health_specialist → For emotional guidance.
2. find_nearby_therapists_by_location → When user asks for nearby doctors/therapists.

If a user expresses suicidal thoughts or self-harm intent,
respond empathetically and calmly.
Emergency handling is managed by the backend system.

Be empathetic, responsible, and supportive.
"""


# ==============================
# 🔍 Stream Parser
# ==============================

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:

        # Tool calls
        tool_data = s.get("tools")
        if tool_data:
            tool_messages = tool_data.get("messages")
            if tool_messages:
                for msg in tool_messages:
                    tool_called_name = getattr(msg, "name", "None")

        # Agent final response
        agent_data = s.get("agent")
        if agent_data:
            messages = agent_data.get("messages")
            if messages:
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response