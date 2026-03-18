import os
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import hstack
from xgboost import XGBClassifier, XGBRegressor

from preprocess import clean_data, META_COLS

# PATH FIX (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

train_path = os.path.join(BASE_DIR, "data", "train.csv")
test_path = os.path.join(BASE_DIR, "data", "test.csv")

# LOAD DATA
train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

train = clean_data(train)

print("✅ Data loaded")

# TEXT FEATURES
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1,2))
X_text = vectorizer.fit_transform(train["journal_text"])

# META FEATURES
X_meta = train[META_COLS]

# COMBINE
X = hstack([X_text, X_meta])

print("✅ Features ready:", X.shape)

# LABELS
le = LabelEncoder()
y_state = le.fit_transform(train["emotional_state"])
y_intensity = train["intensity"]

# MODELS
model_state = XGBClassifier(n_estimators=200)
model_state.fit(X, y_state)

model_intensity = XGBRegressor(n_estimators=200)
model_intensity.fit(X, y_intensity)

# SAVE MODELS
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

pickle.dump(model_state, open(os.path.join(BASE_DIR, "models/model_state.pkl"), "wb"))
pickle.dump(model_intensity, open(os.path.join(BASE_DIR, "models/model_intensity.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(BASE_DIR, "models/vectorizer.pkl"), "wb"))
pickle.dump(le, open(os.path.join(BASE_DIR, "models/label_encoder.pkl"), "wb"))

print("🔥 Training completed successfully")