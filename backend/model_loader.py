from pathlib import Path
import joblib


# Find the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the trained reserve model
RESERVE_MODEL_PATH = BASE_DIR / "ml" / "reserve" / "reserve_model.pkl"


# Load the model once when this module is imported
reserve_model = joblib.load(RESERVE_MODEL_PATH)


def get_reserve_model():
    return reserve_model