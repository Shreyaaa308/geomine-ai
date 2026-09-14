from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

RESERVE_MODEL_PATH = BASE_DIR / "ml" / "reserve" / "reserve_model.pkl"
PRODUCTION_MODEL_PATH = BASE_DIR / "ml" / "production" / "production_model.pkl"

reserve_model = joblib.load(RESERVE_MODEL_PATH)
production_model = joblib.load(PRODUCTION_MODEL_PATH)


def get_reserve_model():
    return reserve_model


def get_production_model():
    return production_model