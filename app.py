import streamlit as st
import requests
import time
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ArvyaX AI", layout="wide")

st.title("🌿 ArvyaX AI Companion")
st.caption("Understand → Decide → Guide")

# ---------------- API CONFIG ----------------
API_URL = st.secrets.get("API_URL", "https://your-api.onrender.com/predict")
API_KEY = st.secrets.get("API_KEY", "arvyax-secret-key")

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("How are you feeling?")

if user_input:

    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # ---------------- USER CONTROLS ----------------
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

    # ---------------- API CALL ----------------
    payload = {
        "journal_text": user_input,
        "stress": stress,
        "energy": energy,
        "sleep": sleep,
        "duration": duration,
        "time_of_day": time_of_day
    }

    headers = {
        "x-api-key": API_KEY
    }

    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        res = res.json()

    except Exception as e:
        st.error("⚠️ Failed to connect to API")
        st.stop()

    # ---------------- RESPONSE DATA ----------------
    state = res.get("state", "unknown")
    intensity = res.get("intensity", 0)
    confidence = res.get("confidence", 0)
    uncertain = res.get("uncertain", 1)
    guidance = res.get("guidance", "No guidance available")

    # ---------------- BOT RESPONSE ----------------
    with st.chat_message("assistant"):

        # Typing effect
        placeholder = st.empty()
        full_text = ""

        for word in guidance.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.015)

        # ---------------- METRICS ----------------
        st.markdown("### 📊 Insight Panel")

        col1, col2, col3 = st.columns(3)

        col1.metric("State", state)
        col2.metric("Intensity", f"{intensity}/5")
        col3.metric("Confidence", round(confidence, 2))

        # ---------------- UNCERTAINTY ----------------
        if uncertain:
            st.warning("⚠️ Model is uncertain — input may be ambiguous")
        else:
            st.success("✅ High confidence prediction")

        # ---------------- VISUALIZATION ----------------
        if "probabilities" in res:
            st.markdown("### 📈 Emotion Distribution")

            labels = list(res["probabilities"].keys())
            values = list(res["probabilities"].values())

            fig, ax = plt.subplots()
            ax.barh(labels, values)
            ax.set_xlabel("Confidence")
            st.pyplot(fig)

    # Save assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": guidance
    })