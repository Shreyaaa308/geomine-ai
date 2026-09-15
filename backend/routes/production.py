import pandas as pd
from fastapi import APIRouter

from backend.model_loader import get_production_model
from backend.schemas import (
    ProductionPredictionRequest,
    ProductionPredictionResponse,
)


router = APIRouter()


@router.post(
    "/predict-production",
    response_model=ProductionPredictionResponse,
)
def predict_production(request: ProductionPredictionRequest):
    model = get_production_model()

    input_data = pd.DataFrame([{
        "downtime_hours": request.downtime,
        "rainfall_mm": request.rainfall,
        "blast_delay_count": request.blast_delay,
        "previous_period_output": request.previous_period_output,
        "month": request.month,
    }])

    predicted_output = model.predict(input_data)[0]

    return ProductionPredictionResponse(
        predicted_output=float(predicted_output)
    )