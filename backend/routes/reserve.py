import pandas as pd
from fastapi import APIRouter

from backend.model_loader import get_reserve_model
from backend.schemas import (
    ReservePredictionRequest,
    ReservePredictionResponse,
)


router = APIRouter()


@router.post("/predict-reserve", response_model=ReservePredictionResponse)
def predict_reserve(request: ReservePredictionRequest):
    model = get_reserve_model()

    input_data = pd.DataFrame([{
        "lat": request.lat,
        "lon": request.lon,
        "grade": request.grade,
        "depth": request.depth,
        "ndvi": request.ndvi,
        "soil_moisture": request.soil_moisture,
        "lst": request.lst,
        "rainfall": request.rainfall,
    }])

    probabilities = model.predict_proba(input_data)[0]
    predicted_class = model.predict(input_data)[0]

    probability_map = dict(zip(model.classes_, probabilities))

    return ReservePredictionResponse(
        probability_high=float(probability_map["High"]),
        probability_medium=float(probability_map["Medium"]),
        probability_low=float(probability_map["Low"]),
        predicted_class=str(predicted_class),
    )