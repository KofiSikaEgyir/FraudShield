# =====================================================
# FraudShield Prediction API Routes
# Purpose: Expose fraud prediction, SMS alert, and prediction history endpoints
# =====================================================

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder

from backend.app.schemas.prediction_schema import TransactionInput, PredictionResponse
from backend.app.services.fraud_model_service import fraud_model_service
from backend.app.services.database_service import database_service
from backend.app.services.sms_service import sms_service


router = APIRouter(
    prefix="/predict",
    tags=["Fraud Prediction"]
)


@router.post("/", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionInput):
    """
    Predict fraud risk for a mobile money-like transaction,
    simulate SMS alert for high-risk cases, and save the result into PostgreSQL.
    """

    transaction_dict = transaction.model_dump()

    # Generate fraud prediction
    prediction_result = fraud_model_service.predict(transaction_dict)

    # Simulate SMS alert based on risk level
    sms_result = sms_service.send_sms_alert(
        customer_phone=transaction_dict.get("customer_phone"),
        transaction_type=transaction_dict["type"],
        amount=transaction_dict["amount"],
        risk_level=prediction_result["risk_level"],
        fraud_probability=prediction_result["fraud_probability"]
    )

    # Save transaction, prediction, and SMS result into PostgreSQL
    log_id = database_service.save_prediction_log(
        transaction=transaction_dict,
        prediction_result=prediction_result,
        sms_result=sms_result
    )

    # Add database log ID and SMS result to response
    prediction_result["log_id"] = log_id
    prediction_result["sms_required"] = sms_result["sms_required"]
    prediction_result["sms_status"] = sms_result["sms_status"]
    prediction_result["sms_message"] = sms_result["sms_message"]
    prediction_result["sms_provider"] = sms_result["sms_provider"]

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


@router.get("/summary")
def get_prediction_summary():
    """
    Retrieve dashboard-style summary statistics for API prediction logs.
    """

    summary = database_service.get_prediction_summary()

    return jsonable_encoder(summary)