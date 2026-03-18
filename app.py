import streamlit as st
import requests
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ArvyaX AI", layout="wide")

st.title("🌿 ArvyaX AI Companion")
st.caption("Understand → Decide → Guide")

# ---------------- SAFE CONFIG ----------------
API_URL = "https://ml1-qinj.onrender.com/predict"
API_KEY = "arvyax-secret-key"

# ---------------- SESSION INIT (FIXED) ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.subheader("⚙️ Context Inputs")
    stress = st.slider("Stress", 1, 10, 5)
    energy = st.slider("Energy", 1, 10, 5)
    sleep = st.slider("Sleep (hrs)", 0, 10, 6)
    duration = st.slider("Session Duration", 5, 60, 20)
    time_of_day = st.selectbox(
        "Time of Day",
        ["morning", "afternoon", "evening", "night"]
    )

# ---------------- USER INPUT ----------------
user_input = st.chat_input("How are you feeling?")

if user_input:

    # Save user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # ---------------- API CALL ----------------
    payload = {
        "journal_text": user_input,
        "stress": stress,
        "energy": energy,
        "sleep": sleep,
        "duration": duration,
        "time_of_day": time_of_day
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.stop()

        res = response.json()

    except Exception as e:
        st.error("⚠️ API connection failed")
        st.write(e)

        # fallback response
        res = {
            "state": "unknown",
            "intensity": 0,
            "confidence": 0,
            "uncertain": 1,
            "guidance": "System couldn't connect. Try again."
        }

    # ---------------- RESPONSE ----------------
    state = res.get("state", "unknown")
    guidance = res.get("guidance", "No guidance")

    with st.chat_message("assistant"):

        # typing effect
        placeholder = st.empty()
        full_text = ""

        for word in guidance.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.01)

    # Save assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": guidance
    })