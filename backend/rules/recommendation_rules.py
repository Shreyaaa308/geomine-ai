DOWNTIME_THRESHOLD = 75.2
RAINFALL_THRESHOLD = 378.7
BLAST_DELAY_THRESHOLD = 5


def calculate_shortfall(predicted_output: float, planned_target: float) -> dict:
    """
    Calculate production shortfall from the P3 prediction output.

    A shortfall exists when predicted output is below the planned target.
    """

    shortfall = max(planned_target - predicted_output, 0.0)

    if planned_target > 0:
        shortfall_percent = (shortfall / planned_target) * 100
    else:
        shortfall_percent = 0.0

    return {
        "shortfall_flag": predicted_output < planned_target,
        "shortfall": shortfall,
        "shortfall_percent": shortfall_percent,
    }


def check_downtime(downtime: float) -> dict:
    """Check whether downtime reaches the configured threshold."""

    triggered = downtime >= DOWNTIME_THRESHOLD

    return {
        "triggered": triggered,
        "threshold": DOWNTIME_THRESHOLD,
        "value": downtime,
        "recommendation": (
            "High downtime detected. Consider maintenance or resource reallocation."
            if triggered
            else None
        ),
    }


def check_rainfall(rainfall: float) -> dict:
    """Check whether rainfall reaches the configured threshold."""

    triggered = rainfall >= RAINFALL_THRESHOLD

    return {
        "triggered": triggered,
        "threshold": RAINFALL_THRESHOLD,
        "value": rainfall,
        "recommendation": (
            "High rainfall detected. Consider adjusting the production schedule."
            if triggered
            else None
        ),
    }


def check_blast_delay(blast_delay: float) -> dict:
    """Check whether blast delay reaches the configured threshold."""

    triggered = blast_delay >= BLAST_DELAY_THRESHOLD

    return {
        "triggered": triggered,
        "threshold": BLAST_DELAY_THRESHOLD,
        "value": blast_delay,
        "recommendation": (
            "High blast delay detected. Consider reprioritizing blasting activities."
            if triggered
            else None
        ),
    }


def calculate_risk_level(
    downtime: float,
    rainfall: float,
    blast_delay: float,
) -> dict:
    """
    Calculate operational risk level from threshold-based conditions.

    Risk classification:
    - 0 triggered conditions -> Low
    - 1-2 triggered conditions -> Medium
    - 3 triggered conditions -> High
    """

    downtime_check = check_downtime(downtime)
    rainfall_check = check_rainfall(rainfall)
    blast_delay_check = check_blast_delay(blast_delay)

    triggered_conditions = []

    if downtime_check["triggered"]:
        triggered_conditions.append("downtime")

    if rainfall_check["triggered"]:
        triggered_conditions.append("rainfall")

    if blast_delay_check["triggered"]:
        triggered_conditions.append("blast_delay")

    trigger_count = len(triggered_conditions)

    if trigger_count == 0:
        risk_level = "Low"
    elif trigger_count <= 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "risk_level": risk_level,
        "trigger_count": trigger_count,
        "triggered_conditions": triggered_conditions,
    }