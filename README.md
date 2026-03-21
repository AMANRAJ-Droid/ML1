# 🌿 ArvyaX ML System  
### *From Understanding Humans → To Guiding Them*

---

## 🚀 Live Demo
🔗 Frontend: https://checkmenow.streamlit.app/
🔗 API Docs: https://ml1-qinj.onrender.com/docs  

---

## 🧠 Problem Statement

Traditional ML systems stop at prediction.  
But real-world emotional data is:

- noisy  
- vague  
- sometimes contradictory  

👉 This project builds an AI system that:
- understands emotional state  
- reasons under uncertainty  
- **guides users toward better actions**

The system processes noisy journal inputs along with contextual signals and outputs:
- Emotional state
- Intensity
- Recommended action (what to do)
- Timing (when to do)
- Confidence and uncertainty

---

## Architecture

Frontend: Streamlit  
Backend: FastAPI (deployed on Render)

User → Streamlit UI → FastAPI API → ML Model → Decision Engine → Response

---

## Features

- Handles noisy and short text inputs
- Combines text + metadata
- Decision engine for actionable guidance
- Uncertainty modeling
- Real-time interactive UI

---

## Model

- Text + metadata features
- XGBoost classifier for state prediction
- Regression for intensity
- Rule-based decision layer

---

## Decision Logic

Uses:
- emotional_state
- intensity
- stress
- energy
- time_of_day

Outputs:
- what_to_do
- when_to_do

---

## Uncertainty Handling

- Confidence score
- Uncertain flag if prediction is weak or ambiguous

---

## Deployment

- Backend: Render
- Frontend: Streamlit Cloud

---

🌟 Philosophy

AI should not just understand humans.
It should help them move toward a better state.

👨‍💻 Author

Aman Raj

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py



