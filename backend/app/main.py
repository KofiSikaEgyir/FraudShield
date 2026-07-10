from fastapi import FastAPI

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
        "environment": "development"
    }
