# =====================================================
# FraudShield Prediction API Routes
# Purpose: Expose fraud prediction endpoint
# =====================================================

from fastapi import APIRouter

from backend.app.schemas.prediction_schema import TransactionInput, PredictionResponse
from backend.app.services.fraud_model_service import fraud_model_service


router = APIRouter(
    prefix="/predict",
    tags=["Fraud Prediction"]
)


@router.post("/", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionInput):
    """
    Predict fraud risk for a mobile money-like transaction.
    """

    transaction_dict = transaction.model_dump()

    prediction_result = fraud_model_service.predict(transaction_dict)

    return prediction_result