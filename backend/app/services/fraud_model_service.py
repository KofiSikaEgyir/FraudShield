# =====================================================
# FraudShield Fraud Model Service
# Purpose: Load saved Random Forest model and generate predictions
# =====================================================

import json
from pathlib import Path

import joblib
import pandas as pd


# Locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Model file paths
MODEL_PATH = PROJECT_ROOT / "model" / "random_forest_fraud_model.pkl"
AMOUNT_THRESHOLD_PATH = PROJECT_ROOT / "model" / "amount_95th.pkl"
API_FEATURES_PATH = PROJECT_ROOT / "model" / "api_input_features.json"


class FraudModelService:
    """
    Service class for loading the saved Random Forest model
    and generating fraud predictions.
    """

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.amount_95th = joblib.load(AMOUNT_THRESHOLD_PATH)

        with open(API_FEATURES_PATH, "r", encoding="utf-8") as file:
            self.api_input_features = json.load(file)

    def assign_risk_level(self, prediction_code: int, fraud_probability: float) -> str:
        """
        Assign risk level based on prediction and probability.
        """
        if prediction_code == 1 and fraud_probability >= 0.80:
            return "High Risk"

        if prediction_code == 1 and fraud_probability >= 0.50:
            return "Moderate Risk"

        return "Low Risk"

    def generate_fraud_reasons(self, transaction: dict) -> list[str]:
        """
        Generate simple reasons to support the alert message.
        """
        reasons = []

        if transaction["type"] in ["TRANSFER", "CASH_OUT"]:
            reasons.append("the transaction type is commonly associated with fraud risk")

        if transaction["amount"] >= self.amount_95th:
            reasons.append("the transaction amount is unusually high")

        if transaction["oldbalanceOrg"] > 0 and transaction["newbalanceOrig"] == 0:
            reasons.append("the sender's balance was reduced to zero after the transaction")

        if not reasons:
            reasons.append("the transaction pattern appears unusual based on the model")

        return reasons

    def generate_alert_message(
        self,
        transaction: dict,
        prediction_code: int,
        fraud_probability: float
    ) -> str:
        """
        Generate user-friendly fraud prevention alert message.
        """
        risk_level = self.assign_risk_level(prediction_code, fraud_probability)
        reasons = self.generate_fraud_reasons(transaction)
        reasons_text = ", and ".join(reasons)

        if risk_level == "High Risk":
            return (
                f"High Risk Fraud Alert: This transaction appears suspicious because {reasons_text}. "
                "Pause before proceeding. Confirm the recipient, amount, and transaction purpose. "
                "Do not share your PIN or OTP with anyone."
            )

        if risk_level == "Moderate Risk":
            return (
                f"Moderate Risk Fraud Alert: This transaction shows possible fraud indicators because {reasons_text}. "
                "Verify the recipient and transaction details before proceeding."
            )

        return (
            "Low Risk: This transaction does not show strong fraud indicators based on the model. "
            "Still remain cautious and never share your PIN or OTP with anyone."
        )

    def predict(self, transaction: dict) -> dict:
        """
        Predict fraud risk for a single transaction.
        """
        input_data = pd.DataFrame([transaction])

        # Ensure the input columns follow the same order used during training
        input_data = input_data[self.api_input_features]

        prediction_code = int(self.model.predict(input_data)[0])
        fraud_probability = float(self.model.predict_proba(input_data)[0][1])

        prediction_label = "Fraud" if prediction_code == 1 else "Non-Fraud"
        risk_level = self.assign_risk_level(prediction_code, fraud_probability)
        alert_message = self.generate_alert_message(
            transaction,
            prediction_code,
            fraud_probability
        )

        return {
            "prediction": prediction_label,
            "prediction_code": prediction_code,
            "fraud_probability": round(fraud_probability, 4),
            "risk_level": risk_level,
            "alert_message": alert_message
        }


# Create a single service instance for the application
fraud_model_service = FraudModelService()