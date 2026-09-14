from fastapi import FastAPI

from backend.routes.reserve import router as reserve_router


app = FastAPI(
    title="GeoMine AI Backend",
    description="Backend API for manganese reserve prediction and production forecasting.",
    version="1.0.0",
)


app.include_router(reserve_router)


@app.get("/")
def root():
    return {
        "message": "GeoMine AI Backend is running"
    }
