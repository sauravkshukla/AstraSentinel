# import streamlit as st
# import requests
# import json
# import streamlit.components.v1 as components

# BACKEND_URL = "http://localhost:8000/ask"

# st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
# st.title("🧠 SafeSpace – AI Mental Health Therapist")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "location" not in st.session_state:
#     st.session_state.location = None


# # ==============================
# # 🌍 Auto Location Detection (Browser)
# # ==============================

# components.html(
#     """
#     <script>
#     navigator.geolocation.getCurrentPosition(
#         function(position) {
#             const coords = {
#                 latitude: position.coords.latitude,
#                 longitude: position.coords.longitude
#             };
#             fetch("http://localhost:8000/set_location", {
#                 method: "POST",
#                 headers: { "Content-Type": "application/json" },
#                 body: JSON.stringify(coords)
#             });
#         }
#     );
#     </script>
#     """,
#     height=0,
# )


# # ==============================
# # Chat Input
# # ==============================

# user_input = st.chat_input("What's on your mind today?")

# if user_input:
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_input
#     })

#     try:
#         response = requests.post(
#             BACKEND_URL,
#             json={
#                 "message": user_input,
#                 "location": "AUTO"  # placeholder
#             },
#             timeout=30
#         )

#         if response.status_code == 200:
#             data = response.json()
#             reply = data.get("response", "No response received.")
#             tool = data.get("tool_called", "None")

#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": f"{reply}\n\n🔧 Tool Used: {tool}"
#             })

#         else:
#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": f"⚠ Backend Error: {response.status_code}"
#             })

#     except Exception as e:
#         st.session_state.chat_history.append({
#             "role": "assistant",
#             "content": f"⚠ Connection Error: {str(e)}"
#         })


# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])


import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("What's on your mind today?")

if user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = requests.post(
            BACKEND_URL,
            json={
                "message": user_input
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", "No response received.")
            tool = data.get("tool_called", "None")

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"{reply}\n\n📍 Location Auto-Detected\n🔧 Tool Used: {tool}"
            })

        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"⚠ Backend Error: {response.status_code}"
            })

    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"⚠ Connection Error: {str(e)}"
        })

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])