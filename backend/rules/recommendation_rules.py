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