from pydantic import BaseModel


class ReservePredictionRequest(BaseModel):
    lat: float
    lon: float
    grade: float
    depth: float
    ndvi: float
    soil_moisture: float
    lst: float
    rainfall: float


class ReservePredictionResponse(BaseModel):
    probability_high: float
    probability_medium: float
    probability_low: float
    predicted_class: str