from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.reserve import router as reserve_router


app = FastAPI(
    title="GeoMine AI Backend",
    description="Backend API for manganese reserve prediction and production forecasting.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reserve_router)


@app.get("/")
def root():
    return {
        "message": "GeoMine AI Backend is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "GeoMine AI Backend"
    }