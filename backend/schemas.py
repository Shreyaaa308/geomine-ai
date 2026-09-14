from pydantic import BaseModel, Field


# ============================================================
# RESERVE PREDICTION
# ============================================================

class ReservePredictionRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    grade: float
    depth: float
    ndvi: float = Field(..., ge=-1, le=1)
    soil_moisture: float
    lst: float
    rainfall: float


class ReservePredictionResponse(BaseModel):
    probability_high: float
    probability_medium: float
    probability_low: float
    predicted_class: str


# ============================================================
# PRODUCTION PREDICTION
# ============================================================

class ProductionPredictionRequest(BaseModel):
    downtime: float = Field(..., ge=0)
    rainfall: float 
    blast_delay: float = Field(..., ge=0)
    previous_period_output: float = Field(..., ge=0)
    month: int = Field(..., ge=1, le=12)


class ProductionPredictionResponse(BaseModel):
    predicted_output: float