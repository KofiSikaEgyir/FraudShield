# =====================================================
# FraudShield Database Service
# Purpose: Save API prediction logs into PostgreSQL
# =====================================================

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found. Check your .env file.")


class DatabaseService:
    """
    Service class for writing FraudShield API prediction logs to PostgreSQL.
    """
    def get_prediction_history(self, limit: int = 10) -> list[dict]:
        """
        Retrieve recent API prediction logs.
        """

        query = text("""
            SELECT
                log_id,
                transaction_type,
                amount,
                oldbalance_org,
                newbalance_orig,
                prediction_label,
                prediction_code,
                fraud_probability,
                risk_level,
                alert_message,
                model_name,
                model_version,
                source_system,
                created_at
            FROM api_prediction_logs
            ORDER BY created_at DESC
            LIMIT :limit;
        """)

        with self.engine.connect() as connection:
            result = connection.execute(query, {"limit": limit})
            rows = result.mappings().all()

        return [dict(row) for row in rows]


    def get_high_risk_predictions(self, limit: int = 10) -> list[dict]:
        """
        Retrieve recent high-risk fraud prediction logs.
        """

        query = text("""
            SELECT
                log_id,
                transaction_type,
                amount,
                oldbalance_org,
                newbalance_orig,
                prediction_label,
                prediction_code,
                fraud_probability,
                risk_level,
                alert_message,
                model_name,
                model_version,
                source_system,
                created_at
            FROM api_prediction_logs
            WHERE risk_level = 'High Risk'
            ORDER BY created_at DESC
            LIMIT :limit;
        """)

        with self.engine.connect() as connection:
            result = connection.execute(query, {"limit": limit})
            rows = result.mappings().all()

        return [dict(row) for row in rows]

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def save_prediction_log(self, transaction: dict, prediction_result: dict) -> int:
        """
        Save transaction input and prediction output into api_prediction_logs.
        Returns the created log_id.
        """

        insert_query = text("""
            INSERT INTO api_prediction_logs (
                transaction_type,
                amount,
                oldbalance_org,
                newbalance_orig,
                prediction_label,
                prediction_code,
                fraud_probability,
                risk_level,
                alert_message,
                model_name,
                model_version,
                source_system
            )
            VALUES (
                :transaction_type,
                :amount,
                :oldbalance_org,
                :newbalance_orig,
                :prediction_label,
                :prediction_code,
                :fraud_probability,
                :risk_level,
                :alert_message,
                :model_name,
                :model_version,
                :source_system
            )
            RETURNING log_id;
        """)

        values = {
            "transaction_type": transaction["type"],
            "amount": transaction["amount"],
            "oldbalance_org": transaction["oldbalanceOrg"],
            "newbalance_orig": transaction["newbalanceOrig"],
            "prediction_label": prediction_result["prediction"],
            "prediction_code": prediction_result["prediction_code"],
            "fraud_probability": prediction_result["fraud_probability"],
            "risk_level": prediction_result["risk_level"],
            "alert_message": prediction_result["alert_message"],
            "model_name": "Random Forest",
            "model_version": "v1.0.0",
            "source_system": "FastAPI Prototype"
        }

        with self.engine.begin() as connection:
            result = connection.execute(insert_query, values)
            log_id = result.scalar_one()

        return log_id


# Create one shared database service instance
database_service = DatabaseService()