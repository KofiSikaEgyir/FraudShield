# =====================================================
# FraudShield SMS Service
# Purpose: Simulate SMS fraud alerts for high-risk transactions
# =====================================================

from datetime import datetime, timezone


class SMSService:
    """
    Service class for generating and simulating SMS fraud alerts.
    Later, this can be extended to Twilio, Hubtel, Mnotify, or other providers.
    """

    def __init__(self):
        self.provider = "Simulation"

    def is_sms_required(self, risk_level: str) -> bool:
        """
        SMS is required only for High Risk predictions.
        """
        return risk_level == "High Risk"

    def generate_sms_message(
        self,
        customer_phone: str,
        transaction_type: str,
        amount: float,
        risk_level: str,
        fraud_probability: float
    ) -> str:
        """
        Generate short SMS alert message for the customer.
        """

        return (
            f"FraudShield Alert: A {risk_level} {transaction_type} transaction "
            f"of GHS {amount:,.2f} was detected with fraud probability "
            f"{fraud_probability:.4f}. Do not share your PIN or OTP. "
            "If you did not authorize this transaction, contact your provider immediately."
        )

    def send_sms_alert(
        self,
        customer_phone: str,
        transaction_type: str,
        amount: float,
        risk_level: str,
        fraud_probability: float
    ) -> dict:
        """
        Simulate sending SMS alert.
        """

        if not self.is_sms_required(risk_level):
            return {
                "sms_required": False,
                "sms_status": "not_required",
                "sms_message": None,
                "sms_provider": self.provider,
                "sms_sent_at": None,
                "sms_error": None
            }

        sms_message = self.generate_sms_message(
            customer_phone=customer_phone,
            transaction_type=transaction_type,
            amount=amount,
            risk_level=risk_level,
            fraud_probability=fraud_probability
        )

        return {
            "sms_required": True,
            "sms_status": "simulated",
            "sms_message": sms_message,
            "sms_provider": self.provider,
            "sms_sent_at": datetime.now(timezone.utc),
            "sms_error": None
        }


# Create one shared SMS service instance
sms_service = SMSService()