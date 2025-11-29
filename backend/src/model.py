"""Model utilities: simple sklearn classifier wrapper for saving and loading models."""
import os, joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "saved_models", "model.joblib")

def create_sklearn_svc():
    clf = make_pipeline(StandardScaler(), SVC(probability=True, kernel='rbf'))
    return clf

def save_model(model, path=MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Train first.")
    return joblib.load(path)
