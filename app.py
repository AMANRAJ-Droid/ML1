import streamlit as st
import requests
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ArvyaX AI", layout="centered")

API_URL = "https://ml1-qinj.onrender.com/predict"

st.title("🌿 ArvyaX AI Companion")
st.caption("Understand → Decide → Guide")

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("How are you feeling today?")

if user_input:

    # Save user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        "journal_text": user_input
    }

    # ---------------- API CALL ----------------
    try:
        with st.spinner("🧠 Understanding your state..."):
            response = requests.post(API_URL, json=payload, timeout=60)
            data = response.json()

    except requests.exceptions.ReadTimeout:
        with st.chat_message("assistant"):
            st.error("⏳ Server is waking up... try again in a few seconds")
        st.stop()

    except Exception as e:
        with st.chat_message("assistant"):
            st.error("⚠️ API connection failed")
            st.write(e)
        st.stop()

    # ---------------- EXTRACT DATA ----------------
    state = data.get("state", "unknown")
    intensity = data.get("intensity", 0)
    confidence = data.get("confidence", 0)
    action = data.get("what_to_do", "rest")
    timing = data.get("when_to_do", "later")
    uncertain = data.get("uncertain_flag", 1)

    # ---------------- SMART MESSAGE ----------------
    message = f"""
You seem **{state}** right now.

Let’s take a small step:
👉 Try **{action.replace('_',' ')}** **{timing}**.

You don’t need to solve everything at once.
"""

    # ---------------- BOT RESPONSE ----------------
    with st.chat_message("assistant"):

        # typing effect
        placeholder = st.empty()
        full_text = ""

        for word in message.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.01)

        # ---------------- VISUAL PANEL ----------------
        st.markdown("### 📊 Insight Panel")

        col1, col2, col3 = st.columns(3)

        col1.metric("State", state)
        col2.metric("Intensity", f"{intensity}/5")
        col3.metric("Confidence", round(confidence, 2))

        # ---------------- PROGRESS BAR ----------------
        st.progress(intensity / 5)

        # ---------------- UNCERTAINTY ----------------
        if uncertain:
            st.warning("⚠️ Model is slightly uncertain — input may be ambiguous")
        else:
            st.success("✅ High confidence prediction")

    # Save response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": message
    })
