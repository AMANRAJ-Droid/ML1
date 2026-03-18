import os
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from scipy.sparse import hstack

from src.preprocess import clean_data, META_COLS
from src.decision_engine import decide_action
from src.uncertainty import compute_uncertainty
from src.guidance import generate_guidance

# ---------------- INIT ----------------
app = FastAPI(title="ArvyaX AI API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- LOAD MODELS ----------------
model_state = pickle.load(open(os.path.join(BASE_DIR, "models/model_state.pkl"), "rb"))
model_intensity = pickle.load(open(os.path.join(BASE_DIR, "models/model_intensity.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "models/vectorizer.pkl"), "rb"))
le = pickle.load(open(os.path.join(BASE_DIR, "models/label_encoder.pkl"), "rb"))

# ---------------- REQUEST SCHEMA ----------------
class UserInput(BaseModel):
    journal_text: str
    stress: int = 5
    energy: int = 5
    sleep: int = 6
    duration: int = 20
    time_of_day: str = "afternoon"

# ---------------- HEALTH CHECK ----------------
@app.get("/")
def health():
    return {"status": "ArvyaX API running 🚀"}

# ---------------- MAIN ENDPOINT ----------------
@app.post("/predict")
def predict(data: UserInput):

    df = pd.DataFrame([{
        "journal_text": data.journal_text,
        "sleep_hours": data.sleep,
        "energy_level": data.energy,
        "stress_level": data.stress,
        "duration_min": data.duration,
        "time_of_day": data.time_of_day
    }])

    df = clean_data(df)

    # Features
    X_text = vectorizer.transform(df["journal_text"])
    X_meta = df[META_COLS]
    X = hstack([X_text, X_meta])

    # Predictions
    pred_state = model_state.predict(X)
    pred_intensity = model_intensity.predict(X).clip(1, 5)

    probs = model_state.predict_proba(X)
    confidence, uncertain_flag = compute_uncertainty(probs)

    state = le.inverse_transform(pred_state)[0]
    intensity = int(pred_intensity[0])

    action, timing = decide_action(
        state, intensity, data.stress, data.energy, data.time_of_day
    )

    guidance = generate_guidance(
        state, intensity, data.stress, data.energy, data.time_of_day, action, timing
    )

    # Response
    return {
        "state": state,
        "intensity": intensity,
        "confidence": float(confidence[0]),
        "uncertain": int(uncertain_flag[0]),
        "action": action,
        "timing": timing,
        "guidance": guidance
    }