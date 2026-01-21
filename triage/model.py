import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

MODEL_DIR = "data/models"
CAT_PATH = os.path.join(MODEL_DIR, "category_model.joblib")
SEV_PATH = os.path.join(MODEL_DIR, "severity_model.joblib")

def _pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=4000)),
        ("clf", LogisticRegression(max_iter=300)),
    ])

def train_models(labeled_csv: str) -> None:
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = pd.read_csv(labeled_csv)
    
    for col in ["message", "category", "severity"]:
        if col not in df.columns:
            raise ValueError(f"Training CSV missing required column: {col}")
        
    X = df["message"].astype(str)
        
    cat_model = _pipeline()
    cat_model.fit(X,  df["category"].astype(str))
    joblib.dump(cat_model, CAT_PATH)
        
    sev_model = _pipeline()
    sev_model.fit(X, df["severity"].astype(str))
    joblib.dump(sev_model, SEV_PATH)

def load_models():
    if not (os.path.exists(CAT_PATH) and os.path.exists(SEV_PATH)):
        raise FileNotFoundError("Model not found. Run train_models() first.")
    return joblib.load(CAT_PATH), joblib.load(SEV_PATH)

def predict(message: str):
    cat_model, sev_model = load_models()
    
    cat_probs = cat_model.predict_proba([message])[0]
    cat_i = int(cat_probs.argmax())
    category = str(cat_model.classes_[cat_i])
    cat_conf = float(cat_probs[cat_i])
    
    sev_probs = sev_model.predict_proba([message])[0]
    sev_i = int(sev_probs.argmax())
    severity = str(sev_model.classes_[sev_i])
    sev_conf = float(sev_probs[sev_i])
    
    confidence = min(cat_conf, sev_conf)
    return category, severity, confidence   
