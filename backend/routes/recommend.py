from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from backend.rules.recommendation_rules import (
    calculate_shortfall,
    calculate_risk_level,
    check_downtime,
    check_rainfall,
    check_blast_delay,
)

router = APIRouter()


BASE_DIR = Path(__file__).resolve().parents[2]
PRODUCTION_PREDICTIONS_FILE = (
    BASE_DIR / "ml" / "production" / "production_predictions.csv"
)


def load_production_predictions():
    return pd.read_csv(PRODUCTION_PREDICTIONS_FILE)

def get_shortfall_recommendation(shortfall_percent: float) -> str:
    if shortfall_percent > 30:
        return (
            "Critical production shortfall detected. "
            "Escalate production recovery actions and reallocate resources."
        )
    elif shortfall_percent >= 20:
        return (
            "Significant production shortfall detected. "
            "Review the production plan and optimize resource allocation."
        )
    else:
        return (
            "Moderate production shortfall detected. "
            "Monitor production closely and make targeted operational adjustments."
        )

def get_downtime_recommendation(downtime: float, threshold: float) -> str:
    if downtime >= threshold * 1.25:
        return (
            "Severe downtime detected. "
            "Initiate urgent maintenance and reallocate operational resources."
        )
    else:
        return (
            "Downtime detected. "
            "Schedule preventive maintenance and optimize resource allocation."
        )

def get_rainfall_recommendation(rainfall: float, threshold: float) -> str:
    if rainfall >= threshold * 1.25:
        return (
            "Severe rainfall conditions detected. "
            "Restrict weather-sensitive operations and revise the production schedule."
        )
    else:
        return (
            "High rainfall detected. "
            "Adjust the production schedule and prioritize safer operations."
        )

def get_blast_delay_recommendation(blast_delay: float, threshold: float) -> str:
    if blast_delay >= threshold * 1.25:
        return (
            "Severe blast delay detected. "
            "Urgently reschedule delayed blasting activities to minimize production disruption."
        )
    else:
        return (
            "Blast delay detected. "
            "Reprioritize delayed blasting activities to maintain production continuity."
        )

def build_recommendation(row):
    shortfall = calculate_shortfall(
        predicted_output=float(row["predicted_output"]),
        planned_target=float(row["planned_target"]),
    )

    downtime = check_downtime(float(row["downtime"]))
    rainfall = check_rainfall(float(row["rainfall"]))
    blast_delay = check_blast_delay(float(row["blast_delay"]))

    risk = calculate_risk_level(
        downtime=float(row["downtime"]),
        rainfall=float(row["rainfall"]),
        blast_delay=float(row["blast_delay"]),
    )
    recommendations = []

    if shortfall["shortfall_flag"]:
        recommendations.append(
            f"Production shortfall of {shortfall['shortfall_percent']:.2f}% predicted "
            f"({float(row['predicted_output']):.2f} MT vs "
            f"{float(row['planned_target']):.2f} MT target). "
            f"{get_shortfall_recommendation(shortfall['shortfall_percent'])}"
        )

    if downtime["triggered"]:
        recommendations.append(
            get_downtime_recommendation(
                float(row["downtime"]),
                downtime["threshold"],
            )
        )

    if rainfall["triggered"]:
        recommendations.append(
            get_rainfall_recommendation(
                float(row["rainfall"]),
                rainfall["threshold"],
            )
        )

    if blast_delay["triggered"]:
        recommendations.append(
            get_blast_delay_recommendation(
                float(row["blast_delay"]),
                blast_delay["threshold"],
            )
        )

    return {
        "mine_id": row["mine_id"],
        "period": row["period"],
        "predicted_output": float(row["predicted_output"]),
        "planned_target": float(row["planned_target"]),
        "risk_level": risk["risk_level"],
        "trigger_count": risk["trigger_count"],
        "triggered_conditions": risk["triggered_conditions"],
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