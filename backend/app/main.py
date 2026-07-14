# =====================================================
# FraudShield FastAPI Application
# Purpose: Main API entry point
# =====================================================

from fastapi import FastAPI

from backend.app.api.prediction_routes import router as prediction_router


app = FastAPI(
    title="FraudShield API",
    description="AI-based mobile money fraud risk detection and prevention API.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to FraudShield API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "fraudshield",
        "environment": "development",
        "model": "Random Forest"
    }


# Register API routes
app.include_router(prediction_router)