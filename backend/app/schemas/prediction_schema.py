# =====================================================
# FraudShield Prediction Schemas
# Purpose: Define request and response structures
# =====================================================

from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TransactionInput(BaseModel):
    """
    Input schema for a mobile money-like transaction.
    These are the fields required by the saved Random Forest model.
    """

    type: Literal["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"] = Field(
        ...,
        description="Transaction type",
        examples=["TRANSFER"]
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount",
        examples=[250000.00]
    )

    oldbalanceOrg: float = Field(
        ...,
        ge=0,
        description="Sender old balance before the transaction",
        examples=[250000.00]
    )

    newbalanceOrig: float = Field(
        ...,
        ge=0,
        description="Sender new balance after the transaction",
        examples=[0.00]
    )

    @field_validator("type", mode="before")
    @classmethod
    def uppercase_transaction_type(cls, value):
        """
        Convert transaction type to uppercase before validation.
        This allows users to enter transfer, Transfer, or TRANSFER.
        """
        if isinstance(value, str):
            return value.upper()

        return value


class PredictionResponse(BaseModel):
    """
    Output schema returned by the fraud prediction API.
    """
    log_id: Optional[int] = Field(
        None,
        description="Database log ID for the saved prediction record"
    )

    prediction: str = Field(
        ...,
        description="Fraud prediction label"
    )

    prediction_code: int = Field(
        ...,
        description="0 means Non-Fraud, 1 means Fraud"
    )

    fraud_probability: float = Field(
        ...,
        description="Predicted probability of fraud"
    )

    risk_level: str = Field(
        ...,
        description="Low Risk, Moderate Risk, or High Risk"
    )

    alert_message: str = Field(
        ...,
        description="Fraud prevention alert message"
    )