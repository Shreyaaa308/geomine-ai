from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from backend.routes.recommend import get_recommendations


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]

RESERVE_PREDICTIONS_FILE = (
    BASE_DIR / "ml" / "reserve" / "reserve_predictions.csv"
)

PRODUCTION_PREDICTIONS_FILE = (
    BASE_DIR / "ml" / "production" / "production_predictions.csv"
)


def load_reserve_predictions():
    return pd.read_csv(RESERVE_PREDICTIONS_FILE)


def load_production_predictions():
    return pd.read_csv(PRODUCTION_PREDICTIONS_FILE)


@router.get("/dashboard-data")
def get_dashboard_data():
    reserve = load_reserve_predictions()
    production = load_production_predictions()
    recommendation_data = get_recommendations()

    reserve_summary = {
        "total_cells": len(reserve),
        "class_counts": reserve["predicted_class"].value_counts().to_dict(),
    }

    production_trend = production[
        [
            "mine_id",
            "period",
            "predicted_output",
            "planned_target",
        ]
    ].to_dict(orient="records")

    return {
        "reserve": {
            "summary": reserve_summary,
            "predictions": reserve.to_dict(orient="records"),
        },
        "production": {
            "trend": production_trend,
        },
        "recommendations": recommendation_data["recommendations"],
    }