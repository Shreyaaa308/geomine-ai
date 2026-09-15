from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from backend.rules.recommendation_rules import calculate_shortfall


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parents[2]
PRODUCTION_PREDICTIONS_FILE = (
    BASE_DIR / "ml" / "production" / "production_predictions.csv"
)


def load_production_predictions():
    return pd.read_csv(PRODUCTION_PREDICTIONS_FILE)
    

def build_recommendation(row):
    shortfall = calculate_shortfall(
        predicted_output=float(row["predicted_output"]),
        planned_target=float(row["planned_target"]),
    )

    recommendations = []

    if shortfall["shortfall_flag"]:
        recommendations.append(
            "Production shortfall predicted. Consider maintenance or resource reallocation."
        )

    return {
        "mine_id": row["mine_id"],
        "period": row["period"],
        "predicted_output": float(row["predicted_output"]),
        "planned_target": float(row["planned_target"]),
        "shortfall_flag": shortfall["shortfall_flag"],
        "shortfall": shortfall["shortfall"],
        "shortfall_percent": shortfall["shortfall_percent"],
        "recommendations": recommendations,
    }

@router.get("/recommendations")
def get_recommendations():
    predictions = load_production_predictions()

    recommendations = [
        build_recommendation(row)
        for _, row in predictions.iterrows()
    ]

    return {
        "recommendations": recommendations
    }