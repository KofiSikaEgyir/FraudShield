# =====================================================
# FraudShield Prediction API Routes
# Purpose: Expose fraud prediction and prediction history endpoints
# =====================================================

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder

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


@router.get("/history")
def get_prediction_history(
    limit: int = Query(10, ge=1, le=100)
):
    """
    Retrieve recent API prediction logs from PostgreSQL.
    """

    history = database_service.get_prediction_history(limit=limit)

    return jsonable_encoder({
        "count": len(history),
        "records": history
    })


@router.get("/high-risk")
def get_high_risk_predictions(
    limit: int = Query(10, ge=1, le=100)
):
    """
    Retrieve recent high-risk fraud prediction logs from PostgreSQL.
    """

    high_risk_records = database_service.get_high_risk_predictions(limit=limit)

    return jsonable_encoder({
        "count": len(high_risk_records),
        "records": high_risk_records
    })