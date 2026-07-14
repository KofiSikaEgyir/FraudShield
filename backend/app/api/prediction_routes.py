# =====================================================
# FraudShield Prediction API Routes
# Purpose: Expose fraud prediction endpoint
# =====================================================

from fastapi import APIRouter

from backend.app.schemas.prediction_schema import TransactionInput, PredictionResponse
from backend.app.services.fraud_model_service import fraud_model_service
from backend.app.services.database_service import database_service


router = APIRouter(
    prefix="/predict",
    tags=["Fraud Prediction"]
)


@router.post("/", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionInput):
    """
    Predict fraud risk for a mobile money-like transaction
    and save the prediction result into PostgreSQL.
    """

    transaction_dict = transaction.model_dump()

    prediction_result = fraud_model_service.predict(transaction_dict)

    log_id = database_service.save_prediction_log(
        transaction=transaction_dict,
        prediction_result=prediction_result
    )

    prediction_result["log_id"] = log_id

    return prediction_result