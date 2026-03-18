import os
import pickle
import pandas as pd
from scipy.sparse import hstack

from preprocess import clean_data, META_COLS
from decision_engine import decide_action
from uncertainty import compute_uncertainty

# PATH FIX
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

test_path = os.path.join(BASE_DIR, "data", "test.csv")

test = pd.read_csv(test_path)
test = clean_data(test)

# LOAD MODELS
model_state = pickle.load(open(os.path.join(BASE_DIR, "models/model_state.pkl"), "rb"))
model_intensity = pickle.load(open(os.path.join(BASE_DIR, "models/model_intensity.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "models/vectorizer.pkl"), "rb"))
le = pickle.load(open(os.path.join(BASE_DIR, "models/label_encoder.pkl"), "rb"))

# FEATURES
X_text = vectorizer.transform(test["journal_text"])
X_meta = test[META_COLS]
X = hstack([X_text, X_meta])

# PREDICTIONS
pred_state = model_state.predict(X)
pred_intensity = model_intensity.predict(X).clip(1,5)

probs = model_state.predict_proba(X)
confidence, uncertain_flag = compute_uncertainty(probs)

pred_state_labels = le.inverse_transform(pred_state)

# DECISION ENGINE
actions, times = [], []

for i in range(len(test)):
    a, t = decide_action(
        pred_state_labels[i],
        pred_intensity[i],
        test["stress_level"].iloc[i],
        test["energy_level"].iloc[i],
        test["time_of_day"].iloc[i]
    )
    actions.append(a)
    times.append(t)

# SAVE OUTPUT
output = pd.DataFrame({
    "id": test["id"],
    "predicted_state": pred_state_labels,
    "predicted_intensity": pred_intensity,
    "confidence": confidence,
    "uncertain_flag": uncertain_flag,
    "what_to_do": actions,
    "when_to_do": times
})

os.makedirs(os.path.join(BASE_DIR, "outputs"), exist_ok=True)
output.to_csv(os.path.join(BASE_DIR, "outputs/predictions.csv"), index=False)

print("🔥 Predictions saved successfully")