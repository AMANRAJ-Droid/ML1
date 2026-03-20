# 🌿 ArvyaX ML System  
### *From Understanding Humans → To Guiding Them*

---

## 🚀 Live Demo
🔗 Frontend: https://your-streamlit-app.streamlit.app  
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

---

## 🏗️ System Architecture

User Input
↓
Streamlit UI 💬
↓
FastAPI Backend ⚙️
↓
ML Model 🧠
↓
Decision Engine 🎯
↓
Guidance Output ✨


---

## ✨ Features

- 💬 Chat-style interaction  
- 🧠 Emotion + intensity prediction  
- 🎯 Action recommendation (what to do)  
- ⏰ Timing decision (when to do)  
- ⚠️ Uncertainty awareness  
- 📊 Emotion visualization  
- 🌐 Fully deployed system  

---
## 📊 Example Output

```json
{
  "state": "stress",
  "intensity": 4,
  "confidence": 0.82,
  "what_to_do": "box_breathing",
  "when_to_do": "now"
}
👉 Human-friendly response:

“You seem stressed right now.
Let’s slow things down. Try a short breathing exercise.”

🧠 Model Approach
🔹 Emotional Understanding

XGBoost classifier → emotional state

Regression → intensity

🔹 Features Used

Text (journal input)

Stress level

Energy level

Sleep hours

Time of day

🛠️ Tech Stack

Frontend: Streamlit

Backend: FastAPI

ML: XGBoost, Scikit-learn

Deployment:

Render (API)

Streamlit Community Cloud (UI)

Philosophy

AI should not just understand humans.
It should help them move toward a better state.

👨‍💻 Author

Aman Raj
